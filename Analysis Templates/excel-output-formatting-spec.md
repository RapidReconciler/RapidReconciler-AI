# Excel Output Formatting Specification

## RapidReconciler Analysis Workbooks — Shared Formatting Reference

This document is the **change master** for Excel output formatting across all RapidReconciler analysis guides. Each guide is fully self-contained and can be used in a two-file session (guide + export) without this document. This document exists so that when formatting changes, they are made here first and then propagated to all guides in a single update session.

**How to use this document:**
- To change formatting across all guides, update this document first, then upload it with all seven guides and ask Claude to propagate the changes.
- Individual guide sessions do not require this document — the guide alone contains everything Claude needs to produce a correctly formatted output.
- When a detail in this document conflicts with a guide, this document is the intended standard and the guide should be updated to match.

**Design intent:** Output workbooks are designed to be readable on widescreen displays at trade shows and in front of users with limited analysis skills. The Analysis sheet leads with a plain-English headline and a single large variance number, then communicates findings as three labelled cards (WHAT happened / WHY it happened / HOW to fix it) rather than as a numbered analytical report. Detail belongs on the source sheet; the Analysis sheet should be scannable from across a room.

---

## Section 1: File Naming

Output files are named with a per-document pattern that identifies both the report type and the specific document being analyzed:

```
{Report Name} Analysis for {key identifier}.xlsx
```

Each guide defines its own `{Report Name}` and `{key identifier}` values. The identifier should be the smallest piece of information that uniquely distinguishes one analysis run from another, so users can save multiple analyses side-by-side without overwriting.

Examples:

| Guide | Output Filename |
|---|---|
| Transaction Detail Analysis | `Transaction Detail Analysis for DOC-00001 RI.xlsx` |
| Item Roll Forward Analysis | `Item Roll Forward Analysis for ITEM-00004.xlsx` |
| Cardex Variance Analysis | `Cardex Variance Analysis for Item {item} {branch}.xlsx` (e.g., `Cardex Variance Analysis for Item 555 IDM.xlsx`) |
| Stock Status / Trial Balance Analysis | `Stock Status Analysis for {company} {period}.xlsx` |

The exact identifier format is specified in each guide's output specification. Where the source export does not contain a single distinguishing field, fall back to the date and time the analysis was run (e.g., `…Analysis 2026-04-25.xlsx`).

---

## Section 2: Workbook Structure

Every output workbook contains exactly two sheets:

| Tab Position | Sheet | Contents |
|---|---|---|
| **1 (left)** | **Analysis sheet** | The card-based analysis written by Claude — this is the active sheet when the workbook opens. Sheet name: `Analysis`. |
| **2 (right)** | **Source sheet** | The original export data, with optional modifications that improve clarity (see below). |

The Analysis sheet must always be the first (leftmost) tab and must be set as the active sheet so it displays when the workbook is opened.

Do not delete or rename the source sheet. Permitted modifications to the source sheet are:

- **Row highlights** matching priority colours (see Section 3.3)
- **AutoFilter** on the header row (see Section 3.1)
- **Freeze panes** so the header stays visible (see Section 3.2)
- **Sorting** the data rows when the export's native order obscures the analysis. In particular, exports that arrive in descending chronological order must be sorted ascending — see Section 3.4.
- **Removing legacy explanatory blocks** ("HIGHLIGHT KEY" legends and similar) that earlier output formats added below the data. These were never part of the source export and conflict with the new Evidence severity badges.
- **Cleaning legacy per-cell text colours** that earlier formats applied as a row-level highlight. The new format relies on fills, not text colour, for severity.
- **Adjusting column widths** for readability if the export ships with widths that clip data. Do not delete or add columns.

Do not add columns, formulas, or comments to the source sheet beyond what is listed above. The source sheet should still be recognisable as the original export — modifications are limited to clarifying what is already there, not augmenting it.

---

## Section 3: Source Sheet Formatting

### 3.1 AutoFilter

Enable AutoFilter on the header row (row 2 in most exports; row 4 in the Item Roll Forward export which has a multi-row header). The filter range covers all columns.

### 3.2 Freeze Panes

Set freeze panes so the header row stays visible while scrolling:

| Export | Freeze At |
|---|---|
| All standard exports (header on row 2) | `A3` |
| Item Roll Forward (header on row 4) | `A5` |

### 3.3 Row Highlights

Apply background colour to data rows based on priority classification. Apply the highlight to all columns in the row. When a row qualifies for multiple priorities, the higher priority (lower number) takes precedence. The same row that is highlighted on the source sheet is the row referenced by an Evidence link on the Analysis sheet — the two views must agree.

| Priority | Fill Colour | Hex | Criteria |
|---|---|---|---|
| **Priority 1** | Light red | `FFE0E0` | Highest severity — the row(s) directly responsible for the variance (Root cause) |
| **Priority 2** | Light orange | `FFF0DC` | High severity — Anchor rows (where the variance is observed) and Related rows (supporting context). See Section 6.5 for the Anchor/Related distinction. |
| **Priority 3** | Light yellow | `FEFBD8` | Informational — context rows, low-priority gaps, configuration observations |

