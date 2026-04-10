**Rapid Reconciler In Transit**

**Training Manual: Using the Application**

**Section 1: In Transit Orders Page**

**1.1 What Is Being Displayed?**

Each row on the Orders page lists a transfer order pair (refer to the In Transit Key Concepts training for the definition of an order pair) that has either an open quantity or an open amount.

The following process flow illustrates how entries appear and are managed on the Orders page, using the example of 100 EA of item number 123 being transferred from Branch A to Branch B at \$1 each on ST 999 / OT 999:

| **Step**                           | **Scenario**            | **Orders Page**                       | **Action Required**                                                        |
| ---------------------------------- | ----------------------- | ------------------------------------- | -------------------------------------------------------------------------- |
| Order Entry                        | -                       | No entry                              | -                                                                          |
| Items Picked                       | All 100                 | No entry                              | -                                                                          |
| Items Ship Confirmed               | All 100                 | Order pair shows 1 EA, \$1 in transit | N/A - goods in transit                                                     |
| Items Received - exact match       | 100 EA for \$1          | Entry automatically disappears        | N/A                                                                        |
| Items Received - amount mismatch   | 100 EA, amount ≠ \$1    | Entry displays with open amount       | Exclude the entry                                                          |
| Items Received - quantity mismatch | Fewer than 100 received | Balance remains in transit            | Exclude if no further activity expected; leave if more activity will occur |

The purpose of the Orders page is to list only the orders and items that are truly in transit. All other entries must be excluded in order to obtain the correct In Transit balance in RapidReconciler.

**1.2 What Is an Exclusion?**

An Exclusion is a RapidReconciler process that allows an order pair to be "closed" so that it no longer counts toward the In Transit balance. This is necessary because mismatches in quantities or amounts between shipments and receipts can occur that cannot be resolved through JD Edwards alone.

**Important:** Performing an order exclusion in RapidReconciler does not change any data in JD Edwards.

**Section 2: In Transit Reconciliation Page**

**2.1 Overview**

The Reconciliation page is the default page that appears when you first log into the application. This is where detailed data is summarized and where the majority of your time will be spent. It is important to review each section carefully, as a thorough understanding of what is displayed here makes working with the supporting details significantly easier.

**2.2 Status Indicators**

Two status indicators are displayed at the top center of the screen. Green indicates success; red indicates an issue that must be resolved. If the System Status light is flashing yellow, the JDE import is still in process. Both lights must be green before making any adjustments to the general ledger.

| **Indicator**             | **Description**                                                                                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **In Transit Validation** | Ensures the carry-forward amount matches the out-of-balance amount from the previous period. If red, hover your cursor over the indicator for more information. |
| **System Status**         | Ensures the import from JD Edwards has fully completed without error. Hover your cursor over the indicator for more information.                                |

**2.3 Period Selector**

The period selector is located in the top right corner of the window and is used to select the period to be reconciled. Key behaviors include:

- The periods displayed in the drop-down depend on the reconciliation start date configured by your administrator.
- New periods are automatically added based on new cardex transactions entered in JD Edwards.
- The period selection remains in place as you navigate across pages within the In Transit module.
- It is recommended that a purge be performed if there are more than 14 periods of data. Contact your RapidReconciler administrator to request a purge.

**2.4 Using the Account Filters**

The account filters operate intuitively using a hierarchy from left to right. Key behaviors include:

- Check the items to be included in the reconciliation; uncheck to exclude.
- Removing a company will automatically remove its associated business units, objects, and subsidiaries.
- Each option has a search row at the top. Begin typing in the field to filter the individual column.
- If there are issues with the items being displayed, click the refresh icon in the top right corner.
- Filter selections persist as you navigate to different pages within the In Transit module.

**Section 3: Valuation Section**

**3.1 Overview**

The Valuation section provides a quick check to confirm whether the In Transit inventory balance for the selected period matches the balance in the general ledger. The totals displayed will depend on the filter selections and period chosen.

| **Field**              | **Description**                                                                                                                                                               |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GL Balance**         | Derived from the F0902 balance table. Should match the trial balance report exactly.                                                                                          |
| **In Transit Balance** | Calculated from the In Transit order types as (Shipments − Receipts). Refer to the Orders Page training for further details.                                                  |
| **Out of Balance**     | If this total is zero, inventory is in balance with the general ledger. Any non-zero amount represents variance that will be broken down in the Variance Calculation section. |

