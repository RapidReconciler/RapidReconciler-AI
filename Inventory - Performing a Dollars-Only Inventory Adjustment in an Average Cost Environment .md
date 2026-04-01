**JD Edwards Inventory Reconciliation**

**Training Guide: Cardex Integrity**

**Topic: Performing a Dollars-Only Inventory Adjustment in an Average Cost Environment**

**Section 1: Overview**

When maintaining cardex integrity, it is sometimes necessary to adjust the total value of cardex transactions to match the amounts on hand. Common causes for this type of discrepancy include:

- Rounding errors accumulated over time.
- Manual overrides of transaction costs.
- Incorrect average cost calculations.

This guide covers how to identify when a dollars-only adjustment is needed and how to perform it correctly in an average cost environment.

**Section 2: Checking Item Integrity**

**2.1 Procedure**

To verify the integrity of an item's cardex, follow these steps:

- Export all qualifying cardex transactions for the item to Excel.
- Summarize the quantities (expressed in primary unit of measure) and extended amounts.
- Compare the summarized totals to the stated on-hand quantity and amount in JD Edwards.

**2.2 Qualifying Transactions**

Qualifying transactions are those where column **ILIPCD** in table F4111 (the cardex) does **not** equal "X." The "X" posting code denotes memo transactions, which include:

- Work order scrap
- Lot releases
- Certain warehousing movements

These transactions must be excluded from the integrity calculation as they do not impact the on-hand balance.

**2.3 Identifying the Need for a Dollars-Only Adjustment**

If the quantity totals reconcile correctly but the extended amounts do not, a **dollars-only adjustment** is required to bring the cardex back into balance.

**Section 3: Performing a Dollars-Only Adjustment**

**3.1 Standard Cost Environment**

In a standard cost environment, a dollars-only adjustment is performed using an **IA (Inventory Adjustment)** transaction on the standard transaction entry screen. Complete the following fields:

- Item number
- Branch plant
- Location
- Lot number (if applicable)
- **Extended Amount** - enter the adjustment amount only

**Important:** Do not enter a quantity or unit cost. Leaving these fields blank ensures the transaction is processed as a dollars-only adjustment. Once posted, the adjustment will appear in the cardex with corresponding GL entries.

**3.2 Average Cost Environment - Additional Consideration**

In an average cost environment, an additional step is required before performing the dollars-only adjustment. The difference lies in the behavior of UDC table **40/AV**.

**3.3 UDC Table 40/AV**

UDC table 40/AV is a user-defined code table that controls which programs are permitted to update the unit cost for average cost items. If the adjustment program P4114 is allowed to update the average cost, the unit cost will be recalculated when the IA transaction is posted - effectively negating the intended dollars-only correction.

To prevent this, the average cost update must be disabled for program P4114 before performing the adjustment.

**Section 4: Step-by-Step Procedure for Average Cost Environments**

Follow these steps to perform a dollars-only adjustment in an average cost environment:

- **Navigate to UDC table 40/AV** in JD Edwards.
- **Locate program P4114** in the table.
- **Change the second description value from "Y" to "N"** - this disables the average cost update for the adjustment program.
- **Process the IA transaction** on the standard transaction entry screen, entering only the item, branch, location, lot number, and extended amount. Do not enter a quantity or unit cost.
- **Verify the adjustment** appears in the cardex with the correct amount and corresponding GL entries.
- **Restore the UDC table 40/AV setting** for P4114 back to "Y" after the adjustment is complete, to re-enable average cost updates for normal processing.

**Section 5: Key Takeaway**

| **Environment**   | **Key Difference**                                                      | **Action Required**                                                         |
| ----------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Standard Cost** | No additional configuration needed.                                     | Process the IA transaction with extended amount only.                       |
| **Average Cost**  | Program P4114 must not recalculate the unit cost during the adjustment. | Set UDC 40/AV for P4114 to "N" before processing; restore to "Y" afterward. |

**Important:** Always restore the UDC 40/AV setting after completing the adjustment. Leaving P4114 set to "N" will prevent the average cost from updating on future legitimate transactions, which will introduce new integrity issues.