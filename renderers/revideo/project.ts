import {makeProject} from '@revideo/core';
import scene from './scene';

/**
 * The project the headless renderer serves.
 *
 * The frame size and rate are compiled in rather than read from the spec:
 * project settings are read once when this module loads, while a spec arrives
 * per render as a scene variable, and the pipeline renders every clip at the
 * same size as its frames anyway.
 *
 * `exporter: '@revideo/core/wasm'` is the point of this file. `renderVideo`
 * has that as a default, but only when no settings are passed at all -- pass
 * `puppeteer` options and the default goes with it, leaving the ffmpeg exporter,
 * which needs a side-channel server the pipeline never starts. The render then
 * fails inside the browser, which surfaces as "Navigating frame was detached"
 * and names nothing.
 */
// Injected by the driver through vite's `define`, because this module is
// evaluated *in the browser*: reading `process.env` here threw "process is not
// defined" before the project ever loaded, and the only symptom anywhere was
// puppeteer reporting a detached frame.
declare const PIPELINE_FRAME: {width: number; height: number; rate: number};

const frame =
  typeof PIPELINE_FRAME === 'undefined'
    ? {width: 1920, height: 1080, rate: 30}
    : PIPELINE_FRAME;
const size = {x: frame.width, y: frame.height};
const fps = frame.rate;

export default makeProject({
  name: 'pipeline-scene',
  scenes: [scene],
  settings: {
    shared: {
      background: '#0D0F14',
      range: [0, Infinity],
      size,
    },
    preview: {fps, resolutionScale: 1},
    rendering: {
      exporter: {name: '@revideo/core/wasm'},
      fps,
      resolutionScale: 1,
      colorSpace: 'srgb',
    },
  },
});
