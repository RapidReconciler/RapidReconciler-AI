**JD Edwards Inventory Reconciliation**

**Training Guide: Period End Close**

**Topic: 3 Reasons Your Stock Status May Not Match Your Trial Balance**

**Section 1: Overview**

A core component of the period-end close process is reconciling inventory balances to the general ledger. This typically involves producing two reports:

- **Stock Status Report** - Lists all stock items, quantity on hand, and extended value at a specific point in time.
- **Trial Balance Report** - Lists general ledger accounts and balances for a designated period end.

Most organizations schedule the stock status report to run after transactional activity has stopped on the last day of the period. The resulting balance is then compared to the trial balance for the inventory account(s) after all batches have been posted.

In practice, however, it is uncommon for these two figures to tie out exactly. The following three reasons explain the most frequent causes of discrepancies.

**Section 2: Reason 1 - Timing**

**2.1 The Issue**

The timing of when the stock status report is run is critical. To produce a balance that is close to the trial balance, there must be **no transactional activity** occurring between the time the report is run and the end of the period in terms of server time.

**2.2 Key Consideration**

Transactions in JD Edwards are recorded according to the clock on the JD Edwards server - not the local time of the user entering the transaction. Organizations with users in multiple time zones must account for this. If any transactions occur after the stock status report is generated but before the period closes on the server, those transactions will appear in the general ledger but not in the stock status report, creating reconciling items that must be accounted for.

**Best Practice:** Coordinate the timing of the stock status report run with the JD Edwards server time and ensure all transactional activity has fully stopped before generating the report.

**Section 3: Reason 2 - Backdating**

**3.1 The Issue**

Backdating occurs when a transaction is posted to a general ledger period that differs from the period in which the inventory quantity actually changed. This creates a mismatch between the stock status (which reflects the physical inventory at the time of the report) and the trial balance (which reflects the GL period to which the transaction was booked).

**3.2 How Backdating Occurs**

Backdating can occur in the following ways:

- **Manual entry** - A user manually inputs a transaction date or GL date on inventory issues, adjustments, transfers, or receipts that falls in a prior period.
- **Processing option settings** - The manufacturing accounting or sales update programs can be configured via processing options to book transactions to a prior period. This is sometimes done intentionally.

**3.3 Example Scenario**

An item is physically shipped on the last day of the period, but the shipment confirmation transaction is not processed until the first day of the following period. The GL date is backdated to the prior period.

**Result:**

- The stock status report shows the goods still in stock (the quantity has not yet been relieved at the time the report was run).
- The backdated GL entry removes the inventory value from the prior period's account balance.
- A reconciling item is created.

**Section 4: Reason 3 - Report Definition**

**4.1 The Issue**

How the stock status report is written and configured can introduce discrepancies independent of any transaction timing or backdating issues. The following common report definition problems should be reviewed:

| **Issue**                               | **Description**                                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Incorrect Cost Method Specification** | Specifying a cost method such as "07" to retrieve the unit cost from table F4105 may not be accurate, particularly in environments that use mixed cost methods (e.g., some items on weighted average and others on standard cost). Use **COCSIN = 'I'** to retrieve the applicable cost regardless of cost type, ensuring the correct cost is used for every item. |
| **Non-Stock Items Included**            | Non-stock items are typically expensed upon receipt and should not carry a unit cost in the inventory system. If a cost is inadvertently associated with a non-stock item, it will be included in the stock status total and create a reconciliation discrepancy.                                                                                                  |
| **Incorrect Data Selection Criteria**   | The data selection criteria used in the report must be carefully reviewed to ensure that stock items are not being inadvertently excluded from the calculation. Missing items will cause the stock status total to be understated relative to the general ledger balance.                                                                                          |

**Section 5: Summary**

The following table summarizes the three reasons a stock status report may not match the trial balance:

| **Reason**            | **Root Cause**                                                                                                                                     | **Key Action**                                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Timing**            | Transactions recorded after the stock status report is run but before the server period closes create items present in the GL but not the report.  | Coordinate report timing with JD Edwards server time and confirm all activity has stopped.                                  |
| **Backdating**        | Transactions posted to a prior GL period after the stock status is run cause a mismatch between physical inventory and the GL balance.             | Review backdating practices in manual entry and processing option configurations.                                           |
| **Report Definition** | Incorrect cost method, inclusion of non-stock items, or flawed data selection criteria cause the stock status total to differ from the GL balance. | Review report configuration for cost method logic (use COCSIN = 'I'), non-stock item handling, and data selection criteria. |

**Note:** While these three reasons are among the most common causes of stock status to trial balance discrepancies, they are not exhaustive. Additional contributing factors exist and will be covered in subsequent training materials.
