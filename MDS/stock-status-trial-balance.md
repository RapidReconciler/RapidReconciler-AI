# JD Edwards Inventory Reconciliation

## Period End Close: Why Your Stock Status May Not Match Your Trial Balance

---

## Overview

A core component of the period-end close process is reconciling inventory balances to the general ledger. This typically involves producing two reports:

- **Stock Status Report** -- Lists all stock items, quantity on hand, and extended value at a specific point in time.
- **Trial Balance Report** -- Lists general ledger accounts and balances for a designated period end.

Most organizations schedule the stock status report to run after transactional activity has stopped on the last day of the period. The resulting balance is then compared to the trial balance for the inventory account(s) after all batches have been posted.

In practice, it is uncommon for these two figures to tie out exactly. This guide covers the five most frequent causes of discrepancies and explains why a dedicated reconciliation tool is a more reliable alternative to running reports manually in JD Edwards.

---

## Section 1: Reason 1 -- Timing

### The Issue

The timing of when the stock status report is run is critical. To produce a balance that is comparable to the trial balance, there must be **no transactional activity** occurring between the time the report is run and the end of the period in terms of server time.

### Key Consideration

Transactions in JD Edwards are recorded according to the clock on the JD Edwards server -- not the local time of the user entering the transaction. Organizations with users in multiple time zones must account for this. If any transactions occur after the stock status report is generated but before the period closes on the server, those transactions will appear in the general ledger but not in the stock status report, creating reconciling items that must be accounted for.

> **Best Practice:** Coordinate the timing of the stock status report run with the JD Edwards server time and ensure all transactional activity has fully stopped before generating the report.

---

## Section 2: Reason 2 -- Backdating

### The Issue

Backdating occurs when a transaction is posted to a general ledger period that differs from the period in which the inventory quantity actually changed. This creates a mismatch between the stock status (which reflects physical inventory at the time of the report) and the trial balance (which reflects the GL period to which the transaction was booked).

### How Backdating Occurs

Backdating can occur in the following ways:

- **Manual entry** -- A user manually inputs a transaction date or GL date on inventory issues, adjustments, transfers, or receipts that falls in a prior period.
- **Processing option settings** -- The manufacturing accounting or sales update programs can be configured via processing options to book transactions to a prior period. This is sometimes done intentionally.

### Example Scenario

An item is physically shipped on the last day of the period, but the shipment confirmation transaction is not processed until the first day of the following period. The GL date is backdated to the prior period.

**Result:**

- The stock status report shows the goods still in stock (the quantity has not yet been relieved at the time the report was run).
- The backdated GL entry removes the inventory value from the prior period's account balance.
- A reconciling item is created.

> **Best Practice:** Review backdating practices in both manual entry and processing option configurations. Establish organizational controls that limit or require approval for prior-period transaction dates.

---

## Section 3: Reason 3 -- Report Definition

### The Issue

How the stock status report is written and configured can introduce discrepancies independent of any transaction timing or backdating issues.

### Common Report Definition Problems

| Issue | Description |
|---|---|
| **Incorrect Cost Method Specification** | Specifying a cost method such as "07" to retrieve the unit cost from table F4105 may not be accurate in environments that use mixed cost methods (e.g., some items on weighted average and others on standard cost). Use **COCSIN = 'I'** to retrieve the applicable cost regardless of cost type, ensuring the correct cost is used for every item. |
| **Non-Stock Items Included** | Non-stock items are typically expensed upon receipt and should not carry a unit cost in the inventory system. If a cost is inadvertently associated with a non-stock item, it will be included in the stock status total and create a reconciliation discrepancy. |
| **Incorrect Data Selection Criteria** | The data selection criteria used in the report must be carefully reviewed to ensure that stock items are not being inadvertently excluded. Missing items will cause the stock status total to be understated relative to the general ledger balance. |

