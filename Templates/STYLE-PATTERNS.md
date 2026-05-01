# RapidReconciler Style Patterns

Reusable CSS + HTML patterns for the SPA template. Built from the Administrator Walkthrough and Complex Password files. Drop the CSS into the `<style>` block as needed; copy the markup into a topic view.

## Color palette (already in :root)

```
--navy:        #1f2d4a   /* primary text, h1/h2/h3 */
--navy-deep:   #142037   /* footer bg */
--navy-soft:   #2c3e63   /* h4 */
--blue:        #2b5fb0   /* links, blue callouts */
--blue-bright: #3d8fd6   /* h1 highlight (em), TOC active fallback */
--blue-pale:   #d6e6f5   /* link underline, blue callout bg */
--orange:      #f08a24   /* nav-cta, next-btn, sidebar accents, page-meta orange */
--orange-deep: #d97316   /* hover state for orange */
--bg-soft:     #f6f8fb   /* card bg, sidebar bg */
--bg-panel:    #eef3f9   /* code bg */
--text-soft:   #5a6479   /* secondary text */
--text-muted:  #8a93a6   /* tertiary, labels */
--rule:        #e1e7ef   /* light borders */
--rule-strong: #c9d3e0   /* darker borders */
--green:       #2e8b57   /* status green, special-character category color */
--red:         #c0392b   /* status red */
```

## 1. Page meta block

Last reviewed / reading time / search hint. Goes at the top of the home view, after the `<h1>` and lead paragraph.

**CSS:**
```css
.page-meta {
  display: flex;
  gap: 18px;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--rule);
}
.page-meta .meta-item { display: inline-flex; align-items: center; gap: 6px; }
.page-meta .meta-item strong { color: var(--text-soft); font-weight: 600; }
.page-meta kbd {
  background: #fff;
  border: 1px solid var(--rule-strong);
  border-bottom-width: 2px;
  border-radius: 3px;
  padding: 1px 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--navy);
}
```

**HTML:**
```html
<div class="page-meta">
  <span class="meta-item"><strong>Last reviewed:</strong>&nbsp;January 2026</span>
  <span class="meta-item"><strong>Reading time:</strong>&nbsp;~5 minutes</span>
  <span class="meta-item">Press <kbd>Ctrl</kbd>+<kbd>F</kbd> (or <kbd>⌘</kbd>+<kbd>F</kbd>) to search this page</span>
</div>
```

## 2. Figure with caption

Properly captioned image. Replaces bare `<img>` tags from old docs.

**CSS:**
```css
.view figure {
  margin: 22px 0;
}
.view figure img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 0 auto;
  border: 1px solid var(--rule);
  border-radius: 6px;
  background: var(--bg-soft);
}
.view figcaption {
  font-size: 13px;
  color: var(--text-soft);
  text-align: center;
  margin-top: 10px;
  line-height: 1.55;
  padding: 0 8px;
}
.view figcaption strong {
  display: block;
  color: var(--navy);
  font-weight: 700;
  font-size: 13.5px;
  margin-bottom: 3px;
}
```

**HTML:**
```html
<figure>
  <img src="images/screenshot-name.png" alt="Long descriptive alt text for screen readers, including any annotations">
  <figcaption><strong>Figure title</strong>One sentence describing what the figure shows or why it matters.</figcaption>
</figure>
```

## 3. Cross-reference link

Styled link from one doc into another (uses an arrow ↗). Distinguishable from inline anchor links.

**CSS:**
```css
.view .xref {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-panel);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--blue-bright);
  padding: 10px 14px;
  border-radius: 4px;
  font-size: 13.5px;
  color: var(--text);
  text-decoration: none !important;
  border-bottom: 1px solid var(--rule) !important;
  margin: 6px 0;
  transition: background 0.15s, border-color 0.15s;
}
.view .xref:hover {
  background: var(--blue-pale);
  color: var(--navy) !important;
  border-left-color: var(--blue) !important;
}
.view .xref::before { content: '↗'; color: var(--blue); font-weight: 700; }
.view .xref strong { color: var(--navy); font-weight: 700; }
```

**HTML:**
```html
<a class="xref" href="administrator-walkthrough.html#users">
  See <strong>Administrator Walkthrough &rarr; User Management</strong> for related steps
</a>
```

