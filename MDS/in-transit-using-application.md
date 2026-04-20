# How to Reconcile In Transit Using RapidReconciler

## A Complete Guide to the In Transit Module

---

## Table of Contents

- [Overview](#overview)
- [Before You Begin](#before-you-begin)
- [Section 1: The Orders Page -- Managing Open Transfer Orders](#section-1-the-orders-page----managing-open-transfer-orders)
- [Section 2: The Reconciliation Page](#section-2-the-reconciliation-page)
- [Section 3: Valuation Section](#section-3-valuation-section)
- [Section 4: Variance Calculation -- Understanding and Resolving Each Source](#section-4-variance-calculation----understanding-and-resolving-each-source)
- [Section 5: Supporting Widgets and Reports](#section-5-supporting-widgets-and-reports)
- [Section 6: In Transit Transactions Page](#section-6-in-transit-transactions-page)
- [Section 7: In Transit As-Of Page](#section-7-in-transit-as-of-page)
- [Section 8: Integrity Reports](#section-8-integrity-reports)
- [Section 9: Step-by-Step Reconciliation Workflow](#section-9-step-by-step-reconciliation-workflow)
- [Section 10: Related Documentation](#section-10-related-documentation)

---

## Overview

The RapidReconciler In Transit module reconciles the goods-in-transit clearing account against open ST/OT transfer order activity. When goods are shipped from Branch A to Branch B, the value of those goods is held in a clearing account (typically via DMAAI 4220 or 4245) until they are received at the destination branch. If the shipment and receipt do not match in both quantity and amount, a balance remains in the clearing account that must be identified, investigated, and resolved.
Although the document references order types ST/OT, it will detect different transfer types based on a flag in the F4211 table.

**What the In Transit module reconciles:**

| Side | Source | Description |
|---|---|---|
| **In Transit Balance** | ST/OT order pairs (Shipments − Receipts) | Open transfer order activity from sales and purchase orders |
| **GL Balance** | F0902 Account Balances | General ledger period-end balance for the In Transit clearing account |
| **Out of Balance** | Difference between the two | What must be explained and resolved |

### How RapidReconciler Helps

Without a dedicated tool, reconciling the In Transit clearing account requires manually comparing shipment and receipt quantities and amounts for every open transfer order, then matching those figures to the GL balance -- a process that becomes increasingly complex as transfer volume grows, cost changes occur, and unresolved order pairs accumulate.

RapidReconciler automates this comparison and surfaces the specific orders, amounts, and variance types that require attention:

| RapidReconciler Feature | How It Helps |
|---|---|
| **Orders Page** | Automatically calculates the in-transit position (Shipments − Receipts) for every order pair and displays only those with an open quantity or amount. Orders that reconcile exactly are removed automatically -- no manual filtering required. |
| **Exclusion Process** | When both the ST and OT orders are fully closed (status 999) but a residual balance remains, the Exclusion feature isolates those amounts from the reconciliation and surfaces the exact journal entry value needed to clear the In Transit GL account. |
| **Exclusion Variance Columns (ExclVarQty / ExclVarAmt)** | Monitors previously excluded orders for new activity. If a receipt is processed against an excluded open PO, these columns surface the discrepancy immediately so the exclusion can be recalculated rather than omitting the new transactions from the reconciliation. |
| **Variance Calculation Section** | Breaks down the full out-of-balance amount into its specific sources -- Carry Forward, GL Batches, End of Day, Transactions, and Exclusions -- so each can be addressed with the correct corrective action rather than treating the total as a single unexplained variance. |
| **As-Of Page** | Reconstructs the in-transit position as of any historical period end date, calculated backwards from the current position. Provides full transaction-level detail with drill-down and export capability for period-end documentation and audit support. |
| **Integrity Report 2 -- Missing GL Classes** | Identifies transfer order pairs where the GL class code is missing from the transit DMAAI table, causing those amounts to be excluded from the reconciliation silently. |
| **Integrity Report 4 -- Transfer Cost Variances** | Lists orders where the ST sales cost or price does not match the OT purchase order cost -- the most common cause of In Transit balances that do not clear after receipt. Surfaces these before they accumulate into large unresolved period-end variances. |

> **Key principle:** RapidReconciler does not correct In Transit issues -- all corrections are made in JD Edwards or through manual journal entries. RapidReconciler's role is to identify exactly which orders are unbalanced, by how much, and why -- so the right corrective action can be taken efficiently rather than discovered at period end.

> **Before proceeding:** Ensure you understand your organization's transfer order types and whether goods are transferred at cost or with a markup. This determines the DMAAI configuration in use. See the [In Transit Key Concepts Guide](../MDS/in-transit-key-concepts.md) for background.

---

## Before You Begin

### Prerequisites

| Item | Requirement |
|---|---|
| **RapidReconciler access** | Login credentials provided by your administrator |
| **Permissions** | Access to the In Transit module and applicable companies |
| **JD Edwards access** | Required to investigate and correct issues identified in RapidReconciler |
| **Background knowledge** | Familiarity with ST/OT order types, DMAAI configuration, and the In Transit clearing account |

### Key Rules Before Starting

- Both status lights must be **green** before making any adjustments to the general ledger.
- RapidReconciler data is refreshed **nightly** -- transactions entered in JD Edwards after the most recent import will not appear until the following night's refresh.
- RapidReconciler does **not** modify JD Edwards data. All corrections are made in JD Edwards; RapidReconciler reflects those corrections after the next nightly refresh.
- The Orders page always shows the **current** in-transit position regardless of the period selected. Changing the period on this page does not change what is displayed.

---

## Section 1: The Orders Page -- Managing Open Transfer Orders

### 1.1 What Is Displayed

Each row on the Orders page lists a transfer order pair that has either an open quantity or an open amount. An **order pair** is a summarized view of a transfer at the ST sales order, OT purchase order, and item number level -- lines and lots are collapsed into a single row.

The Orders page shows the **current** in-transit position. Only orders with a remaining balance appear here. Orders that have shipped and been fully received at matching quantities and amounts are automatically removed.

> **The purpose of the Orders page is to list only what is truly in transit.** All other entries -- orders where both sides are fully closed but a residual balance exists -- must be excluded to obtain the correct In Transit balance.

### 1.2 Order Lifecycle on the Orders Page

The following table shows how an order pair progresses through the Orders page, using 100 EA of item 123 transferred from Branch A to Branch B at $1 each:

| Step | Scenario | Orders Page | Action Required |
|---|---|---|---|
| Order Entry | -- | No entry | -- |
| Items Picked | All 100 | No entry | -- |
| Items Ship Confirmed | All 100 | Order pair shows 100 EA, $100 in transit | N/A -- goods legitimately in transit |
| Items Received -- exact match | 100 EA for $1 | Entry automatically disappears | None |
| Items Received -- amount mismatch | 100 EA, amount ≠ $1 | Entry displays with open amount | Investigate; exclude if unresolvable |
| Items Received -- quantity mismatch | Fewer than 100 received | Remaining balance stays in transit | Leave open if more receipts expected; exclude if no further activity will occur |

### 1.3 Order Pair Columns

| Column | Description |
|---|---|
| **From / To** | Shipping and receiving branch plants |
| **Item** | Item number |
| **Ship Qty** | Total quantity shipped on the ST order |
| **Rec Qty** | Total quantity received on the OT order |
| **TranQty** | In-transit quantity (Ship Qty − Rec Qty) |
| **Ship Amt** | Total amount shipped |
| **Rec Amt** | Total amount received |
| **TranAmt** | In-transit amount (Ship Amt − Rec Amt) |
| **Ship Sts** | Current status of the ST sales order |
| **Rec Sts** | Current status of the OT purchase order |
| **ExclQty** | Quantity previously excluded on this order pair |
| **ExclAmt** | Amount previously excluded on this order pair |
| **ExclVarQty** | New quantity activity on a previously excluded order -- must be reviewed |
| **ExclVarAmt** | New dollar activity on a previously excluded order -- must be reviewed |

> **Monitor ExclVarQty and ExclVarAmt every period.** Any non-zero value means transactions have occurred on a previously excluded order. Unexclude and re-exclude the order pair to recalculate the exclusion amount. See the [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md).

### 1.4 What Is an Exclusion?

An Exclusion closes an order pair in RapidReconciler so it no longer counts toward the In Transit balance. This is used when a quantity or amount mismatch exists between the shipment and receipt that cannot be resolved through JD Edwards -- typically because both the ST and OT orders are at status **999** and no further transactions are possible.

> **Important:** Performing an exclusion in RapidReconciler does **not** change any data in JD Edwards. The excluded amount still exists in the GL clearing account and requires an **offsetting journal entry in JD Edwards** to clear.

**When to exclude vs. when to leave open:**

| Situation | Action |
|---|---|
| Both ST and OT at status 999 with remaining balance | **Exclude** -- no further JD Edwards processing is possible |
| OT not yet fully received; more receipts expected | **Leave open** -- the order is legitimately in transit |
| Partial receipt processed; remaining quantity unclear | **Investigate** before excluding -- confirm with the warehouse |
| Cost variance only; quantity is zero | **Exclude** and post a journal entry for the dollar variance |

For the complete exclusion and journal entry procedure, see the [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md).

---

## Section 2: The Reconciliation Page

### 2.1 Overview

The Reconciliation page is the default page displayed on login. This is where all variance sources are summarized and where the majority of reconciliation work is performed.

### 2.2 Status Indicators

Both indicators must be **green** before making any adjustments to the general ledger.

| Indicator | Green Means | Red Means | Action if Red |
|---|---|---|---|
| **In Transit Validation** | The carry-forward from the prior period is accurate | A prior period issue exists | Hover for details; resolve the prior period before proceeding |
| **System Status** | The JD Edwards import completed successfully | The import encountered an error | Hover for details; contact your administrator |

> If the System Status light is **flashing yellow**, the import is still in progress. Wait for it to complete before reviewing data.

### 2.3 Period Selector

- Located in the top right corner.
- Periods are automatically added as new transfer order activity occurs in JD Edwards.
- Selection persists as you navigate across pages within the In Transit module.
- If more than 14 periods of data exist, contact your administrator to request a purge.

### 2.4 Account Filters

- Operate as a hierarchy from left to right (Company → Business Unit → Object → Subsidiary).
- Removing a company automatically removes its associated business units, objects, and subsidiaries.
- Use the search row at the top of each column to filter within that column.
- Filter selections persist across pages within the In Transit module.

---

## Section 3: Valuation Section

The Valuation section confirms whether the In Transit balance matches the GL balance for the selected period and filters.

| Field | Description | Source |
|---|---|---|
| **GL Balance** | General ledger balance for the In Transit account | F0902 -- matches the trial balance |
| **In Transit Balance** | Calculated from transfer order pairs as (Shipments − Receipts) | ST/OT order activity |
| **Out of Balance** | Difference between GL Balance and In Transit Balance | Zero = fully reconciled |

> **If the Out of Balance amount is zero**, In Transit reconciles to the GL for the selected period. No further action is required.

> **If the Out of Balance amount is non-zero**, proceed to Section 4 to identify and resolve each variance source.

---

## Section 4: Variance Calculation -- Understanding and Resolving Each Source

The Variance Calculation section lists every source of variance. The sum of all lines equals the Out of Balance amount. Each non-zero line requires attention.

### 4.1 Carry Forward

**What it is:** The out-of-balance amount carried forward from the prior period.

**How to resolve:**
- Return to the prior period and investigate the remaining variance.
- If the prior period is closed, include the carry-forward amount in the current period's manual journal entry.
- Document the amount and reason for the carry forward.

### 4.2 GL Batches

**What it is:** Entries in F0911 where the posted code is not "P" -- the batch has not been posted to the GL.

**How to resolve:**
- Work with the finance department to post the outstanding batches.
- A **bell icon** on this row indicates unposted batches more than 2 days old -- prioritize these.
- If a batch header cannot be located, run the JD Edwards "Missing Batch Header" report.

> GL Batches must be zero before performing closing activities.

### 4.3 End of Day

**What it is:** Transfer sales orders that have been ship confirmed but not yet processed through Sales Update (R42800/P42800).

**How to resolve:**
- A **bell icon** indicates open orders more than 2 days old -- investigate why Sales Update has not processed them.
- Confirm that the Sales Update version configured for transfer orders is scheduled and completing successfully.
- The In Transit Sales Update version must have the A/R interface turned off.

> End of Day must be zero before performing closing activities. The Sales Update program processes ST orders to the GL; until this runs, the shipment has no batch number or GL date.

### 4.4 Transactions

**What it is:** Documents where the item ledger (F4111) does not match the GL (F0911) based on the matching criteria. Common causes include DMAAI mismatches, fiscal period differences, and account number discrepancies.

**How to resolve:**
- Navigate to the Transactions page (Section 6) to investigate each item.
- The corrective action is always an **offsetting journal entry in JD Edwards**.
- Enter a note in RapidReconciler for each resolved transaction for audit documentation.

### 4.5 Exclusions

**What it is:** The "leftover" balance from order pairs that have been excluded from the In Transit calculation because both orders are at status 999 with a remaining mismatch.

**How to resolve:**
- The excluded amount identifies the exact value of the **offsetting journal entry** needed to clear the In Transit GL account.
- Post the journal entry in JD Edwards -- debit or credit the In Transit account and offset to an appropriate expense or variance account per your organization's policy.
- Document the order numbers, amounts, and reason for each exclusion.

> For journal entry guidance and the complete exclusion procedure, see the [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md).

### 4.6 Manual Journal Entries

**What it is:** Manual entries posted directly to the In Transit GL account. This line confirms they are visible in the reconciliation.

**Note:** This is informational -- it shows that manual entries have been accounted for in the overall variance calculation.

### 4.7 Variance Calculation Example

| Variance Source | Amount | Status |
|---|---|---|
| Carry Forward | ($750.10) | Investigate prior period |
| GL Batches | $0.00 | ✓ Clear |
| End of Day | $0.00 | ✓ Clear |
| Transactions | $0.00 | ✓ Clear |
| Exclusions | ($23.31) | Post journal entry |
| Manual Journal Entries | $0.00 | ✓ Clear |
| **Unreconciled Variance** | **($773.41)** | Total requiring resolution |

---

## Section 5: Supporting Widgets and Reports

### 5.1 Drill Down Widget

Provides a visual breakdown of where the largest variances exist -- most useful in multi-company environments.

- Default starting point is the currency code; click through to drill down to company, business unit, and account level.
- Hovering over a section displays the item name and variance amount.
- Filter selections update automatically as you drill down.
- No chart is displayed if there is no variance.

### 5.2 Offset Account Widget

The star icon appears when hovering over the **End of Day** row in the Variance Calculation section. Clicking it opens a pop-up with the company, period, In Transit account, and suggested offset account.

> **Important:** The In Transit module provides an offset for **End of Day only** -- there is no Transactions offset available in this module.

**After exporting to Excel:** Replace any "Tolerance Adjust" and "TBD" placeholders with the correct GL account numbers, then copy the two rightmost columns and paste into JD Edwards. This tool is designed for use during the close -- mid-period entries are not reflected.

### 5.3 Out of Balance History Graph

Displays the out-of-balance trend over the most recent 14 periods.

- Hovering over a period displays the date and variance total.
- Clicking a data point changes the period filter to that period.
- A perfectly reconciled system shows all periods at $0.

### 5.4 Journal Entry Button

Produces an Excel report of the GL and In Transit balances for the selected accounts and period. Used for account-level journal entries when detailed transaction review is not required.

### 5.5 Audit Report

Documents the complete reconciliation results for the period. **Produce and save this report at the end of every period** -- detail data may be removed during a purge.

| Section | Contents |
|---|---|
| **Accounts Summary** | Valuation and variance calculation summary for each account |
| **Unposted GL Batches** | Details for any remaining unposted batches |
| **End of Day** | Remaining sales orders awaiting Sales Update processing |
| **Manual Journal Entries** | All manual entries made to the account |
| **Variances** | Transaction variances for the period, including user-entered notes |
| **Perpetual Details** | Item balances and values at the end of the selected period |

Output format: Excel or PDF.

---

## Section 6: In Transit Transactions Page

### 6.1 Overview

The Transactions page lists documents where the item ledger (F4111) does not match the GL (F0911). Only reconciling items are displayed -- internally matched transactions do not appear.

### 6.2 Rounding and Tolerance

Transactions differing by less than 1 monetary unit are not displayed by default. These sub-tolerance amounts are still counted in the Transactions line of the Variance Calculation section, so the two totals may differ slightly. The tolerance setting can be changed by the administrator.

### 6.3 Notes and Worked Transactions

Manual notes can be added to any transaction to document corrective actions. These notes appear on the period-end audit report.

**Best practices for notes:**
- Include your name and date in the note text
- Notes can be deleted after the fact if necessary
- Additional notes can be added to the same transaction at any time

Marking a transaction as **"Worked"** allows it to be filtered off the grid. This does not change variance totals or permanently remove transactions -- it is a view filter only.

> The corrective action for all transactions on this page is an **offsetting journal entry in JD Edwards** plus a note in RapidReconciler.

### 6.4 Grid Column Definitions

| Column | Description |
|---|---|
| **Worked** | Checked = cleared via the Edit Notes process |
| **Note** | Hover to view any note that has been added |
| **Company Number** | The company number associated with the transaction |
| **Long Account** | The account number associated with the transaction |
| **Sort Key** | The concatenated sales order / purchase order number |
| **Document Type** | The JD Edwards document type |
| **Document Number** | The JD Edwards document number |
| **Order Type / Number** | The JD Edwards order type and number |
| **Transit Amount** | The total from the Orders page for applicable activity |
| **Ledger Amount** | The total from F0911 |
| **Variance** | Ledger Amount minus Transit Amount |
| **Comment** | Helpful information provided by RapidReconciler |
| **Currency** | The currency code of the transaction |
| **Batch Number** | The JD Edwards batch number |
| **Period Ends** | The period ending date |
| **Transaction Date** | The creation date from the cardex, or GL date for GL-only transactions |
| **Rel Type / Rel Order** | Related order type and number, if applicable |

### 6.5 Transaction Detail Report

Click the **+** icon at the left of any row to access the transaction detail. The report is organized into six sections:

| Section | Description |
|---|---|
| **Section 1 -- Unassigned Account** | Cardex transactions with a GL class code not in the model DMAAI table |
| **Section 2 -- F4111 Cardex** | All F4111 rows for the selected company, document type, and document number |
| **Section 3 -- F0911 GL** | All F0911 rows for the selected company, document type, and document number |
| **Section 4 -- RapidReconciler** | How RapidReconciler matches the data. One row = match; multiple rows = mismatch |
| **Section 5 -- Order Data** | For PO receipts and sales shipments, all lines for the associated order |
| **Section 6 -- DMAAs** | All DMAAI entries for each GL class code. First row is from the model table. |

**Analysis tips:**
- Verify company number, account number, and period ending date match across Sections 2 and 3
- If account numbers differ between Sections 2 and 3, consult the DMAAI setup in Section 6
- For DMAAI configuration details, see the [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md)

---

## Section 7: In Transit As-Of Page

### 7.1 Overview

The As-Of page lists items, quantities, and amounts that were in transit as of the selected period end date. Quantities and amounts are calculated **backwards from the Orders page totals** by subtracting each period's transfer order activity.

**Key behaviors:**

- The Orders page always reflects the **current** in-transit position. The As-Of page works backward from that position to reconstruct what was in transit at any prior period end.
- Calculations are dynamic -- backdated activity can change the As-Of position in prior periods.
- The As-Of total will always match the Reconciliation page total for the same period. It will only match the Orders page total if the **current period** is selected.

### 7.2 Item Activity Drill-Down

Clicking the **+** sign at the left of any row produces a list of transactions in reverse date sequence. Data is sourced from the sales and purchase orders -- not the item ledger. Details can be exported to Excel.

**Exclusion Adjust entries:** If an order pair has been excluded, an "Exclusion Adjust" entry appears in the transaction detail. This is a RapidReconciler adjustment, not a JD Edwards transaction -- it ensures the As-Of balance accurately reflects the reconciliation position.

### 7.3 Exporting

Grid data is exported by clicking the export icon at the top of the grid.

---

## Section 8: Integrity Reports

Integrity reports identify configuration issues that will cause reconciling items if not corrected. Review these reports when RapidReconciler is first installed and **monthly** as part of the period-end process.

| Report | Name | When to Review | Purpose |
|---|---|---|---|
| **Report 0** | JDE AAIs | Debugging only | Analyze DMAAI configuration. Use when investigating Transactions page items. See [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md). |
| **Report 1** | Model AAI Table | Before GL adjustments | Lists DMAAI table 4152 entries used to assign GL accounts to transfer order transactions. Must be accurate before making GL adjustments. |
| **Report 2** | Missing GL Classes | **Monthly** | Lists transfer order pairs where the GL class code is missing from the transit DMAAI table 4310. Missing entries are excluded from the reconciliation. |
| **Report 3** | Order Exclusions | **Monthly** | Lists all excluded order pairs for the selected period. Use to verify exclusions were not performed in error and to confirm the audit trail. See [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md). |
| **Report 4** | Transfer Cost Variances | **Monthly** | Lists orders where the sales cost or price differs from the OT purchase order cost. Key indicator of DMAAI 4335 issues or ST/OT price management problems. See [Transfer Order Reference Guide](../MDS/transfer_order_reference.md). |

### Report 4 -- Transfer Cost Variances: Key Columns

| Column | Description |
|---|---|
| **TransPrc** | The transfer cost or price of the item |
| **SOExtCost / SOExtAmt** | Extended cost and extended price on the sales order |
| **POUnitCost / POTotal** | Unit cost and total on the purchase order |
| **UnitPrVar** | The variance between the sales price and purchase cost -- the amount that will not clear from In Transit |
| **QtyVar** | The difference in units shipped versus received |
| **CostMthd** | The cost method in the receiving branch -- determines how variances are handled |

> A non-zero **UnitPrVar** on this report means the In Transit account will carry a balance for this order pair even after receipt. This is the most common cause of unresolved In Transit balances. Review DMAAI 4335 configuration and ST/OT price management procedures. See the [Transfer Order Reference Guide](../MDS/transfer_order_reference.md).

---

## Section 9: Step-by-Step Reconciliation Workflow

### 9.1 Frequency Guidance

| Activity | Recommended Frequency |
|---|---|
| Review Orders page; process exclusions | **Daily or weekly** -- do not wait until period end |
| Confirm Sales Update has run for transfer orders | **Daily** |
| Full reconciliation review | **Weekly** |
| Closing activities and audit report | **Period-end close** |

### 9.2 Step 1 -- Log In and Select the Data Set

1. Log in to RapidReconciler at [https://rapidreconciler.getgsi.com](https://rapidreconciler.getgsi.com)
2. Navigate to the **In Transit** module.
3. Confirm both status lights are **green**. Do not proceed if either is red.
4. Select the period to be reconciled using the period selector (top right).
5. Apply the appropriate company and account filters.

### 9.3 Step 2 -- Review the Orders Page

1. Navigate to the **Orders page**.
2. Review all order pairs for items that need to be excluded:
   - Both ST and OT at status **999** with a remaining balance = **exclude**
   - OT not yet received or partially received = **leave open**
3. Before excluding, research each order to confirm no further JD Edwards activity will occur.
4. Check the **ExclVarQty** and **ExclVarAmt** columns. Any non-zero value requires unexclude and re-exclude.
5. Note the total Exclusions amount -- this will become the journal entry amount.

### 9.4 Step 3 -- Review the Reconciliation Page

1. Navigate to the **Reconciliation page**.
2. Check the Valuation section. If Out of Balance = $0, skip to Step 6.
3. Review each line in the Variance Calculation section:

| Line | Required Before Close? | Action |
|---|---|---|
| **Carry Forward** | Investigate | Address in prior period or include in current entry |
| **GL Batches** | **Must be zero** | Work with finance to post all outstanding batches |
| **End of Day** | **Must be zero** | Confirm Sales Update processed all transfer orders |
| **Transactions** | Investigate | Navigate to Transactions page; prepare journal entries |
| **Exclusions** | Prepare journal entry | Use the amount to prepare the offsetting entry |
| **Manual Journal Entries** | Informational | Confirm entries are reflected correctly |

### 9.5 Step 4 -- Investigate and Resolve Transactions

1. Navigate to the **Transactions page**.
2. Review each item using the **+** drill-down to open the Transaction Detail report.
3. Determine the root cause (DMAAI mismatch, period mismatch, account mismatch).
4. Prepare an offsetting **journal entry in JD Edwards** for each transaction variance.
5. Add a **note** in RapidReconciler documenting the corrective action.
6. Optionally mark the transaction as **"Worked"** to filter it off the grid.

### 9.6 Step 5 -- Perform Closing Activities

Before closing, confirm:

- [ ] GL Batches = **$0**
- [ ] End of Day = **$0**
- [ ] All transaction variances reviewed and journal entries prepared
- [ ] Exclusion journal entry prepared for the Exclusions amount
- [ ] Carry-forward amount included in the journal entry if applicable

**To post the closing journal entry:**

- Use the **Journal Entry button** for account-level entries.
- Use the **Offset Account widget** (star icon on End of Day row) for transaction-level offsets.
- For exclusion amounts, refer to the [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md) for journal entry guidance.

After posting entries in JD Edwards, wait for the next nightly refresh and confirm the Out of Balance amount is zero.

### 9.7 Step 6 -- Review Integrity Reports

As part of the period-end close, review Integrity Reports 1 through 4:

- **Report 1** -- Model AAI Table: Verify all GL class codes have correct account assignments
- **Report 2** -- Missing GL Classes: Add missing GL class codes to the transit DMAAI table
- **Report 3** -- Order Exclusions: Confirm all exclusions are correct and accounted for
- **Report 4** -- Transfer Cost Variances: Investigate any orders with a non-zero UnitPrVar

### 9.8 Step 7 -- Produce and Save the Audit Report

Click the **Audit Report** button and save the output (Excel or PDF) to a dedicated period-end folder. The audit report should be produced **before** any purge is performed, as detail data may be removed during a purge.

---

## Section 10: Related Documentation

| Document | Relevance |
|---|---|
| [In Transit Key Concepts](../MDS/in-transit-key-concepts.md) | ST/OT definitions, DMAAI accounting setup, order pair concepts, and common issues |
| [Transfer Order Reference Guide](../MDS/transfer_order_reference.md) | Full accounting detail for all transfer scenarios, DMAAI 4335 configuration, and period-end reconciliation |
| [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md) | Complete exclusion procedure, ExclVar columns, unexclude/re-exclude process, and journal entry guidance |
| [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md) | Complete AAI reference for all distribution and manufacturing transactions |
| [Sales Order Reference Guide](../MDS/sales_order_reference.md) | Sales Update (R42800) processing -- resolves End of Day variances |
| [Stock Status and Trial Balance Reconciliation](../MDS/stock-status-trial-balance.md) | Root causes of GL vs. perpetual discrepancies |
| [How to Reconcile Inventory](../MDS/inventory-using-application.md) | Inventory module reconciliation guide -- parallel workflow for perpetual inventory |
| [Getting Started with RapidReconciler](../MDS/getting-started-with-rapidreconciler.md) | Login, navigation, and application overview |