> **Best Practice:** Use **COCSIN = 'I'** for cost retrieval. Review data selection criteria carefully at each period end to confirm no items are being excluded. Periodically audit the report definition itself -- report configurations can drift over time as items and cost methods change.

---

## Section 4: Reason 4 -- DMAAI Setup

### The Issue

Distribution/Manufacturing Automatic Accounting Instruction (DMAAI) configuration is critical for accurately reflecting inventory value in the general ledger. This is the most complex of all five reasons a stock status may not match the trial balance.

### How DMAIs Affect the Reconciliation

DMAIs define how inventory transactions are mapped to general ledger accounts. Each transaction type -- receipts, issues, adjustments, transfers, shipments, and more -- references specific DMAAI tables to determine which accounts are debited and credited.

An incorrect account number in any one of these tables is sufficient to cause reconciling items between the perpetual inventory balance and the general ledger.

> **Key Point:** DMAAI tables include both inventory balance sheet accounts and non-inventory accounts such as expense and variance accounts. If a transaction type is mapped to the wrong account -- for example, an inventory transaction posting to an expense account instead of an inventory account -- the stock status and trial balance will not agree, and the error may be difficult to trace without a thorough DMAAI review.

### What Makes This Difficult to Detect

Unlike timing or backdating issues, incorrect DMAAI configuration does not produce an error message. Transactions post successfully to the wrong account, and the discrepancy only surfaces during reconciliation. Tracing the root cause requires reviewing DMAAI table entries, transaction document types, and GL class code assignments -- a time-consuming process when done manually.

> **Best Practice:** Periodically review DMAAI configuration to verify that all inventory GL class codes are correctly mapped to the intended balance sheet accounts. Use RapidReconciler's integrity reports and the Model AAI Table report to streamline this review.

For a complete reference on DMAAI configuration, see the [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md).

---

## Section 5: Reason 5 -- GL Class Code Changes

### The Issue

Changing a GL class code may appear to be a routine maintenance task, but it carries significant risk if not performed correctly. Changing a GL class code on a location record **while inventory is on hand will not automatically generate a journal entry** to reclassify the associated dollar value to the new account.

### Impact on Reconciliation

Without the corresponding journal entry -- or without following the proper inventory adjustment procedure -- the dollar value of the inventory on hand will remain posted to the original GL account while subsequent transactions begin posting to the new account. This creates a mismatch between the stock status (which reflects the current GL class code) and the trial balance (which still carries the value in the original account).

### Required Procedure

To avoid this issue, the following procedure must be followed when changing a GL class code on an item with quantity on hand:

1. **Adjust the inventory quantity to zero** under the current GL class code.
2. **Change the GL class code** at all required levels -- item master, item branch, item location, open purchase order lines, and open sales order lines.
3. **Adjust the inventory back in** under the new GL class code.

This ensures that the inventory value is properly reclassified in the general ledger through actual inventory transactions, maintaining a clean item ledger and avoiding reconciling items at period end.

For the complete procedure, see the [GL Class Code Management and Change Procedures](../MDS/gl-class-code-changes.md) guide.

---

## Section 6: Summary of All Five Reasons

| Reason | Description | Key Action |
|---|---|---|
| **1 -- Timing** | Transactions processed after the stock status report is run create items in the GL not reflected in the report. | Run the stock status after all activity has stopped; coordinate with JD Edwards server time. |
| **2 -- Backdating** | Transactions posted to a prior GL period after the stock status is run cause a mismatch. | Review backdating practices in manual entry and processing option configurations. |
| **3 -- Report Definition** | Incorrect cost method, non-stock items, or flawed data selection cause totals to differ. | Use COCSIN = 'I' for cost retrieval; review data selection criteria carefully. |
| **4 -- DMAAI Setup** | Incorrect account mapping in DMAAI tables causes inventory transactions to post to the wrong GL accounts. | Periodically review DMAAI configuration and verify balance sheet account mappings. |
| **5 -- GL Class Code Changes** | Changing a GL class code with quantity on hand does not automatically reclassify the GL value. | Follow the adjust-out, change code, adjust-in procedure before making GL class code changes. |