The specific criteria that trigger each priority level are defined in each analysis guide.

**Source-sheet hygiene when reformatting an existing workbook:** earlier versions of some workbooks added explanatory legend blocks ("HIGHLIGHT KEY") below the data on the source sheet. These violate the rule that the source sheet contains only export data plus the spec-permitted modifications. When reformatting, remove any such legend blocks — including their values, fills, borders, and merged cells — before applying the new highlights. The Evidence severity badges on the Analysis sheet replace the need for an inline legend.

### 3.4 Data Order — Ascending by Sequence Key

Exports that contain a sequence key (`ukid`, `transdate`, document number, period — whatever advances monotonically with time) must be sorted **ascending** before analysis. Many JD Edwards exports default to descending order (most recent transaction first), which is helpful for browsing recent activity but actively misleading for root-cause work because:

- Running totals (`runqty`, `runamt`, balance fields) only make sense bottom-up in descending order. Reading top-down in descending order makes each row look like the running total *before* the transaction posted, when in fact it's the running total *after*.
- Cause-and-effect relationships are inverted. The transaction that caused a downstream problem appears below the symptom, not above it.

The analysis itself must be performed against the data in ascending order — every "qty change" calculation, every cumulative total, every "what caused what" reasoning step assumes ascending traversal. If the export arrives in descending order, sort the source sheet ascending before applying highlights, and re-point Evidence hyperlinks at the new row positions.

Anchor rows (Curr bal, RR Total, period closing balance) typically sort to the bottom of the data after ascending sort because they carry the highest sequence key by design (e.g., `ukid = 999999999999` on the Curr bal row). Reference rows (Beg bal, opening position) sort to the top. This is the natural reading order: start at the opening, watch the ledger build through the transaction history, end at the current state.

Specific exports that require sorting:

| Export | Sort Key | Direction | Notes |
|---|---|---|---|
| Item Roll Forward | `ukid` (column C) | Ascending | Beg bal (ukid 0) sorts to top; Curr bal (ukid 999999999999) sorts to bottom |
| Transaction Detail | (no sort needed) | — | The source already groups by section type rather than sequence |
| Other exports | Per guide | Ascending where a sequence key exists | Default to ascending whenever a clear sequence key is present |

---

## Section 4: Analysis Sheet Layout

### 4.1 Overall Structure

The Analysis sheet uses a **5-column card layout** designed to be scannable on widescreen displays. The vertical flow is fixed:

1. **Brand strip** (1 thin navy row)
2. **Headline row** — the page's primary subject (item ID for item-focused analyses, document ID for document-focused analyses). Navy fill, white text, 20pt bold.
3. **Variance subline** — the variance described in plain English. Light blue fill, dark blue text, 12pt bold.
4. **Secondary context strip** — the small reference fields (GL class, GL account, std cost, period, company, etc.) that don't fit in the headline or subline. White fill, dark grey text, 10pt.
5. **Variance card** — Priority strip + huge variance number + pattern label + priority rationale (priority colour fill)
6. **Three findings cards** — WHAT happened / WHY it happened / HOW to fix it
7. **Evidence list** — hyperlinks to the relevant rows on the source sheet, with severity badges
8. **Caution note** — wheat-coloured warning row
9. **Footer** — small italic line identifying the guide and date

Findings are NOT organized as numbered sections (Document / Unassigned Check / RR Summary / Root Cause / Evidence / Recommended Action) as in earlier versions. The card layout replaces that structure.

**Headline vs. subline content depends on the report type:**

| Report type | Headline (navy strip) | Subline (light blue) |
|---|---|---|
| Item-focused (Cardex Variance, Item Roll Forward) | Item ID and primary identifying location | Variance described in plain English |
| Document-focused (Transaction Detail) | Document ID, type, and order context | Variance described in plain English |
| Period/aggregate analyses | Period and scope (company, branch) | Aggregate variance summary |

The headline answers "what is this page about" — usually a noun phrase, no verb. The subline answers "what's wrong" — a full sentence with a number.

### 4.2 Column Structure

| Column | Width (chars) | Typical Content |
|---|---|---|
| A | 24 | Card titles, evidence link text, headline labels |
| B | 30 | (Used in merges with A) |
| C | 38 | Pattern label, evidence detail text |
| D | 22 | (Used in merges with A:C for card bodies) |
| E | 22 | Severity badges; right-hand margin on card bodies |

**Merge patterns:**

| Element | Merge | Notes |
|---|---|---|
| Headline | A:E | Full width |
| Variance subline | A:E | Full width |
| Secondary context strip | A:E | Full width |
| Variance priority strip | A:E | Full width |
| Variance number row | A:B \| C:E | Big number on the left half, pattern + rationale on the right |
| Card header (WHAT/WHY/FIX) | A:E | Full width |
| Card body (WHAT/WHY/FIX) | **A:D** | Column E carries the same fill as the body (acts as right margin) — narrower body width keeps line length comfortable |
| Evidence header | A:B \| C:D \| E | Title on the left, blank middle, "Severity" on the right |
| Evidence row | A:B \| C:D \| E | Hyperlink, detail, severity badge |
| Caution note | A:E | Full width |
| Footer | A:E | Full width |

