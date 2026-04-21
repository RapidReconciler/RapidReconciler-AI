# Transaction Detail Analysis Guide

## RapidReconciler Inventory -- Transaction Detail Report Reference

---

## Table of Contents

- [Overview](#overview)
- [Section 1: Report Structure](#section-1-report-structure)
- [Section 2: Section-by-Section Field Reference](#section-2-section-by-section-field-reference)
- [Section 3: How RapidReconciler Matches Transactions](#section-3-how-rapidreconciler-matches-transactions)
- [Section 4: Common Variance Patterns and Root Causes](#section-4-common-variance-patterns-and-root-causes)
- [Section 5: DMAAI Analysis](#section-5-dmaai-analysis)
- [Section 6: Step-by-Step Analysis Procedure](#section-6-step-by-step-analysis-procedure)
- [Section 7: Sub Type Reference](#section-7-sub-type-reference)
- [Section 8: Document Type Reference](#section-8-document-type-reference)
- [Section 9: Related Documentation](#section-9-related-documentation)
- [Section 10: Using Claude for Automated Analysis](#section-10-using-claude-for-automated-analysis)

---

## Overview

The Transaction Detail report in RapidReconciler is produced when drilling into an unreconciled transaction on the Transactions page. It provides a complete side-by-side view of what exists in the item ledger (F4111) versus what exists in the general ledger (F0911) for a specific company, document type, and document number.

The report is the primary diagnostic tool for identifying the root cause of transaction-level variances. A thorough understanding of each section and how RapidReconciler uses them is essential for effective analysis.

> **Who should use this guide:** JD Edwards business analysts, cost accountants, and inventory accountants responsible for investigating and resolving transaction variances in RapidReconciler.

---

## Section 1: Report Structure

The Transaction Detail report is organized into the following sections, always appearing in this order:

| Section | Name | Purpose |
|---|---|---|
| **Unassigned** | Unassigned Account | **Appears only when GL class codes are missing from the model table.** Lists F4111 cardex rows that RapidReconciler cannot assign to a GL account. These rows are excluded from the reconciliation and do NOT appear in the F4111 Data section or F4111 Total. |
| **Doc Header** | Document Header | High-level summary of the document being analyzed including the variance amount and sub type |
| **F4111 Data** | Item Ledger Data | All cardex records for the document from the item ledger table -- **excludes any rows in the Unassigned section** |
| **F0911 Inv Acct** | GL Inventory Account | All GL entries posted to inventory balance sheet accounts for the document |
| **F0911 Exp Acct** | GL Expense Account | All GL entries posted to non-inventory (expense/variance) accounts for the document |
| **RR Summary** | RapidReconciler Summary | How RapidReconciler matched and summarized the data; shows the net cardex total, GL total, and variance |
| **Header Comp** | Header Comparison | Purchase order or sales order header data for context |
| **Receipts** | Receipt and Voucher Detail | All F43121 records (receipts, voucher matches, reversals) for the order being analyzed |
| **DMAAs** | DMAAI Entries | All AAI entries for each GL class code in the transaction, starting with the model table (4152) |

> **Critical:** If the Unassigned section is present, the F4111 Total shown in the report is **understated**. The true cardex total is the F4111 Total plus the Unassigned Total. The variance displayed in the Doc Header and RR Summary only reflects the portion of the transaction that RapidReconciler can match -- not the full picture. Always check whether the Unassigned section is present before interpreting variance amounts.

---

## Section 2: Section-by-Section Field Reference

### 2.1 Unassigned Section

The Unassigned section appears at the top of the report **only when one or more GL class codes in the transaction are missing from the model DMAAI table (4152)**. It is the first indicator that a model table gap exists.

| Field | Description |
|---|---|
| **Account** | Displays "outside operations" or another internal RapidReconciler label -- not a real GL account number, because no model table entry exists to assign one |
| **CardexAmount** | The F4111 amount for this row -- excluded from the F4111 Total and from all reconciliation matching |
| **LedgerAmount** | Always $0.00 in this section |
| **Variance** | Equal to CardexAmount -- the full amount is unmatched |
| **Comment** | "Unassigned Account" -- confirms why the row appears here |
| **Unassigned Tot** | The total of all unassigned rows. **Add this to the F4111 Total to get the true cardex amount for the document.** |

> **What to do:** When the Unassigned section is present, immediately go to the DMAAs section and look for "Missing model table entry" in the Comment column. Identify which GL class code is missing and add it to DMAAI table 4152 in JD Edwards. After the next RapidReconciler refresh, the previously unassigned rows will move into the F4111 Data section and the full variance will be visible.

### 2.2 Doc Header

| Field | Description |
|---|---|
| **Period** | The fiscal period the transaction falls in |
| **Account** | The GL account number |
| **Source** | Always "Doc Header" |
| **Company** | JD Edwards company number |
| **Doc** | The document number being analyzed |
| **DT** | Document type (e.g., OV = receipt, PV = voucher match, PD = payment, IM = inventory issue) |
| **OrderNum** | The associated purchase or sales order number |
| **OT** | Order type (e.g., OP = purchase order) |
| **LedgerAmount** | The total GL amount for this document -- the variance to be explained |
| **Sub Type** | RapidReconciler classification of the variance type (see Section 7) |

### 2.3 F4111 Data

| Field | Description |
|---|---|
| **F4111 Tot** | The total cardex (item ledger) amount for this document. If zero and the GL has an amount, this is a GL-only entry -- a common and significant finding. |

Individual F4111 rows (when present) include:

| Field | Description |
|---|---|
| **TransDate** | The transaction creation date |
| **GLDate** | The GL date assigned to the transaction |
| **GLClass** | The GL class code from the item location record |
| **Batch** | The JD Edwards batch number |
| **BT** | Batch type |
| **Doc / DT** | Document number and type |
| **OrderNum / OT** | Order number and type |
| **Line** | The order line number |
| **PC** | Posting code. "P" = posted; blank or other = not posted. "X" = memo transaction (excluded from reconciliation) |
| **Branch** | Branch plant |
| **Item** | Item number |
| **Location / Lot** | Location and lot number |
| **Qty** | Transaction quantity |
| **UM** | Unit of measure |
| **UnitCost** | Unit cost on the transaction |
| **CardexAmount** | Extended amount from the cardex |

### 2.4 F0911 Inv Acct

GL entries posted to inventory balance sheet accounts. These are the entries RapidReconciler expects to match to the F4111 cardex.

| Field | Description |
|---|---|
| **Account** | The GL account number |
| **TransDate / GLDate** | Transaction and GL dates |
| **Batch / BT** | Batch number and type |
| **Doc / DT** | Document number and type |
| **LedgerAmount** | The GL amount for this entry |
| **Comment** | Supplier name or other descriptive text from the GL |
| **F0911 Tot** | Total of all GL inventory account entries for this document |

### 2.5 F0911 Exp Acct

GL entries posted to non-inventory accounts (expense, variance, RNV, tax). These entries are visible for context but are not included in the inventory reconciliation matching.

### 2.6 RR Summary

The most important section for understanding what RapidReconciler sees and how it matched the transaction.

| Field | Description |
|---|---|
| **CardexAmount** | The total F4111 amount RapidReconciler used for matching |
| **LedgerAmount** | The total F0911 inventory account amount RapidReconciler used for matching |
| **Variance** | CardexAmount minus LedgerAmount. Non-zero = unreconciled. |
| **RR Total row** | Summary line showing the net variance. The Variance column here matches what appears on the Transactions page. |

> **Key diagnostic:** If CardexAmount = 0 and LedgerAmount is non-zero, the variance is entirely GL-side with no cardex entry. If LedgerAmount = 0 and CardexAmount is non-zero, the variance is entirely cardex-side with no GL entry. If both are non-zero but unequal, compare at the individual batch and account level -- a single line item may be missing from one side even though other lines in the same batch reconcile cleanly (see Section 4.3).

### 2.7 Header Comp

Purchase order or sales order header context. Key fields:

| Field | Description |
|---|---|
| **TransDate / GLDate** | Dates on the order header |
| **GLClass** | GL class code on the order line |
| **Doc / DT** | Document number and type |
| **OrderNum / OT** | Order number and type |
| **Line** | Line number |
| **LineTy** | Line type (e.g., S = stock, N = non-stock, F = freight, D = direct ship, W = work order) |
| **NxtSts** | Next status. 999 = fully closed. Important for determining whether further JD Edwards processing is possible. |
| **Branch / Item / Location / Lot** | Item details |
| **Qty / UM / UnitCost** | Quantity, unit of measure, and unit cost on the order |
| **CardexAmount** | The cardex amount associated with this order line |
| **Comment** | Additional context (e.g., "Taxes", "Voucher Match", "Landed Cost", "non stock line", "sales ext cost error calc") |

> **Key indicator -- GLDate of 2000-01-01 and Doc of 0:** When a Header Comp row shows a GL date of **2000-01-01** and a document number of **0**, this is a RapidReconciler flag indicating the order line was **never processed through Sales Update**. The line exists in JD Edwards but has no invoice document and no GL entry. If the CardexAmount is also $0.00, no cardex was written either. These lines may represent unbilled quantities, cancelled lines that were not properly closed, or calculation errors. Look for an accompanying comment such as "sales ext cost error calc = [amount]" which indicates RapidReconciler detected a discrepancy in the extended cost calculation for the line.

### 2.8 Receipts

All F43121 records for the order. This is the most detailed section for understanding the full purchasing history.

| Field | Description |
|---|---|
| **Source** | Always "Receipts" |
| **TransDate / GLDate** | Receipt or voucher match dates |
| **GLClass** | GL class code |
| **Batch / BT** | Batch number and type. "No Cx" in the Batch field means no cardex record was created -- this is significant. |
| **Doc / DT** | Document number and type |
| **OrderNum / OT** | Order number and type |
| **Line** | Line number |
| **NxtSts** | Next status on the F43121 record |
| **Qty / UM / UnitCost** | Quantity and cost details |
| **CardexAmount** | The cardex (F4111) amount for this receipt/voucher |
| **LedgerAmount** | The GL (F0911) amount for this receipt/voucher |
| **Variance** | Difference between CardexAmount and LedgerAmount for this specific document |
| **Comment** | Context such as tax amounts ("Taxes = 1057.02"), "Landed Cost", "Voucher Match" |

### 2.9 DMAAs

All DMAAI entries for each GL class code in the transaction. The first row is always from the model table (4152).

| Field | Description |
|---|---|
| **Account** | The full account number (Business Unit.Object.Subsidiary) |
| **DMAAI Table** | The specific AAI table number and name |
| **Company** | The company the AAI is configured for |
| **GLClass** | The GL class code |
| **Object** | The object account in the AAI |
| **Ty** | Order type the AAI applies to |
| **Comment** | RapidReconciler flags such as "Mismatch - object", "Mismatch - BU", "Net Zero" |

> **Critical:** Any entry in the Comment column of the DMAAs section indicates a configuration problem. "Mismatch - object" means the AAI object account does not match the model table. "Mismatch - BU" means the business unit differs. "Net Zero" means the debit and credit AAIs point to the same account, producing no net GL impact.

---

## Section 3: How RapidReconciler Matches Transactions

RapidReconciler matches F4111 and F0911 records using the following fields:

- Company number
- Account number
- Fiscal period
- Document type
- Document number
- Order number
- Batch number

A difference in **any one of these fields** results in a mismatch. The RR Summary section will show multiple rows when a mismatch exists -- one row per unique combination of matching fields found.

**Single row in RR Summary = match. Multiple rows = mismatch on one or more fields.**

Common mismatch scenarios:

| Mismatch Type | What It Looks Like | Common Cause |
|---|---|---|
| Account mismatch | CardexAmount and LedgerAmount on separate rows | DMAAI misconfiguration; GL class code change |
| Period mismatch | Same amounts but in different period rows | Backdating; Sales Update or Manufacturing Accounting processed in a different period than the cardex |
| GL-only entry | CardexAmount = 0, LedgerAmount has a value | Manual journal entry to inventory account; payment or discount entry coded to inventory; voucher with no receipt |
| Cardex-only entry | LedgerAmount = 0, CardexAmount has a value | Unposted batch; cardex written but GL not updated |
| Partial cardex-only entry | Both totals are non-zero but unequal; one or more RR Summary rows show LedgerAmount = 0 for a specific batch/account | A single line item within an otherwise-posted batch has no GL counterpart -- see Section 4.3 |

---

## Section 4: Common Variance Patterns and Root Causes

### 4.1 Unassigned Account -- Missing Model Table Entry

**Symptoms:**
- An **Unassigned** section appears at the top of the report before the Doc Header
- F4111 rows appear in the Unassigned section with an account labeled "outside operations" or similar internal label
- The F4111 Total is zero or lower than expected
- The DMAAs section shows **"Missing entry / Missing model table entry"** for one or more GL class codes
- The variance shown in the Doc Header and RR Summary reflects only the portion of the transaction with a known GL class -- the unassigned portion is hidden

**What is happening:**

RapidReconciler uses DMAAI table 4152 to assign a GL account to every F4111 cardex row during import. If a GL class code has no entry in the model table, RapidReconciler cannot assign an account and places those rows in the Unassigned section instead of F4111 Data. These rows are completely excluded from the reconciliation matching -- they do not appear in the F4111 Total, do not appear in the RR Summary, and do not contribute to the displayed variance.

This means the **true variance is larger than what RapidReconciler is showing**. The actual unmatched cardex amount is the F4111 Total plus the Unassigned Total.

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| New GL class code added to items but not to model table | DMAAs shows "Missing model table entry" for the GL class; Integrity Report 3 also lists this class | Add the GL class code to DMAAI table 4152 in JD Edwards with the correct account. After the next refresh, unassigned rows move to F4111 Data. |
| GL class code changed on item without updating model table | Recent GL class code change visible in GL Class Integrity (Integrity Report 5) | Same resolution -- add the new GL class to the model table |
| \*OP outside operation items with specialist GL class | Item numbers contain \*OP suffix; GL class is specific to outside operations | Add the outside operations GL class to the model table pointing to the correct inventory account |

> **Important:** Fixing the model table entry will cause previously invisible cardex amounts to become visible in the reconciliation after the next refresh. The displayed variance will increase before it can be resolved. This is expected -- it represents the true state of the reconciliation, not a new problem.

### 4.2 GL-Only Entry (No Cardex)

**Symptoms:**
- F4111 Total = $0.00
- F0911 Total has a non-zero amount
- RR Summary shows CardexAmount = 0, LedgerAmount = non-zero

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| Manual journal entry posted to inventory account | Doc type is JE or similar; no F43121 record exists | Investigate who posted the entry and why. Recode to correct account via reversing journal entry. |
| A/P payment (PD document) hitting inventory | Doc type PD; appears in F0911 inventory account; no F4111 record | Payment discount or currency adjustment coded to wrong account. Recode to discount/variance account. |
| Tax variance at voucher match | PV document; tax amount in comment differs between receipt and voucher rows | Tax rate or taxable amount changed between receipt and voucher match. Post manual journal entry for the difference. |
| Voucher posted without a receipt | PV document; no matching OV in F43121 | Receipt may have been reversed after voucher match. Investigate F43121 history. |
| **Non-stock line posted to inventory account** | F0911 Comment reads **"Non stock line in Inv acct"**; line type in Header Comp is N, F, or another non-inventory type; F4111 is empty | The line type definition is configured with a GL offset that routes to an inventory GL class. Review the line type definition for the applicable order type. Post a manual journal entry to move the GL amount from the inventory account to the correct expense or COGS account. If this pattern appears on multiple transactions, the line type configuration requires correction rather than transaction-by-transaction journal entries. |
| Sales return (RM) with IB batch type | Doc type is RM; batch type is IB rather than I; F4111 is empty | The return was processed via a manual correction batch (IB) that posted to the inventory account without writing a cardex record. Investigate who created the IB batch and whether it was intended as a correction. Post a journal entry to recode if the inventory account is incorrect. |

### 4.3 Cardex-Only Entry (No GL)

**Symptoms:**
- F4111 Total has a non-zero amount **and** F0911 Total = $0.00 (full cardex-only); **OR**
- F0911 Total is non-zero but smaller than the F4111 Total for the same GL class and batch, and one or more RR Summary rows show CardexAmount non-zero with LedgerAmount = $0.00 (partial cardex-only -- a single line item within an otherwise-posted batch has no GL counterpart)
- Appears in the GL Batches variance on the Reconciliation page

> **Important distinction:** The partial variant does not set off the obvious "F0911 Total = $0.00" alarm. The batch is fully posted and other lines reconcile cleanly. The only indicators are the RR Summary cardex-only row for a specific batch/account combination and a gap between the F4111 and F0911 totals for that GL class. Always compare totals at the GL class and batch level, not just at the document level.

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| Unposted batch | PC field in F4111 is not "P"; batch visible in GL Batches variance | Post the batch in JD Edwards |
| Batch posted to wrong period or company | F4111 record exists but GL entry is in different period/company | Locate the GL entry; determine if a period or company mismatch exists |
| Partial batch GL failure -- single line missing from an otherwise-posted batch | PC = "P" on all F4111 rows; all other lines in the same batch and GL class have matching F0911 entries; one cardex line has no GL counterpart; the missing line often has a unit cost that is a significant outlier relative to other lines in the same transaction | First, query F0911 for the document and batch across **all** accounts (not just inventory) -- the GL entry may have posted to an unexpected account rather than being absent entirely. If no entry exists anywhere, post a manual journal entry for the specific line amount. Investigate whether the outlier unit cost caused the GL interface to reject or suppress the line. |

### 4.4 Account Mismatch (Both Cardex and GL Exist but in Different Accounts)

**Symptoms:**
- Multiple rows in RR Summary
- CardexAmount and LedgerAmount are on separate rows
- Variance equals the amount on each row

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| DMAAI misconfiguration | DMAAs section shows "Mismatch" flag | Correct the AAI in JD Edwards. Post manual journal entry to move the GL amount to the correct account. |
| GL class code changed after receipt | Item has different GL class on the order line vs. current location | Manual journal entry to recode the GL amount to match the cardex account |
| Flex accounting producing unexpected account | BUFlex or SubFlex active in DMAAs section | Review flex accounting rules for the item/customer combination |

### 4.5 Period Mismatch

**Symptoms:**
- Multiple rows in RR Summary with different Period values
- Amounts match but are in different fiscal periods

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| Backdated GL entry | GLDate on F0911 row is in a prior period vs. F4111 TransDate | Manual journal entry to move the GL amount to the correct period |
| Sales Update or Manufacturing Accounting processed after period close | End of Day variance visible; batch number populated after the period | No correction needed if intentional; document for audit |

### 4.6 Tax Variance

**Symptoms:**
- Receipt rows in the Receipts section show "Taxes = [amount]" in Comment
- Tax amount at voucher match differs from tax amount at receipt
- Variance amount matches the tax difference

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| Tax rate changed between receipt and voucher match | Compare Taxes comment on OV receipt row vs. PV voucher row | Review tax explanation code and rate on the order. Post manual journal entry for the net difference. |
| Tax explanation code change | Tax code visible on order header; different from what was used at receipt | Investigate which code should apply; correct in JD Edwards if possible; journal entry if not |

### 4.7 Landed Cost Variance

**Symptoms:**
- Receipts section contains rows with "Landed Cost" in Comment
- Landed cost CardexAmount or LedgerAmount is zero or mismatched

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| Landed cost applied but not vouchered (PRLAND = 3) | No PV row for the landed cost in Receipts section | Accrual-only landed cost -- no voucher will be generated. Suspend in RapidReconciler if creating a false variance. |
| Landed cost reversed without re-application | Reversal visible in Receipts; no subsequent application | Re-apply landed cost or post manual journal entry |

### 4.8 "No Cx" in Batch Field

**Symptoms:**
- A receipt row in the Receipts section shows "No Cx" in the Batch column
- This means the voucher match was processed but no cardex record was written

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| Voucher match processed against a previously reversed receipt | OV receipt was reversed (Match Type 3) before voucher match occurred | Investigate F43121 history; determine correct sequence of events; manual journal entry to clear |
| Line type does not interface with inventory | LineTy field shows non-stock line type | Expected behavior for non-stock lines; verify AAI configuration |

### 4.9 Standard Cost Change After Work Order Completion

**Symptoms:**
- Document type is **IC** (work order completion)
- F4111 has **two rows** for the same document number:
  - Row 1: Comment "Completed W.O.'s To Inventory" -- normal completion with quantity and unit cost
  - Row 2: Comment "Standard Cost Change" -- **zero quantity, zero unit cost**, with a dollar amount only
- F0911 GL has only **one entry** -- the original completion amount -- referencing a **different document number** than the cardex (Manufacturing Accounting summarizes completions into a GL document)
- RR Summary shows two rows: one GL-only (the completion matched to the GL doc) and one cardex-only (the net cardex amount with no GL match)
- The variance amount equals the Row 2 "Standard Cost Change" amount exactly

**What is happening:**

When a work order completion is processed, the cardex is written at the current standard cost. If the standard cost is subsequently updated via R30835 (Frozen Standard Update) **after** the completion has already posted, JD Edwards writes a second cardex row to revalue the completed inventory to the new standard. However, if WIP Revaluation (R30837) was not configured to run -- or was not called from R30835 -- the corresponding GL journal entry is never created, leaving the cardex revaluation with no GL counterpart.

The GL document number mismatch (e.g., cardex shows doc 545031 but GL shows 566580) is **normal behavior** for IC transactions -- Manufacturing Accounting (R31802A) summarizes multiple work order transactions into a single GL document. This is not the cause of the variance but can cause confusion when tracing the transaction.

**Common causes:**

| Cause | How to Identify | Resolution |
|---|---|---|
| R30837 (WIP Revaluation) not run after standard cost update | F4111 Row 2 shows "Standard Cost Change" with no matching GL entry; variance amount matches Row 2 exactly | Post a manual journal entry: debit inventory account for the variance amount; credit the appropriate variance account (AAI 3260 Planned Variance or 3240 Material Variance). Review WIP Revaluation configuration to prevent recurrence. |
| R30837 run but work order was already closed at status 999 | Work order NxtSts = 999; R30837 does not revalue closed work orders | Same journal entry resolution. Note: R30837 only revalues open work orders -- closed work orders require manual correction. |

> **Aged variance note:** This pattern frequently produces historic variances dating back months or years, since the cost change and the missing GL entry may not be detected until the next reconciliation review. Assess materiality before posting a journal entry for small or very old amounts.

### 4.10 IB Cost Change -- Net Zero GL Entries
- Document type is **IB** with comment "Inventory Cost Change"
- F4111 has a single entry with a non-zero amount
- F0911 Inv Acct has **two entries that net to zero** -- one debit and one credit of the same amount, both to the same account
- F0911 Total = $0.00 despite individual entries existing
- RR Summary shows CardexAmount = non-zero, LedgerAmount = $0.00
- DMAAs section shows **"Net zero review - 4134, 4136"** in the Comment column

**What is happening:**

An IB cost change transaction in JD Edwards generates two journal entries -- a debit via AAI **4134** (Inv Cost Chg) to the inventory account, and a credit via AAI **4136** (Exp Cost Chg) to an expense or variance account. When both AAIs are configured to point to the **same object account**, the debit and credit cancel each other within the inventory account, producing a net GL impact of zero. The cardex still records the full amount, creating a variance.

This is distinct from a simple cardex-only entry -- both GL entries exist, but they are in the same account and net to zero. RapidReconciler flags this specifically in the DMAAs Comment column.

| Cause | How to Identify | Resolution |
|---|---|---|
| AAI 4134 and 4136 point to the same object account | DMAAs Comment shows "Net zero review - 4134, 4136"; F0911 shows equal debit and credit to same account; F0911 Total = $0 | (1) Correct AAI 4136 to point to a cost change expense or variance account. (2) Post a manual journal entry to create the missing expense account entry and relieve the inventory account for the current variance amount. (3) Review other IB transactions in the same company and GL class for the same issue. |

---

## Section 5: DMAAI Analysis

The DMAAs section at the bottom of the Transaction Detail report is critical for diagnosing account-level mismatches. Work through it in the following order:

**Step 1 -- Check the Model Table (4152)**

The first row is always the model table entry. Confirm:
- The account matches the account shown in the F0911 Inv Acct section
- If they don't match, the GL entry posted to a different account than the model table -- this is the account mismatch

**Step 2 -- Check for Comment Flags**

Any entry with a value in the Comment column requires investigation:

| Flag | Meaning | Action |
|---|---|---|
| **Missing entry / Missing model table entry** | The GL class code for this transaction has no entry in model DMAAI table 4152. All cardex rows with this GL class are excluded from the reconciliation and appear in the Unassigned section instead. | Add the GL class code to DMAAI table 4152 in JD Edwards with the correct account. After the next refresh, previously unassigned rows will move into F4111 Data and the full variance will be visible. Also check Integrity Report 3 (Excluded GL Classes) for a full list of missing codes. |
| **Mismatch - object** | The object account in this AAI differs from the model table | Correct the AAI object account to match the model table |
| **Mismatch - BU** | The business unit in this AAI differs from the model table | Correct the AAI business unit or confirm the difference is intentional |
| **Mismatch - sub** | The subsidiary in this AAI differs from the model table | Correct the AAI subsidiary |
| **Net Zero** | The debit and credit AAIs point to the same account | The transaction has no net GL impact -- investigate whether this is intentional |
| **Net zero review - 4134, 4136** | AAIs 4134 (Inv Cost Chg) and 4136 (Exp Cost Chg) both point to the same object account | IB cost change entries are netting to zero within the inventory account. Correct AAI 4136 to point to an expense or variance account. See Section 4.10. |
| **Net zero review - 4122, 4124** | AAIs 4122 (Inv Adj) and 4124 (Exp Adjust) both point to the same object account | IA inventory adjustment entries are netting to zero. Correct AAI 4124 to point to an expense or variance account different from AAI 4122. |

**Step 3 -- Identify Which AAI Caused the Mismatch**

Cross-reference the account shown in F0911 Inv Acct against the AAI entries in the DMAAs section. The AAI whose account matches the F0911 entry is the one that drove the GL posting. If that AAI's account differs from the model table account, that is the root cause.

**Step 4 -- Check for Flex Accounting**

Entries labeled "flex" in the Account column indicate Flexible Accounting is active for that AAI. The business unit or subsidiary was dynamically constructed from transaction fields. If the flex result is unexpected, review the flex accounting rules in P40296.

---

## Section 6: Step-by-Step Analysis Procedure

Use this procedure for every Transaction Detail report:

**Step 1 -- Read the Doc Header**

Note the document number, document type, order number, order type, and the total LedgerAmount (the variance to be explained). Note the Sub Type -- this gives the first indication of the variance category.

**Step 2 -- Check for the Unassigned Section**

Before reviewing anything else, scan the top of the report for an **Unassigned** section. If present:
- The F4111 Total is understated -- the true cardex amount is F4111 Total plus Unassigned Total
- The displayed variance is partial -- the full variance is larger than shown
- Go to the DMAAs section immediately and look for "Missing model table entry"
- See Section 4.1 for the resolution procedure

**Step 3 -- Check the RR Summary**

- Is CardexAmount zero? → GL-only entry. The variance is entirely on the GL side.
- Is LedgerAmount zero? → Cardex-only entry. Check for unposted batches.
- Are there multiple rows? → Mismatch on company, account, period, or document fields.
- Are both totals non-zero but unequal, with one or more rows showing LedgerAmount = $0.00 for a specific batch? → Partial cardex-only entry. A single line item within an otherwise-posted batch may be missing from the GL. See Section 4.3.
- Single row with matching amounts? → This should not appear as unreconciled. Investigate the tolerance setting.

**Step 4 -- Review the F4111 Data**

- Is the section empty? → No cardex records exist for this document. Confirm whether one should exist.
- Check the PC (posting code) field. "X" = memo transaction; should not be present for stock transactions.
- Note the GLDate vs. TransDate. A large gap may indicate a period mismatch.
- Are there two rows for the same document with one showing zero quantity and a "Standard Cost Change" or "Inventory Cost Change" comment? → See Sections 4.9 and 4.10.
- When the RR Summary shows a partial cardex-only pattern, scan the F4111 unit costs for outliers. A single line with a unit cost that is a significant multiple of all others is a strong indicator of where the GL gap originates.

**Step 5 -- Review the F0911 Inv Acct**

- What account did the GL entry post to?
- Does the account match the F4111 GLClass and the model table account?
- Note the batch number -- does it match the F4111 batch number?
- Check the Comment field for supplier name or other context.
- When the RR Summary shows a partial cardex-only pattern, compare the F0911 entries for each GL class and batch individually against the corresponding F4111 lines. A GL class total that is smaller than its F4111 counterpart points to the specific account and batch where the missing line item will be found. Before concluding the GL entry is absent, query F0911 across **all** accounts for the document and batch -- the entry may have posted to an unexpected account rather than being missing entirely.

**Step 6 -- Review the Receipts Section**

- Trace the full receipt and voucher history for the order.
- Note any "No Cx" batch entries (no cardex written).
- Compare tax amounts in Comments between OV (receipt) and PV (voucher match) rows.
- Check for landed cost rows and their CardexAmount vs. LedgerAmount.
- Note the NxtSts (next status) -- 999 means fully closed; no further JD Edwards processing is possible.

**Step 7 -- Review the DMAAs Section**

- Check for Comment flags (Missing entry, Mismatch, Net Zero).
- Identify which AAI produced the GL account shown in F0911.
- Compare to the model table account.
- If the DMAAs show no flags and the DMAAI configuration is clean, the variance is not a configuration issue -- focus the investigation on the GL posting history for the specific document and batch (see Step 5 note on partial cardex-only patterns).

**Step 8 -- Determine Root Cause and Corrective Action**

Based on the analysis above, classify the variance using Section 4 of this guide and identify the appropriate corrective action. All corrections are made in JD Edwards; the corrective action is always one of:
- Post a manual journal entry to recode the GL amount to the correct account
- Post the unposted batch
- Correct the DMAAI configuration and document the impact
- Add missing GL class to model table 4152
- Suspend the order in RapidReconciler if the variance is a known exception

**Step 9 -- Document in RapidReconciler**

Add a note to the transaction in RapidReconciler documenting the root cause, corrective action taken, and the date. Mark as "Worked" once resolved.

---

## Section 7: Sub Type Reference

RapidReconciler assigns a Sub Type to each unreconciled transaction on the Transactions page:

| Sub Type | Description |
|---|---|
| **Accounts** | Account number mismatch between F4111 and F0911 |
| **Periods** | Fiscal period mismatch between F4111 and F0911 |
| **Transfers** | ST/OT transfer order variance |
| **Intercompany** | Intercompany order variance |
| **Direct Ship** | Direct ship order variance |
| **Voucher Variance** | Variance on a voucher match transaction |
| **Vouchers** | GL-only voucher entry with no corresponding cardex |

---

## Section 8: Document Type Reference

Common document types appearing in the Transaction Detail report:

| Document Type | Description |
|---|---|
| **OV** | Purchase order receipt (creates inventory debit and RNV credit) |
| **PV** | Voucher match (clears RNV; creates A/P credit) |
| **PD** | A/P payment. Should not normally appear in the inventory account. |
| **IM** | Inventory issue (material issue to work order) |
| **IA** | Inventory adjustment |
| **IT** | Inventory transfer |
| **II** | Inventory issue (sales) |
| **IC** | Work order completion to finished goods inventory. The GL entry for IC transactions is created by Manufacturing Accounting (R31802A) and is typically assigned a **different document number** than the cardex -- this is normal. If F4111 contains two rows for the same IC document (one completion, one "Standard Cost Change" with zero quantity), and the GL only has the completion entry, a standard cost was updated after the completion posted without a corresponding GL revaluation. See Section 4.9. |
| **IH** | Manufacturing accounting journal entry |
| **IB** | Inventory balance adjustment. Covers zero balance adjustments, Re-Roll operations, and **inventory cost changes (P4105 manual cost revision)**. When the comment reads "Inventory Cost Change," check AAIs 4134 and 4136 for the net zero pattern described in Section 4.10. |
| **ST** | Transfer order sales (shipment) |
| **OT** | Transfer order purchase (receipt) |
| **SI** | Intercompany sales order |
| **SK** | Intercompany sales (inter-branch) |
| **OK** | Intercompany purchase order |
| **JS** | Sales order shipment (cost-of-sales entry). The same standard cost change after shipment pattern seen on IC transactions can occur on JS -- if a second F4111 row appears with zero quantity and comment "Standard Cost Change," the GL revaluation entry is missing. See Section 4.9. |
| **RI** | Sales invoice / shipment. Covers standard SO and direct ship S6 order types. If F0911 Comment reads "Non stock line in Inv acct," a non-stock line type (N, F, or similar) posted to the inventory account -- investigate line type definition. Lines showing GL date 2000-01-01 and document 0 were never processed through Sales Update. |
| **RM** | Sales return / credit memo. If the batch type is **IB** rather than I, the return was processed via a manual correction batch that posted to the inventory account without writing a cardex record -- this produces a GL-only variance. Investigate who created the IB batch and whether the inventory account coding is correct. |

---

## Section 9: Related Documentation

- [Inventory: Using the Application](../MDS/inventory-using-application.md)
- [DMAAI Reference Guide](../MDS/distribution-aais.md)
- [GL Class Code Management Guide](../MDS/gl-class-code-changes.md)
- [Item Ledger and Cardex Analysis Guide](../MDS/item-ledger-faq.md)
- [Zero Balance Adjustments Guide](../MDS/zero-balance-adjustments.md)
- [Cardex Integrity Variance Guide](../MDS/cardex_variance.md)
- [Purchase Order Reference Guide](../MDS/purchase_order_reference.md)
- [Stock Status and Trial Balance Reconciliation](../MDS/stock-status-trial-balance.md)

---

## Section 10: Using Claude for Automated Analysis

Claude can perform the full Section 6 analysis procedure automatically and return a single updated `.xlsx` file with the findings written directly into the workbook and all problem rows highlighted. This eliminates manual annotation and ensures consistent output across analysts.

### 10.1 First Request in a Session

On the first request, upload **both files** together:

1. This guide (`.md`)
2. The Transaction Detail report (`.xlsx`)

Then use the following prompt:

> *"Analyze this file using the guide as a template, then produce an updated copy of the Excel file with the analysis written to a new sheet called 'RR Analysis' and all problem rows highlighted."*

Claude will read the guide to understand the report structure and variance patterns, work through the Section 6 procedure against the Excel data, highlight the relevant rows on the Transaction Details sheet, and add the analysis as a new sheet in the same workbook. The returned file is a drop-in replacement for the original -- the Transaction Details sheet is unchanged except for the highlights.

### 10.2 Follow-On Requests in the Same Session

Once the guide has been uploaded in a session, Claude retains it in context for the remainder of the conversation. Subsequent Transaction Detail reports **do not require the guide to be uploaded again**. Simply upload the new `.xlsx` and use a shorter prompt:

> *"Analyze this file and return it with the analysis sheet and highlights."*

Start a new session when switching to a different guide version or when the conversation has been idle long enough that context may have been lost. When in doubt, include the guide again -- Claude will use it and ignore the duplication.

### 10.3 Output Specification

**File naming:** The returned file will use the original filename as the base with the document number and document type appended, e.g. `TransactionDetails_20260421-1103_1309532_IM.xlsx`. Claude will read the document number and type from the Doc Header row of the Transaction Details sheet before saving.

The returned workbook will contain two sheets:

**Sheet 1 — Transaction Details (original sheet, highlights added)**

| Highlight | Color | Rows |
|---|---|---|
| Root cause | Red | The specific F4111 line item(s) directly responsible for the variance |
| Related | Orange | Doc Header; the corresponding F0911 Inv Acct entries for the affected GL class and batch; the RR Summary rows showing the unmatched cardex and orphaned GL amounts |

**Sheet 2 — RR Analysis (new sheet)**

The analysis sheet will follow this structure:

| Section | Content |
|---|---|
| **Document** | Document number, type, order number, order type, company, period, variance amount |
| **Unassigned Check** | Whether an Unassigned section is present; true cardex total if understated |
| **RR Summary Findings** | CardexAmount, LedgerAmount, Variance; whether the pattern is full cardex-only, GL-only, partial, or account/period mismatch |
| **Root Cause** | Section 4 pattern classification; specific item, batch, GL class, and account involved |
| **Evidence** | Row numbers from the Transaction Details sheet that support the finding |
| **Recommended Action** | Corrective action from Section 4; journal entry details where applicable; any further investigation steps required before posting |

### 10.4 Notes and Limitations

- Claude analyzes the data as exported. If the source report was generated with filters applied or sections suppressed, the analysis reflects only what is present in the file.
- The highlight colors applied by Claude are standard fills. If the original file already uses cell fill colors for other purposes, advise Claude of the existing convention in the prompt so it can use different colors.
- For very large Transaction Detail reports spanning many documents or periods, include a note in the prompt identifying the specific document number to focus on if only one transaction is under investigation.
- Claude will note if a finding requires further investigation in JD Edwards (e.g., querying F0911 across all accounts for a specific batch) that cannot be completed from the Excel file alone. These items will appear as open questions in the Recommended Action section of the analysis sheet.