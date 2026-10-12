# The resource library

What every scene can draw on. The model making a scene is shown an index of this
folder and the method notes, so anything added here becomes something it can use.

| Folder | What goes in it |
| --- | --- |
| `code/` | The kits a scene's program imports, by name: `manimkit.py` (Manim scenes), `scenekit.py` (frame-by-frame scenes), `webkit.js` (web-page scenes). Start each file with a docstring saying what it is for. |
| `assets/` | Pictures, icons, fonts, sounds, data files. A scene reads them from the `SCENE_RESOURCES` folder. |
| `methods/` | How-to notes and worked examples the agent reads. `scene-contract.md` is what every scene must do; `motion.md` is the moves that explain an idea; `web-scenes.md` and `revideo-scenes.md` are how to build those scenes, each with a worked example. Add a note here to teach the agent a technique, a library's pitfalls, or a house style. |

Add files here by hand, or from the Generation page (Setup tab).

Only add what you have the right to use. A scene that takes a resource from
outside records its source and licence in its own `sources.json`.