These are starting widths. Do not auto-stretch columns to the full sheet width.

### 4.3 Wrap Text and Row Heights

- Enable wrap text on **all cells** on the Analysis sheet.
- Card body rows are sized so the longest expected wrapped paragraph fits without clipping. Standard heights:

| Row Type | Height |
|---|---|
| Brand strip | 6pt |
| Headline | 38pt |
| Variance subline | 24pt |
| Secondary context strip | 18pt |
| Variance priority strip | 20pt |
| Variance number + pattern + rationale row | 80–90pt |
| Card header (WHAT / WHY / FIX) | 28pt |
| WHAT card body | 100–130pt |
| WHY card body | 130–215pt (varies — paragraph breaks help) |
| FIX card body | 200–290pt (typically the tallest — must accommodate numbered steps with blank-line separators) |
| Evidence header | **40pt (fixed)** |
| Evidence row | 44pt |
| Caution note | 70pt |
| Footer | 18pt |
| Spacer rows | 8–14pt |

These are nominal values. If a particular case has unusually long card text, increase the affected card body row only. The Evidence header is **fixed at 40pt** regardless of content — this is not a calculated height.

### 4.4 Grid Lines

Disable grid lines on the Analysis sheet (`showGridLines = False`).

### 4.5 Page Setup

Set the print area to cover the full analysis content (typically `A1:R28` for current builds — adjust to match the last row of the analysis content, which extends further than older versions because of the secondary context strip and paragraph-broken card bodies). Landscape, fit-to-page enabled, paper size Tabloid (11×17). Margins 0.3 in all sides, horizontally centered. This is set during the initial save — do **not** re-open the workbook to set page setup, as openpyxl drops the cell styles when re-saving.

---

## Section 5: Colour Palette

### 5.1 Structure Colours

| Element | Fill | Text | Size | Bold |
|---|---|---|---|---|
| Brand strip / Headline / Card header (1, 3) | `1F3864` (dark navy) | `FFFFFF` (white) | 20pt headline / 13pt card header | Yes |
| Sub-card header (card 2 — WHY) | `2E75B6` (medium blue) | `FFFFFF` (white) | 13pt | Yes |
| Document context line | `D6E4F0` (light blue) | `1F3864` (dark blue) | 11pt | No |
| Evidence header / table header | `D6E4F0` (light blue) | `1F3864` (dark blue) | 11pt | Yes |
| Standard data / card body fill A | `FFFFFF` (white) | `000000` (black) | 11pt | No |
| Alternating data / card body fill B | `F2F2F2` (light grey) | `000000` (black) | 11pt | No |

Card 1 (WHAT) uses the navy header on a white body. Card 2 (WHY) uses the medium-blue header on a grey body. Card 3 (FIX) uses the navy header on a white body. The alternating header colour on Card 2 is intentional — it visually breaks the three cards apart so the eye doesn't read them as one block.

Body font on the Analysis sheet is **11pt** (up from the earlier 10pt) so it remains readable on a tradeshow widescreen.

### 5.2 Priority Colours

Use **lighter fills** and **non-bold text** on priority rows so the content remains easy to read.

| Priority | Fill | Text Colour | Bold |
|---|---|---|---|
| **Priority 1** | `FFE0E0` (light red) | `8B0000` (dark red) | No |
| **Priority 2** | `FFF0DC` (light orange) | `6B3A00` (dark brown) | No |
| **Priority 3** | `FEFBD8` (light yellow) | `4A3B00` (dark olive) | No |

**Important:** Do not use saturated fills (`FFCCCC`, `FFE5CC`, `FFFACD`) or bright text colours (`C00000`, `FF0000`) on priority rows. These make content difficult to read.

The variance card priority strip and variance number row both use the same priority colour matching the severity of the finding. Priority colours also appear on the Evidence severity badges (column E) and on the row highlights on the source sheet.

### 5.3 Note Boxes

The caution note at the bottom of the Analysis sheet uses a distinct wheat treatment that is intentionally outside the priority colour scheme. The wheat fill signals "be careful before acting" rather than indicating a severity level.

| Element | Specification |
|---|---|
| Fill | `F5DEB3` (wheat) |
| Text colour | `000000` (black) |
| Style | Italic |
| Merge | Columns A–E |
| Wrap text | Enabled |
| Row height | Fixed at **70pt** |

The caution note is included once on every workbook, immediately above the footer. The standard text is:

> ⚠ **Before making any changes in JD Edwards:** test all configuration changes in a non-production environment first. For any GL journal entry, review the Transactions page in RapidReconciler for the affected items to confirm exact amounts and accounts before posting.

