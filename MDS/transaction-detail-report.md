**JD Edwards Inventory Reconciliation**

**Training Guide: A Significant RapidReconciler Update**

**Topic: Transaction Detail Report Enhancements**

**Section 1: Overview**

This guide covers a significant enhancement to the Transaction Detail Report within the RapidReconciler product by GSI. The update expands the depth of information available when investigating completed transactions that have failed reconciliation between the item ledger detail and the general ledger detail.

**Section 2: What Is the Transaction Detail Report?**

The Transaction Detail Report is a drill-down report accessible from the list of completed transactions that have failed reconciliation. End users generate this data by expanding a single transaction row on the grid. The report is available for any transaction type displayed on the Transactions page.

The primary purpose of the report is to identify the **root cause** of the discrepancy between the item ledger (F4111) and the general ledger (F0911).

**Section 3: Example - Purchase Order Receipt with Zero Balance Adjustment**

The following example illustrates how the enhanced report surfaces a root cause that would previously have required significant manual research.

**3.1 Scenario**

A purchase order receipt added **\$1,434.65** to inventory as shown in the F4111 Data section of the report. However, two rows were generated for this transaction:

- The standard receipt line for the primary receipt amount.
- A **zero balance adjustment** line for **\$411.40** - which is exactly the amount of the reconciliation variance.

**3.2 Root Cause**

General ledger entries to the inventory account only recorded a debit for the first line of the transaction. The zero balance adjustment line was not posted to the inventory account.

By reviewing the DMAAI configuration included in the report details, it was identified that the debits and credits for zero balance adjustment processing were both netting to the **same expense account** - meaning the adjustment had no net impact on the inventory GL account, while it did affect the item ledger.

**3.3 Resolution**

A one-minute configuration change in JD Edwards to correct the DMAAI setup for zero balance adjustments will prevent this issue from recurring in the future. The report provided the exact setup detail needed to identify and implement this fix without any additional research or ad hoc reporting.

**Section 4: What's New in This Update**

The enhanced Transaction Detail Report now includes more comprehensive details for the following transaction types:

- **Intercompany Orders** - Full cross-company transaction detail for improved analysis of intercompany variances.
- **Transfer Orders** - Complete ST/OT order pair detail to support In Transit reconciliation investigations.
- **Direct Ship Orders** - Enhanced detail for SD/OD order types to identify account routing issues.
- **Various Other Transaction Types** - Broader coverage across additional JD Edwards transaction types.

These enhancements replace hours of manual lookups in JD Edwards or the creation of ad hoc reports, significantly reducing the time required to investigate and resolve reconciling items.

**Section 5: Important Notes**

- **Trained eye required** - Interpreting the Transaction Detail Report effectively requires a working knowledge of JD Edwards transaction flows and DMAAI configuration. The data is comprehensive and is best reviewed by a JDE business analyst or someone with equivalent experience.
- **GSI support available** - If assistance is needed in analyzing the report output, the report can be sent to GSI for review and analysis.
- **Deployment** - This enhancement will be deployed in an upcoming RapidReconciler release. Contact GSI with any questions or feedback.
