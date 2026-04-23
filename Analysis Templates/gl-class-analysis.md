# GL Class Analysis Guide

## RapidReconciler — GL Class Integrity (Item Branch to Location Mismatches) Integrity Report 5

---

## Section 1: Using Claude for Automated Analysis

Claude can perform the full analysis procedure automatically and return a single updated `.xlsx` file with the RR Analysis sheet added.

### What to Upload

Upload **two files:**

1. This guide (`.md`)
2. The Integrity Report 5 export (`.xlsx`)

Then use the following prompt:

> *"Analyze this Integrity Report 5 file using the guide as reference, then produce an updated copy of the Excel file with the analysis written to a new sheet called 'RR Analysis'. Blank location GL class codes on stock items are a red flag and should be Priority 1. GL class mismatches should be Priority 2. Group findings by pattern where possible."*

### Follow-On Requests in the Same Session

Once this guide has been uploaded, it remains in context. Use:

> *"Analyze this Integrity Report 5 file and return it with the RR Analysis sheet."*

### Output Specification

**File naming:** Name the output file `DMAAI Analysis.xlsx`.

**Sheet 1 — Integrity (original)**
- Source data, unchanged
- No row highlighting required

**Sheet 2 — RR Analysis (new)**
- Report Summary
- Issue Type Summary (color-coded by priority)
- Row Count by Company
- Findings by Priority (with item detail, root cause, verification steps, and resolution for each)
- Recommended Actions (numbered, in execution order)

### Notes and Limitations

- **Blank LocationClass detection:** The LocationClass column in this export may contain space-padded values (e.g., four spaces) rather than true empty cells. Claude must strip whitespace from GL class fields before classifying rows — a cell containing only spaces is treated as blank, not as a GL class code. Always check for this before counting blank rows.
- Claude analyzes the data as exported. The StockType column is used to determine whether a blank LocationClass is a red flag — blank location GL class on Stocking Type S is always Priority 1.
- GL class code interpretation (whether a code is stock vs non-stock) requires JDE access to the chart of accounts and DMAAI setup — Claude flags codes that appear unusual based on the data pattern but cannot confirm their purpose without JDE access.
- Mismatch resolution requires JDE access to confirm which GL class (branch or location) is correct for each item.
- For exports with many mismatches following the same GL class pair pattern, Claude groups findings by pattern to make the summary workable.

---


## Overview

Integrity Report 5 — **GL Class Integrity** — compares the GL class code on every Item Branch record (F4102) against the GL class code on each corresponding Item Location record (F41021). It identifies discrepancies between the two records that would cause inventory transactions to post to incorrect GL accounts during reconciliation.

This guide is a reusable template for analyzing any customer's Integrity Report 5 export. The JD Edwards functionality, report structure, issue types, and analysis procedure are consistent across all environments. The specific companies, items, branch plants, GL class codes, and findings will reflect the customer data in the uploaded export.

> **Who should use this guide:** JD Edwards cost accountants, inventory accountants, and item setup administrators responsible for investigating and resolving GL class code integrity findings.

> **Important:** All corrections are made in JD Edwards. RapidReconciler displays integrity findings for visibility but does not modify JD Edwards data.

---

## Section 2: Why GL Class Codes Matter

In JD Edwards EnterpriseOne, the GL class code is the bridge between an inventory item and the GL account it posts to. RapidReconciler uses the GL class code from the item location record (F41021) to assign every item ledger transaction (F4111) to the correct inventory account during the nightly import.

The GL class code exists in two places for each item:

| Record | Table | Program | Used By |
|---|---|---|---|
| **Item Branch** | F4102 | P41026 (Item Branch/Plant Info) | Work order material issues and completions (R31802A) |
| **Item Location** | F41021 | P41024 (Item Location Info) | Inventory adjustments (P4114), transfers (P4113), PO receipts (P4312), and all other F4111 transactions |

When the two records carry the same GL class code, all transaction types for that item post to the same inventory account — and reconciliation works cleanly. When they differ, the same physical item will post to different accounts depending on how it is transacted, creating a structural account mismatch.

### The Blank Location GL Class — Red Flag

A blank GL class code on the Item Location record is the most serious finding in this report. When the location record has no GL class:

