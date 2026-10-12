# Revideo / Motion Canvas scenes: scene.tsx

Renderer `revideo`. The entry file is `scene.tsx`, a Motion Canvas scene in
Revideo's form. It is compiled and rendered in headless Chrome.

- Export it as `export default makeScene2D('scene', function* (view) { ... })`.
  Revideo's `makeScene2D` takes a name first (it is added for you if missed).
- Import from `@revideo/2d` (`Txt`, `Rect`, `Circle`, `Line`, `Img`, `Layout`,
  `Latex`, `Code`, `Path`, `Spline`) and `@revideo/core` (`all`, `chain`,
  `sequence`, `delay`, `waitFor`, `createRef`, `createSignal`, easings, `spring`).
- Import the brief from `./kit`:
  `brief`, `look`, `seconds`, `width`, `height`, `pictures` (URLs for `<Img src>`),
  `font`, `prepare(view)`, `when("exact words")`, `until(t)`, `finish()`.
- Call `prepare(view)` first: it sets the project's font for the
  whole scene (Revideo's default is a serif). Give each `Txt` `fill={look.text}`.
- The origin (0, 0) is the **centre** of the 1920x1080 frame; x right, y down.
- Time each beat with `yield* until(when("the words"))`, and end with
  `yield* finish()` so the clip lasts exactly the narration.
- Text and motion are judged from the frames (the visual review), so keep text
  large (fontSize 44+), inside the frame and never overlapping.

Strengths: springs and eased motion that reads as physical, `Latex` typeset in
the browser (no TeX needed), `Code` typed in line by line, layouts that reflow.

## Worked example

```tsx
import {Img, Line, Rect, Txt, makeScene2D} from '@revideo/2d';
import {all, createRef, easeInOutCubic} from '@revideo/core';
import {finish, look, pictures, prepare, seconds, until, when} from './kit';

export default makeScene2D('scene', function* (view) {
  prepare(view);
  const title = createRef<Txt>();
  const picture = createRef<Img>();
  const start = createRef<Rect>();
  const link = createRef<Line>();
  view.add(<Txt ref={title} text="Padma's story" fill={look.text} fontSize={64}
                fontWeight={700} y={-420} opacity={0} />);
  view.add(<Img ref={picture} src={pictures[0]} height={620} x={-400} y={40} scale={0.6}
                opacity={0} />);
  view.add(<Rect ref={start} x={480} y={-180} padding={[14, 24]} radius={12} fill={look.panel}
                 opacity={0}><Txt text="A promising start" fill={look.text} fontSize={44} /></Rect>);
  view.add(<Line ref={link} points={[[480, -120], [480, 140]]} stroke={look.accent}
                 lineWidth={8} endArrow end={0} />);

  yield* all(title().opacity(1, 0.8), title().y(-400, 0.8));
  yield* all(picture().opacity(1, 1), picture().scale(1, 1, easeInOutCubic));   // grows in
  yield* until(when('promising'));                                              // on the word
  yield* all(start().opacity(1, 0.6), start().x(440, 0.6));
  yield* until(seconds * 0.4);
  yield* link().end(1, 1.2);                                                    // drawn
  yield* until(when('her body'));
  yield* all(picture().scale(1.25, 1.4), picture().x(-340, 1.4));              // zoom in
  yield* finish();
});
```
