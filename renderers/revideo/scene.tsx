/** @jsxImportSource @revideo/2d/lib */
/**
 * The Motion Canvas scene repertoire, driven entirely by one spec.
 *
 * Revideo is here for the kinds where a browser beats Manim, not to reimplement
 * a plotting library in TypeScript:
 *
 * - `formula` typesets with **MathJax**, in the browser, so a machine with no
 *   TeX distribution still gets real mathematics. Manim's `MathTex` needs
 *   `latex` on PATH; most machines do not have it, and this is the whole reason
 *   to keep a second backend alive.
 * - `code` is syntax-highlighted and typed in, line by line.
 * - the shape kinds -- flow, compare, stack, cycle, timeline, counter, morph --
 *   are spring-animated rather than eased, which reads as physical rather than
 *   as a slide transition.
 *
 * Nothing here invents content: every label, number and term arrives in the
 * spec, which came from the source material. The scene reads `spec` out of the
 * project's variables, so one compiled project renders every scene in a video.
 */
import {Circle, Code, Latex, Layout, Line, Rect, Txt, makeScene2D} from '@revideo/2d';
import {
  all,
  createRef,
  createSignal,
  easeOutCubic,
  spring,
  PlopSpring,
  SmoothSpring,
  useScene,
  waitFor,
} from '@revideo/core';

interface Spec {
  kind?: string;
  caption?: string;
  nodes?: string[];
  edges?: number[][];
  labels?: string[];
  values?: number[];
  formula?: string;
  steps?: string[];
  code?: string;
  seconds?: number;
  background?: string;
  accent?: string;
  text?: string;
  dim?: string;
}

const FALLBACK: Spec = {kind: 'flow', nodes: ['one', 'two'], seconds: 3};

function readSpec(): Spec {
  const scene = useScene();
  const given = (scene.variables.get('spec', FALLBACK) as () => Spec)();
  return {...FALLBACK, ...(given ?? {})};
}

/** How long one piece of the build takes, from how many there are. */
function beatFor(seconds: number, parts: number): number {
  return Math.max(0.28, Math.min(1.0, seconds / Math.max(2, parts + 2)));
}

export default makeScene2D('pipeline-scene', function* (view) {
  const spec = readSpec();
  const accent = spec.accent ?? '#E879A8';
  const text = spec.text ?? '#E8EAF0';
  const dim = spec.dim ?? '#9AA3B5';
  const seconds = Math.max(1.5, spec.seconds ?? 4);

  view.fill(spec.background ?? '#0D0F14');

  const body = createRef<Layout>();
  view.add(<Layout ref={body} y={0} />);

  if (spec.caption) {
    const caption = createRef<Txt>();
    view.add(
      <Txt
        ref={caption}
        text={spec.caption.slice(0, 70)}
        fill={text}
        fontSize={44}
        fontFamily={'Segoe UI, Inter, sans-serif'}
        y={-440}
        opacity={0}
      />,
    );
    yield* caption().opacity(1, 0.4);
    body().y(40);
  }

  const kind = spec.kind ?? 'flow';
  const draw = BUILDERS[kind];
  if (!draw) {
    throw new Error(`${kind} is not a kind this renderer draws`);
  }
  yield* draw(body, spec, {accent, text, dim}, seconds);

  // Hold on the finished picture: the narration usually keeps talking about it
  // after the last piece lands. The Python side trims to the exact length.
  yield* waitFor(0.6);
});

interface Palette {
  accent: string;
  text: string;
  dim: string;
}

type Builder = (
  body: () => Layout,
  spec: Spec,
  palette: Palette,
  seconds: number,
) => Generator;

/** A labelled box, added invisible and small so it can spring into place. */
function addBox(
  body: () => Layout,
  label: string,
  palette: Palette,
  x: number,
  y: number,
  width = 360,
  height = 150,
) {
  const box = createRef<Rect>();
  body().add(
    <Rect
      ref={box}
      x={x}
      y={y}
      width={width}
      height={height}
      radius={16}
      stroke={palette.accent}
      lineWidth={4}
      scale={0.7}
      opacity={0}
    >
      <Txt
        text={label.slice(0, 30)}
        fill={palette.text}
        fontSize={34}
        fontFamily={'Segoe UI, Inter, sans-serif'}
        maxWidth={width - 40}
        textWrap={true}
        textAlign={'center'}
      />
    </Rect>,
  );
  return box;
}

function* arrive(box: () => Rect, at: number) {
  yield* all(
    box().opacity(1, at * 0.7),
    spring(PlopSpring, 0.7, 1, value => box().scale(value)),
  );
}

function* drawArrow(
  body: () => Layout,
  palette: Palette,
  from: [number, number],
  to: [number, number],
  at: number,
) {
  const line = createRef<Line>();
  body().add(
    <Line
      ref={line}
      points={[from, to]}
      stroke={palette.accent}
      lineWidth={5}
      endArrow={true}
      arrowSize={14}
      end={0}
    />,
  );
  yield* line().end(1, at, easeOutCubic);
}