- JD Edwards cannot look up the inventory account from the DMAAI table for that transaction
- JDE falls back to the Item Branch GL class or a wildcard AAI entry — which may map to a different account, or error entirely
- RapidReconciler cannot assign the item's transactions to the correct inventory account during import

**Blank location GL class codes on stock items (Stocking Type S) are never expected and should always be treated as data quality errors requiring correction.**

A blank location GL class may be acceptable only for non-stock items (Stocking Type N or similar) that are intentionally excluded from perpetual inventory tracking. If the report shows blank location GL classes on Stocking Type S items, those require immediate investigation.

---

## Section 3: Report Structure and Field Reference

### Export Column Definitions

| Column | Description | Notes |
|---|---|---|
| **CompanyNumber** | JD Edwards company number | Formatted with leading zeros |
| **BranchPlant** | The branch plant (Item Branch record) where the item is stocked | May differ from company number |
| **ItemNumber** | JD Edwards item number (short format) | |
| **ThirdItem** | Third item number / customer part number | May match ItemNumber if not separately configured |
| **Description** | Item description from the Item Master | |
| **Location** | The specific bin/rack/location within the branch | Blank indicates no location-level tracking |
| **Lot** | Lot number, if lot-controlled | Blank for non-lot items |
| **StockType** | Stocking Type from the Item Branch record | S = stock; N = non-stock. Blank location GL class is only acceptable for non-stock types |
| **BranchClass** | GL class code on the Item Branch record (F4102) | Source for work order transactions |
| **LocationClass** | GL class code on the Item Location record (F41021) | Source for inventory transactions. **Blank = red flag for stock items** |

---

## Section 4: Issue Type Reference

Integrity Report 5 produces two types of findings:

### Blank Location GL Class

**LocationClass field is empty on one or more rows.**

**Impact:** The item location record has no GL class code. JD Edwards cannot route inventory transactions to the correct account via the DMAAI lookup. The system falls back to the branch record GL class or a wildcard AAI — which may post to a different account or generate an AAI error.

**Severity:** HIGH for Stocking Type S items. This is a data quality error, not a configuration mismatch.

**Example:** An item with Branch GL class 6180 has a blank Location GL class. Every inventory adjustment and PO receipt for that item at that location will use the fallback AAI path rather than the intended account for GL class 6180.

### GL Class Mismatch

**BranchClass ≠ LocationClass (both populated, but different values).**

**Impact:** The item will post to different inventory accounts depending on the transaction type — location-sourced transactions (adjustments, transfers, receipts) go to the account for the location GL class, while work order transactions go to the account for the branch GL class. This creates a structural split in the inventory GL balance.

**Severity:** MEDIUM-HIGH. May be intentional in some configurations (e.g., consignment locations, returns locations) but requires verification before classification.

**Example:** An item has Branch GL class 6101 and Location GL class 6102. Inventory adjustments post to the 6102 account; work order material issues post to the 6101 account.

---

## Section 5: Report Summary — [Generated from Customer Export]

This section is populated by Claude based on the uploaded Integrity Report 5 export.

### Report Header

| Field | Value |
|---|---|
| **Report Type** | Integrity Report 5 — GL Class Integrity |
| **Source Tables** | F4102 (Item Branch) vs F41021 (Item Location) |
| **Period End** | *[Derived from export]* |
| **Export Generated** | *[Derived from export]* |
| **Total Rows** | *[Derived from export]* |
| **Companies** | *[Derived from export]* |

### Issue Type Summary

One row per issue type found in the export:

| Column | Description |
|---|---|
| **Issue Type** | Blank LocationClass or GL Class Mismatch |
| **Row Count** | Count of rows with this issue |
| **% of Total** | Row count as a percentage of total export rows |
| **Companies Affected** | Company numbers present for this issue type |
| **Description** | Plain-language description of the finding and its impact |

Color-code rows: Priority 1 / red for Blank LocationClass; Priority 2 / orange for GL Class Mismatch.

### Row Count by Company

Summarize total rows, blank LocationClass count, and GL class mismatch count for each company. Flag any company with blank location GL class rows at Priority 1 (red).

---

## Section 6: Findings by Priority — [Generated from Customer Export]