### 5.4 Font

Arial throughout. Font sizes by element:

| Element | Size |
|---|---|
| Headline | 20pt bold |
| Variance subline | 12pt bold |
| Secondary context strip | 10pt |
| Variance number | 24–36pt bold (smaller end if quantity + amount on two lines; larger if a single dollar value) |
| Pattern label + priority rationale | 12–13pt |
| Card header | 13pt bold |
| Card body | 11pt |
| Evidence link text | 11pt bold (with hyperlink underline, blue `0563C1`) |
| Evidence detail text | 10pt |
| Severity badge | 10pt bold |
| Caution note | 11pt italic |
| Footer | 9pt italic, grey `808080` |

---

## Section 6: Required Sections of the Analysis Sheet

These sections appear in this exact order on every Analysis sheet. The content of each is filled in from the analysis; the structure does not vary between guides.

### 6.1 Headline

The page's primary subject — what the analysis is about — in noun-phrase form. For item-focused analyses, this is the item identification (`Item {n} — Branch {b}, Location {loc}`). For document-focused analyses, this is the document identification (`Document {doc} ({DT name}) — Order {ord} ({OT})`).

Navy fill (`1F3864`), white text, 20pt bold, indented 1 character. Merged A:E. Row height 38pt.

The headline is what someone walking up to a tradeshow display reads first to know "what is this page about." Keep it under ~70 characters so it doesn't wrap on widescreen displays.

### 6.2 Variance Subline

The variance described in plain English, as a full sentence with a number. Examples:

- `GL credit of $338.00 has no inventory match`
- `Item ledger shows 10.35 LB ($59.15) the on-hand table doesn't see`
- `Inventory understated by $12,450 across 3 items`

Light blue fill (`D6E4F0`), dark blue text (`1F3864`), 12pt bold, indented 1 character. Merged A:E. Row height 24pt.

Avoid jargon — a junior analyst should be able to read the headline and subline together and understand what is wrong without consulting a glossary.

### 6.3 Secondary Context Strip

A small reference line carrying the identifying fields that don't belong in the headline or subline — typically GL class, GL account, std cost, period, company, or analogous fields. Format as `Label  Value          Label  Value          Label  Value` with double spaces between label and value and four spaces between fields.

White fill, dark grey text (`404040`), 10pt, indented 1 character. Merged A:E. Row height 18pt.

This strip is intentionally low-emphasis — it's reference information, not the message. If a particular guide doesn't have meaningful secondary context fields, omit this strip and adjust subsequent row numbers.

### 6.4 Variance Card

Two rows:

1. **Priority strip** — text reads `VARIANCE  (Priority {N} — {action label})`, where `{action label}` is one of:
   - `investigate immediately` (P1)
   - `review within 1 business day` (P2)
   - `low priority — include in next backlog` (P3)
   
   Filled with the priority colour, text in the priority text colour, 10pt bold. Merged A:E. Row height 20pt.

2. **Variance number + pattern + rationale** — A:B merged for the dollar amount or quantity (24–32pt bold, priority text colour, centered). C:E merged for the pattern label (12–13pt, priority text colour, left-aligned). Both halves use the priority fill. Row height 80–90pt.

The C:E content is two paragraphs separated by a blank line:

```
Pattern:  {Pattern Name} — {plain-English description}

{priority rationale — see Section 6.4.1}
```

### 6.4.1 Priority Calculation

The priority level is **computed** from the relationship between the variance and the typical transaction or document size. This prevents large absolute variances on high-volume items from being confused with material variances on low-volume items, and vice versa.

**General rule:**

```
ratio = |variance| / denominator
```

| Ratio | Priority | Action label |
|---|---|---|
| ≥ 50% | 1 | investigate immediately |
| ≥ 10% | 2 | review within 1 business day |
| < 10% | 3 | low priority — include in next backlog |

**Denominator depends on the report type:**

| Report type | Denominator | Rationale |
|---|---|---|
| Cardex Variance / Item Roll Forward | **Two ratios — see Section 6.4.1.1 below** | Some items have negligible cost, making the amount ratio meaningless; quantity has to be considered too |
| Transaction Detail | `max(\|CardexAmount\|, \|LedgerAmount\|)` from the RR Summary line | Captures the document's intended size regardless of which side has the value |
| Other reports | Per guide — must be a "normal magnitude" reference | Default to total throughput / number of records if no clearer denominator |

The denominator is always computed against a stable view of the data — for sorted exports, compute against the sorted view, so the result doesn't change with row order.

**Priority rationale must be displayed on the variance card** below the pattern label, so a reviewer can sanity-check the call. The exact format depends on whether the calculation is single-ratio or dual-ratio; see the report-specific subsections below.

The thresholds (50% and 10%) are deliberately wide so that priority changes meaningfully between levels rather than flickering near a boundary. They can be tuned per guide if a particular report type has different sensitivity, but should be documented in the guide rather than changed per-analysis.

