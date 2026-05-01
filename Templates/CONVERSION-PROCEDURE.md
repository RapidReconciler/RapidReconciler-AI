# SPA Conversion Procedure

How to convert a single-article RapidReconciler University doc into the PO Receipts–style SPA layout.

## Inputs you need before starting

1. The source HTML file (single-article style, like Getting Started or Complex Password)
2. A clear sense of what the topics will be (the major divisions of the existing content)
3. Decide: are these topics **sequential** (a walkthrough) or **lookup-style** (reference)?
   - If walkthrough → group them under "Reconciliation Steps" or similar with `id="sidebar-steps"` so they get auto-numbered orange badges
   - If reference → group them under "Reference" without numbering
   - If both → use multiple groups (Overview / Steps / Reference) like PO Receipts itself

## Step-by-step

### 1. Catalog the source content

Read the source file and write down:
- The current top-level sections (`<h2>` headings)
- The current sub-sections (`<h3>` headings) under each — these will usually become inline headings inside a topic, NOT separate views
- Any tables, callouts, lists, images, or special markup that need to carry over
- Any cross-links to other docs (`administrator-walkthrough.html#users`, `complex-password.html`, etc.)

### 2. Decide the topic split

**Rule of thumb:** Each `.view` panel should be a substantial, readable chunk — not one paragraph. If a section is short (under ~200 words), merge it with an adjacent section. If a section is long (over ~600 words) and has clear sub-divisions, consider splitting.

For Getting Started, the natural split is:
- Index (home view with intro + table of topics)
- Logging In to the Application (was section 1, includes 1.1, 1.2, 1.3 as `<h2>` inside)
- Navigating the Application (was section 2, includes 2.1–2.4 as `<h2>` inside)
- Preparing to Use the Application (was section 3, includes 3.1, 3.2 as `<h2>` inside)

### 3. Copy the template

Copy `/home/claude/templates/SPA-TEMPLATE.html` to your working file. Replace the placeholder tokens:

| Placeholder | Replace with |
|---|---|
| `{{TITLE}}` | Page title (appears in browser tab) |
| `{{LOGO_DATA_URI_OR_PATH}}` | The base64 GSI logo (extract from any RapidReconciler doc — search for `<img src="data:image/jpeg;base64,/9j/4AAQ` and copy the entire src value, or use a relative path if logos are in an Images folder) |
| `{{PARENT_SECTION_ANCHOR}}` | e.g. `getting-started`, `po-receipts`, `inventory` |
| `{{PARENT_SECTION_NAME}}` | e.g. `Getting Started`, `PO Receipts`, `Inventory` |
| `{{CURRENT_PAGE_NAME}}` | e.g. `Application Basics` |
| `{{TITLE_LEFT}}` | First part of `<h1>`, normal navy |
| `{{TITLE_HIGHLIGHT}}` | Last word(s) of `<h1>`, blue-bright color |
| `{{SIDEBAR_TITLE}}` | All-caps orange header inside the sidebar card, e.g. `Application Basics`, `PO Receipts Walkthrough` |
| `{{HOME_HEADING}}` | `<h1>` of the Index/home view |
| `{{HOME_LEAD_PARAGRAPH}}` | First paragraph (use class `lead`) — sets the scene, says what this guide covers |

### 4. Build the sidebar

For each group of topics, add:

```html
<div class="sidebar-section-label">Group Name</div>
<ul class="sidebar-nav">
  <li data-target="slug1"><button onclick="showView('topic-slug1')">Topic Title</button></li>
  <li data-target="slug2"><button onclick="showView('topic-slug2')">Topic Title</button></li>
</ul>
```

For sequential numbered steps (auto-numbered orange circle badges):

```html
<div class="sidebar-section-label">Reconciliation Steps</div>
<ul class="sidebar-nav" id="sidebar-steps">
  <li data-target="step1" class="step-num"><button onclick="showView('topic-step1')">Step One</button></li>
  <li data-target="step2" class="step-num"><button onclick="showView('topic-step2')">Step Two</button></li>
</ul>
```

The first `<ul>` always contains `<li data-target="home">` for the Index button.

### 5. Build the Index (home) view