const drawFlow: Builder = function* (body, spec, palette, seconds) {
  const nodes = (spec.nodes ?? []).slice(0, 5);
  const beat = beatFor(seconds, nodes.length);
  const width = Math.min(360, 1680 / nodes.length - 60);
  const gap = width + 90;
  const first = -((nodes.length - 1) * gap) / 2;

  const boxes = nodes.map((label, index) =>
    addBox(body, label, palette, first + index * gap, 0, width),
  );

  yield* arrive(boxes[0], beat);
  for (let index = 1; index < boxes.length; index += 1) {
    const left = first + (index - 1) * gap + width / 2 + 10;
    const right = first + index * gap - width / 2 - 10;
    yield* all(
      drawArrow(body, palette, [left, 0], [right, 0], beat * 0.6),
      arrive(boxes[index], beat),
    );
  }
};

const drawCompare: Builder = function* (body, spec, palette, seconds) {
  const nodes = (spec.nodes ?? []).slice(0, 6);
  const labels = (spec.labels ?? []).slice(0, 3);
  const columns = Math.max(2, Math.min(labels.length || 2, 3));
  const perColumn = Math.ceil(nodes.length / columns);
  const beat = beatFor(seconds, nodes.length);
  const columnWidth = 520;
  const firstX = -((columns - 1) * columnWidth) / 2;

  for (let column = 0; column < columns; column += 1) {
    const items = nodes.slice(column * perColumn, (column + 1) * perColumn);
    if (!items.length) continue;
    const x = firstX + column * columnWidth;

    if (column < labels.length) {
      const heading = createRef<Txt>();
      body().add(
        <Txt
          ref={heading}
          text={labels[column].slice(0, 24)}
          fill={palette.accent}
          fontSize={40}
          fontFamily={'Segoe UI, Inter, sans-serif'}
          x={x}
          y={-260}
          opacity={0}
        />,
      );
      yield* heading().opacity(1, beat * 0.5);
    }
    if (column > 0) {
      const rule = createRef<Line>();
      body().add(
        <Line
          ref={rule}
          points={[[x - columnWidth / 2, -230], [x - columnWidth / 2, 280]]}
          stroke={palette.dim}
          lineWidth={2}
          end={0}
        />,
      );
      yield* rule().end(1, beat * 0.4);
    }
    for (let index = 0; index < items.length; index += 1) {
      const box = addBox(body, items[index], palette, x, -100 + index * 150, 440, 120);
      yield* arrive(box, beat * 0.8);
    }
  }
};

const drawStack: Builder = function* (body, spec, palette, seconds) {
  const nodes = (spec.nodes ?? []).slice(0, 6);
  const beat = beatFor(seconds, nodes.length);
  const height = Math.min(120, 620 / nodes.length);
  const bottom = ((nodes.length - 1) * (height + 20)) / 2;

  for (let index = 0; index < nodes.length; index += 1) {
    const box = addBox(body, nodes[index], palette, 0,
      bottom - index * (height + 20), 760, height);
    yield* arrive(box, beat);
  }
};

const drawCycle: Builder = function* (body, spec, palette, seconds) {
  const nodes = (spec.nodes ?? []).slice(0, 6);
  const beat = beatFor(seconds, nodes.length);
  const radius = 300;
  const places: [number, number][] = nodes.map((_, index) => {
    const angle = Math.PI / 2 - (index * 2 * Math.PI) / nodes.length;
    return [radius * Math.cos(angle), -radius * Math.sin(angle)];
  });

  const boxes = nodes.map((label, index) =>
    addBox(body, label, palette, places[index][0], places[index][1], 300, 110),
  );
  for (const box of boxes) {
    yield* arrive(box, beat);
  }
  for (let index = 0; index < nodes.length; index += 1) {
    const from = places[index];
    const to = places[(index + 1) % nodes.length];
    const towards = Math.atan2(to[1] - from[1], to[0] - from[0]);
    yield* drawArrow(
      body, palette,
      [from[0] + Math.cos(towards) * 170, from[1] + Math.sin(towards) * 90],
      [to[0] - Math.cos(towards) * 170, to[1] - Math.sin(towards) * 90],
      beat * 0.45,
    );
  }
};

const drawTimeline: Builder = function* (body, spec, palette, seconds) {
  const nodes = (spec.nodes ?? []).slice(0, 6);
  const beat = beatFor(seconds, nodes.length);

  const rail = createRef<Line>();
  body().add(
    <Line
      ref={rail}
      points={[[-820, 0], [820, 0]]}
      stroke={palette.dim}
      lineWidth={4}
      end={0}
    />,
  );
  yield* rail().end(1, beat);

  const step = nodes.length > 1 ? 1600 / (nodes.length - 1) : 0;
  for (let index = 0; index < nodes.length; index += 1) {
    const x = nodes.length > 1 ? -800 + index * step : 0;
    const dot = createRef<Circle>();
    const words = createRef<Txt>();
    body().add(
      <Circle ref={dot} x={x} y={0} size={26} fill={palette.accent} scale={0} />,
    );
    body().add(
      <Txt
        ref={words}
        text={nodes[index].slice(0, 24)}
        fill={palette.text}
        fontSize={32}
        fontFamily={'Segoe UI, Inter, sans-serif'}
        x={x}
        y={index % 2 === 0 ? -80 : 80}
        opacity={0}
      />,
    );
    yield* all(
      spring(PlopSpring, 0, 1, value => dot().scale(value)),
      words().opacity(1, beat * 0.7),
    );
  }
};