#### 6.4.1.1 Cardex Variance — Dual-Ratio Priority

Cardex Variance is the only report type that computes priority on **both quantity and amount** and takes the higher of the two as the governing ratio.

**Why both dimensions:**

- **Cost-bearing items** (standard cost meaningfully > 0): the two ratios usually agree because `|AmtVar| ≈ |QtyVar| × cost` and `mean(|amt change|) ≈ mean(|qty change|) × cost`. Either ratio gives the same answer; showing both is just transparency.
- **Zero or near-zero cost items**: the amount ratio is undefined or pathological because every transaction has near-zero dollar value, but a 10,000-unit inventory gap is still a real operational problem. The quantity ratio carries the signal.
- **Mixed-cost items** (cost shifts during the history): a single outlier transaction can inflate one ratio while the other reads sensibly. Taking the max biases toward the higher-priority outcome, which is the conservative choice for variance work.

**Calculation:**

```
qty_ratio = |QtyVar| / mean(|qty change| across transactions)
amt_ratio = |AmtVar| / mean(|amt change| across transactions)
governing_ratio = max(qty_ratio, amt_ratio)   # whichever dimensions are defined
priority = priority_from_threshold(governing_ratio)
```

Both means are computed across the **transaction rows** of the sorted-ascending source sheet, excluding the Beg bal and Curr bal anchor rows. The Beg bal value is used as the starting position for the first transaction's delta calculation.

**Edge cases:**

| Condition | Handling |
|---|---|
| `mean_qty == 0 and mean_amt == 0` | Degenerate — no real activity. Default to Priority 3 with rationale "No transaction activity to measure against." |
| `mean_qty == 0` only | Use amount ratio alone. Mark quantity as "no quantity activity (mean = 0)" in the rationale. Unusual case. |
| `mean_amt == 0` only | Use quantity ratio alone. Mark amount as "no dollar activity (mean = $0)" in the rationale. This is the zero-cost item case. |
| Both defined | Use `max(qty_ratio, amt_ratio)` as governing ratio. |

**Rationale string format on the variance card:**

```
Qty:  {qty_var:.2f} {uom} vs {mean_qty:.2f} mean = {qty_ratio:.0f}%     Amt:  ${amt_var:.2f} vs ${mean_amt:.2f} mean = {amt_ratio:.0f}%
{conclusion}  →  Priority {N}
```

Where `{conclusion}` is one of:

- `Higher ratio governs` — both ratios defined
- `Quantity ratio governs` — amount ratio undefined (zero-cost item)
- `Amount ratio governs` — quantity ratio undefined (unusual)
- `No transaction activity to measure against` — both undefined

The two-clause format is used regardless of whether both ratios are defined — it makes the input data visible and lets a reviewer see at a glance whether the analysis is dollar-driven, quantity-driven, or both. When a clause is undefined, replace its content with a short explanation: e.g., `Amt:  no dollar activity (mean = $0)`.

#### 6.4.1.2 Transaction Detail — Single-Ratio Priority

Transaction Detail uses a single ratio:

```
ratio = |variance| / max(|CardexAmount|, |LedgerAmount|)
```

`CardexAmount` and `LedgerAmount` come from the RR Summary line. Taking the max captures the document's intended size regardless of which side has the value (a GL-only entry has Cardex = 0 and Ledger ≠ 0; a cardex-only entry is the reverse).

**Rationale string format:**

```
${variance:.2f} variance vs ${denominator:.2f} document amount = {ratio:.0f}%  →  Priority {N}
```

When both Cardex and Ledger are zero (no document found), treat the ratio as 100% and assign Priority 1 — the analysis is being run against something that doesn't reconcile to anything, which is itself a P1 finding.

### 6.5 Findings Cards

Three cards in fixed order, each consisting of a header row and a body row:

| Card | Header Text | Header Fill | Body Fill |
|---|---|---|---|
| 1 | `1.  WHAT happened` | Navy `1F3864` | White |
| 2 | `2.  WHY it happened` | Mid-blue `2E75B6` | Grey `F2F2F2` |
| 3 | `3.  HOW to fix it` | Navy `1F3864` | White |

The header row is merged A:E. Header text is 13pt bold white, indented 2 characters.

The body row merges **A:D** (not A:E). Column E carries the same fill as the body cell so the card still reads as a rectangle, but the body text only flows across A:D — this gives a comfortable line length on widescreen displays. Body text is 11pt black, **top-aligned**, indented 2 characters, **no borders**. Visual separation between cards is provided by the colored header strips and the alternating white/grey body fills, not by cell borders.

**Body content guidance:**

- **WHAT happened** — describe the symptom in 2–4 sentences, using the language a non-analyst would use. Identify the account, batch, comment, and amount.
- **WHY it happened** — explain the cause: which line type, which AAI, which configuration setting, which user action. Walk through the data narratively if a chronological or pairing argument is the basis of the diagnosis. **Include candidate-but-not-confirmed entries** when they cannot be ruled out — say so explicitly rather than overcommitting to a single root cause.
- **HOW to fix it** — numbered steps in execution order. **Each step is separated by a blank line** so the eye can navigate the list. If the fix is a journal entry, give the entry on indented lines after a Step 1 lead-in. If the fix references current variance numbers, include a step that has the user export the source from JD Edwards and re-derive the current variance via the relevant guide before making corrections.