```html
<section id="home" class="view active">
  <h1>Page Title</h1>
  <p class="lead">One-paragraph orientation.</p>
  <div class="diamond-divider"><span class="diamond"></span></div>

  <h2>Getting Started</h2>
  <p>Direction for new users — link to first topic with
    <a href="javascript:void(0)" onclick="showView('topic-X')">Topic Name</a>.</p>

  <h2>Topics</h2>
  <table>
    <thead><tr><th>Topic</th><th>What It Covers</th></tr></thead>
    <tbody>
      <tr>
        <td><a href="javascript:void(0)" onclick="showView('topic-X')">Topic Name</a></td>
        <td>Short description.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout principle">
    <div class="callout-label">Key principle</div>
    <p>One-sentence guiding truth, if applicable.</p>
  </div>
</section>
```

The `class="active"` on the home view is crucial — it's what makes the home visible by default. No other view should have `active` in the source HTML.

### 6. Build each topic view

Pattern (duplicate per topic):

```html
<section id="topic-slug" class="view">
  <h1>Topic Title</h1>
  <p>Intro paragraph.</p>
  <div class="diamond-divider"><span class="diamond"></span></div>

  <!-- Topic content: h2 sub-headings, paragraphs, tables, callouts, figures -->

  <div class="topic-footer-nav">
    <button class="back-btn" onclick="goHome()">&larr; Back to Index</button>
    <button class="next-btn" onclick="showView('topic-NEXT')">Next: Next Title &rarr;</button>
  </div>
</section>
```

**Important conventions:**
- The `<h1>` inside each topic view repeats the topic title (the page-header `<h1>` is the doc-level title; topic `<h1>` is the topic title).
- Sub-sections that were `<h3>` in the original become `<h2>` inside the topic view (they're now under the topic `<h1>`, so they bump up one level).
- The diamond divider goes after the intro paragraph, before the first `<h2>`.
- Always include the `topic-footer-nav` at the bottom of each topic view.
- For the **last topic**, change the next button to `<button class="next-btn" onclick="goHome()">Return to Index &#8634;</button>`.

### 7. Image handling

If the source uses relative paths like `<img src="../Images/foo.png">` and you can't bundle the images:
- Either get the user to provide the images (mention this in the review)
- Or replace static images with synthetic SVG mockups inline

For real screenshots that you do have, place them in an `images/` folder next to the HTML and reference them as `images/filename.png`. Wrap each in a `<figure>` with a `<figcaption>`:

```html
<figure>
  <img src="images/foo.png" alt="Detailed description for screen readers">
  <figcaption><strong>Figure title</strong>One-line caption explaining what this shows.</figcaption>
</figure>
```

(The `<figure>`/`<figcaption>` styles need to be added — they're not in the PO Receipts CSS by default. Steal them from the Complex Password output.)

### 8. Cross-links between docs

Use the `.xref` style (also borrow from Complex Password CSS):

```html
<a class="xref" href="administrator-walkthrough.html#users">
  See <strong>Administrator Walkthrough &rarr; User Management</strong> for related steps
</a>
```

When the destination doc is also a SPA, the hash should match the topic slug, e.g. `complex-password.html#resetting`. The receiving SPA's JS already handles hash routing on load.

### 9. Final checks before delivery

Run these greps/tests on the output file:
- `grep -c '<section id=' file.html` — should equal the number of topics + 1 (for home)
- `grep -c 'class="view active"' file.html` — should equal exactly 1
- `grep -c 'topic-footer-nav' file.html` — should equal the number of topics (not home)
- HTML balance: `<section>` open count == close count, `<figure>` open count == close count

Then move the file to `/mnt/user-data/outputs/` and call `present_files`.

## Optional add-ons (carry from prior files)

These are CSS/markup patterns we developed for previous files but aren't in the base PO Receipts CSS. Add them to the `<style>` block as needed:

- **`.page-meta`** (last reviewed / reading time / Ctrl+F hint) — useful at the top of the home view
- **`figure` / `figcaption`** — for proper image captions
- **`.xref`** — for styled cross-doc links
- **`.quick-ref`** — orange-bordered side panel with a `dl` of task→location mappings
- **Common Pitfalls clusters** — multiple `.callout.tip` with diagnostic Q→A pattern

See `STYLE-PATTERNS.md` for the markup and CSS for each.
