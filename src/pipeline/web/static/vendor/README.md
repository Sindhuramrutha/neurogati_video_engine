# Vendored libraries

## pptx-preview 1.0.7 (ISC)

Renders a `.pptx` in the browser from the raw file — no server-side conversion,
no derived PDF or PNG. The deck the pipeline stores is the deck you look at.

Vendored rather than loaded from a CDN so the app keeps working offline, which
is the same reason the file icons are drawn rather than fetched.

The UMD build is used because it carries its own zip reader and defines a single
global (`pptxPreview`), so the page needs no module loader and no other script.

## pdf.js 4.10.38 (Apache-2.0, `pdfjs-LICENSE.txt`)

Draws a PDF's pages in the browser from the raw file, for the page strip on the
Inputs page -- thumbnails down the left, one page at full width, and pages that
can be deleted -- which the browser's own PDF viewer cannot give.

`pdf.min.js` and `pdf.worker.min.js` are `build/pdf.min.mjs` and
`build/pdf.worker.min.mjs` from the npm package `pdfjs-dist`, renamed so the
static server sends them as JavaScript. Both are ES modules.

## CodeMirror 5.65.16 (MIT, `codemirror/LICENSE`)

The code editor for a scene's script in the Generation stage's side panel:
line numbers, Python colouring, bracket matching and search. The minified files
are jsDelivr's builds of the npm package `codemirror@5.65.16` (`lib/`, `mode/python`,
`addon/edit/matchbrackets`, `addon/search/{search,searchcursor}`,
`addon/dialog/dialog`, `theme/material-darker`). Version 5 rather than 6 because
it is plain scripts with one global (`CodeMirror`), needing no bundler.