## 4. Quick reference panel (task → location)

Orange left-bordered side panel. Useful on the home view to give users an at-a-glance "where do I do X" map.

**CSS:**
```css
.view .quick-ref {
  background: var(--bg-soft);
  border: 1px solid var(--rule);
  border-left: 4px solid var(--orange);
  border-radius: 4px;
  padding: 16px 20px;
  margin: 18px 0;
}
.view .quick-ref-title {
  font-family: 'Source Sans 3', sans-serif;
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--orange);
  margin-bottom: 10px;
}
.view .quick-ref dl {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 6px 18px;
  margin: 0;
}
.view .quick-ref dt {
  font-weight: 700;
  color: var(--navy);
  font-size: 13.5px;
}
.view .quick-ref dd {
  margin: 0;
  font-size: 13.5px;
  color: var(--text-soft);
}
```

**HTML:**
```html
<div class="quick-ref">
  <div class="quick-ref-title">Quick Reference</div>
  <dl>
    <dt>Add a user</dt>
    <dd>Admin &rarr; Users &rarr; Add User</dd>
    <dt>Reset a password</dt>
    <dd>Admin &rarr; Users &rarr; (select user) &rarr; Reset</dd>
    <dt>Change company info</dt>
    <dd>Admin &rarr; Company</dd>
  </dl>
</div>
```

## 5. Common Pitfalls cluster

Several `.callout.tip` callouts in a row, each with a diagnostic Q→A pattern. Used at the end of topics where users frequently get stuck.

**HTML (CSS already in place):**
```html
<h2>Common Pitfalls</h2>

<div class="callout tip">
  <div class="callout-icon">i</div>
  <div>
    <p><strong>Q: Why don't I see the new user in the list?</strong></p>
    <p>A: The list is paginated; check page 2 or use the search field at the top of the table.</p>
  </div>
</div>

<div class="callout tip">
  <div class="callout-icon">i</div>
  <div>
    <p><strong>Q: Why didn't the user get the welcome email?</strong></p>
    <p>A: Confirm the email address is correct and ask the user to check their spam folder. If still missing, see <a class="xref" href="complex-password.html">Complex Passwords &rarr; Resetting a Password</a>.</p>
  </div>
</div>
```

The `<div>` wrapper inside `.callout` is needed when the content is multiple paragraphs — the base `.callout` flexes the icon and a single child. Add this CSS if not present:

```css
.view .callout > div { flex: 1; }
.view .callout > div p { margin-bottom: 12px; }
.view .callout > div p:last-child { margin-bottom: 0; }
```

## 6. SVG mockup container

When you need to draw a synthetic UI element (menu, popup, breakdown diagram) inline. The container ensures consistent spacing.

**CSS:**
```css
.view .svg-mock {
  display: block;
  margin: 18px auto 8px;
  max-width: 100%;
  height: auto;
}
```

**HTML pattern (example: a menu strip):**
```html
<svg class="svg-mock" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 80" font-family="'Source Sans 3', sans-serif" role="img" aria-label="Admin menu showing three items: Users, Company, Settings">
  <rect x="0" y="0" width="600" height="80" fill="#1f2d4a" rx="4"/>
  <text x="40"  y="48" font-size="16" font-weight="600" fill="#fff">Users</text>
  <text x="160" y="48" font-size="16" font-weight="600" fill="#fff">Company</text>
  <text x="320" y="48" font-size="16" font-weight="600" fill="#fff">Settings</text>
</svg>
```

Use SVGs (not PNGs) for diagrams that don't represent a real screenshot — they scale crisply and are easy to edit. Reserve PNGs for actual annotated screenshots.

## 7. "Done — Back to Index" green button (last topic)

For the last topic in a sequential walkthrough, swap the orange `next-btn` for a green completion button.

**CSS (add):**
```css
.view .topic-footer-nav .done-btn {
  background: var(--green);
  border-color: var(--green);
  color: #fff;
  border: 1px solid;
  padding: 10px 18px;
  border-radius: 4px;
  font-family: 'Open Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.view .topic-footer-nav .done-btn:hover {
  background: #246e44;
  border-color: #246e44;
}
```

