// What a model writes back, as it is shown.
//
// Unlike the contract checks next door, these run the code: the renderer takes
// untrusted text straight from a provider and turns it into HTML, so its
// behaviour is worth executing rather than reading.
//
// Run with `node tests/test_answer_rendering.mjs`.

import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const staticDirectory = join(
  dirname(fileURLToPath(import.meta.url)), "..", "src", "pipeline", "web", "static");

const { renderModelMarkdown } = await import(
  pathToFileURL(join(staticDirectory, "shared-client.js")).href);

let failureCount = 0;
function check(description, assertion) {
  try { assertion(); console.log(`  ok   ${description}`); }
  catch (failure) { failureCount++; console.error(`  FAIL ${description}\n       ${failure.message}`); }
}

console.log("model answers:");

check("bold, italic and code become tags", () => {
  const html = renderModelMarkdown("**Planning** says *fine*, see `plan.json`");
  assert.match(html, /<b>Planning<\/b>/);
  assert.match(html, /<i>fine<\/i>/);
  assert.match(html, /<code>plan\.json<\/code>/);
});

check("headings do not shout over the answer", () => {
  const html = renderModelMarkdown("## Which is weaker?\n\nThe plan.");
  assert.match(html, /answer-heading/);
  assert.ok(!/<h[1-6]/.test(html), "a real heading tag would outsize the reply");
  assert.ok(!html.includes("##"), "the hashes are still visible");
});

check("bullets and numbered points become one list", () => {
  const html = renderModelMarkdown("- first\n- second\n\n1. one\n2. two");
  assert.equal((html.match(/<ul>/g) ?? []).length, 2);
  assert.equal((html.match(/<li>/g) ?? []).length, 4);
  assert.ok(!html.includes("1."), "the numbering is still in the text");
});

check("paragraphs survive; blank lines do not double up", () => {
  const html = renderModelMarkdown("One.\n\n\n\nTwo.");
  assert.equal((html.match(/<p>/g) ?? []).length, 2);
});

// The safety property. Escaping runs over the whole string before any tag is
// added, so nothing a provider returns can become live markup.
check("a reply containing HTML is shown, not run", () => {
  const html = renderModelMarkdown("<script>alert(1)</script>");
  assert.ok(!html.includes("<script>"), "the tag reached the page intact");
  assert.match(html, /&lt;script&gt;/);
});

check("an image tag with a handler cannot execute", () => {
  const html = renderModelMarkdown('<img src=x onerror="alert(1)">');
  assert.ok(!html.includes("<img"), "the tag reached the page intact");
  assert.ok(!html.includes('onerror="'), "the handler survived as an attribute");
});

check("markup inside bold is escaped too", () => {
  const html = renderModelMarkdown("**<b onclick='x'>hi</b>**");
  assert.match(html, /<b>&lt;b onclick/);
  assert.ok(!html.includes("onclick='x'>"), "the attribute survived");
});

check("quotes and ampersands come through readable", () => {
  const html = renderModelMarkdown(`He said "it's 3 & 4"`);
  assert.ok(!html.includes('"it'), "a raw quote could close an attribute");
  assert.match(html, /&amp;/);
});

check("an asterisk that is not emphasis is left alone", () => {
  const html = renderModelMarkdown("3 * 4 = 12");
  assert.match(html, /3 \* 4 = 12/);
});

check("empty and missing text do not throw", () => {
  assert.equal(renderModelMarkdown(""), "");
  assert.doesNotThrow(() => renderModelMarkdown(null));
});

console.log(failureCount ? `\n${failureCount} failed` : "\nall answer checks hold");
process.exit(failureCount ? 1 : 0);
