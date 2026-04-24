# Excel Output Formatting Specification

## RapidReconciler Analysis Workbooks — Shared Formatting Reference

This document is the **change master** for Excel output formatting across all RapidReconciler analysis guides. Each guide is fully self-contained and can be used in a two-file session (guide + export) without this document. This document exists so that when formatting changes, they are made here first and then propagated to all guides in a single update session.

**How to use this document:**
- To change formatting across all guides, update this document first, then upload it with all seven guides and ask Claude to propagate the changes.
- Individual guide sessions do not require this document — the guide alone contains everything Claude needs to produce a correctly formatted output.
- When a detail in this document conflicts with a guide, this document is the intended standard and the guide should be updated to match.

---

## Section 1: File Naming

All output files are named:

```
DMAAI Analysis.xlsx
```

---

## Section 2: Workbook Structure

Every output workbook contains exactly two sheets:

| Tab Position | Sheet | Contents |
|---|---|---|
| **1 (left)** | **Analysis sheet** | The structured analysis written by Claude — this is the active sheet when the workbook opens |
| **2 (right)** | **Source sheet** | The original export data, unchanged except for row highlights, AutoFilter, and freeze panes |

The analysis sheet must always be the first (leftmost) tab and must be set as the active sheet so it displays when the workbook is opened.

Do not delete, rename, or reorder the source sheet. Do not add columns, rows, or formulas to the source sheet. The only permitted modifications to the source sheet are cell background colour (highlights), AutoFilter, and freeze panes.

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

Apply background colour to data rows based on priority classification. Apply the highlight to all columns in the row. When a row qualifies for multiple priorities, the higher priority (lower number) takes precedence.

| Priority | Fill Colour | Hex | Criteria |
|---|---|---|---|
| **Priority 1** | Light red | `FFE0E0` | Highest severity — immediate action required |
| **Priority 2** | Light orange | `FFF0DC` | High severity — resolve within 1 business day |
| **Priority 3** | Light yellow | `FEFBD8` | Normal backlog — include in next scheduled run |

The specific criteria that trigger each priority level are defined in each analysis guide.

---

## Section 4: Analysis Sheet Layout

### 4.1 Column Structure

The analysis sheet uses **5 columns** as the standard layout for most guides. Some guides use a different column count where the content requires it — the specific column count is noted in each guide.

**Standard 5-column widths:**

| Column | Width (chars) | Typical Content |
|---|---|---|
| A | 22 | Labels, section numbers, short identifiers |
| B | 28 | Item details, descriptions |
| C | 36 | Longer descriptions, findings |
| D | 20 | Values, accounts, counts |
| E | 20 | Notes, status, resolution |

**Alternate layouts** (where noted in the guide):

| Layout | Columns | Widths |
|---|---|---|
| 3-column | A, B, C | 28, 52, 26 |
| 4-column | A, B, C, D | 28, 52, 20, 16 |
| 6-column (DMAAI) | A, B, C, D, E, F | 28, 40, 14, 22, 20, 52 |

These are starting widths. Do not auto-stretch columns to the full sheet width.

### 4.2 Wrap Text and Row Heights

- Enable wrap text on **all cells** on the analysis sheet.
- Set row heights based on content: `ceil(len(longest_line_in_cell) / col_width) × 13pt` per cell, take the max across all cells in the row.
- Cap data row heights at **80pt**. Cap body text rows at **180pt**. Cap resolution rows at **100pt**.
- Minimum row height: 16pt. Summary table rows: 42pt.

### 4.3 Numeric Columns and Total Rows

When a finding table includes a calculated monetary value (e.g., GL gap, inventory understatement), put it in its own numeric cell rather than embedding it in a text string:

- The numeric cell should use `#,##0.00` number format and right-align.
- A companion QOH column (integer, right-aligned) should appear immediately to the left.
- Add a **total row** directly below the item list, spanning cols A–D merged as a label, with the sum in the numeric column. Use the column header fill (`D6E4F0`) on the total row to visually separate it from the data.

### 4.3 Grid Lines

Disable grid lines on the analysis sheet (`showGridLines = False`).

---

## Section 5: Colour Palette

### 5.1 Structure Colours (Section and Sub-Section Headers)

| Element | Fill | Text | Size | Bold |
|---|---|---|---|---|
| Section header | `1F3864` (dark blue) | `FFFFFF` (white) | 11pt | Yes |
| Sub-section header | `2E75B6` (medium blue) | `FFFFFF` (white) | 10pt | Yes |
| Column header row | `D6E4F0` (light blue) | `1F3864` (dark blue) | 10pt | Yes |
| Alternating data row | `F2F2F2` (light grey) | `000000` (black) | 10pt | No |
| Standard data row | `FFFFFF` (white) | `000000` (black) | 10pt | No |

### 5.2 Priority Colours

Use **lighter fills** and **non-bold text** on priority rows so the content remains easy to read.

| Priority | Fill | Text Colour | Bold |
|---|---|---|---|
| **Priority 1** | `FFE0E0` (light red) | `8B0000` (dark red) | No |
| **Priority 2** | `FFF0DC` (light orange) | `6B3A00` (dark brown) | No |
| **Priority 3** | `FEFBD8` (light yellow) | `4A3B00` (dark olive) | No |

