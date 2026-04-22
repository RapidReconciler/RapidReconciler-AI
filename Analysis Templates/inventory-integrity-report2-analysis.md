# Integrity Report 5 Analysis Guide

## RapidReconciler — DMAAI Entry Integrity (Integrity Report 2)

---

## Table of Contents

- [Overview](#overview)
- [Section 1: What Is Integrity Report 2?](#section-1-what-is-integrity-report-2)
- [Section 2: The Model DMAAI Table — Foundation Concept](#section-2-the-model-dmaai-table--foundation-concept)
- [Section 3: Report Structure and Field Reference](#section-3-report-structure-and-field-reference)
- [Section 4: DMAAI Tables in This Report](#section-4-dmaai-tables-in-this-report)
- [Section 5: Comment / Issue Type Reference](#section-5-comment--issue-type-reference)
- [Section 6: Report Summary — March 31, 2026](#section-6-report-summary--march-31-2026)
- [Section 7: Findings by Priority](#section-7-findings-by-priority)
- [Section 8: Net Zero — Verification Protocol](#section-8-net-zero--verification-protocol)
- [Section 9: Step-by-Step Analysis Procedure](#section-9-step-by-step-analysis-procedure)
- [Section 10: Excel Output Formatting Rules](#section-10-excel-output-formatting-rules)
- [Section 11: Using Claude for Automated Analysis](#section-11-using-claude-for-automated-analysis)
- [Section 12: AAI Quick Reference](#section-12-aai-quick-reference)
- [Section 13: Related Documentation](#section-13-related-documentation)

---

## Overview

Integrity Report 2 — **DMAAI Entry Integrity** — compares every active entry in the JD Edwards Distribution/Manufacturing AAI Values table (F4095) against the **Model DMAAI Table** (table 4152, document type PI). It identifies discrepancies in business unit, object account, and subsidiary that would cause transactions to post to incorrect GL accounts during reconciliation.

This guide covers the analysis of the Integrity Report 2 export dated **March 31, 2026**, containing **3,902 rows** across **9 companies** and **10 DMAAI table numbers**. It is the companion reference document for the **RR Analysis** sheet in the exported Excel file.

> **Who should use this guide:** JD Edwards cost accountants, inventory accountants, and RapidReconciler administrators responsible for investigating and resolving DMAAI integrity findings.

> **Important:** All corrections are made in JD Edwards. RapidReconciler displays integrity findings for visibility but does not modify JD Edwards data.

---

## Section 1: What Is Integrity Report 2?

RapidReconciler uses the DMAAI table (F4095) to assign GL accounts to every item ledger and location record during the nightly import from JD Edwards. The assignment logic works as follows:

1. Each item ledger transaction carries a **GL class code** (from the item's item location record, item branch record, or order line).
2. During import, RapidReconciler looks up that GL class code in the **Model DMAAI Table** (4152 PI) to find the correct business unit, object account, and subsidiary.
3. RapidReconciler then checks whether every other balance sheet DMAAI table that references inventory accounts (3110, 3130, 4122, 4126, 4134, 4172, 4240, 4310) is consistent with the model table for the same company and GL class code.
4. Any inconsistency is reported in Integrity Report 2 with a description of the type of mismatch.

**Why this matters:** A single mismatched DMAAI entry can cause every transaction of a given GL class to post to the wrong account — producing a systematic variance that grows each period. Integrity Report 2 surfaces these issues before they compound into large reconciling items at period end.

---

## Section 2: The Model DMAAI Table — Foundation Concept

### What Is the Model DMAAI Table?

The **Model DMAAI Table** is DMAAI table **4152** with document type **PI** (Physical Inventory). It has been designated as the master reference for inventory GL account assignments in RapidReconciler.

- Table **4152** is hard-coded in RapidReconciler and cannot be changed.
- Document type **PI** is the default; this may be changed by the RR administrator in Company settings to a custom document type (e.g., I9) if PI contains non-inventory GL class codes.
- The model table defines which **GL accounts are perpetual inventory accounts** for each company and GL class code.

### What the Model Table Controls

| Function | Description |
|---|---|
| **Inventory account identification** | Determines which BU/Object/Subsidiary combinations are perpetual inventory accounts |
| **Item ledger assignment** | Appends GL account information to every F4111 record during import |
| **Filter population** | Populates the business unit, object, and subsidiary filters on the RapidReconciler reconciliation page |
| **Satellite table validation** | Used as the reference point for Integrity Report 2 comparisons |

### Tables Validated Against the Model

| Table | Description | Module |
|---|---|---|
| **3110** | Raw Material WIP — Material Issues | Manufacturing |
| **3130** | WIP Completions | Manufacturing |
| **4122** | Inventory Debit (Adjustments, Transfers, Issues) | Inventory |
| **4126** | Received Not Vouchered (RNV) Debit | Purchasing |
| **4134** | In-Transit Inventory | Inventory |
| **4172** | Physical Inventory Adjustment | Inventory |
| **4240** | Cost of Goods Sold | Sales |
| **4310** | Inventory — Purchase Order Receipt | Purchasing |

> **Note:** DMAAI tables 4162 (Inventory Transfer), 4385 (Outbound Logistics), and 4400 (Intercompany/Advanced Pricing) also appear in this report, indicating those tables are also being validated.

### Vetting the Model Table

Before relying on Integrity Report 2 findings, the model table itself must be correct. Integrity Report 1 (Model DMAAI) is used to validate the model table. Each entry should be verified for:

- Correct business unit, object account, and subsidiary for each company/GL class combination
- Inclusion of all stock inventory GL class codes
- Exclusion of non-stock and expense GL class codes from document type PI (or establishment of a dedicated document type)

---

## Section 3: Report Structure and Field Reference

### Export Column Definitions

| Column | Description | Notes |
|---|---|---|
| **CompanyNumber** | JD Edwards company number for which the DMAAI entry exists | Formatted as integer; leading zeros dropped in export |
| **TransactionComp** | Transaction company — typically matches CompanyNumber | May differ for intercompany configurations |
| **TableNumber** | DMAAI table number (e.g., 4122, 4134) | Corresponds to the transaction type being validated |
| **DocType** | Document type on the DMAAI entry (e.g., IA, IB, IR, VV) | Specific to each table; see Section 4 |
| **GLClass** | GL class code on the DMAAI entry | Four-character code from item setup (e.g., OUTG, 6101, 1421) |
| **AAIAccount** | Full account number in the DMAAI entry being reviewed | Format: BU.Object or Object only |
| **ModelAccount** | Full account number from model table 4152 PI | NaN if no model entry exists for this company/GL class |
| **Comment** | RapidReconciler classification of the discrepancy | See Section 5 |
| **FlexBu** | Whether Flexible Accounting is set up for the Business Unit component | Yes/No |
| **FlexSub** | Whether Flexible Accounting is set up for the Subsidiary component | Yes/No |
| **LongAccount** | Long-form account number as displayed in JDE | May include BU + Object + Subsidiary |

### Account Number Format

Account numbers in this report use the format **BU.Object** (e.g., `2.1421` = Business Unit 2, Object Account 1421). When only an object account is shown (e.g., `1421.0`), the business unit is blank in the DMAAI setup and will be sourced from the transaction's branch/plant.

---

## Section 4: DMAAI Tables in This Report

### Manufacturing Tables (3000 Series)

| Table | Document Type | Transaction Type | Description |
|---|---|---|---|
| **3110** | IM | Work Order Material Issue | Debits WIP for materials issued to a work order; credits raw material inventory (AAI 3110 = raw material account). Mismatch here causes material issues to post to wrong inventory account. |
| **3130** | IC | Work Order Completion | Credits WIP and debits the finished goods account on work order completion. Mismatch here affects finished goods valuation. |

> **Cost Type A1 note:** The comment "Mismatch - object OrTy WO CostTy A1" indicates the mismatch applies specifically to work orders with Order Type **WO** and Cost Type **A1** (Actual Cost). Standard cost work orders use a different path and may not be affected.

### Inventory Tables (4100 Series)

| Table | Document Type(s) | Transaction Type | Description |
|---|---|---|---|
| **4122** | IA, II, IJ, IL, IM, IP, IR, IV | Inventory Debit | Primary inventory account for adjustments (IA), internal transfers (II), physical inventory adjustments (IJ), lot transfers (IL), material issues (IM), physical inventory (IP), receipts (IR), and voids (IV). This is the most critical inventory table. |
| **4126** | VV | Received Not Vouchered (RNV) Debit | Debits the RNV account on voucher match. Paired with 4128 (RNV Credit). Present only for companies with purchasing activity: 2, 3, and 22 in this report. |
| **4134** | IB | In-Transit Inventory (Branch Transfer) | Used when inventory is in transit between branch plants. 4134 debits the in-transit account; 4136 credits it on receipt. Must point to different accounts for in-transit tracking to function. |
| **4162** | IX | Inventory Transfer — Cross-Company | Used for inventory transfers between companies. Present for company 2 only in this report. |

### Sales Tables (4200 Series)

| Table | Document Type | Transaction Type | Description |
|---|---|---|---|
| **4240** | SO | Cost of Goods Sold | Debits COGS and credits inventory on sales shipment. Mismatch here causes COGS to post to wrong account. Present for companies 2 and 22. |

### Purchasing Tables (4300 Series)

| Table | Document Type(s) | Transaction Type | Description |
|---|---|---|---|
| **4310** | OR | Inventory — Purchase Order Receipt | Debits inventory on PO receipt. Paired with a credit to the RNV account (4320). Mismatch causes PO receipts to post to wrong inventory account. |
| **4385** | OB, OC, OM, OP, OR, OW | Outbound Logistics / Order Settlement | Used for outbound logistics processing. Present for companies 2 and 22. |
| **4400** | IV, OB, OC, OP | Intercompany / Advanced Pricing Settlement | Used for intercompany billing and advanced pricing adjustments. Present for companies 2, 3, and 22. |

---

## Section 5: Comment / Issue Type Reference

Integrity Report 2 assigns one of the following comments to each row:

### Mismatch — Object Account

> `Mismatch - object`

The object account in the DMAAI entry does not match the object account in the model table (4152 PI) for the same company and GL class code. The account numbers differ in the object component.

**Impact:** Transactions using this DMAAI entry will post to the wrong object account in the GL. Reconciliation variances will accumulate for every transaction of this GL class and doc type.

**Example:** Table 4122, GL class OUTG, company 2 — DMAAI has object 1421, model expects 1423. Every inventory adjustment for OUTG-class items in company 2 posts to object 1421 instead of 1423.

### Mismatch — Object Account (Work Order Cost Type A1)

> `Mismatch - object OrTy WO CostTy A1`

Same as object account mismatch, but specifically flagged for **Work Order (WO)** transactions with **Cost Type A1** (actual cost). This appears in manufacturing tables 3110 and 3130.

**Impact:** Manufacturing material issues and completions for actual-cost work orders post to the wrong inventory/WIP account.

### Mismatch — Business Unit

> `Mismatch - Business unit`

The business unit in the DMAAI entry does not match the business unit in the model table for the same company and GL class code. The object accounts may match, but the BU differs.

**Impact:** Transactions post to the correct object account but under the wrong business unit — causing GL balances to appear in the wrong branch/plant, department, or division. This can affect all departmental reporting and branch-level reconciliation.

**Example:** Company 67, all GL classes — DMAAI has BU 67010, model has no BU (expects BU from branch/plant). Every inventory transaction for company 67 posts to 67010.1421 regardless of which branch plant was used.

### Net Zero Review

> `Net zero review - 4122,4124`  
> `Net zero review - 4126,4128`  
> `Net zero review - 4134,4136`

RapidReconciler has detected that the entries in a paired set of tables (debit and credit) may result in a net-zero posting — meaning the debit and credit sides of the inventory entry land on the same account, or that one side is missing.

**This is a flag for verification, not a confirmed error.** Net zero may be intentional in some configurations (e.g., a clearing account that nets out by design). However, in inventory balance sheet tables, net zero almost always indicates a setup error.

> **Critical:** Do not mark net zero findings as resolved without confirming the account structure in JDE. See Section 8 for the full verification protocol.

---

## Section 6: Report Summary — March 31, 2026

| Field | Value |
|---|---|
| **Report Type** | Integrity Report 2 — DMAAI Entry Integrity |
| **Source Table** | F4095 — Distribution/Manufacturing AAI Values |
| **Period End** | March 31, 2026 |
| **Export Generated** | April 22, 2026  6:25 PM |
| **Total Rows** | 3,902 |
| **Companies** | 00002, 00003, 00009, 00012, 00022, 00041, 00043, 00067, 00073 |
| **DMAAI Tables** | 3110, 3130, 4122, 4126, 4134, 4162, 4240, 4310, 4385, 4400 |
| **Model Table** | 4152 / Document Type PI |

### Variance Type Summary

| Comment / Issue Type | DMAAI Table Description | Row Count | % of Total | Companies | Doc Types | GL Class Codes Impacted |
|---|---|---|---|---|---|---|
| Net zero review — 4134 / 4136 | **4134:** In-Transit Inventory — records change to COGS when item cost changes. **4136:** Offsetting credit side. Used by Quantity Revisions (P41022), Item Branch/Plant (P41026), Batch Cost Maintenance (R41802). | 1,944 | 49.8% | All 9 | IB, VV | (blank), 1421, 6101, 6102, 6104–6115, 6152, 6161–6163, 6165–6167, 6169, 6171–6172, 6174–6178, 6180–6185, 6190–6192, 7352–7354, 7357–7358, 7360, 7398–7399, 7502, 7505, 7515, 7526–7527, 7529, 7531, 7533, 7542, 7549, 7553, 7558, 7560–7573, 7575, 7577, 7579, 7581, 7586, 7588, 7591, 7699, 7707, 7730, 7749, 7751, 7801, 7859, 7875, 7878, A101, A749, BLDM, CNSP, EMAP, IN10, IN99, MAJT, MNFS, MNMS, MNOL, MNPS, MNRS, MNVR, NS20, OUTG, PTSP, TIRE, VEND |
| Net zero review — 4122 / 4124 | **4122:** Inventory / Expense or COGS — journal entry for issues, adjustments, and transfers. **4124:** Offsetting credit side. Used by Inventory Issues (P4112), Transfers (P4113), Adjustments (P4114), Reclassifications (P4116). | 1,296 | 33.2% | All 9 | IR, VV | Same GL class code set as 4134/4136 above |
| Net zero review — 4126 / 4128 | **4126:** Inventory / Expense or COGS — zero balance adjustment, used when quantity equals zero but dollars remain. **4128:** Offsetting credit side. Used by Inventory Issues (P4112), Transfers (P4113), Adjustments (P4114), Reclassifications (P4116). | 324 | 8.3% | 2, 3, 22 | VV | Same GL class code set as 4134/4136 above |
| Mismatch — Business Unit (Tables 4122 and 4310, Company 67) | **4122:** Inventory Debit — Inventory Issues, Adjustments, Transfers (P4112/P4113/P4114). **4310:** Inventory — Debit inventory at time of PO receipt (P4312). | 216 | 5.5% | 67 only | IA, II, IJ, IL, IM, IP, IR, IV (4122); OR (4310) | Same GL class code set as 4134/4136 above |
| Mismatch — Object Account (Multiple tables, multiple companies) | **4122:** Inventory Debit. **4126:** RNV Debit. **4162:** Cross-company Transfer. **4240:** Inventory — Standard sales (R42800). **4310:** Inventory at PO receipt. **4385:** Inventory or Landed Cost / Landed Cost Temporary Liability (P4312). **4400:** Inventory / COGS or Expense — zero balance adjustment at receipt (P4312). | 118 | 3.0% | 2, 3, 9, 12, 22, 41, 43, 67, 73 | IA, II, IJ, IL, IM, IP, IR, IV, IX, OB, OC, OM, OP, OR, OW, SO | OUTG, 6101, 7563, 7564 |
| Mismatch — Object Account (WO Cost Type A1) (Tables 3110 / 3130, Companies 2 and 22) | **3110:** Raw Material / Sub-Assembly Inventory — credit side of material issues, uses GL class codes of components (R31802A). **3130:** Finished Goods / Sub-Assembly Inventory — debit for completions; scrap account for IS transactions (R31802A). | 4 | 0.1% | 2, 22 | IC, IM | OUTG |
| **TOTAL** | | **3,902** | **100%** | | | |

### Row Count by Company

| Company | Total Rows | Net Zero | Mismatch — BU | Mismatch — Object Account |
|---|---|---|---|---|
| 00002 | 591 | 540 | — | 51 |
| 00022 | 579 | 540 | — | 39 |
| 00003 | 548 | 540 | — | 8 |
| 00067 | 542 | 324 | 216 | 2 |
| 00009 | 338 | 324 | — | 14 |
| 00012 | 326 | 324 | — | 2 |
| 00041 | 326 | 324 | — | 2 |
| 00043 | 326 | 324 | — | 2 |
| 00073 | 326 | 324 | — | 2 |

### Row Count by DMAAI Table

| Table | Rows | Primary Comment | Companies Present |
|---|---|---|---|
| 4134 | 1,944 | Net zero — 4134/4136 | All 9 |
| 4122 | 1,454 | Net zero — 4122/4124 + Mismatch — Object Account | All 9 |
| 4126 | 340 | Net zero — 4126/4128 + Mismatch — Object Account | 2, 3, 22 |
| 4310 | 113 | Mismatch — BU (Co 67) + Mismatch — Object Account | 2, 22, 67 |
| 4400 | 32 | Mismatch — Object Account | 2, 3, 22 |
| 4385 | 12 | Mismatch — Object Account | 2, 22 |
| 3130 | 2 | Mismatch — Object Account (WO) | 2, 22 |
| 3110 | 2 | Mismatch — Object Account (WO) | 2, 22 |
| 4240 | 2 | Mismatch — Object Account | 2, 22 |
| 4162 | 1 | Mismatch — Object Account | 2 |

---

## Section 7: Findings by Priority

### Priority 1 — Business Unit Mismatch: Company 67 (Tables 4122 and 4310)

**Severity: HIGH — Systematic error affecting all GL class codes for company 67**

**What Was Found**

Company 67 has a business unit mismatch across **216 rows** in two DMAAI tables:

- **Table 4122** (108 rows): All inventory adjustment, transfer, and receipt doc types (IA, II, IJ, IL, IM, IP, IR, IV) for all GL class codes
- **Table 4310** (108 rows): All purchase order receipt (OR) doc types for all GL class codes

In both tables, the AAI entries have account **67010.1421** (Business Unit 67010, Object 1421). The model table (4152 PI) shows account **1421** with no business unit prefix — meaning the model expects the business unit to come from the transaction's branch/plant, not to be hard-coded in the DMAAI.

**GL Class Codes Affected**

108 GL class codes are affected. These include numeric codes in the 6101–6192 range, 7352–7878 range, and alphabetic codes including: BLDM, CNSP, EMAP, IN10, IN99, MAJT, MNFS, MNMS, MNOL, MNPS, MNRS, MNVR, NS20, OUTG, PTSP, TIRE, VEND, and others.

**Root Cause**

The DMAAI entries for company 67 in tables 4122 and 4310 have business unit 67010 hard-coded. Per JDE DMAAI design, when a business unit is left blank in the DMAAI entry, the system pulls the BU from the branch/plant on the transaction. Hard-coding 67010 overrides this behavior — every inventory and purchasing transaction for company 67 posts to BU 67010 regardless of which branch plant was used.

Either:
- BU 67010 is the correct and intended inventory account for all of company 67's transactions (consolidated plant), or
- BU 67010 was entered in error and should be removed so the branch/plant drives the account

**Verification Steps**

1. Navigate to DMAAI in JDE (fast path: `DMAAI`)
2. Inquire on table 4122, company 67, doc type IA
3. Confirm whether BU 67010 is listed in the Business Unit field
4. Check whether BU 67010 exists in the chart of accounts (P0901) and is set up as an inventory account
5. Review recent GL postings for company 67 inventory transactions to determine which BU they posted to
6. Cross-reference with model table 4152 — determine whether the model needs updating or the DMAAI does

**Resolution**

| If... | Then... |
|---|---|
| BU 67010 is correct | Update model table 4152 PI for company 67 to include BU 67010 for all affected GL class codes. Refresh RapidReconciler. |
| BU 67010 is incorrect | Remove the hard-coded BU from all 4122 and 4310 entries for company 67 in JDE DMAAI. Allow the transaction branch/plant to drive the BU. Refresh RapidReconciler. |

---

### Priority 2A — Object Account Mismatch: GL Class OUTG, Companies 2 and 22 (Multiple Tables)

**Severity: HIGH — Systematic object account error across all balance sheet DMAAI tables for OUTG items**

**What Was Found**

GL class **OUTG** has an object account discrepancy across every validated DMAAI table for companies 2 and 22:

| Table | Doc Types | Co 2 AAI | Co 2 Model | Co 22 AAI | Co 22 Model |
|---|---|---|---|---|---|
| 4122 | IJ, IL, IM, IP, IV | 1421 | 2.1423 | 1421 | 22.1423 |
| 4126 | IA, II, IJ, IL, IM, IP, IR | 2.1421 | 2.1423 | 22.1421 | 22.1423 |
| 4126 | IV | 1421 | 2.1423 | 1421 | 22.1423 |
| 4162 | IX | 2.1421 | 2.1423 | — | — |
| 4240 | SO | 1421 | 2.1423 | 1421 | 22.1423 |
| 4310 | OR | 1421 | 2.1423 | 1421 | 22.1423 |
| 4385 | OB, OC, OM, OP, OR, OW | 1421 | 2.1423 | 1421 | 22.1423 |
| 4400 | IV, OB, OC, OP | 1421 | 2.1423 | 1421 | 22.1423 |

**Pattern:** The DMAAI tables consistently have object **1421** (or BU.1421) for OUTG, while the model consistently expects object **1423** (or BU.1423) for OUTG in companies 2 and 22.

**Root Cause**

Either object 1421 or object 1423 is the correct inventory account for GL class OUTG. A discrepancy at the model level (4152) has propagated across all satellite tables, or the satellite tables were set up without being updated when the model changed. The mismatch is entirely in the **object account** component (1421 vs 1423); business units are consistent within each table.

**Note on Table 4126 Entries with BU**

For table 4126, some entries show `2.1421` (Co 2) or `22.1421` (Co 22) in the AAI field — meaning the BU is populated in 4126 but the object is still wrong (1421 vs model 1423). The BU component matches the model; only the object differs.

**Resolution**

1. Determine the correct object account for OUTG inventory: review the chart of accounts, item setup, and existing GL postings to confirm whether OUTG items should post to object 1421 or 1423.
2. **If 1423 is correct:** Update all affected DMAAI table entries for OUTG GL class in companies 2 and 22 to use object 1423. Tables to update: 3110, 3130 (see Priority 2C), 4122, 4126, 4162, 4240, 4310, 4385, 4400.
3. **If 1421 is correct:** Update model table 4152 PI for companies 2 and 22, GL class OUTG, to use object 1421.
4. Do not correct 4122 in isolation — all satellite tables must be updated in the same pass.
5. Refresh RapidReconciler after all changes.

---

### Priority 2B — Object Account Mismatch: GL Class OUTG, IA/II Doc Types, Table 4122 (Multiple Companies)

**Severity: MEDIUM-HIGH — Intercompany adjustment entries show inverse OUTG object account mismatch**

**What Was Found**

For **document types IA and II** in table 4122, the OUTG object mismatch is **inverted** compared to Priority 2A:

| Company | Doc Types | AAI Account | Model Account |
|---|---|---|---|
| 2 | IA, II | 1423 | 3.1421, 9.1421, 12.1421, 41.1421, 43.1421, 1421 |
| 3 | IA, II | 1423 | 3.1421 |
| 9 | IA, II | 1423 | 3.1421, 9.1421, 12.1421, 41.1421, 43.1421, 1421 |
| 12 | IA, II | 1423 | 12.1421 |
| 41 | IA, II | 1423 | 41.1421 |
| 43 | IA, II | 1423 | 43.1421 |
| 67 | IA, II | 1423 | 1421 |
| 73 | IA, II | 1423 | 1421 |

The IA and II doc types have object **1423** in the DMAAI, while the model expects object **1421**. This is the inverse of the IJ/IL/IM/IP/IV object account pattern in Priority 2A.

**Important Observation**

The multi-company model account column (e.g., `3.1421, 9.1421, 12.1421`) indicates that these IA/II entries appear to be intercompany transactions where company 2 or company 9 is the source and the entry references multiple transaction companies. The intercompany inventory adjustment may intentionally use a different object account from standard inventory adjustments.

**Resolution**

Analyze in conjunction with Priority 2A. Before correcting:
1. Confirm whether IA (Inventory Adjustment — In) and II (Internal/Intercompany Adjustment) transactions are intended to use the same object as other inventory adjustments or a different object.
2. If IA/II should use object 1421 (same as model): update table 4122 IA and II entries for all listed companies to use 1421 for OUTG.
3. If IA/II should use object 1423 (which is what they currently have): update the model table for the IA/II scenario.
4. Document the design decision before making changes — the inverse pattern across all 8 companies suggests this may be a deliberate intercompany account.

---

### Priority 2C — Object Account Mismatch: Work Order Cost Type A1 (Tables 3110 and 3130) — Companies 2 and 22

**Severity: MEDIUM — Manufacturing WIP object accounts affected for actual-cost work orders**

**What Was Found**

Tables 3110 (Material Issues) and 3130 (WIP Completions) have the same OUTG object mismatch as Priority 2A, specifically for work orders with **Order Type WO, Cost Type A1** (actual cost):

| Company | Table | Doc Type | AAI Account | Model Account |
|---|---|---|---|---|
| 2 | 3110 | IM | 1421 | 2.1423 |
| 2 | 3130 | IC | 1421 | 2.1423 |
| 22 | 3110 | IM | 1421 | 22.1423 |
| 22 | 3130 | IC | 1421 | 22.1423 |

**Root Cause**

Same root cause as Priority 2A — the OUTG object account discrepancy (1421 vs 1423) propagates into the manufacturing WIP tables. Cost Type A1 entries are specifically flagged, meaning this affects actual-cost work orders for OUTG-class items in companies 2 and 22.

**Manufacturing Accounting Context**

- **Table 3110** feeds the raw material side of the WIP journal entry — debiting WIP and crediting raw material inventory when materials are issued to a work order
- **Table 3130** feeds the completion side — debiting finished goods and crediting WIP when work orders are completed
- Manufacturing accounting (R31802A) is the batch program that creates these GL entries; it runs once per work order in final mode and **cannot be rerun**

If OUTG-class materials are being issued to actual-cost work orders and the DMAAI is wrong, the WIP account is off. Corrections to future transactions are straightforward, but past work orders already processed by R31802A cannot be reprocessed.

**Resolution**

Resolve in conjunction with Priority 2A — the correct object account (1421 or 1423) must be determined first. Once determined, update tables 3110 and 3130 for companies 2 and 22. Coordinate with manufacturing accounting to identify any work orders that have already been processed with the incorrect account.

---

### Priority 2D — Object Account Mismatch: Table 4400 (Intercompany/Advanced Pricing) — Companies 2, 3, and 22

**Severity: MEDIUM — Intercompany billing and advanced pricing object accounts may be incorrect**

**What Was Found**

Table 4400 (Intercompany/Advanced Pricing) has two distinct mismatch patterns:

**Pattern 1 — OUTG GL Class — Object Account Mismatch (same as Priority 2A):**

| Company | Doc Types | AAI Account | Model Account |
|---|---|---|---|
| 2 | IV, OB, OC, OP | 1421 | 2.1423 |
| 22 | IV, OB, OC, OP | 1421 | 22.1423 |

**Pattern 2 — GL Classes 6101, 7563, 7564 — Business Unit and Object Account Mismatch:**

| Company | GL Class | Doc Types | AAI Account | Model Account |
|---|---|---|---|---|
| 2 | 6101, 7563, 7564 | OB, OC, OP | 2200.6101 / 2200.7563 / 2200.7564 | 2.1421 |
| 22 | 6101, 7563, 7564 | OB, OC, OP | 22200.6101 / 22200.7563 / 22200.7564 | 22.1421 |
| 3 | 7563, 7564 | OB, OC, OP | 3210.7563 / 3210.7564 | 3.1421 |

**Analysis**

For Pattern 1, the same OUTG object account mismatch from Priority 2A applies to the intercompany tables. These should be corrected as part of the same OUTG correction pass.

For Pattern 2, the AAI uses business units 2200, 22200, and 3210 — which may be dedicated intercompany clearing business units, not inventory BUs. The object accounts differ from the model (6101/7563/7564 vs model object 1421). This could indicate:
- The intercompany billing entries legitimately use different accounts than standard inventory
- Or the 4400 entries were set up independently without reference to the model

**Resolution**

Do not correct Pattern 2 (GL classes 6101/7563/7564) without first confirming whether BU 2200, 22200, and 3210 are intentional intercompany clearing accounts. Correct Pattern 1 (OUTG) as part of the broader OUTG resolution in Action 2 of the Recommended Actions.

---

### Priority 3 — Net Zero Review (All Tables) — All 9 Companies

**Severity: REQUIRES VERIFICATION — Not a confirmed error; may be intentional**

**What Was Found**

3,564 rows carry a "Net zero review" comment across three table pairs:

| Table Pair | DMAAI Table Description | Row Count | Companies | Doc Types |
|---|---|---|---|---|
| 4134 / 4136 (In-Transit) | **4134:** In-Transit Inventory — records change to COGS when item cost changes. **4136:** Offsetting credit side. Used by Quantity Revisions (P41022), Item Branch/Plant (P41026), Batch Cost Maintenance (R41802). | 1,944 | All 9 | IB, VV |
| 4122 / 4124 (Inventory / Relief) | **4122:** Inventory / Expense or COGS — journal entry for issues, adjustments, and transfers. **4124:** Offsetting credit side. Used by Inventory Issues (P4112), Transfers (P4113), Adjustments (P4114), Reclassifications (P4116). | 1,296 | All 9 | IR, VV |
| 4126 / 4128 (Zero Balance Adjustment) | **4126:** Inventory / Expense or COGS — zero balance adjustment, used when quantity equals zero but dollars remain. **4128:** Offsetting credit side. Used by Inventory Issues (P4112), Transfers (P4113), Adjustments (P4114), Reclassifications (P4116). | 324 | 2, 3, 22 | VV |

**Key Observation**

For all net zero rows, the **ModelAccount column is blank (NaN)**. This means RapidReconciler cannot compare these entries directly against the model table — the model table (4152 PI) does not have entries for the IR, VV, or IB doc types with the same GL class codes. The net zero flag is generated by comparing the table pair (e.g., 4122 vs 4124) rather than against the model.

**What Net Zero Means in Practice**

A net zero configuration occurs when the debit entry (e.g., 4122) and the credit entry (e.g., 4124) for the same GL class and doc type point to the same account. The journal entry created debits and credits the same account, resulting in no net movement. This is problematic for inventory because:

- **4122 / 4124 pair:** The debit to inventory (4122) and the credit from inventory (4124) both hit the same account → no inventory balance change recorded in the GL → reconciliation cannot balance. These tables are used by Inventory Issues (P4112), Transfers (P4113), Adjustments (P4114), and Reclassifications (P4116).
- **4134 / 4136 pair:** The in-transit debit (4134) and in-transit credit (4136) both hit the same account → in-transit inventory cannot be tracked separately from on-hand. These tables are used by Quantity Revisions (P41022), Item Branch/Plant (P41026), and Batch Cost Maintenance (R41802).
- **4126 / 4128 pair:** The zero balance adjustment debit (4126) and its credit (4128) both hit the same account → the adjustment nets to zero and no correction is recorded. These tables are used by the same inventory programs as 4122/4124 (P4112, P4113, P4114, P4116).

See Section 8 for the full verification protocol.

---

## Section 8: Net Zero — Verification Protocol

### Step 1: Access DMAAI in JDE

Navigate to the DMAAI setup using fast path **`DMAAI`** from any distribution setup menu. This opens the Distribution/Manufacturing AAI Values (F4095) inquiry screen.

### Step 2: Compare the Table Pair

For each net zero flag, compare the account numbers in the two paired tables:

| Net Zero Comment | Base Table | Check Against |
|---|---|---|
| Net zero review — 4122,4124 | DMAAI 4122 | DMAAI 4124 |
| Net zero review — 4126,4128 | DMAAI 4126 | DMAAI 4128 |
| Net zero review — 4134,4136 | DMAAI 4134 | DMAAI 4136 |

For each combination of **Company**, **Doc Type**, and **GL Class Code**:
1. Note the account number in the base table (4122, 4126, or 4134)
2. Note the account number in the complement table (4124, 4128, or 4136)
3. If the accounts are the same → this is the net zero condition

### Step 3: Determine Intent

Ask the accounting team: *Is it intentional that the [4122] and [4124] entries for [GL class] in [company] point to the same account?*

Common reasons for intentional net zero (rare but possible):
- A clearing account where the system self-offsets and a separate journal is used for the actual entry
- A test or placeholder configuration
- Flexible Accounting is expected to override the DMAAI entry

Reasons net zero is almost always an error:
- The complement table (4124, 4128, or 4136) entry was never set up
- The complement table entry was accidentally set to the same account as the base table
- A DMAAI copy operation duplicated an entry without updating the account

### Step 4: Correct If Necessary

If the net zero is confirmed as an error:
1. Navigate to the complement table entry in DMAAI
2. Update the account to the correct offsetting account (e.g., for 4124, this should be the credit-side of the inventory entry — typically a different object than 4122)
3. Verify the change is correct by reviewing the AAI design documentation
4. Refresh RapidReconciler after all changes are saved

### Step 5: Document the Review

For entries confirmed as intentional: document the business reason and mark as reviewed. For entries corrected: document the before and after account numbers, date of correction, and who authorized the change.

---

## Section 9: Step-by-Step Analysis Procedure

Use this procedure each time an Integrity Report 2 export is received.

### Step 1: Review the Export Header

Confirm the period-end date and generation timestamp in the first row of the export. Verify this matches the expected reporting period.

### Step 2: Establish the Issue Count Baseline

Sort by the **Comment** column and count rows by comment type. Use this as the baseline to track resolution over subsequent exports.

### Step 3: Address Mismatches Before Net Zero

Mismatch findings (object and business unit) represent confirmed discrepancies where the DMAAI and model table disagree. These should always be prioritized over net zero findings, which require verification before being classified as errors.

### Step 4: Work Mismatches by Company and Table

For each mismatch finding:
1. Identify the company, table, GL class, doc type, and account discrepancy
2. Open DMAAI in JDE and locate the specific entry
3. Compare the AAI entry to the model table entry side-by-side
4. Determine which account is correct (DMAAI or model)
5. Make the correction in the appropriate location (DMAAI entry or model table)

### Step 5: Work Net Zero by Table Pair

For each net zero flag, follow the verification protocol in Section 8. Do not skip verification — mark net zero items as verified (intentional) or corrected, not as automatically resolved.

### Step 6: Verify Corrections

After making corrections in JDE:
1. Trigger a data refresh in RapidReconciler
2. Re-run Integrity Report 2
3. Confirm that corrected items no longer appear in the export
4. Verify that corrections have not introduced new flags

### Step 7: Document Findings

Maintain a running log of:
- Each finding from the export (company, table, GL class, issue type)
- Determination: error or intentional
- Action taken: JDE DMAAI correction, model table update, or verified as intentional
- Date and responsible party

---

## Section 10: Excel Output Formatting Rules

### File Naming

```
Integrity_[Period-End-Date]_[Timestamp]_Analysis.xlsx
```

**Example:** `Integrity_2026-03-31_20260422-1825_Analysis.xlsx`

### Sheet Structure

| Sheet | Contents |
|---|---|
| **Integrity** | The original source data, unchanged |
| **RR Analysis** | The analysis sheet (see below) |

Do not delete, rename, or reorder the source sheet.

### RR Analysis Sheet Structure

| Section | Content |
|---|---|
| **Report Summary** | Period-end date, generation timestamp, total row count, companies present, tables present, issue type breakdown |
| **Variance Type Summary** | One row per comment type with six columns: Comment / Issue Type, DMAAI Table Description (sourced from distribution-aais.md), Row Count, Companies Affected, Doc Types, and GL Class Codes Impacted. Color-coded by severity. |
| **Findings by Priority** | One sub-section per priority finding. Each sub-section contains the detailed account analysis, root cause, and resolution path. Followed by a note box with key observations. |
| **Recommended Actions** | Numbered action steps in execution order, with the specific tables, companies, and responsible owner for each. |

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
| **Priority 3 rows** | Yellow fill (`FFFACD`), dark gold text (`5C4A00`) |
| **Note boxes** | Light gold fill (`FFF3CD`), dark gold italic text (`7B4C00`); full-width merged cell; wrap text enabled |
| **Column widths** | Column A: 35 characters; Column B: 40 characters; Column C: 12 characters; Column D: 20 characters; Column E: 18 characters; Column F: 110 characters (GL class codes) |

---

## Section 11: Using Claude for Automated Analysis

Claude can perform the full analysis procedure automatically and return a single updated `.xlsx` file with the RR Analysis sheet added.

### What to Upload

Upload **two files:**

1. This guide (`.md`)
2. The Integrity Report 2 export (`.xlsx`)

Then use the following prompt:

> *"Analyze this Integrity Report 2 file using the guide as reference, then produce an updated copy of the Excel file with the analysis written to a new sheet called 'RR Analysis'. Any comment with net zero needs to be verified, not marked as a potential issue. Mismatches with the model table should be labeled as object account mismatches or business unit mismatches and prioritized by impact. Use the DMAAI table descriptions from the distribution-aais.md reference for the Variance Type Summary."*

### Follow-On Requests in the Same Session

Once this guide has been uploaded, it remains in context. Use:

> *"Analyze this Integrity Report file and return it with the RR Analysis sheet."*

### Output Specification

**File naming:** Append `_Analysis` to the original filename.

**Sheet 1 — Integrity (original)**
- Source data, unchanged
- No row highlighting required for Integrity Report 2 (unlike End of Day exports)

**Sheet 2 — RR Analysis (new)**
- Report Summary
- Variance Type Summary (color-coded by priority)
- Findings by Priority (with detail, root cause, and resolution for each)
- Recommended Actions (numbered, in execution order)

### Notes and Limitations

- Claude analyzes the data as exported. Account numbers are interpreted from the export columns; the actual JDE DMAAI setup must be verified in JD Edwards.
- Net zero findings are flagged for verification, not automatically classified as errors.
- Mismatch resolution requires JDE access to confirm which account (DMAAI or model) is correct.
- The analysis cannot determine the intended chart of accounts structure — that must be provided by the accounting team.
- For exports with systematic mismatches across many GL class codes, the analysis groups findings by pattern (e.g., "all OUTG entries in tables 4122, 4126, 4240, 4310 for companies 2 and 22") to make the summary workable.

---

## Section 12: AAI Quick Reference

### Balance Sheet DMAAI Tables Validated by Integrity Report 2

| Table | Module | Transaction Event | Typical Doc Types | Debit / Credit |
|---|---|---|---|---|
| **3110** | Manufacturing | Material issued to work order | IM | Debit WIP; Credit Raw Material |
| **3130** | Manufacturing | Work order completion | IC | Debit Finished Goods; Credit WIP |
| **4122** | Inventory | Inventory adjustment, transfer, receipt | IA, II, IJ, IL, IM, IP, IR, IV | Debit Inventory |
| **4124** | Inventory | Inventory relief (credit side of 4122) | IA, II, IJ, IL, IM, IP, IR, IV | Credit Inventory |
| **4126** | Purchasing | RNV debit (voucher match) | VV | Debit RNV |
| **4128** | Purchasing | RNV credit reversal | VV | Credit RNV |
| **4134** | Inventory | In-transit debit (branch transfer) | IB | Debit In-Transit |
| **4136** | Inventory | In-transit credit on receipt | IB | Credit In-Transit |
| **4162** | Inventory | Cross-company inventory transfer | IX | Debit Inventory — Receiving |
| **4172** | Inventory | Physical inventory adjustment | IJ | Debit/Credit Inventory |
| **4240** | Sales | Cost of Goods Sold | SO | Debit COGS; Credit Inventory |
| **4310** | Purchasing | Inventory on PO receipt | OR | Debit Inventory |
| **4385** | Purchasing | Outbound logistics | OB, OC, OM, OP, OR, OW | Varies |
| **4400** | Sales | Intercompany / Advanced Pricing | IV, OB, OC, OP | Varies |

### AAI Key Structure

An AAI entry requires a unique combination of:
- **Company Number**
- **Document Type**
- **GL Class Code**

If a specific combination is not found, JDE searches in this fallback order:
1. Company [X], GL Class [specific code]
2. Company [X], GL Class \*\*\*\* (wildcard)
3. Company 00000, GL Class [specific code]
4. Company 00000, GL Class \*\*\*\* (wildcard)
5. Error if still not found

### GL Class Code Sources by Transaction Type

| Transaction Type | GL Class Code Source |
|---|---|
| Work Orders (issues & completions) | Item Branch level |
| Sales Orders / Purchase Orders | Order line level (copied from Item Location) |
| Inventory Transactions | Item Location level |

### Business Unit in AAI Entries

When the Business Unit field is **blank** in the DMAAI entry:
- The system pulls the BU from the **Branch/Plant on the transaction**
- Exception: If a Project Number is assigned to the BU, the Project Number is used as the BU
- Exception: Sales Update (R42800) processing option 5 controls BU source for sales transactions
- Exception: Flexible Accounting rules (P40296) can override the BU dynamically

When the Business Unit field is **populated** in the DMAAI entry:
- The hard-coded BU is used regardless of the transaction's branch/plant
- This is appropriate only for accounts that are not branch/plant-specific (e.g., corporate accounts)

### Flexible Accounting Notes

Flexible Accounting (P40296) allows the business unit or subsidiary to be dynamically constructed from transaction fields (customer, item, etc.). If FlexBu or FlexSub is **Yes** in the report:
- The BU or subsidiary shown in the AAI account may not be the actual posting BU/Sub
- Flexible Accounting rules must be reviewed in P40296 to determine the actual account
- Per AAI setup requirements, if Flexible Accounting populates the BU, the BU must be left **blank** in the DMAAI entry

In this report, **FlexBu = Yes** for all rows in table 4122 and some rows in other tables for companies 2 and 22. This means the BU in the AAI account column may be overridden at posting time. The object account mismatch findings still apply (Flexible Accounting cannot flex the object account).

---

## Section 13: Related Documentation

- [End of Day Analysis Guide](end-of-day-analysis-guide.md) — Reference for EOD variance analysis in RapidReconciler
- [DMAAI Reference Guide](distribution-aais.md) — Complete reference for JDE Distribution and Manufacturing AAIs (F4095), including all table numbers, key structure, fallback sequence, and Flexible Accounting setup
- [Inventory Key Concepts Training Manual](inventory-key-concepts.md) — Foundation concepts including the Model DMAAI Table, GL class code hierarchy, variance sources, and cardex variance

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*