**Paragraph breaks within a card body** — for any card body longer than 3 sentences, split at natural pivot points using a blank line (`\n\n` in the source). The eye loses its place in dense unbroken text. Aim for paragraphs of 2–4 sentences.

**Where a journal entry is included**, format the lines as:

```
    DR  {account}  {description}  ${amount}
    CR  {account}  {description}  ${amount}
```

Do not split debit/credit across separate cells — keep the journal entry as wrapped lines inside the merged FIX card body, indented inside the relevant Step.

**FIX card sub-bullets** — when a step contains a list of items to check, format the sub-bullets with leading whitespace and a bullet character:

```
    •  First item
    •  Second item
    •  Third item
```

**Re-Roll instruction** — if a fix step calls for running Re-Roll in RapidReconciler, the standard wording is:

> Run Re-Roll on the RapidReconciler As Of page for all locations for Item {n} and confirm QtyVar and AmtVar both go to zero on the next refresh.

This wording specifies the exact UI location (As Of page), the scope (all locations), and the confirmation criterion (both variances at zero on next refresh).

### 6.6 Evidence List

A small table beneath the cards that gives the user direct jump-links to the relevant rows on the source sheet.

**Header row (fixed height 40pt):**

- A:B merged: `Evidence  (click to jump to the row on the {source sheet name})`, light blue fill, dark blue 11pt bold, indented 1 character.
- C:D merged: light blue fill, blank.
- E: `Severity`, light blue fill, dark blue 11pt bold, centered.

**Evidence rows (height 44pt each):**

- A:B merged: hyperlink text `{label}  →  Row {N}`, where `{label}` is a short descriptor (e.g., "GL credit", "Order line 13", "DMAAI gap") and `{N}` is the row number on the source sheet. The hyperlink target is `#'{source sheet name}'!A{N}`. Format the cell with Excel hyperlink underline and blue `0563C1` text. Bold, 11pt.
- C:D merged: 1–2 lines of detail describing the row, 10pt black, left-aligned, indented 1 character.
- E: severity badge — text reads `Root cause` / `Related` / `Informational` (or similar), with the cell filled in the matching priority colour and text in the matching priority text colour, 10pt bold, centered.

Severity badge → row highlight mapping:

| Badge text | Severity | Fill | Text | Meaning |
|---|---|---|---|---|
| Root cause | Priority 1 | `FFE0E0` | `8B0000` | The specific row that caused the variance |
| Anchor | Priority 2 | `FFF0DC` | `6B3A00` | Where the variance is observed (Curr bal, RR Summary line, doc header) — not the cause |
| Related | Priority 2 | `FFF0DC` | `6B3A00` | Supporting rows that contributed context (earlier transactions, secondary findings) |
| Informational | Priority 3 | `FEFBD8` | `4A3B00` | Reference rows (Beg bal, configuration entries, low-priority gaps) |

**Anchor vs. Root cause** — many guides have a clear distinction between *where the variance shows* and *what caused it*. The Curr bal row on a Cardex analysis is the obvious example: the user sees the variance there, but the cause is some specific transaction further up the ledger. Use **Anchor** for the observation row and reserve **Root cause** for the actual offending transaction. There should usually be only one Root cause row per analysis. If two transactions are jointly responsible, both can be Root cause; if one is the primary cause and the second is a downstream symptom, the second is Related.

**Anchor and Related share the same priority and colour** (P2 amber). The badge text is the only thing that distinguishes them — both render as amber row highlights on the source sheet. This is intentional: the colour communicates severity, the badge text communicates role.

The same row referenced by the hyperlink must be highlighted with the same priority colour on the source sheet. Aim for 3–6 evidence rows; if a real-world case has more, cap the visible list and add a final row reading `+ {N} more on {source sheet name}` (no hyperlink, no severity badge).

### 6.7 Caution Note

A single wheat-coloured row (see Section 5.3) immediately below the evidence list, separated from it by an 8pt blank spacer.

### 6.8 Footer

A single italic 9pt grey row at the bottom: `Analysis produced using the {Guide Name}  ·  RapidReconciler  ·  {date}`.

### 6.9 Floating Note Text Box (Right of the Analysis Content)

Every Analysis sheet must include a floating text box anchored to column F, spanning to column R, rows 1 through the last row of the analysis content (typically 1–28 for current builds). The text box is positioned to the right of the analysis content so it does not overlap any data rows.

| Element | Specification |
|---|---|
| Position | Anchored col F → col R, rows 1 through last analysis row, floating (does not affect row heights) |
| Fill | None |
| Border | None |
| Font | Arial throughout |
| Title | Workbook name (e.g., "Transaction Detail Analysis"), 16pt bold |
| Section headings | 13pt bold; 3pt space after each heading |
| Body text | 12pt, not bold |
| Spacers | Small spacer paragraphs between sections |

