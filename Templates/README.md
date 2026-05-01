# RapidReconciler University SPA Templates

Reusable assets for converting single-article RapidReconciler docs into the PO Receipts–style SPA layout.

## Files in this folder

- **`SPA-TEMPLATE.html`** — The full SPA boilerplate (793 lines). Complete CSS block from PO Receipts, top nav, page header, sidebar shell, content card, and JS. Placeholder tokens marked `{{LIKE_THIS}}` and `<!-- TODO -->` comments mark where to insert content.

- **`CONVERSION-PROCEDURE.md`** — Step-by-step procedure for converting any single-article doc. Covers cataloging source content, deciding the topic split, replacing template tokens, building the sidebar, building the index view, building each topic, image handling, cross-links, and final HTML balance checks.

- **`STYLE-PATTERNS.md`** — Quick-reference for reusable patterns developed for the Administrator Walkthrough and Complex Password files. Includes copy-paste CSS + HTML for: page meta, figure/figcaption, xref links, quick reference panels, common pitfalls clusters, SVG mockup containers, "Done" green button, email preview, KV grid, status pills, numbered table cells, checklist cards, plus the PIL annotation pattern for screenshots.

## Workflow for the next file

1. Read source HTML.
2. Read `CONVERSION-PROCEDURE.md`.
3. Copy `SPA-TEMPLATE.html` to working file, replace top-of-file placeholders.
4. Catalog source sections, decide topic split, build sidebar accordingly.
5. Build index/home view + each topic view.
6. Pull in optional add-ons from `STYLE-PATTERNS.md` as needed (page meta, xref, figures).
7. Run HTML balance + active-view checks (described in procedure).
8. Move to outputs, present_files.

## Style decisions established (don't relitigate)

- Colors and fonts as in `:root` of SPA-TEMPLATE
- Topic `<h1>` repeats topic title (page-header `<h1>` is doc-level title)
- Sub-sections that were `<h3>` in source become `<h2>` inside topic view
- Diamond divider after intro paragraph, before first `<h2>`
- Each topic ends with `topic-footer-nav` (back + next buttons)
- Last topic in a sequential walkthrough uses green "Done" button
- Preserve UI typos verbatim ("lowercse", etc.) — users search for actual error text
- SVG inline for synthetic diagrams; PNG (with figure/figcaption) for annotated screenshots
- aria-hidden="true" on decorative `§` num spans