const drawCounter: Builder = function* (body, spec, palette, seconds) {
  const values = (spec.values ?? [0, 100]).slice(0, 2);
  const [start, end] = values.length > 1 ? values : [0, values[0] ?? 100];
  const places = Number.isInteger(start) && Number.isInteger(end) ? 0 : 2;
  const running = createSignal(start);

  const number = createRef<Txt>();
  body().add(
    <Txt
      ref={number}
      text={() => running().toFixed(places)}
      fill={palette.accent}
      fontSize={240}
      fontFamily={'Segoe UI, Inter, sans-serif'}
      y={-40}
      opacity={0}
    />,
  );
  const label = createRef<Txt>();
  body().add(
    <Txt
      ref={label}
      text={((spec.nodes ?? [''])[0] ?? '').slice(0, 36)}
      fill={palette.text}
      fontSize={44}
      fontFamily={'Segoe UI, Inter, sans-serif'}
      y={140}
      opacity={0}
    />,
  );

  yield* all(number().opacity(1, 0.4), label().opacity(1, 0.4));
  yield* running(end, Math.max(1.0, seconds - 1.4), easeOutCubic);
};

const drawMorph: Builder = function* (body, spec, palette, seconds) {
  const nodes = (spec.nodes ?? []).slice(0, 2);
  if (nodes.length < 2) {
    throw new Error('a morph needs something to become something else');
  }
  const words = createRef<Txt>();
  body().add(
    <Txt
      ref={words}
      text={nodes[0].slice(0, 26)}
      fill={palette.text}
      fontSize={110}
      fontFamily={'Segoe UI, Inter, sans-serif'}
      opacity={0}
    />,
  );
  const note = (spec.labels ?? [])[0];
  if (note) {
    const under = createRef<Txt>();
    body().add(
      <Txt
        ref={under}
        text={note.slice(0, 30)}
        fill={palette.dim}
        fontSize={36}
        fontFamily={'Segoe UI, Inter, sans-serif'}
        y={150}
        opacity={0}
      />,
    );
    yield* under().opacity(1, 0.4);
  }

  yield* words().opacity(1, 0.5);
  yield* waitFor(Math.max(0.3, seconds * 0.2));
  // Out, changed, and back in: two different strings have no shared shapes to
  // interpolate, and a cross-fade through nothing reads as the deliberate
  // replacement it is.
  yield* all(words().opacity(0, 0.35), words().scale(0.85, 0.35));
  words().text(nodes[1].slice(0, 26));
  words().fill(palette.accent);
  yield* all(
    words().opacity(1, 0.45),
    spring(SmoothSpring, 0.85, 1, value => words().scale(value)),
  );
};

const drawFormula: Builder = function* (body, spec, palette, seconds) {
  const steps = [spec.formula ?? '', ...(spec.steps ?? [])].filter(step => step.trim());
  if (!steps.length) {
    throw new Error('a formula needs something to write');
  }
  const beat = beatFor(seconds, steps.length);

  // MathJax, in the browser. This is the kind that exists because most machines
  // have no TeX distribution and Manim's MathTex needs one.
  const written = createRef<Latex>();
  body().add(
    <Latex
      ref={written}
      tex={steps[0]}
      fill={palette.text}
      fontSize={62}
      opacity={0}
    />,
  );
  yield* written().opacity(1, Math.max(beat, 0.5));

  for (const step of steps.slice(1, 5)) {
    yield* waitFor(Math.max(beat, 0.5));
    yield* written().opacity(0.15, 0.25);
    written().tex(step);
    yield* written().opacity(1, 0.35);
  }
};

const drawCode: Builder = function* (body, spec, palette, seconds) {
  const source = (spec.code ?? (spec.nodes ?? []).join('\n')).slice(0, 900);
  if (!source.trim()) {
    throw new Error('a code scene needs code');
  }
  const lines = source.split('\n');
  const beat = beatFor(seconds, lines.length);

  const block = createRef<Code>();
  body().add(
    <Code ref={block} code={''} fontSize={36} opacity={0} />,
  );
  yield* block().opacity(1, 0.3);

  // Typed in a line at a time, which is how it is read aloud.
  let written = '';
  for (const line of lines.slice(0, 14)) {
    written = written ? `${written}\n${line}` : line;
    yield* block().code(written, Math.max(0.18, beat * 0.5));
  }
  assertUsed(palette);
};

function assertUsed(_palette: Palette) {
  // The code block carries its own theme; the palette is unused here on purpose.
}

const BUILDERS: Record<string, Builder> = {
  flow: drawFlow,
  compare: drawCompare,
  stack: drawStack,
  cycle: drawCycle,
  timeline: drawTimeline,
  counter: drawCounter,
  morph: drawMorph,
  formula: drawFormula,
  code: drawCode,
};