---

## Section 7: Why RapidReconciler Is a Better Solution

Each of the five issues described above is difficult to identify and resolve using standard JD Edwards reports alone. The manual approach has significant limitations that compound at period end -- precisely when accuracy and speed matter most.

### The Limitations of Manual JDE Reporting

**Point-in-time snapshots only.** The stock status report captures inventory value at a single moment. Any transaction that posts after the report runs but before the period closes creates an immediate discrepancy. There is no built-in mechanism to detect or flag these transactions automatically.

**No cross-referencing between inventory and the GL.** The stock status and trial balance are separate reports with no automated comparison between them. Identifying where and why they differ requires manually tracing individual transactions -- a process that can take hours or days depending on transaction volume.

**DMAAI errors are invisible until period end.** Incorrect account mappings in DMAAI tables post silently to the wrong accounts. There is no JD Edwards report that proactively identifies these mismatches -- they only surface as unexplained variances during reconciliation.

**GL class code mismatches go undetected.** JD Edwards allows GL class code changes at any level without checking whether inventory is on hand. Integrity Report 5 identifies mismatches between Item Branch and Item Location records but does not flag the accounting impact or alert users to the risk of a pending change.

**Report definitions are fragile.** Stock status reports depend on correct cost method logic, data selection criteria, and inclusion rules. These configurations can drift over time as items, cost methods, and business units are added or changed, and there is no automated validation to ensure the report remains accurate.

**No continuous reconciliation.** The manual process is inherently periodic. Issues that occur mid-period are not detected until the next reconciliation cycle, by which time the volume of transactions to review has grown and the trail has gone cold.

---

### How RapidReconciler Solves These Problems

RapidReconciler by GSI is purpose-built to address the limitations of manual JD Edwards inventory reconciliation. Rather than relying on point-in-time reports, RapidReconciler provides a **continuous, real-time view** of inventory value against the general ledger -- updated with every import cycle.

| Problem | RapidReconciler Solution |
|---|---|
| **Timing** | Reconciliation is updated automatically with each nightly import cycle, eliminating the dependency on a perfectly timed manual report run. |
| **Backdating** | Backdated transactions are visible immediately in the reconciliation, clearly identified by document date and GL date so variances can be investigated as they occur rather than at period end. |
| **Report Definition** | RapidReconciler reads directly from JD Edwards data tables -- F4111, F0902, and others -- eliminating the risk of incorrect cost method logic or flawed data selection criteria in a custom report. |
| **DMAAI Setup** | RapidReconciler's integrity reports identify inventory transactions that are posting to non-inventory accounts, surfacing DMAAI mismatches that would otherwise be invisible until reconciliation. The Model AAI Table report allows DMAAI configuration to be reviewed at a glance. |
| **GL Class Code Changes** | RapidReconciler makes the impact of GL class code changes immediately visible. Variances caused by an incorrect class code change appear in the reconciliation as soon as the next import cycle runs, allowing the issue to be identified and corrected before it compounds. |

### Additional Benefits

- **Drill-down capability** -- From any reconciling item, users can drill down to the underlying JD Edwards transactions to identify the root cause without switching between multiple JD Edwards screens and reports.
- **Reduced period-end workload** -- Because reconciliation is continuous rather than periodic, the period-end close process becomes a confirmation of an already-reconciled position rather than a discovery exercise.
- **Consistent methodology** -- RapidReconciler applies the same reconciliation logic every period, eliminating variation caused by manual report configuration changes or user error.
- **Audit trail** -- All reconciling items and their resolutions are tracked, providing a complete audit trail for internal and external review.

---

> For more information on RapidReconciler, contact [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com).

---

## Related Documentation

- [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md)
- [GL Class Code Management and Change Procedures](../MDS/gl-class-code-changes.md)
- [Account Management -- Adding an Inventory Account](../MDS/add-account-rr.md)