This section is populated by Claude based on the uploaded export. One sub-section per issue type, ordered by priority.

### Priority Classification

| Priority | Condition | Severity |
|---|---|---|
| **Priority 1** | Blank LocationClass on any Stocking Type S item | HIGH |
| **Priority 2** | GL class mismatch — branch and location GL class codes differ (both populated) | MEDIUM-HIGH |

### Finding Sub-Section Template

Each finding sub-section contains:

**What Was Found**
List all affected items with company, branch, item number, description, location, branch class, and location class. Note any patterns (e.g., all blank items at locations with a common suffix, all mismatches in the same GL class pair).

**Root Cause**
Explain the most likely cause based on the data pattern. Common causes are listed in Section 7. Present possible explanations without assuming which is correct — determination requires JDE access and accounting team input.

**Verification Steps**
Step-by-step instructions to locate and confirm the finding in JDE using Item Branch (P41026) and Item Location (P41024).

**Resolution**


> ⚠ **Before making any changes in JD Edwards:** Test all configuration changes in a non-production environment first. For any scenario where a GL journal entry may be required, review the Transactions page in RapidReconciler for the affected items to confirm exact amounts and accounts before posting.
Decision table:

| If… | Then… |
|---|---|
| [Condition — which record is correct] | [Action — what to update in JDE] |

---

## Section 7: Common Root Causes

### Blank Location GL Class

| Cause | How to Identify | Resolution |
|---|---|---|
| Item was received into a new location before GL class was set up | Location record creation date earlier than GL class setup date | Populate GL class on the Item Location record to match the branch record |
| GL class changed on Item Branch but location records were not updated | Branch GL class differs from the expected value for that product category | Update all location records for the item to match the new branch GL class |
| Consignment / temporary / external location where GL class was not configured | Location code suffix (e.g., -CF, -CONS, -EXT) or description indicates non-standard location | Determine intended GL class for that location type; populate accordingly, or change Stocking Type if truly non-stock |
| Item was set up incorrectly at initial data load | Blank appears on multiple items across the same branch | Bulk update location records via SQL or JDE mass update tool (if available) |

### GL Class Mismatch

| Cause | How to Identify | Resolution |
|---|---|---|
| GL class changed on branch record but not propagated to location records | Branch class is newer/different from location class; same pattern across multiple locations for the same item | Update location records to match the branch record |
| Item intentionally uses different GL classes for different locations | Location code indicates a specific purpose (consignment, returns, demo stock) | Verify intent with accounting team; document if intentional; update DMAAI model if needed |
| Item set up with wrong GL class on one of the records at initial load | No obvious reason for the difference; item description doesn't suggest a multi-class scenario | Determine correct GL class from the chart of accounts and item type; update the incorrect record |
| Two items with different GL classes were consolidated under one item number | Item has a long history and the GL class changed partway through | Review transaction history to determine which GL class was used historically; align both records to the correct current class |

---

## Section 8: JDE Navigation Reference

| Task | Program | Fast Path / Menu |
|---|---|---|
| View/update Item Branch GL class | P41026 — Item Branch/Plant Information | Fast path: `IBP` or Inventory Management > Item Branch |
| View/update Item Location GL class | P41024 — Item Location Information | From P41026 → Location Revisions row exit; or Inventory Inquiry P41202 → row exit |
| View all locations for an item | P41202 — Inventory Inquiry | Fast path: `INQ` |
| View item transaction history | P4111 — Item Ledger Inquiry | Fast path: `CARDEX` |
| Run Integrity Report 5 | R41416 — GL Class Integrity | Inventory Management > Reports > Integrity Reports |

---

## Section 9: Step-by-Step Analysis Procedure

Use this procedure each time an Integrity Report 5 export is received.

**Step 1 — Scan for Blank Location GL Class First**

Filter the LocationClass column for blank values. Any blank on a Stocking Type S item is Priority 1. Group blank items by branch plant — a cluster of blanks at the same branch or location type often indicates a systemic setup gap rather than individual data entry errors.

**Step 2 — Assess GL Class Mismatches**

For each mismatch row, compare the branch and location GL class codes. Identify patterns:
- Same GL class pair appearing multiple times (e.g., many items with 6101 branch vs 6102 location) suggests a batch GL class change that was not fully propagated
- Single-item mismatches with unusual GL classes (e.g., non-inventory class codes on what appears to be a stock item) suggest item setup errors