**Section 4: Variance Calculation**

**4.1 Overview**

The Variance Calculation section lists and quantifies all sources of variance. Each non-zero amount should be reviewed. The sum of all variances matches the out-of-balance amount shown in the Valuation section, confirming that all items are accounted for.

**4.2 Variance Sources**

- **Carry Forward** - The out-of-balance amount carried forward from the prior period. Return to the prior period to resolve, or offset with a manual journal entry in the current period if needed.
- **GL Batches** - GL batches that need to be posted. Work with the finance department to get these batches posted.
- **End of Day** - Transfer sales orders that have not been processed to the general ledger. Get orders processed through the sales update program.
- **Transactions** - Completed transactions with a discrepancy between the item ledger and the general ledger. These require an offsetting manual journal entry.
- **Exclusions** - The "leftover" adjustment needed to account for mismatched units or amounts between what was shipped and what was received.
- **Manual Journal Entries** - Any manual entries made to the account(s) to correct out-of-balance amounts.

**Section 5: Supporting Widgets**

**5.1 Drill Down Widget**

The Drill Down widget provides a visual aid for identifying where the largest out-of-balance amounts exist. This is especially useful in multi-company organizations with many business units being monitored.

- The chart follows the hierarchy of the account filters. The default starting point is the currency code.
- The legend on the right displays the items being shown.
- Hovering over a section of the chart displays the item name and variance amount.
- Clicking on a chart section drills down to the next level.
- The back arrow returns to the previous level.
- Filter selections automatically update as you click through levels.
- If there is no variance, no chart will be displayed.

**5.2 Offset Account Widget**

The Offset Account widget is represented by a star icon that appears when hovering over the End of Day or Transactions row in the Variance Calculation section. Clicking the icon opens a pop-up window listing the company, period, inventory account, and the offset account to be used for the applicable variance. The data can be exported to Excel and copied into the JD Edwards journal entry screen.

The exported data contains the following elements:

- **je_account column** - Contains one row for the perpetual inventory side, one row for "Tolerance Adjust," and one or more rows for any remaining variance.
- **Tolerance Adjust** - Accounts for the tolerance setting applied to transaction variances below 1 monetary unit. These rounding amounts still require adjustment.
- **TBD** - The default placeholder for any remaining variance. The administrator can configure specific offset accounts for different transaction types. When configured, the correct accounts will display in the data set.

**Note:** After exporting the data to Excel, manually replace "Tolerance Adjust" and "TBD" cells with the applicable GL account numbers, then copy the two rightmost columns and paste into JD Edwards. This feature is designed for use during the close. Entries made mid-period are not taken into account.

**Important:** The In Transit module provides an offset for "End of Day" only - there is no "Transactions" offset in this module.

**5.3 Out of Balance History Graph**

The Out of Balance History graph displays variance trends over time.

- The most recent 14 period ending dates are displayed. If fewer than 14 periods exist, all available data is shown.
- A system in perfect balance would show all periods at \$0.
- Hovering over an individual period displays the date and variance total.
- Clicking on a data point changes the period filter to that period end date.

**5.4 Journal Entry Button**

Clicking the Journal Entry button produces an Excel report of the GL and In Transit balances for the selected accounts and single period. This is used to make journal entries at the account level when a more detailed review is not required.

**5.5 Audit Report Button**

The Audit Report documents the reconciliation results for the period being analyzed. The report contains a summary page listing all accounts, the In Transit balance, GL balance, and out-of-balance amount. Each account is then broken down into the following detail sections:

| **Section**                | **Description**                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| **Accounts Summary**       | The valuation and variance calculation summary for each account.                           |
| **Unposted GL Batches**    | Details for any remaining unposted GL batches.                                             |
| **End of Day**             | Lists any remaining sales orders awaiting processing through sales update.                 |
| **Manual Journal Entries** | Lists any manual entries made to the account.                                              |
| **Variances**              | Lists transaction variances that occurred in the period, including any user-entered notes. |
| **Perpetual Details**      | A list of item balances and values at the end of the selected period.                      |

