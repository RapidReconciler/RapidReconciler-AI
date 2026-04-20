# How to Reconcile PO Receipts (RNV) Using RapidReconciler

## A Complete Guide to the PO Receipts Module

---

## Table of Contents

- [Overview](#overview)
- [Before You Begin](#before-you-begin)
- [Section 1: The Orders Page](#section-1-the-orders-page)
- [Section 2: Orders Page Column Definitions](#section-2-orders-page-column-definitions)
- [Section 3: Line Details](#section-3-line-details)
- [Section 4: Things to Check on the Orders Page](#section-4-things-to-check-on-the-orders-page)
- [Section 5: The Reconciliation Page](#section-5-the-reconciliation-page)
- [Section 6: Line Analysis Page](#section-6-line-analysis-page)
- [Section 7: Step-by-Step Reconciliation Workflow](#section-7-step-by-step-reconciliation-workflow)
- [Section 8: Working Unreconciled Purchase Orders](#section-8-working-unreconciled-purchase-orders)
- [Section 9: Common Issues and How to Resolve Them](#section-9-common-issues-and-how-to-resolve-them)
- [Section 10: Related Documentation](#section-10-related-documentation)

---

## Overview

The RapidReconciler PO Receipts module reconciles the Received-Not-Vouchered (RNV) balance sheet liability account against open purchase order receipt activity. The RNV account (DMAAI 4320) holds the value of goods received from suppliers until the corresponding supplier invoice is matched and vouchered through Accounts Payable.

**What the module reconciles:**

| Side | Source | Description |
|---|---|---|
| **Open Receipts Balance** | F43121 Match Type 1 records | Receipts not yet vouchered |
| **GL Balance** | F0902 Account Balances | General ledger balance for the RNV account |
| **Out of Balance** | Difference between the two | What must be explained and resolved |

**Key difference from Inventory and In Transit modules:** The PO Receipts module has **no period selector**. Because the F43121 table overwrites records on reversal rather than creating new entries, As-Of reporting is not possible. The reconciliation is always performed as a **current balance-to-balance comparison** -- open receipts now vs. GL balance now.

### How RapidReconciler Helps

Without a dedicated tool, reconciling the RNV account requires manually extracting F43121 data, matching Match Type 1 and Match Type 2 records by order and line, identifying which receipts have no corresponding voucher, and comparing the net open balance to the GL -- across potentially thousands of purchase order lines. The absence of As-Of reporting from F43121 means there is no historical roll-forward to work from; only the current state of the table is available.

RapidReconciler imports F43121 and F0911 data automatically and performs the comparison on every nightly cycle, surfacing only the orders and documents that require attention:

| RapidReconciler Feature | How It Helps |
|---|---|
| **Orders Page** | Automatically calculates the open receipt position for every purchase order and displays only those with open amounts or variances between F43121 and the GL. Fully vouchered and reconciled orders are removed automatically. |
| **Reconciled / Suspended Filters** | Allow the user to focus on unreconciled orders, audit suspended orders, or validate the full open receipts listing -- without manual sorting or filtering of raw data. |
| **Calculation Section** | Separates the total out-of-balance amount into Open Receipts, Unreconciled, and Batches components, and provides a Suggested Entry amount that excludes outstanding variances -- making it straightforward to decide whether to close around unresolved items or resolve them first. |
| **PO Receipts Aging Chart** | Provides a visual breakdown of open receipts by period, immediately identifying whether the RNV balance is driven by recent legitimate activity or by aging receipts that have not been vouchered -- without running a separate aging report. |
| **Suspension Feature** | Removes orders cleared by manual voucher entry, PRLAND = 3 landed cost records, or data cutoff artifacts from the variance calculation -- isolating genuine unresolved items from known exceptions without requiring changes to JD Edwards data. |
| **Line Analysis Page** | Provides a side-by-side F43121 vs. GL comparison at the document level for any purchase order line, with the ability to exclude specific documents and add audit notes -- making it possible to trace the exact document causing a variance rather than reviewing the full order. |
| **Document Button** | Displays all transactions for a PO line with a Variance column identifying precisely which documents have discrepancies between F43121 and F0911, eliminating the need to cross-reference two separate data extracts. |
| **Unreconciled Link** | Navigates directly from the Reconciliation page to a pre-filtered Orders page showing only the orders requiring action -- removing the need to manually filter through the full order listing each period. |

> **Key principle:** RapidReconciler does not correct RNV issues -- all corrections are made in JD Edwards or through manual journal entries. RapidReconciler's role is to identify which purchase orders are unbalanced, at which line and document, and by how much -- so the correct corrective action can be applied efficiently rather than discovered at period end.

> **Before proceeding:** Ensure you are familiar with the RNV account, F43121 match types, and what creates and clears the RNV balance. See the [PO Receipts Key Concepts Guide](../MDS/po-receipts-key-concepts.md).

---

## Before You Begin

### Prerequisites

| Item | Requirement |
|---|---|
| **RapidReconciler access** | Login credentials provided by your administrator |
| **Module permissions** | Access to the PO Receipts module and applicable companies |
| **Suspension permission** | Must be granted by your administrator to suspend orders |
| **Exclusion permission** | Must be granted by your administrator to exclude documents |
| **JD Edwards access** | Required to investigate and correct issues identified in RapidReconciler |

### Key Rules Before Starting

- Both status lights must be **green** before making any adjustments to the general ledger.
- RapidReconciler data is refreshed **nightly**. Any JD Edwards report used for comparison should be run at approximately the same time as the RapidReconciler data was imported.
- The **Open Receipts balance** in RapidReconciler should match an Open Receipts report run directly from JD Edwards. Resolve any discrepancies between the two before making journal entries.
- The reconciliation objective is to ensure that **amounts on receipts and vouchers match between F43121 and the GL** -- not to match individual vouchers to receipts. A receipt without a voucher is a legitimate open receipt and correctly contributes to the RNV balance.

---

## Section 1: The Orders Page

### 1.1 Overview

The Orders page lists all purchase orders -- summarized to the order level -- where one or more of the following conditions exist:

- **Open Receipts** -- A receipt document (Match Type 1) has not yet been matched to a supplier invoice (Match Type 2)
- **Variances** -- A receipt or voucher in F43121 has an amount that does not match the corresponding GL entry in the RNV account

Orders that have been fully received, fully vouchered, and where everything reconciles are **automatically removed** from the list.

### 1.2 Filtering Results

Results can be filtered using the drop-downs at the top of the grid:

| Filter | All | Yes | No |
|---|---|---|---|
| **Reconciled** | Show all orders | Show only reconciled orders | Show only unreconciled orders |
| **Suspended** | Show all orders | Show only suspended orders | Show only non-suspended orders |

**Recommended filter combinations:**

| Reconciled | Suspended | What You See | Purpose |
|---|---|---|---|
| All | No | All orders contributing to the Open Receipts balance | Validate the total open receipts amount |
| No | No | All unreconciled, non-suspended orders | Identify orders requiring investigation |
| All | Yes | All suspended orders | Audit that suspensions are still warranted |

### 1.3 What Is a Suspension?

A suspension in PO Receipts is equivalent to flagging an order as "Ignore Me." Suspending an order removes its amounts from the out-of-balance and variance calculations.

**Common reasons to suspend:**

| Reason | Description |
|---|---|
| **Data cutoff artifact** | RapidReconciler was loaded by date and only the voucher was imported, not the original receipt. The order processed correctly -- it's a start-up issue. |
| **Manual voucher clearance** | A supplier invoice was entered using standard voucher entry (P0411) instead of being matched to the PO (P4314), leaving a paid receipt showing as open in F43121. Correcting in JD Edwards is preferred; suspension is the alternative. |
| **PRLAND = 3 landed cost** | An accrual-only landed cost that will never be vouchered. These records permanently contribute to the F43121 balance and should be suspended to prevent a false variance. |
| **Aged receipt under review** | An older open receipt that is being actively investigated but not yet resolved. Suspend temporarily with a note explaining the status. |

> **Important:** Performing a suspension in RapidReconciler does **not** change any data in JD Edwards. If the order should be corrected in JD Edwards, make that correction first.

If an order is suspended in error, it can be unsuspended. Suspension permission must be granted by your administrator.

---

## Section 2: Orders Page Column Definitions

| Column | Description |
|---|---|
| **Suspended** | Checkbox indicating the order has been suspended |
| **Note** | Icon indicating a text note has been entered. Click "Edit Note" to view. |
| **Company** | The company number associated with the RNV account |
| **Long Account** | The RNV account number being reconciled |
| **Supplier** | The address book number on the PO. May show two addresses if landed costs are applied. |
| **Name** | Name of the supplier on the row |
| **Order** | Purchase order number |
| **Type** | Purchase order type |
| **MostRecReceipt** | The date of the most recent receipt -- key field for aging analysis |
| **UnitsRec** | Total units received |
| **AmtRec** | Total value of units received |
| **UnitsVouch** | Total units vouchered |
| **AmtVouch** | Total value of units vouchered |
| **UnitsOpen** | Units received but not yet vouchered |
| **AmtOpen** | Value of units received but not yet vouchered. When Reconciled = All and Suspended = No, this column total matches the Open Receipts balance on the Reconciliation page. |
| **RecTotal** | Total value of all order transactions from F43121 |
| **GLTotal** | Total value of all order transactions posted to the GL RNV account |
| **Variance** | RecTotal minus GLTotal. Ideally zero. Non-zero values indicate an issue to resolve. |
| **ExclAmount** | The total exclusion amount for the order |
| **CurrCode** | Currency code associated with amounts |

> **Key distinction:** **AmtOpen** reflects legitimate open receipts (receipts not yet vouchered). **Variance** reflects a discrepancy between F43121 and the GL for the same document -- this is a reconciling issue, not a legitimate open receipt.

---

## Section 3: Line Details

### 3.1 Accessing Line Details

Click the **+** icon on the left of any order row to expand the line detail. This shows each individual PO line and whether it has an open receipt amount or a variance.

- Unreconciled lines are highlighted in **grey**
- Reconciled lines are displayed in **white**
- Details can be exported to Excel using the green down arrow

### 3.2 Line Analysis

Clicking the **Line Analysis** button within the expanded row navigates directly to the Line Analysis page with filter data pre-populated for that line. This is the fastest way to investigate a specific unreconciled line.

---

## Section 4: Things to Check on the Orders Page

Before proceeding to the Reconciliation page, validate the Orders page to ensure the Open Receipts balance is accurate. Work through the following checks:

| Check | How | What to Look For |
|---|---|---|
| **Identify aged open receipts** | Sort by **MostRecReceipt** ascending | Oldest receipts at top -- confirm whether they are still active or candidates for suspension or JD Edwards correction |
| **Audit suspended orders** | Set Reconciled = All; Suspended = Yes | Confirm every suspended order still genuinely warrants suspension -- review the note for each |
| **Identify orders requiring review** | Set Reconciled = No; Suspended = No | These orders have variances that must be resolved |
| **Review unreconciled lines** | Expand any order by clicking **+** | Grey lines indicate unreconciled lines -- click Line Analysis for detail |
| **Validate the open receipts total** | Set Reconciled = All; Suspended = No | The **AmtOpen** total must be validated before comparing to the GL balance |

> The open receipts listing **must be validated** before proceeding with the reconciliation. The quality of the reconciliation depends on the accuracy of the Orders page. Any order on the list in error -- either correct in JD Edwards or suspend in RapidReconciler.

---

## Section 5: The Reconciliation Page

### 5.1 Overview

The Reconciliation page is the default page displayed on login. This is where the open receipts balance is compared to the GL balance and all variance sources are identified.

### 5.2 Status Indicators

Both indicators must be **green** before making any adjustments to the general ledger.

| Indicator | Green Means | Red Means | Action if Red |
|---|---|---|---|
| **PO Receipt Validation** | Carry-forward from prior period is accurate | Prior period issue exists | Hover for details; resolve before proceeding |
| **System Status** | JD Edwards import completed successfully | Import error occurred | Hover for details; contact your administrator |

### 5.3 No Period Selector

Unlike the Inventory and In Transit modules, PO Receipts has **no period selector**. This is because F43121 overwrites records on reversal rather than maintaining a transaction history -- As-Of reporting is not possible. The module always shows the current balance position.

### 5.4 Account Filters

- Operate as a hierarchy from left to right (Company → Business Unit → Object → Subsidiary)
- Removing a company automatically removes associated business units, objects, and subsidiaries
- Search rows at the top of each column filter within that column
- Filter selections persist across pages within the PO Receipts module

### 5.5 Calculation Section

| Field | Description | Source |
|---|---|---|
| **GL Balance** | General ledger balance for the RNV account | F0902 -- matches the trial balance exactly |
| **Open Receipts** | Calculated from F43121 Match Type 1 records | F43121 |
| **Out of Balance** | Difference between GL Balance and Open Receipts | Zero = fully reconciled |
| **Unreconciled** | Total variance between F43121 and GL for unreconciled orders | Orders page Variance column total |
| **Batches** | GL batches awaiting posting | Unposted F0911 entries |
| **Total Variance** | Sum of Unreconciled and Batches amounts | -- |
| **Suggested Entry** | Out of Balance minus Unreconciled amount | The journal entry amount if unreconciled orders are excluded from the current close |
| **Manual Entries** | Manual adjustments made to the selected accounts | Informational |

**Understanding Suggested Entry vs. Out of Balance:**

| Use | Amount | When to Use |
|---|---|---|
| **Out of Balance** | Includes unreconciled orders | Use when all unreconciled variances have been resolved before closing |
| **Suggested Entry** | Excludes unreconciled orders | Use when unreconciled orders will be carried forward for resolution next period |

> **Best Practice:** Resolve all unreconciled orders before closing the period. Using the Suggested Entry amount to close around outstanding variances defers the problem and accumulates carry-forward balances over time.

### 5.6 PO Receipts Aging Chart

The aging chart provides a visual breakdown of open receipts by period. Use this to identify whether open receipts are recent (normal) or aging (requires investigation). A large proportion of aged open receipts is a signal that the voucher match process is not keeping pace with receipts.

---

## Section 6: Line Analysis Page

### 6.1 Accessing the Line Analysis Page

> **Always access the Line Analysis page from the Orders page** by clicking the Line Analysis button on an expanded order row. This pre-populates the filter with the correct order and line data. Clicking the Line Analysis link in the Main Navigation pane does not populate filter data and may cause confusion.

### 6.2 Edit Note Button

The Edit Note button is used to:

- Add a note for future reference or audit documentation
- Exclude a specific document (receipt or voucher) from variance calculations

**Procedure:**

1. Click the grid row(s) to be edited
2. Type in the text box to add a note
3. Check the **Excluded** box to remove amounts from the variance calculation after recalculation
4. Click **Save**

> If an exclusion is made in error, unchecking the box will reinstate the document. Exclusion permission must be granted by your administrator.

**When to use document exclusion:** Document exclusion at the line level is different from order suspension. Use document exclusion when a specific receipt or voucher document has a known discrepancy that is being tracked -- for example, a receipt that was partially reversed out of sequence, creating an entry in F43121 that no longer matches the GL.

### 6.3 Document Button

The Document button displays a pop-up listing all documents associated with the PO line, combining data from F43121 and F0911. This provides a **side-by-side comparison** of the receipts table and GL amounts for each document.

| Column | Description |
|---|---|
| **Cutoff Date** | The earliest date considered during import. Discrepancies caused by the cutoff date are less likely the further the capture date is from the cutoff. |
| **Capture Date** | The date the data was imported into RapidReconciler |
| **Variance** | The difference between the F43121 amount and the GL amount by document -- the key field to review |

### 6.4 Filter Drop-Downs

| Filter | Options | Use |
|---|---|---|
| **Exc (Excluded Docs)** | All / Yes / No | Show all, only excluded, or only non-excluded documents |
| **Rec (Reconciled Docs)** | All / Yes / No | Show all, only reconciled, or only unreconciled documents |
| **Doc** | Individual document selection | Filter to a specific document number |

> **Helpful Trick:** Change the line number to **0** and click Query to display data for **all lines** on the PO. This is extremely useful when diagnosing variances that span multiple lines. The Document button will then show all documents for the entire order.

### 6.5 Recalc and Export

- **Recalc** -- Recalculates variances after documents have been excluded. A gear icon in the top right corner indicates the recalculation is in progress. Results are available within a few minutes.
- **Export** -- Exports grid data to Excel.

### 6.6 Documents Grid

Lists all transactions for the PO line(s) being filtered, split by data source:

- **F43121 rows** -- Receipt and voucher data from the receipts table
- **F0911 rows** -- GL detail entries for the same transactions
- Reconciled rows are displayed in **light color**; unreconciled rows are displayed in **grey**

For a side-by-side comparison, click the **Document** button rather than reading the grid rows individually.

---

## Section 7: Step-by-Step Reconciliation Workflow

### 7.1 Frequency Guidance

| Activity | Recommended Frequency |
|---|---|
| Review Orders page for aged receipts | **Weekly** |
| Audit suspended orders | **Monthly** |
| Full reconciliation review | **Weekly** |
| Period-end closing activities | **Period-end close** |

### 7.2 Step 1 -- Log In and Select the Data Set

1. Log in to RapidReconciler at [https://rapidreconciler.getgsi.com](https://rapidreconciler.getgsi.com)
2. Navigate to the **PO Receipts** module
3. Confirm both status lights are **green** -- do not proceed if either is red
4. Apply the appropriate company and account filters

### 7.3 Step 2 -- Validate the Orders Page

1. Set filters to **Reconciled = All; Suspended = No**
2. Sort by **MostRecReceipt** ascending to identify the oldest open receipts
3. Review all orders for accuracy:
   - Orders that are genuinely in transit -- leave open
   - Orders cleared by manual voucher -- correct in JD Edwards or suspend in RapidReconciler
   - PRLAND = 3 landed cost records -- suspend in RapidReconciler
   - Orders at status 999 with no further JD Edwards activity possible -- suspend
4. Set filters to **Reconciled = All; Suspended = Yes** -- confirm all suspended orders still warrant suspension and have a note explaining why
5. Confirm the **AmtOpen** total is accurate before proceeding

### 7.4 Step 3 -- Review the Reconciliation Page

1. Navigate to the **Reconciliation page**
2. If Out of Balance = $0, skip to Step 6
3. Review the Calculation section:

| Field | Required Before Close | Action |
|---|---|---|
| **GL Balance** | Informational | Confirm matches the trial balance |
| **Open Receipts** | Validate first | Confirm matches a JD Edwards Open Receipts report |
| **Out of Balance** | Must be resolved | Investigate each contributing source |
| **Unreconciled** | Resolve or carry forward | Click the link to navigate to unreconciled orders |
| **Batches** | **Must be zero** | Work with finance to post outstanding GL batches |
| **Suggested Entry** | Use if carrying variances forward | Journal entry amount excluding unreconciled orders |

### 7.5 Step 4 -- Work Unreconciled Orders

1. Click the **Unreconciled** link on the Reconciliation page (or set Orders page filters to Reconciled = No; Suspended = No)
2. Expand each unreconciled order using the **+** icon
3. Click **Line Analysis** on each grey (unreconciled) line
4. On the Line Analysis page:
   - Change Rec filter to **All** and Line to **0**, then click **Query** to see all transactions for the order
   - Click the **Document** button to view the F43121 vs. GL side-by-side comparison
   - Review the **Variance** column to identify which specific documents are out of balance
5. Determine the root cause and take corrective action (see Section 9)
6. If the document cannot be corrected, use **Edit Note** to exclude it and add an audit note
7. Click **Recalc** to update the variance calculations after any exclusions

### 7.6 Step 5 -- Make the Adjusting Journal Entry

Once all unreconciled orders have been addressed:

- If all variances are resolved: use the **Out of Balance** amount as the journal entry
- If carrying forward unresolved variances: use the **Suggested Entry** amount
- Post the journal entry in JD Edwards to the RNV account with the appropriate offset account

**Common offset accounts for RNV journal entries:**

| Situation | Offset Account |
|---|---|
| Unvouchered receipt to be written off | Expense / Cost of Goods Sold |
| Price variance between receipt and invoice | Purchase Price Variance (AAI 4330) |
| Goods consumed before voucher match | Cost of Sales Variance (AAI 4332) |
| Correction of a processing error | Appropriate correcting account per the error |

### 7.7 Step 6 -- Produce and Save the Audit Report

After the reconciliation is complete and the journal entry has been posted:

1. Navigate to the Reconciliation page
2. Confirm the Out of Balance amount is zero after the next nightly refresh
3. Produce and save documentation of the reconciliation for audit purposes

> There is no dedicated Audit Report button in the PO Receipts module as there is in Inventory and In Transit. Save a copy of the Reconciliation page and Orders page (exported to Excel) as the period-end documentation.

---

## Section 8: Working Unreconciled Purchase Orders

### 8.1 Display Unreconciled Orders

Click the **Unreconciled** link on the Reconciliation page. This opens the Orders page with filters preset to Reconciled = No; Suspended = No -- showing only orders with variances.

### 8.2 Select and Expand the Order

Click the **+** icon on the left of the order row to expand it. Identify which lines are displayed in grey (unreconciled). Click **Line Analysis** on the line to be investigated.

### 8.3 Perform Order and Line Analysis

On the Line Analysis page:

1. Change the **Rec filter to ALL** and the **Line filter to 0**, then click **Query** to see all transactions for the full order
2. Click the **Document** button for a side-by-side F43121 vs. GL comparison
3. Review the **Variance** column -- identify which document(s) show a non-zero variance
4. For each document with a variance, determine whether the discrepancy is in F43121, the GL, or both

### 8.4 Corrective Actions

| Variance Type | Cause | Corrective Action |
|---|---|---|
| F43121 amount differs from GL | Receipt cost and GL entry do not match | Investigate the receipt transaction; post a manual journal entry to the GL if needed |
| GL entry exists but no F43121 record | Manual GL entry posted to RNV account | Exclude the GL document in Line Analysis; document the manual entry |
| F43121 record exists but no GL entry | Unposted batch | Post the outstanding batch in JD Edwards |
| Reversal out of sequence | Receipt or voucher reversed after period close | Investigate the reversal; post a correcting journal entry |
| Cutoff date artifact | Data imported from a date after the original receipt | Exclude the document if the original receipt predates the import cutoff |

---

## Section 9: Common Issues and How to Resolve Them

| Issue | Cause | Resolution |
|---|---|---|
| **Open Receipts balance does not match JD Edwards** | Timing difference -- RapidReconciler imports nightly; JD Edwards report run at a different time | Run both reports at approximately the same time; confirm timing of last import |
| **Suspended order reappears after unsuspension** | New activity posted against the order | Review the new activity; re-suspend if appropriate or process the voucher match |
| **Aged open receipts accumulating** | Supplier invoices not being processed promptly; or receipts processed without corresponding voucher matches | Investigate each aged receipt; contact the supplier for the invoice; consider writing off if the receipt is no longer valid |
| **Large number of unreconciled orders** | DMAAI misconfiguration causing receipts to post to a different account than expected | Review DMAAI 4320 configuration. See [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md) |
| **Variance on a specific document** | Reversed receipt or voucher processed out of sequence; rounding difference; tax entry mismatch | Use Line Analysis Document view to compare F43121 vs. GL; exclude the document if the discrepancy is known and justified |
| **PRLAND = 3 records causing permanent variance** | Accrual-only landed costs that will never be vouchered | Suspend the order in RapidReconciler |
| **Tax entries creating unexpected variances** | Tax explanation codes S, U, V, C, or B generate different AAI entries at receipt vs. voucher match | Review tax configuration. See [Purchase Order Reference Guide](../MDS/purchase_order_reference.md) |
| **Carry-forward balance growing each period** | Unresolved variances being deferred using Suggested Entry instead of being resolved | Prioritize working unreconciled orders before close; avoid using Suggested Entry as a routine practice |

---

## Section 10: Related Documentation

| Document | Relevance |
|---|---|
| [PO Receipts Key Concepts](../MDS/po-receipts-key-concepts.md) | F43121 table, match types, PRLAND field, accounting flow, and reconciliation challenges |
| [Reconciling RNV in RapidReconciler](../MDS/reconciling-rnv.md) | Summary reconciliation, drill-down, suspension, and match type reference |
| [Purchase Order Reference Guide](../MDS/purchase_order_reference.md) | Tax treatment by code, landed cost setup and journal entries, receipts routing accounting |
| [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md) | Complete AAI configuration for all purchasing transactions |
| [Stock Status and Trial Balance Reconciliation](../MDS/stock-status-trial-balance.md) | Root causes of GL balance discrepancies |
| [How to Reconcile Inventory](../MDS/inventory-using-application.md) | Parallel workflow for perpetual inventory reconciliation |
| [How to Reconcile In Transit](../MDS/in-transit-using-application.md) | Parallel workflow for goods in transit reconciliation |
| [Getting Started with RapidReconciler](../MDS/getting-started-with-rapidreconciler.md) | Login, navigation, and application overview |