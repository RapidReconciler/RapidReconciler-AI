**JD Edwards Inventory Reconciliation**

**Training Guide: Cardex Analysis**

**Topic: Avoiding the 3 Common Analyst Errors**

**Section 1: Overview**

Analyzing the JD Edwards item ledger (cardex) for integrity issues is a task that arises periodically when a transaction has not been recorded in the item ledger correctly, or when the item balance table has not been updated as expected.

The validation process requires summarizing all transaction totals and comparing them to the balances displayed at the top of the item ledger screen. These balances are fetched from the following tables:

- **F41021** - Item Location table (quantity on hand)
- **F4105** - Item Cost table (unit cost)

To summarize the transaction totals, the grid must be exported to Excel and the quantity and extended amount columns totaled. This is where analysts frequently encounter issues. The following three common errors should be understood and avoided.

**Section 2: Error 1 - Including Memo Transactions**

**2.1 The Issue**

Certain transactions in the item ledger do **not** count toward the on-hand totals and must be filtered out before performing the analysis. These are known as **memo transactions** and include:

- Location adds
- Lot releases
- Manufacturing scrap

**2.2 How to Identify Memo Transactions**

Memo transactions are flagged with an **"X"** in the posting code field **ILIPCD**. However, this field is not displayed by default on the item ledger grid. The data can be viewed using the JD Edwards **data browser** feature.

**Action Required:** Before totaling the exported grid, identify and remove all rows where the ILIPCD posting code field contains an "X." Including these transactions in the summary will result in an incorrect total that does not match the on-hand balance.

**Section 3: Error 2 - Ignoring Alternate Units of Measure**

**3.1 The Issue**

After exporting the item ledger grid to Excel, analysts must review the transaction unit of measure column to determine whether more than one UOM is referenced. The on-hand quantity total displayed at the top of the screen is always expressed in the **primary unit of measure**.

Any transaction recorded in a unit of measure other than the primary UOM must be **converted to the primary UOM** before the totals are compared. Failing to do so produces an "apples to oranges" comparison and will make it appear that a variance exists when there may not be one.

**3.2 How to Handle UOM Differences**

- After exporting the grid, scan the transaction UOM column and identify any rows that are not in the primary UOM.
- Apply the appropriate conversion factor to bring those quantities into the primary UOM.
- In later versions of JD Edwards, a grid column labelled **"Quantity in Primary"** may be available. If this column is present, use it for the analysis - manual conversion will not be required.

**Section 4: Error 3 - Incorrect Analysis Level for Average Cost Items**

**4.1 The Issue**

Analyzing average cost items requires a different approach than standard cost items, and the correct method depends on the **item's cost level**.

- **Standard Cost Items** - Analysis is performed at the lot level. Each combination of item, branch, location, and lot should summarize accurately to the balance shown at the top of the screen.
- **Average Cost Items** - The analysis must be performed **in accordance with the item's cost level setting**.

**4.2 Cost Level Rules for Average Cost Items**

| **Cost Level**   | **Required Analysis Approach**                                                                                                                                                                                                                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cost Level 2** | The location and lot filter fields at the top of the item ledger screen must be populated with **"\*"** (wildcard). The analysis must include all locations and lots together - individual location or lot filtering is not valid at this cost level. |
| **Cost Level 3** | A specific location and lot may be specified in the filter. Analysis can be performed at the individual location and lot level.                                                                                                                       |

**Important:** If a Cost Level 2 item is analyzed by filtering to a specific location or lot, an apparent discrepancy may be identified that is actually offset by transactions in another location. This is not a true variance - it is a result of analyzing the data at the wrong level.

**Section 5: Summary**

The following table summarizes the three common errors and the corresponding actions required to avoid them:

| **Error**                                       | **Root Cause**                                                                      | **Corrective Action**                                                                                                                             |
| ----------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Memo Transactions Included**                  | Transactions flagged with "X" in ILIPCD are included in the summary total.          | Identify and remove all memo transactions before totaling the grid.                                                                               |
| **Alternate UOM Not Converted**                 | Transactions in non-primary units of measure are included without conversion.       | Convert all non-primary UOM transactions to primary UOM before comparing totals, or use the "Quantity in Primary" column if available.            |
| **Incorrect Cost Level for Average Cost Items** | Average cost items analyzed at the wrong level produce misleading variance results. | For Cost Level 2 items, use a wildcard (\*) for location and lot filters. For Cost Level 3 items, individual location and lot filtering is valid. |

Applying these three checks consistently when performing a cardex analysis will ensure that the transaction summary is accurate and that any true integrity issues are correctly identified.