The report may be output in Excel or PDF format. You will be prompted to select a format after clicking the button.

**Important:** It is highly recommended that an audit report be produced and saved at the end of each period, as detail data may be removed during a purge.

**Section 6: In Transit Transactions Page**

**6.1 Overview**

The Transactions page lists documents where the data in the item ledger F4111 does not match the data in the general ledger F0911, per the matching criteria covered in the Key Concepts training. Only reconciling items are displayed. Any transaction that has been internally reconciled will not appear. Reviewing the transaction detail report is typically performed by a JDE business analyst or someone with a similar skill set.

**6.2 A Note About Rounding and Tolerance**

Due to decimal precision and other system factors, many transactions may fail by a penny or other very small amount. RapidReconciler is designed with a tolerance setting that defaults to 1, meaning any transaction variance of less than 1 monetary unit will not be displayed.

**Important:** These sub-tolerance variances are still counted toward the total out-of-balance amount. As a result, the total shown on the Transactions line in the Variance Calculation section may differ slightly from the total displayed on the Transactions page. The tolerance setting may be changed by the RapidReconciler administrator if greater precision is required.

**6.3 Edit Notes and Worked Transactions**

Manual notes can be added to transactions in the grid to document corrective actions taken. These notes will appear on the period-end audit report.

Best practices for notes:

- Include your name and the date within the body of the note text.
- Notes can be deleted after the fact if necessary.
- Additional notes can be added to the same transaction at any time.

Flagging a transaction as "Worked" allows it to be filtered off the grid. This does not change variance totals or permanently remove transactions. The corrective action for any transaction on this page is an offsetting manual journal entry in JD Edwards, along with a note entry in RapidReconciler for audit purposes.

**6.4 Grid Column Definitions**

| **Column**               | **Description**                                                                |
| ------------------------ | ------------------------------------------------------------------------------ |
| **Worked**               | Checked indicates the transaction has been cleared via the Edit Notes process. |
| **Note**                 | Hover to view any note that has been added.                                    |
| **Company Number**       | The company number associated with the transaction.                            |
| **Long Account**         | The account number associated with the transaction.                            |
| **Sort Key**             | The concatenated sales order/purchase order number.                            |
| **Document Type**        | The JD Edwards document type.                                                  |
| **Document Number**      | The JD Edwards document number.                                                |
| **Order Type**           | The JD Edwards order type.                                                     |
| **Order Number**         | The JD Edwards order number.                                                   |
| **Transit Amount**       | The total from the Orders page for applicable activity.                        |
| **Ledger Amount**        | The total from F0911.                                                          |
| **Variance**             | Ledger Amount minus Cardex Amount.                                             |
| **Comment**              | Helpful information provided by RapidReconciler.                               |
| **Currency**             | The currency code of the transaction.                                          |
| **Batch Number**         | The JD Edwards batch number.                                                   |
| **Period Ends**          | The period ending date assigned by the date logic algorithm.                   |
| **Transaction Date**     | The creation date from the cardex, or the GL date for GL-only transactions.    |
| **Rel Type / Rel Order** | The related order type and number, if applicable.                              |

**6.5 Producing a Transaction Detail Report**

Details for a specific transaction are accessed by clicking the **+** icon at the far left of the applicable grid row. Results are based on the company number, document type, and document number. The account, period, and order information are not passed, resulting in a complete data set for analysis.

The transaction detail report is organized into six sections:

| **Section**                        | **Description**                                                                                                                                                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Section 1 - Unassigned Account** | Lists cardex transactions with a GL class code not referenced in the model DMAAI table. If the item is a stock item, the GL class must be added to the model table. This section will not appear if all cardex records have stock GL class codes. |
| **Section 2 - F4111 Cardex**       | All F4111 rows for the selected company, document type, and document number.                                                                                                                                                                      |
| **Section 3 - F0911 GL**           | All F0911 rows for the selected company, document type, and document number. For work orders, the sub-ledger field and cross-reference table F3106 are also considered.                                                                           |
| **Section 4 - RapidReconciler**    | Shows how RapidReconciler matches and summarizes the transaction. One row indicates matching criteria are met; multiple rows indicate a mismatch.                                                                                                 |
| **Section 5 - Order Data**         | For PO receipts and sales order shipments, contains all lines for the associated order. For intercompany orders, includes related order information.                                                                                              |
| **Section 6 - DMAAs**              | Lists all DMAAI entries for each GL class code in the transaction. The first row is from the model table.                                                                                                                                         |