**Important:** Do not use saturated fills (`FFCCCC`, `FFE5CC`, `FFFACD`) or bright text colours (`C00000`, `FF0000`) on priority rows. These make content difficult to read.

Priority sub-section header rows use the same fill as their priority level but with bold text.

### 5.3 Note Boxes

Note boxes (⚠ observations and warnings) use a distinct wheat treatment that is intentionally outside the priority colour scheme. Do not substitute a priority colour for note boxes — the wheat fill signals an observation or caution rather than a severity level.

| Element | Specification |
|---|---|
| Fill | `F5DEB3` (wheat) — distinct from all priority fills |
| Text colour | `000000` (black) |
| Style | Italic |
| Merge | Columns A–E |
| Wrap text | Enabled |
| Row height | Fixed at **75pt (≈ 100px)** — do not auto-size note rows |

### 5.4 Font

Arial throughout. Use 10pt for all data content. Section headers 11pt, sub-section headers 10pt.

---

## Section 6: Standard Section Types

### 6.1 Report Summary

Key-value layout: label in column A (bold), value spans columns B–E (or to the last column). Row height 16pt. Alternating white/grey fill.

### 6.2 Colour Key

Always include a colour key section near the top of the analysis sheet, after the Report Summary. One row per colour with the fill applied to the row so it is self-illustrating. Columns: Colour name, Meaning, Applies To.

### 6.3 Data Tables

Column headers use the `D6E4F0` / `1F3864` column header style. Data rows alternate white and light grey. Row height calculated from content.

### 6.4 Resolution Tables

Use a **two-column layout** — do not merge the full row width:

| Columns | Content |
|---|---|
| A–B (merged) | Condition: "If…" |
| C–E (merged) | Action: "Then…" |

Header row uses the standard column header style with "If…" and "Then…" labels.

**Resolution warning:** Always include the following note block once, immediately before or after the first resolution table in the analysis:

> ⚠ **Before making any changes in JD Edwards:** Test all configuration changes in a non-production environment first. For any scenario where a GL journal entry may be required, review the Transactions page in RapidReconciler for the affected items to confirm exact amounts and accounts before posting.

### 6.5 Body Text Rows

Long-form text (root cause explanations, what-was-found descriptions) spans columns A–E merged. Wrap text enabled. Row height calculated from content.

### 6.6 Blank Separator Rows

Use 6pt height blank rows between major sections for visual breathing room.


### 6.7 Trade Show / Public Display Text Box

Every analysis sheet must include a floating text box anchored to column F, spanning to column R, rows 1–18. The text box is positioned to the right of the analysis content so it does not overlap any data rows.

| Element | Specification |
|---|---|
| Position | Anchored col F → col R, rows 1–18, floating (does not affect row heights) |
| Fill | None |
| Border | None |
| Font | Arial throughout |
| Title | Workbook name, 16pt bold |
| Section headings | 13pt bold; 3pt space after each heading |
| Body text | 12pt, not bold |
| Spacers | Small spacer paragraphs between sections |

**Required sections in order:**
1. Title (workbook name)
2. What is [report name]? — definition of the report type, including the key JD Edwards tables it compares
3. Why does it matter? — business impact of the variance or integrity issue
4. What does this workbook show? — specific findings structure
5. About this workbook — one-line sheet guide (Analysis sheet = findings; Source sheet = export data)

**No gridlines** on the analysis sheet (`showGridLines = False`).

---

## Section 7: Applying Formatting to Existing Workbooks

When reformatting an existing workbook (not building from scratch), apply the following changes only — do not alter the content:

1. **Source sheet:** Add AutoFilter on the header row; set freeze panes per Section 3.2; remap existing highlight colours to the palette in Section 5.2.
2. **Analysis sheet:** Set column widths per Section 4.1; enable wrap text on all cells; recalculate row heights per Section 4.2; remap existing fills to the palette in Section 5; remap existing text colours to the palette in Section 5; remove bold from priority-coloured rows.
3. **Font colour remapping:**

| Old Colour | New Colour | Context |
|---|---|---|
| `C00000` | `8B0000` | Priority 1 text |
| `C55A11` | `6B3A00` | Priority 2 text |
| `7B6000` | `4A3B00` | Priority 3 text |
| `FF0000` | `8B0000` | Any bright red text |
| `FFA500` | `6B3A00` | Any bright orange text |
| `7B4C00` | `000000` | Old gold note box text → black |
| `5C4A00` | `000000` | Old dark olive note box text → black |

4. **Fill colour remapping:**

| Old Fill | New Fill | Context |
|---|---|---|
| `FFCCCC` | `FFE0E0` | Priority 1 rows |
| `FFE5CC` | `FFD966` | Priority 2 rows |
| `FFF0DC` | `FFD966` | Priority 2 rows (alternate old value) |
| `FFFACD` | `FFF2CC` | Priority 3 rows |
| `FEFBD8` | `FFF2CC` | Priority 3 rows (alternate old value) |
| `FF0000` | `FFE0E0` | Solid red (source sheet) |
| `FFA500` | `FFD966` | Solid orange (source sheet) |
| `FFF3CD` | `F5DEB3` | Old gold note boxes → wheat |

**
