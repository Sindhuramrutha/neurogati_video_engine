// Contract checks over the browser modules.
//
// These are static assertions, not a DOM test suite: they guard invariants that
// are easy to break silently during a refactor and impossible to notice by
// reading one file. Run with `node tests/test_frontend_contracts.js`.

import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const staticDirectory = join(
  dirname(fileURLToPath(import.meta.url)), "..", "src", "pipeline", "web", "static");

const javascriptFiles = readdirSync(staticDirectory).filter(name => name.endsWith(".js"));
// One stylesheet per page, plus the base they share. Read as a set rather than
// by name so a new page's stylesheet is covered the day it is added.
const stylesheetNames = readdirSync(join(staticDirectory, "styles"))
  .filter(name => name.endsWith(".css"));
// Line endings are normalised away: this repo checks out CRLF on Windows and LF
// elsewhere, and a contract about what the code does must not depend on which.
const readModule = name =>
  readFileSync(join(staticDirectory, name), "utf8").replace(/\r\n/g, "\n");

let failureCount = 0;
function check(description, assertion) {
  try { assertion(); console.log(`  ok   ${description}`); }
  catch (failure) { failureCount++; console.error(`  FAIL ${description}\n       ${failure.message}`); }
}

console.log("frontend contracts:");

check("no module calls fetch directly — all HTTP goes through requestJsonFromApi", () => {
  const offenders = javascriptFiles.filter(name =>
    name !== "shared-client.js" && /\bfetch\s*\(/.test(readModule(name)));
  assert.deepEqual(offenders, [],
    `these bypass the shared HTTP contract: ${offenders.join(", ")}`);
});

check("only shared-client defines HTML escaping", () => {
  const offenders = javascriptFiles.filter(name =>
    name !== "shared-client.js" && /function escapeHtml|const escapeHtml\s*=\s*\w+\s*=>/.test(readModule(name)));
  assert.deepEqual(offenders, [],
    `duplicate escaping implementations drift apart: ${offenders.join(", ")}`);
});

check("only document-editing generates item identifiers", () => {
  const offenders = javascriptFiles.filter(name =>
    name !== "document-editing.js" && /crypto\.randomUUID/.test(readModule(name)));
  assert.deepEqual(offenders, [],
    `inline id generation drifted back into: ${offenders.join(", ")}`);
});

check("only document-editing implements optimistic save with rollback", () => {
  const offenders = javascriptFiles.filter(name =>
    name !== "document-editing.js" && /structuredClone\(applicationState/.test(readModule(name)));
  assert.deepEqual(offenders, [],
    `a stage reimplemented the save/rollback dance: ${offenders.join(", ")}`);
});

check("every project-scoped state field is cleared on project switch", () => {
  const uiKit = readModule("ui-kit.js");
  const scopedBlock = uiKit.slice(
    uiKit.indexOf("PROJECT_SCOPED_STATE_DEFAULTS = {"),
    uiKit.indexOf("};", uiKit.indexOf("PROJECT_SCOPED_STATE_DEFAULTS = {")));
  // Every per-project document must appear in the reset list, or switching
  // project leaves one project's data addressable under another's slug.
  for (const documentKind of ["plan", "script", "composition", "review", "stageSettings"]) {
    assert.ok(scopedBlock.includes(`${documentKind}:`),
      `${documentKind} is not cleared when the project changes`);
  }
});

check("a save sends the edited document, not whatever a redraw reloaded", () => {
  // Every stage's render reloads its document from the server. When the body
  // was built after the optimistic redraw, it was built from that reloaded,
  // unedited copy, and every click-edit on four stages was silently lost.
  const editing = readModule("document-editing.js");
  const payloadAt = editing.indexOf("const payload = JSON.stringify(buildPayload(");
  const redrawAt = editing.indexOf("if (!silent) await rerender();");
  assert.ok(payloadAt > 0, "the payload must be captured into a variable");
  assert.ok(redrawAt > 0, "the optimistic redraw moved; re-check this contract");
  assert.ok(payloadAt < redrawAt, "the payload is built after the redraw that reloads the document");
  assert.ok(editing.includes("inFlightSavesByDocumentKind.has(documentKind)\n      && applicationState[documentKind]"),
    "a load during a save must return the edited copy, not the server's old one");
});

check("saves verify the project has not changed mid-request", () => {
  const editing = readModule("document-editing.js");
  assert.ok(editing.includes("projectSlugAtEditTime"),
    "editStageDocument must capture the project it started against");
  assert.ok(editing.includes("selectedProject?.slug !== projectSlugAtEditTime"),
    "a response arriving after a project switch must be discarded");
});

check("no in-flight guard silently drops a user action", () => {
  const offenders = [];
  for (const name of javascriptFiles) {
    const source = readModule(name);
    if (/(InFlight|isSaving\w*)\)\s*return;/.test(source)) offenders.push(name);
  }
  assert.deepEqual(offenders, [],
    `these drop a click with no feedback: ${offenders.join(", ")}`);
});

check("the stylesheet has no truncated or empty rules", () => {
  // Self-inflicted, once: a regex meant for `color:` also matched the `color:`
  // inside `border-color:` and left `border-` behind in thirteen rules. A
  // browser drops a malformed declaration silently, so nothing failed and those
  // rules simply stopped working. Cheap to check, invisible otherwise.
  const stylesheet = stylesheetNames
    .map(name => readFileSync(join(staticDirectory, "styles", name), "utf8"))
    .join("\n");

  const truncated = stylesheet.match(/[a-z-]+:\s*[;}]|[a-z]+-\s*[;}]/g) ?? [];
  assert.deepEqual(truncated, [], `truncated declarations: ${truncated.join(", ")}`);

  const empty = stylesheet.match(/\{\s*\}/g) ?? [];
  assert.equal(empty.length, 0, `${empty.length} rule(s) declare nothing`);

  const openers = (stylesheet.match(/\{/g) ?? []).length;
  const closers = (stylesheet.match(/\}/g) ?? []).length;
  assert.equal(openers, closers, "unbalanced braces in the stylesheet");
});