**HTML (last topic only):**
```html
<div class="topic-footer-nav">
  <button class="back-btn" onclick="goHome()">&larr; Back to Index</button>
  <button class="done-btn" onclick="goHome()">Done &mdash; Back to Index &#x2713;</button>
</div>
```

## 8. Email preview block (kept from original PO Receipts CSS)

For inline-display of an email's "from / subject / body" content. CSS already in PO Receipts; HTML pattern:

```html
<div class="email-card">
  <div class="label">From</div>
  <div class="addr">rrsupport@getgsi.com</div>
  <div class="label">Subject</div>
  <p style="margin: 4px 0 12px; font-weight: 600;">Your RapidReconciler password reset</p>
  <p>Hi {{name}},</p>
  <p>Click the link below to reset your password. This link expires in 24 hours.</p>
  <p style="margin-bottom: 0;"><a href="#" class="email-compose-btn">Reset Password</a></p>
</div>
```

## 9. KV grid (key-value cards)

Already in PO Receipts CSS. Use to show a small set of facts in card form.

```html
<div class="kv-grid">
  <div class="kv-card">
    <div class="kv-label">Module</div>
    <div class="kv-value"><strong>PO Receipts</strong></div>
  </div>
  <div class="kv-card">
    <div class="kv-label">Source Tables</div>
    <div class="kv-value">F43121, F0902, F0911</div>
  </div>
</div>
```

## 10. Status pills (green / yellow / red)

Already in PO Receipts CSS. Use inline in tables or paragraphs.

```html
<span class="status-pill green">Reconciled</span>
<span class="status-pill yellow">In Progress</span>
<span class="status-pill red">Out of Balance</span>
```

## 11. Numbered cells in tables (orange numbers)

Already in PO Receipts CSS. Use for sequential rows in process-flow tables.

```html
<table>
  <thead>
    <tr><th>#</th><th>Step</th><th>Result</th></tr>
  </thead>
  <tbody>
    <tr><td class="num-cell">1</td><td>PO Receipt</td><td>Increases RNV</td></tr>
    <tr><td class="num-cell">2</td><td>Voucher Match</td><td>Decreases RNV</td></tr>
  </tbody>
</table>
```

## 12. Checklist card (boxes, not bullets)

Already in PO Receipts CSS. Use for "before you begin" or "things to verify" lists where each item is a check.

```html
<ul class="checklist">
  <li class="checklist-title">Before you begin</li>
  <li>You have administrator access in JD Edwards</li>
  <li>Period close has not yet been finalized</li>
  <li>JDE data has been imported into RapidReconciler today</li>
</ul>
```

(Visual: navy header bar; each item has an empty checkbox icon to the left.)

---

## Annotation pattern for screenshots (PIL/Pillow)

When you need to annotate a real screenshot — orange highlight box on a UI element + white callout box with explanation — use this Python pattern:

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.open('source.png').convert('RGBA')

# Extend canvas right for callout panel
W, H = img.size
panel_w = 220
canvas = Image.new('RGBA', (W + panel_w, H), '#f6f8fb')
canvas.paste(img, (0, 0))

draw = ImageDraw.Draw(canvas)
# Orange highlight rectangle around UI element
# Coordinates in original-image space (not canvas)
hl_x, hl_y, hl_w, hl_h = 100, 200, 180, 30
draw.rectangle([hl_x, hl_y, hl_x + hl_w, hl_y + hl_h], outline='#f08a24', width=3)

# Arrow from highlight to callout
draw.line([(hl_x + hl_w, hl_y + hl_h // 2), (W + 20, hl_y + hl_h // 2)],
          fill='#f08a24', width=2)

# Callout box
cx, cy, cw, ch = W + 20, hl_y - 20, 180, 80
draw.rectangle([cx, cy, cx + cw, cy + ch], fill='#fff', outline='#1f2d4a', width=1)
font_bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
font_reg = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
draw.text((cx + 10, cy + 8), 'Callout title', fill='#1f2d4a', font=font_bold)
draw.text((cx + 10, cy + 28), 'Body explanation,\nwrapped manually.', fill='#5a6479', font=font_reg)

canvas.convert('RGB').save('annotated.png', 'PNG')
```

Verify the actual UI text from the source by reading it directly — never paraphrase error messages or button labels. If the original UI has a typo (e.g. "lowercse"), preserve it; users searching for the literal error text need to find your doc.
