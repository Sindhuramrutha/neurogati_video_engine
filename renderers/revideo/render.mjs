/**
 * Render one scene spec to an mp4, reading the spec as JSON on stdin.
 *
 * A subprocess rather than a server: the Python side already owns the render's
 * timing and file layout, and a long-lived Node process would be a second thing
 * to supervise for one clip at a time.
 *
 * **This drives vite and Chrome itself rather than calling `renderVideo`.** Not
 * by preference -- three separate things had to be found before a single frame
 * appeared, and only the last of them needs this file to be unusual:
 *
 * 1. `renderVideo`'s default settings include the one exporter that works
 *    without a side-channel ffmpeg server -- but defaults are replaced, not
 *    merged, so passing any settings at all silently removed it.
 * 2. The project module is evaluated *in the browser*, so reading
 *    `process.env` there threw "process is not defined" before the scene
 *    loaded. The frame size is compiled in with vite's `define` instead.
 * 3. `renderVideo` pushes `--single-process` into Chrome's arguments
 *    unconditionally (@revideo/renderer 0.10.4, server/render-video.js:29).
 *    On Windows that crashes the tab during navigation.
 *
 * Every one of those failed as `Navigating frame was detached`, which names
 * none of them: it is what puppeteer sees when the page dies while it is
 * waiting. So this file sets up the same vite server and the same /render URL
 * the library does, keeps the browser under our control, and prints what the
 * page actually said when something goes wrong.
 *
 * `--probe <kind>` draws the smallest real example of one kind and prints `ok`,
 * which is how the registry finds out what this machine can actually draw.
 * `--verbose` attaches the page's console, errors and failed requests.
 */