**6.6 Analyzing the Transaction Detail Report**

The following tips are useful when reviewing the report:

- **Matching Criteria** - Verify that the company number, account number, and period ending date match for each row in Sections 2 and 3. Section 4 will show multiple rows if they do not.
- **Order Information Review** - Confirm that the unit cost for the item on the order matches Section 2. For sales orders, verify that the quantity shipped on the order line matches the quantity in the cardex.
- **DMAAI Review** - If the account number in GL Section 3 differs from the account assigned in cardex Section 2, consult the DMAAI set up in Section 6 to determine the cause.

**Reminder:** The corrective action for any item on the Transactions page is an offsetting journal entry in JD Edwards and a note entry in RapidReconciler, as the transaction has already been completed and documentation is required for audit purposes.

**Section 7: In Transit As-Of Page**

**7.1 Overview**

The In Transit As-Of page lists items, quantities, and amounts that were in transit as of the selected period end date. Quantities and amounts are calculated backwards from the totals on the Orders page.

Key behaviors to understand:

- The Orders page always lists what is currently in transit, regardless of the period selected in the drop-down. These item totals serve as the starting point for the calculations.
- Each item's transfer order activity is subtracted by period to produce the As-Of totals.
- The calculations are dynamic - backdated activity can change reconciliations in prior periods.

**7.2 Exporting the Grid**

Grid data is exported by clicking the export icon at the top of the grid.

**7.3 Item Activity**

Clicking the **+** sign at the left of a row produces a list of transactions in reverse date sequence. Data is sourced from the sales orders and purchase orders - not the item ledger. The details can be exported to Excel for further review.

**7.4 In Transit Totals**

The amount total at the bottom of the grid will always match (rounding aside) the total on the Reconciliation page for any period selected.

**Note:** This total will only match the total on the Orders page if the current period is selected.

**Section 8: In Transit Integrity Reports**

**8.1 Report 0 - JDE AAIs**

The JDE Transit AAI report is used primarily for debugging items listed on the Transactions page. It provides a quick method of analyzing DMAAI configuration through filtering, sorting, and Excel export. Flex accounting for inventory is supported. JDE data comes from tables F4095 and F4096.

**Grid Columns:**

| **Column**                      | **Description**                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------- |
| **CompanyNumber**               | Company number from JD Edwards.                                                 |
| **TableNumber**                 | DMAAI table number from JD Edwards.                                             |
| **DocType**                     | Document type from JDE table F4095.                                             |
| **GLClass**                     | GL class from F4095. Value "\*\*\*\*" is a wildcard meaning all GL class codes. |
| **Cost Type**                   | Cost type from JDE table F4095.                                                 |
| **BusinessUnit / Object / Sub** | Account fields from JDE table F4095.                                            |

**8.2 Report 1 - Model AAI Table**

The Model AAI Table report lists entries in DMAAI table 4152 for the document type specified in the company setup. It is used during data import to assign each item ledger transaction and item balance record a GL account number based on the company number of the branch plant and GL class code.

**Grid Columns:**

| **Column**        | **Description**                                                                 |
| ----------------- | ------------------------------------------------------------------------------- |
| **CompanyNumber** | Company number from JD Edwards.                                                 |
| **TableNumber**   | DMAAI table number from JD Edwards.                                             |
| **DocType**       | Document type from JDE table F4095.                                             |
| **GLClass**       | GL class from F4095. Value "\*\*\*\*" is a wildcard meaning all GL class codes. |
| **Long Account**  | The concatenated business unit, object account, and subsidiary.                 |

**8.3 Report 2 - Missing GL Classes**

The Missing GL Classes report lists transfer order pairs where the GL class code is missing from the transit DMAAI table 4310 for the purchase order type. Any value for items listed here will not be counted in the reconciliation.

**Grid Columns:**