**Required sections in order:**

1. Title (workbook name)
2. **What is {report name}?** — definition of the report type, including the key JD Edwards tables it compares
3. **Why does it matter?** — business impact of the variance or integrity issue
4. **What does this workbook show?** — specific findings structure
5. **About this workbook** — one-line guide: `Analysis sheet = findings and actions.   {Source sheet name} = source export data.   Click any "Row N" link in the Evidence section to jump to that row.`

If the source sheet has been sorted ascending by a sequence key (per Section 3.4), extend the "About this workbook" entry to mention the sort and indicate which row is the start (typically Beg bal at the top) and which is the end (typically Curr bal at the bottom). This helps first-time users understand the chronological reading order.

The "About this workbook" entry must explicitly mention the jump-to-row hyperlinks so first-time users know to click them.

---

## Section 7: Building the Analysis Sheet (Implementation Notes)

These notes apply when generating the workbook with openpyxl. They prevent known failure modes and ensure the variance card reflects the computed priority correctly.

### 7.1 Set Page Setup Before the First Save

Set `print_area`, `page_setup`, `page_margins`, and `print_options` on the worksheet **before** calling `wb.save()` for the first time. Re-opening a saved workbook to add page setup and re-saving causes openpyxl to drop the cell styles (fills, fonts, borders), producing a workbook that opens in Excel with all formatting stripped.

### 7.2 Inject the Floating Text Box via Direct XML Post-Processing

openpyxl's text-box support is incomplete. Build the text box by:

1. Saving the workbook with openpyxl (no text box yet).
2. Opening the resulting `.xlsx` (a zip) and writing `xl/drawings/drawing1.xml` directly with the required formatted paragraphs.
3. Adding a relationship in `xl/worksheets/_rels/sheet1.xml.rels` of type `…/relationships/drawing` pointing to `../drawings/drawing1.xml`.
4. Adding a `<drawing xmlns:r="…/relationships" r:id="{rId}"/>` element inside `xl/worksheets/sheet1.xml` immediately before `</worksheet>`. The `xmlns:r` declaration must be on the `<drawing>` tag itself if the worksheet root does not already declare it; otherwise the workbook fails XML parsing.
5. Adding an `<Override PartName="/xl/drawings/drawing1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>` to `[Content_Types].xml` if not already present.

### 7.3 Highlight Source Rows to Match Evidence Links

For every evidence row that links to a source-sheet row, apply the matching priority fill across all columns of that source-sheet row. The visual feedback when the user clicks the link and lands on the source row is essential — an unhighlighted destination row breaks the workflow.

### 7.4 Sorting the Source Sheet (when required)

When the spec requires sorting the source sheet (Section 3.4), do this before applying highlights and before computing Evidence row references:

1. Capture the data rows (typically rows 3 to N) as a list of value tuples.
2. Sort the list by the sequence key column.
3. Write the sorted values back to the same row range.
4. **Clear legacy text colours and fills on the data rows.** Many exports apply per-cell text colour (red, amber) as a row-level highlight rather than using fills. Sorting moves the *values* but not the *styles*, so the old colours stay attached to their physical positions and end up coloring the wrong rows. Reset every data cell's font colour to black and fill to none after sorting, then apply the new priority highlights.
5. Recompute all Evidence row references against the sorted positions before writing hyperlinks.

### 7.5 Compute Priority Before Building the Variance Card

The priority level (Section 6.4.1) must be computed before the variance card is rendered, since the card's fill colour, text colour, priority strip label, and rationale text all derive from the computed priority. Order of operations:

1. Read the source data (or the sorted view of it, when sorting is required).
2. Compute the denominator per the report-type rule in Section 6.4.1.
3. Compute `ratio = |variance| / denominator` and assign Priority 1 / 2 / 3 from the threshold table.
4. Render the variance card using the computed priority's fill, text colour, action label, and rationale string.

If the denominator computation depends on traversing the data in chronological order (the cardex case), traverse the **sorted-ascending view** regardless of the export's native order. This makes the priority result stable across runs.

---

## Section 8: Applying Formatting to Existing Workbooks

When reformatting an existing workbook (not building from scratch), the migration is more substantial than in earlier versions of this spec because the layout changed from a numbered-section report to a card layout. Two passes are required.

### 8.1 Layout Migration

Replace the existing Analysis sheet content entirely. Do not attempt to re-style the old numbered sections — rebuild from scratch following Section 6, sourcing the content from the old sheet:

