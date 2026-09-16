# Vendored libraries

## pptx-preview 1.0.7 (ISC)

Renders a `.pptx` in the browser from the raw file — no server-side conversion,
no derived PDF or PNG. The deck the pipeline stores is the deck you look at.

Vendored rather than loaded from a CDN so the app keeps working offline, which
is the same reason the file icons are drawn rather than fetched.

The UMD build is used because it carries its own zip reader and defines a single
global (`pptxPreview`), so the page needs no module loader and no other script.