**Step 3 — Cross-Reference with DMAAI Model Table**

For each GL class code appearing in the report, confirm that it exists in the DMAAI model table (4152 PI) for the relevant company. If a GL class code is not in the model table, RapidReconciler cannot assign an account — and Integrity Report 2 (DMAAI Entry Integrity) should also show a finding for that class.

**Step 4 — Determine Intent for Each Finding**

For each item, determine with the accounting team and item setup team whether the branch or location GL class is correct. Do not assume the branch record is always the source of truth — in some environments the location record is maintained more carefully.

**Step 5 — Correct in JDE**

Update the incorrect record in JDE. After corrections:
1. Trigger a RapidReconciler data refresh
2. Re-run Integrity Report 5
3. Confirm corrected items no longer appear

**Step 6 — Document Findings**

Maintain a log of each finding, the determination (error vs intentional), the action taken, and the date and responsible party.

---

## Section 10: Excel Output Formatting Rules

### File Naming

Output file name: `DMAAI Analysis.xlsx`

### Sheet Structure

| Sheet | Contents |
|---|---|
| **Integrity** | The original source data, unchanged |
| **RR Analysis** | The analysis sheet (see below) |

Do not delete, rename, or reorder the source sheet.

### RR Analysis Sheet Structure

| Section | Content |
|---|---|
| **Report Summary** | Period-end date, generation timestamp, total row count, companies present, stock types present |
| **Issue Type Summary** | One row per issue type with row count, % of total, companies affected, and description. Color-coded by severity. |
| **Row Count by Company** | Total rows, blank LocationClass count, and mismatch count per company |
| **Findings by Priority** | One sub-section per priority level. Each sub-section lists affected items with detail, root cause, verification steps, and resolution path. |
| **Recommended Actions** | Numbered action steps in execution order, with the specific items, companies, and responsible owner for each. |

### Analysis Sheet Formatting

| Element | Specification |
|---|---|
| **Font** | Arial throughout |
| **Section headers** | Dark blue fill (`1F3864`), white bold text, 11pt |
| **Sub-section headers** | Medium blue fill (`2E75B6`), white bold text, 10pt |
| **Column headers** | Light blue fill (`D6E4F0`), dark blue bold text, 10pt |
| **Data rows** | Alternating white and light gray (`F2F2F2`) fill; 10pt Arial |
| **Priority 1 rows** | Red fill (`FFCCCC`), dark red bold text (`C00000`) |
| **Priority 2 rows** | Orange fill (`FFE5CC`), dark brown text (`7B3F00`) |
| **Note boxes** | Light gold fill (`FFF3CD`), dark gold italic text (`7B4C00`); full-width merged cell; wrap text enabled |
| **Column widths** | Fixed widths sized for readability — not auto-stretched to full sheet width. Typical widths: Col A 22, B 28, C 36, D 20, E 20. |
| **Row heights** | Calculated from content length and column width — not a flat default. |
| **Wrap text** | Enabled on all cells on the RR Analysis sheet. |
| **Resolution tables** | Two-column layout: condition spans cols A–B, action spans cols C–E. Do not merge the full row width. |
| **Colour palette** | Priority 1 fill `FFE0E0` / text `8B0000`; Priority 2 fill `FFF0DC` / text `6B3A00`. Lighter fills and non-bold text for readability. |
| **Source sheet** | AutoFilter on row 2; freeze panes at row 3. Row highlights match analysis priority colours. |
| **Colour key** | Include a colour key section at the top of the analysis sheet. |

---

## Section 11: Related Documentation

- [DMAAI Analysis Guide](dmaai-analysis.md) — Reference for Integrity Report 2 (DMAAI Entry Integrity). GL class codes that appear in this report should also be present in the model DMAAI table (4152 PI).
- [Cardex Variance Analysis Guide](cardex-variance-analysis.md) — If a blank or mismatched GL class has caused transactions to post to the wrong account, cardex variances may result.
- [End of Day Analysis Guide](end-of-day-analysis.md) — AAI errors caused by missing GL class entries produce End of Day variances.

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*
