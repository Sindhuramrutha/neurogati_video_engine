# The resource library

What every scene script can draw on. The Generation agent is shown an index of
this folder each time it writes a scene, so anything added here becomes
something it can use.

| Folder | What goes in it |
|---|---|
| `code/` | Python the scenes can import: helpers, components, whole techniques. Importable by name from any scene. Start each file with a docstring saying what it is for. |
| `assets/` | Pictures, icons, fonts, sounds, data files. A scene reads them from the `SCENE_RESOURCES` folder. |
| `methods/` | How-to notes and worked examples the agent reads: a technique, a library's pitfalls, a house style. Markdown, or a complete example `.py`. |

Add files here by hand, or from the Generation page (Setup tab).

Only add what you have the right to use. A scene that takes a resource from
outside records its source and licence in its own `sources.json`.