| Old Section | New Card / Element |
|---|---|
| Document section | Headline + variance subline + secondary context strip (Sections 6.1–6.3) |
| Unassigned Check section | Mention in WHAT card body if relevant; otherwise omit |
| RR Summary Findings + Pattern Classification | Variance card (Section 6.4) and pattern label, plus priority rationale (Section 6.4.1) |
| Root Cause section | Body of the WHY card (Section 6.5) |
| Evidence section | Evidence list with hyperlinks (Section 6.6) |
| Processing Options — Suggested Causes | Distill the most likely cause into the WHY card; full reference list lives in the guide, not in the workbook |
| Recommended Action / Corrective Action section | Body of the FIX card (Section 6.5) — numbered steps with blank lines between |
| Preventive Actions section | Fold the most important one or two into the FIX card body or a follow-up sentence; full preventive list lives in the guide |
| Open Items / Open Questions section | Omit from the workbook; surface as a follow-up bullet inside the FIX card if material |

**Source sheet hygiene during migration:** older workbooks may have added an inline "HIGHLIGHT KEY" legend or similar explanatory block below the data on the source sheet. Remove these completely (values, fills, borders, merged cells, custom row heights) before applying the new highlights. The source sheet should contain only the original export data plus the priority highlights, AutoFilter, and freeze panes — nothing else.

### 8.2 If Building from a Template That Already Has the Card Layout

Apply the following changes only — do not alter the content:

1. **Source sheet:** Add AutoFilter on the header row; set freeze panes per Section 3.2; remap existing highlight colours to the palette in Section 5.2.
2. **Analysis sheet:** Set column widths per Section 4.2; enable wrap text on all cells; set row heights per Section 4.3 (note the Evidence header is fixed at 40pt); remap existing fills to the palette in Section 5; remap existing text colours to the palette in Section 5; remove bold from priority-coloured rows.

### 8.3 Colour Remapping Tables

**Font colour remapping:**

| Old Colour | New Colour | Context |
|---|---|---|
| `C00000` | `8B0000` | Priority 1 text |
| `C55A11` | `6B3A00` | Priority 2 text |
| `7B6000` | `4A3B00` | Priority 3 text |
| `FF0000` | `8B0000` | Any bright red text |
| `FFA500` | `6B3A00` | Any bright orange text |
| `7B4C00` | `000000` | Old gold note box text → black |
| `5C4A00` | `000000` | Old dark olive note box text → black |

**Fill colour remapping:**

| Old Fill | New Fill | Context |
|---|---|---|
| `FFCCCC` | `FFE0E0` | Priority 1 rows |
| `FFE5CC` | `FFF0DC` | Priority 2 rows |
| `FFD966` | `FFF0DC` | Priority 2 rows (alternate old value) |
| `FFFACD` | `FEFBD8` | Priority 3 rows |
| `FFF2CC` | `FEFBD8` | Priority 3 rows (alternate old value) |
| `FF0000` | `FFE0E0` | Solid red (source sheet) |
| `FFA500` | `FFF0DC` | Solid orange (source sheet) |
| `FFF3CD` | `F5DEB3` | Old gold note boxes → wheat |

---

## Section 9: Deprecated Elements

The following appeared in earlier versions of this spec and are **no longer used** in the card layout. Guides referencing them should be updated.

- **Report Summary key-value table** (label/value rows). Replaced by the headline + variance subline + secondary context strip (Sections 6.1–6.3).
- **Single-line "Document Context" row** combining all identifying fields. Replaced by the headline / subline / secondary context split, which separates the page subject (headline) from the variance description (subline) from the reference fields (context strip).
- **Colour Key section** at the top of the Analysis sheet. The card layout makes the meaning of colours self-evident from the severity badges and source-sheet highlights; a separate key takes up valuable visual space and is omitted.
- **Numbered Recommended Actions table** (1, 2, 3, 4 …). Replaced by the FIX card numbered steps with blank lines between them. Where multiple actions are genuinely required, list them inside the FIX card body, not as a separate table.
- **Resolution table with two-column "If… / Then…" layout.** No longer used on the Analysis sheet. Conditional resolutions are summarized in plain language inside the FIX card. The "If/Then" reasoning belongs in the guide document, not in the workbook output.
- **Total rows on finding tables** (with merged label cells in cols A–D and a sum in the numeric column). The card layout does not contain finding tables. If a guide produces a multi-item analysis (e.g., several items with individual variances), each item gets its own variance card stacked vertically; aggregate totals appear in the headline only.
- **Body text rows merged across A–E for long-form root-cause explanations.** Replaced by the WHY card with body merged across A:D. Long-form prose belongs in the guide, not in the workbook.
- **Card body borders.** Earlier versions wrapped each card body in a thin grey border. Removed — the colored header strips and alternating body fills already separate the cards visually, and the borders added clutter without clarifying anything.
- **Hardcoded "Priority 1 — investigate immediately"** labels on the variance card. Priority is now computed from the variance / denominator ratio (Section 6.4.1) and the action label is derived from the computed priority.
- **Blank separator rows of 6pt between major sections.** Still allowed where natural between the card stack and the evidence list, and between the evidence list and the caution note, but no longer required between every section since the card layout has fewer sections to separate. Use 8–14pt for clearer visual breaks.
