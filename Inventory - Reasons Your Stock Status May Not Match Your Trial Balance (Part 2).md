**JD Edwards Inventory Reconciliation**

**Training Guide: Period End Close**

**Topic: Additional Reasons Your Stock Status May Not Match Your Trial Balance (Part 2)**

**Section 1: Overview**

This guide continues the series on why the Stock Status report may not match the Trial Balance during period-end inventory reconciliation. Part 1 covered the following three reasons:

- **Timing** - The stock status report must be run late on the last day of the period, with no further transactions processed until the first day of the following period.
- **Backdating** - Manually inputting dates on transactions can change the trial balance for a prior period without affecting the stock status at all.
- **Report Definition** - Hard-coding the cost method or using poor data selection criteria can lead to mismatches between the two reports.

This installment covers two additional reasons that are equally important to understand.

**Section 2: Reason 4 - DMAAI Setup**

**2.1 The Issue**

Distribution/Manufacturing Automatic Accounting Instruction (DMAAI) configuration is critical for accurately reflecting inventory value in the general ledger. This is the most complex of all the reasons a stock status may not match the trial balance.

**2.2 How DMAAs Affect the Reconciliation**

DMAAs define how inventory transactions are mapped to general ledger accounts. Each transaction type - receipts, issues, adjustments, transfers, shipments, and more - references specific DMAAI tables to determine which accounts are debited and credited.

An incorrect account number in any one of these tables is sufficient to cause reconciling items between the perpetual inventory balance and the general ledger.

**Key point:** DMAAI tables include both inventory balance sheet accounts and non-inventory accounts such as expense and variance accounts. If a transaction type is mapped to the wrong account - for example, an inventory transaction posting to an expense account instead of an inventory account - the stock status and trial balance will not agree, and the error may be difficult to trace without a thorough DMAAI review.

**Best Practice:** Periodically review DMAAI configuration using RapidReconciler's integrity reports and the Model AAI Table report to verify that all inventory GL class codes are correctly mapped to the intended balance sheet accounts.

**Section 3: Reason 5 - GL Class Code Changes**

**3.1 The Issue**

Changing a GL class code may appear to be a routine maintenance task, but it carries significant risk if not performed correctly. Specifically, changing a GL class code on a location record **while there is inventory on hand will not automatically generate a journal entry** to reclassify the associated dollar value to the new account.

**3.2 Impact on Reconciliation**

Without the corresponding journal entry - or better yet, without following the proper inventory adjustment procedure - the dollar value of the inventory on hand will remain posted to the original GL account while subsequent transactions begin posting to the new account. This creates a mismatch between the stock status (which reflects the current GL class code) and the trial balance (which still carries the value in the original account).

**3.3 Required Procedure**

To avoid this issue, the following procedure must be followed when changing a GL class code on an item with quantity on hand:

- Adjust the inventory quantity to zero under the current GL class code.
- Change the GL class code in all required locations (item branch, item location, open purchase order lines, open sales order lines).
- Adjust the inventory back in under the new GL class code.

This ensures that the inventory value is properly reclassified in the general ledger through actual inventory transactions, maintaining a clean item ledger and avoiding reconciling items.

**Section 4: Summary**

The following table provides a consolidated reference for all five reasons covered across both parts of this series:

| **Reason**                    | **Description**                                                                                                 | **Key Action**                                                                               |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **1 - Timing**                | Transactions processed after the stock status report is run create items in the GL not reflected in the report. | Run the stock status after all activity has stopped; coordinate with JD Edwards server time. |
| **2 - Backdating**            | Transactions posted to a prior GL period after the stock status is run cause a mismatch.                        | Review backdating practices in manual entry and processing option configurations.            |
| **3 - Report Definition**     | Incorrect cost method, non-stock items, or flawed data selection cause totals to differ.                        | Use COCSIN = 'I' for cost retrieval; review data selection criteria carefully.               |
| **4 - DMAAI Setup**           | Incorrect account mapping in DMAAI tables causes inventory transactions to post to the wrong GL accounts.       | Periodically review DMAAI configuration and verify balance sheet account mappings.           |
| **5 - GL Class Code Changes** | Changing a GL class code with quantity on hand does not automatically reclassify the GL value.                  | Follow the adjust-out, change code, adjust-in procedure before making GL class code changes. |

**Note:** With all of these factors potentially impacting financial statements, an automated reconciliation tool can be invaluable for identifying and resolving these issues efficiently. For more information on the RapidReconciler product by GSI, contact <rrsupport@getgsi.com>.