| **Column**                           | **Description**                                                                                              |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **GLClass**                          | The GL class missing from the model DMAAI table. Blank means the GL class code is missing from the JDE data. |
| **CompanyNumber**                    | The company number associated with the item branch.                                                          |
| **OrderNumber / OrderType / LineID** | Sales order number, type, and line for the associated transfer.                                              |
| **RelOrder / RelType / RelLine**     | Purchase order number, type, and line for the associated transfer.                                           |
| **Branch**                           | The branch plant associated with the item.                                                                   |
| **ShortItem / Item / ThirdItem**     | The three item number formats from JDE.                                                                      |
| **Description**                      | The JDE item description.                                                                                    |
| **Quantity / Amount**                | The current item balance and value from JDE.                                                                 |

**8.4 Report 3 - Order Exclusions**

The Order Exclusions report lists all order pairs that have been excluded for the selected period. Use this report to research any issues and confirm that exclusions were not performed in error.

**Grid Columns:**

| **Column**                     | **Description**                                                         |
| ------------------------------ | ----------------------------------------------------------------------- |
| **CompanyNumber**              | The company number associated with the transaction.                     |
| **ShortAccount / LongAccount** | The In Transit short and long account numbers.                          |
| **PeriodEnds**                 | The period ending date of the transfer, associated with the shipment.   |
| **OrderType / OrderNumber**    | The sales order type and number.                                        |
| **RelType / RelOrder**         | The purchase order type and number.                                     |
| **ShortItem / ItemNumber**     | The JDE short and second item numbers.                                  |
| **Lot**                        | Lot number if lot processing is enabled; otherwise blank (recommended). |
| **UOM**                        | The unit of measure associated with the transaction.                    |
| **InsertDate**                 | The date the exclusion was performed.                                   |
| **Quantity / Amount**          | The current item balance and value from JDE.                            |
| **Note**                       | Any note entered by the user during the exclusion process.              |

**8.5 Report 4 - Transfer Cost Variances**

The Transfer Cost Variances report lists orders where the sales cost or price differs from the purchase order cost. If transferring at cost, the sales cost is compared. If transferring with markup, the sales price is used.

**Grid Columns:**

| **Column**                                | **Description**                                                       |
| ----------------------------------------- | --------------------------------------------------------------------- |
| **CompanyNumber**                         | The company number associated with the transaction.                   |
| **PeriodEnds**                            | The period ending date of the transfer, associated with the shipment. |
| **LongAccount**                           | The In Transit long account number.                                   |
| **ShipCompany / RcptComp**                | The shipping and receiving company numbers.                           |
| **Order / Type / Line**                   | Sales order number, type, and line.                                   |
| **Item / ShipLot / RcptLot**              | Item number and lot numbers for the sales and purchase orders.        |
| **RelOrder / RelType / RelLine**          | Purchase order number, type, and line.                                |
| **ShipBranch / RecBranch**                | Branch plants for the shipment and receipt.                           |
| **SOQty**                                 | The quantity on the sales order.                                      |
| **TransPrc**                              | The transfer cost or price of the item.                               |
| **SOExtCost / SoExtAmt / SOCurr**         | Extended cost, extended price, and currency code on the sales order.  |
| **POQty / POUnitCost / POTotal / POCurr** | Quantity, unit cost, total, and currency code on the purchase order.  |
| **UnitsRec**                              | The number of units received.                                         |
| **UnitPrVar**                             | The variance between the sales price and purchase cost.               |
| **QtyVar**                                | The difference in units shipped versus units received.                |
| **CostMthd**                              | The cost method associated with the item in the receiving branch.     |

**Section 9: How to Reconcile In Transit**

**9.1 Reconciliation Process**

Follow these steps to complete the In Transit reconciliation:

- **Review the Orders page** and perform applicable exclusions. Research each order before excluding it to confirm that no further transactions will occur.
- **Confirm all transfer sales orders** have been processed through the sales update program for the period.
- **Confirm all transfer batches** have been posted to the general ledger.
- **Review unreconciled transactions** and perform any applicable corrective actions.
- **Make an adjusting entry** to bring the In Transit account back into balance. The total entry amount should offset the transaction variance plus any carry forward.
- **Once all tasks are completed**, produce and save a copy of the audit report.
