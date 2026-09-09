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
const readModule = name => readFileSync(join(staticDirectory, name), "utf8");

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

console.log(failureCount ? `\n${failureCount} contract(s) failed` : "\nall contracts hold");
process.exit(failureCount ? 1 : 0);
