/**
 * A real code editor for a scene's script: line numbers, Python colouring,
 * bracket matching, search (Ctrl+F), Tab to indent, Ctrl+/ to comment, Ctrl+S to
 * save and run, and a full-screen view.
 *
 * CodeMirror 5, vendored (`vendor/codemirror`) so it works offline like the rest
 * of the page, and loaded only when a scene's script is first shown.
 */

const BASE = "/static/vendor/codemirror/";
const STYLES = ["codemirror.min.css", "material-darker.min.css", "dialog.min.css"];
const SCRIPTS = ["codemirror.min.js", "python.min.js", "matchbrackets.min.js",
  "searchcursor.min.js", "dialog.min.js", "search.min.js"];

let loading = null;

function loadEditor() {
  loading ??= (async () => {
    // The styles are waited for: an editor laid out before them measures its
    // line-number gutter wrong, and the first letters of each line hide under it.
    await Promise.all(STYLES.map(name => new Promise(resolve => {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = BASE + name;
      link.onload = link.onerror = resolve;
      document.head.append(link);
    })));
    for (const name of SCRIPTS) {          // in order: the addons need CodeMirror first
      await new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = BASE + name;
        script.onload = resolve;
        script.onerror = () => reject(new Error(`The code editor could not load ${name}.`));
        document.head.append(script);
      });
    }
  })();
  return loading;
}

/** `# ` added to every selected line, or taken off when they all have it. */
function toggleComment(editor) {
  const lines = new Set();
  for (const range of editor.listSelections()) {
    const [from, to] = [range.anchor.line, range.head.line].sort((a, b) => a - b);
    for (let line = from; line <= to; line++) lines.add(line);
  }
  const chosen = [...lines].filter(line => editor.getLine(line).trim());
  const commented = chosen.every(line => /^\s*#/.test(editor.getLine(line)));
  editor.operation(() => {
    for (const line of chosen) {
      const text = editor.getLine(line);
      const indent = text.match(/^\s*/)[0].length;
      if (commented) {
        const mark = text.slice(indent).startsWith("# ") ? 2 : 1;
        editor.replaceRange("", { line, ch: indent }, { line, ch: indent + mark });
      } else {
        editor.replaceRange("# ", { line, ch: indent });
      }
    }
  });
}

/**
 * Turns the textarea into the editor. `onChange(text)` on every edit, `onSave()` on
 * Ctrl+S. Resolves to the editor, or null when the panel was redrawn meanwhile.
 */
export async function mountCodeEditor(textarea, { onChange, onSave }) {
  await loadEditor();
  if (!textarea.isConnected) return null;
  const { CodeMirror } = window;
  const editor = CodeMirror.fromTextArea(textarea, {
    mode: { name: "python", version: 3 }, theme: "material-darker",
    lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
    matchBrackets: true,
    extraKeys: {
      Tab: cm => (cm.somethingSelected() ? cm.indentSelection("add")
        : cm.replaceSelection("    ", "end")),
      "Shift-Tab": cm => cm.indentSelection("subtract"),
      "Ctrl-/": toggleComment, "Cmd-/": toggleComment,
      "Ctrl-S": () => onSave(), "Cmd-S": () => onSave(),
    },
  });
  editor.on("change", () => onChange(editor.getValue()));
  // Measured again once laid out and once the fonts are in, for the same reason.
  requestAnimationFrame(() => editor.refresh());
  document.fonts?.ready.then(() => editor.refresh());
  return editor;
}