check("every stage has its own stylesheet, and the page loads them all", () => {
  // One stylesheet per page is deliberate, and costs a request each: knowing
  // where to change a page's look is worth more here than the request is. A
  // stage added without one would quietly land its rules back in the base.
  const stageKeys = readFileSync(join(staticDirectory, "..", "..", "stages.py"), "utf8")
    .match(/^\s{4}[A-Z_]+ = "([a-z-]+)"$/gm)
    .map(line => line.split('"')[1]);
  const page = readFileSync(join(staticDirectory, "index.html"), "utf8");

  for (const key of stageKeys) {
    assert.ok(stylesheetNames.includes(`${key}.css`), `no stylesheet for the ${key} stage`);
  }
  for (const name of stylesheetNames) {
    assert.ok(page.includes(`/static/styles/${name}`), `${name} is never loaded`);
  }
  assert.ok(page.indexOf("styles/base.css") < page.indexOf("styles/extraction.css"),
    "the base must load before the pages that override it");
});

check("no source file carries invisible control characters", () => {
  // U+0080-U+009F never belong in hand-written source; they arrive by accident.
  // The list bullet in Extracted text was one: the CSS escape `\2022` passed
  // through a Python string, where `\202` is octal for U+0082, and every list
  // item showed a stray "2".
  const everySource = [
    ...readdirSync(staticDirectory)
      .filter(name => /\.(js|css|html)$/.test(name))
      .map(name => [name, join(staticDirectory, name)]),
    ...stylesheetNames.map(name => [`styles/${name}`, join(staticDirectory, "styles", name)]),
  ];
  const damaged = everySource
    .flatMap(([name, path]) => readFileSync(path, "utf8").replace(/\r\n/g, "\n").split("\n")
      .map((line, index) => /[\u0080-\u009f]/.test(line) ? `${name}:${index + 1}` : null)
      .filter(Boolean));
  assert.deepEqual(damaged, [], `control characters at ${damaged.join(", ")}`);
});

console.log(failureCount ? `\n${failureCount} contract(s) failed` : "\nall contracts hold");
process.exit(failureCount ? 1 : 0);