import puppeteer from 'puppeteer';
import {createServer} from 'vite';
import {createRequire} from 'node:module';
import {randomUUID} from 'node:crypto';
import {existsSync, mkdirSync, readFileSync, renameSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {dirname, join, resolve} from 'node:path';

const require = createRequire(import.meta.url);
const pluginModule = require('@revideo/vite-plugin');
// The plugin is CommonJS, so an ESM default import lands on the module object
// rather than on the function.
const motionCanvas = pluginModule.default ?? pluginModule;
const {rendererPlugin} = require('@revideo/renderer/lib/server/renderer-plugin');

const PROBES = {
  flow: {nodes: ['electrode', 'amplifier', 'filter']},
  compare: {nodes: ['one', 'two', 'three', 'four'], labels: ['Before', 'After']},
  stack: {nodes: ['application', 'transport', 'link']},
  cycle: {nodes: ['sense', 'decide', 'act']},
  timeline: {nodes: ['1943', '1958', '1986']},
  counter: {values: [0, 120], nodes: ['samples per second']},
  morph: {nodes: ['a spike', 'a number']},
  formula: {formula: 'y = mx + c', steps: ['y - c = mx']},
  code: {code: 'def spike(v):\n    return v > 50'},
};

const RENDER_TIMEOUT_MS = 180000;
const verbose = process.argv.includes('--verbose');

async function draw(spec) {
  const output = resolve(spec.output);
  mkdirSync(dirname(output), {recursive: true});

  const frame = {
    width: spec.width ?? 1920,
    height: spec.height ?? 1080,
    rate: spec.frameRate ?? 30,
  };
  // Every scene brings its own project file (scene_revideo.py).
  const projectFile = spec.project;
  if (!projectFile) throw new Error('the spec names no project file');
  const timeoutMs = spec.timeoutMs ?? RENDER_TIMEOUT_MS;
  const fileName = `scene-${process.pid}`;
  const folderId = randomUUID();
  const working = join(tmpdir(), `revideo-${fileName}-${folderId}`);

  const server = await createServer({
    configFile: false,
    plugins: [
      motionCanvas({project: resolve(process.cwd(), projectFile), output: './output'}),
      rendererPlugin(
        {exporter: {name: '@revideo/core/wasm'}},
        {spec},
        undefined,
        projectFile,
      ),
    ],
    define: {PIPELINE_FRAME: JSON.stringify(frame)},
    server: {port: 0, hmr: false},
    logLevel: verbose ? 'warn' : 'silent',
  });
  await server.listen();
  const port = server.httpServer.address().port;

  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      // Software rendering is the safe default for the small probes; a full
      // scene asks for the GPU (`spec.gpu`), which is many times faster.
      ...(spec.gpu ? [] : ['--disable-gpu', '--use-gl=swiftshader']),
    ],
    protocolTimeout: timeoutMs,
  });

  try {
    const page = await browser.newPage();
    const said = [];
    page.on('pageerror', error => said.push(`page error: ${error.message}`));
    page.on('error', error => said.push(`crashed: ${error.message}`));
    if (verbose) {
      page.on('console', message => console.error('[console]', message.type(), message.text()));
      page.on('requestfailed', request =>
        console.error('[requestfailed]', request.url(), request.failure()?.errorText));
    }

    const finished = new Promise((done, failed) => {
      page.exposeFunction('onRenderComplete', () => done());
      page.exposeFunction('onRenderFailed', message => failed(new Error(String(message))));
      page.exposeFunction('browserError', message => failed(new Error(String(message))));
      page.exposeFunction('logProgress', progress => {
        if (verbose) {
          console.error('[progress]', Math.round(progress * 100) + '%');
        }
      });
    });

    const url = `http://localhost:${port}/render?fileName=${fileName}`
      + `&workerId=0&totalNumOfWorkers=1&hiddenFolderId=${folderId}`;
    await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 60000});

    // The limit's timer is cleared when the render finishes: a pending timer keeps
    // Node alive, so a render would last its whole time limit (a clip done in
    // 12 s would take 300 s to come back).
    let limit;
    try {
      await Promise.race([
        finished,
        new Promise((_done, failed) => {
          limit = setTimeout(() => failed(new Error(
            `the render did not finish in ${timeoutMs / 1000}s`
            + (said.length ? `: ${said[0]}` : ''))), timeoutMs);
        }),
      ]);
    } finally {
      clearTimeout(limit);
    }

    // The wasm exporter writes the frames it muxed into its own working folder.
    // There is no audio to merge: the narration is muxed by the Python side,
    // which owns the video's clock.
    const visuals = join(working, 'visuals.mp4');
    if (!existsSync(visuals)) {
      throw new Error(said[0] ?? 'the renderer produced no clip');
    }
    renameSync(visuals, output);
    return output;
  } finally {
    // A newer Chromium may never answer close(): it then waited out the whole
    // protocol timeout -- the clip was done in seconds and the render took ten
    // minutes. A few seconds' grace, then the process is ended.
    const grace = new Promise(done => setTimeout(done, 5000));
    await Promise.race([browser.close().catch(() => {}), grace]);
    browser.process()?.kill('SIGKILL');
    await Promise.race([server.close().catch(() => {}), new Promise(done => setTimeout(done, 3000))]);
    rmSync(working, {recursive: true, force: true});
  }
}

const argv = process.argv.slice(2);
const probeAt = argv.indexOf('--probe');

if (probeAt >= 0) {
  const kind = argv[probeAt + 1];
  if (!PROBES[kind]) {
    console.log(`no such kind: ${kind}`);
    process.exit(2);
  }
  const target = join(tmpdir(), `revideo-probe-${kind}-${process.pid}.mp4`);
  try {
    await draw({
      ...PROBES[kind],
      kind,
      caption: 'probe',
      seconds: 2,
      width: 480,
      height: 270,
      frameRate: 15,
      output: target,
    });
    console.log('ok');
  } catch (failure) {
    console.log(String(failure?.message ?? failure).split('\n')[0].slice(0, 200));
    process.exit(1);
  } finally {
    rmSync(target, {force: true});
  }
} else {
  const spec = JSON.parse(readFileSync(0, 'utf8'));
  console.log(await draw(spec));
}
