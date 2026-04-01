**JD Edwards Inventory Reconciliation**

**Training Guide: Resolving the Top 6 Issues (Part 3)**

**Topic: Product Costing and Cost Component Integrity**

**Section 1: Overview**

This guide continues the series on the top six issues with JD Edwards inventory reconciliation. Previous installments covered DMAAs (Part 1) and GL class code changes (Part 2). This installment focuses on product costing and how to verify cost setup integrity to prevent reconciliation variances.

**Section 2: Standard Cost Structure**

In a standard cost system, each item's total standard cost is made up of several individual cost components. A cost roll-up procedure calculates and sets the cost ledger value to equal the sum of all of those components.

**Example:** If the sum of all values in the Simulated Total column across all cost components equals \$389, the Cost Ledger field should also reflect \$389 after a proper cost roll-up is performed.

**Section 3: The Problem - Cost Ledger and Component Mismatch**

A discrepancy can occur when the cost ledger amount does not match the sum of its cost components. This typically happens when the cost ledger is changed manually without going through the proper roll-up procedure.

**3.1 Impact on Reconciliation**

When the cost ledger and cost components are out of sync, the item ledger and the general ledger will record different values for the same transaction, resulting in a reconciling item.

**Example Scenario:**

- The sum of all cost components for an item equals **\$389**.
- The cost ledger has been manually changed to **\$400**.
- When this item is issued to a work order, the **item ledger (cardex)** records the transaction at the cost ledger amount: **\$400**.
- When manufacturing accounting runs, the **general ledger** books the transaction by cost component: **\$389**.
- This leaves an **\$11 discrepancy** between the item ledger and the general ledger - a direct reconciling variance.

**Section 4: How to Identify the Issue - Report R30543**

**4.1 Cost Component/Ledger Integrity Report**

The R30543 Cost Component/Ledger Integrity Report is the tool used to identify items where the cost ledger value does not equal the sum of the cost components.

**To use this report:**

- Run report R30543 in JD Edwards.
- Review the output for any items listed - each row represents an item where a mismatch exists between the cost ledger and the sum of its cost components.
- For each item identified, perform a cost re-roll to recalculate and reset the cost ledger to the correct sum of components.
- Re-rolling the affected items will bring costs back into alignment and prevent future variances from occurring.

**Section 5: Best Practice Recommendation**

**Recommendation:** Cost accountants should run the R30543 Cost Component/Ledger Integrity Report on a periodic basis to proactively identify and resolve any product cost discrepancies before they result in reconciliation variances.

Catching these mismatches early - before items are issued to work orders or processed through manufacturing accounting - eliminates the downstream impact on the item ledger and general ledger, and avoids unnecessary reconciling items at period end.

**Section 6: What's Next**

The next topic in this series will cover another potential costing issue: **WIP (Work in Process) Revaluation** and its impact on inventory reconciliation. Understanding how WIP revaluation interacts with the item and general ledgers is an important step in maintaining a clean and accurate reconciliation.