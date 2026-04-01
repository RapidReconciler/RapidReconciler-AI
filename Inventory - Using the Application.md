**Rapid Reconciler Inventory**

**Training Manual: Using the Application**

**Section 1: Inventory Reconciliation Page**

**1.1 Overview**

The Reconciliation page is the default page that appears when you first log into the application. This is where detailed data is summarized and where the majority of your time will be spent. It is important to review each section carefully, as a thorough understanding of what is displayed here makes working with the supporting details significantly easier.

**1.2 Status Indicators**

Two status indicators are displayed at the top center of the screen. Green indicates success; red indicates an issue that must be resolved. If the System Status light is flashing yellow, the JDE import is still in process. Both lights must be green before making any adjustments to the general ledger.

| **Indicator**            | **Description**                                                                                                                                                 |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Inventory Validation** | Ensures the carry-forward amount matches the out-of-balance amount from the previous period. If red, hover your cursor over the indicator for more information. |
| **System Status**        | Ensures the import from JD Edwards has fully completed without error. Hover your cursor over the indicator for more information.                                |

**1.3 Period Selector**

The period selector is located in the top right corner of the window and is used to select the period to be reconciled. Key behaviors include:

- The periods displayed in the drop-down depend on the reconciliation start date configured by your administrator.
- New periods are automatically added based on new cardex transactions entered in JD Edwards.
- The period selection remains in place as you navigate across pages within the perpetual inventory module.
- It is recommended that a purge be performed if there are more than 14 periods of data. Contact your RapidReconciler administrator to request a purge.

**1.4 Using the Account Filters**

The account filters operate intuitively using a hierarchy from left to right. Key behaviors include:

- Check the items to be included in the reconciliation; uncheck to exclude.
- Removing a company will automatically remove its associated business units, objects, and subsidiaries.
- Each option has a search row at the top. Begin typing in the field to filter the individual column.
- If there are issues with the items being displayed, click the refresh icon in the top right corner.
- Filter selections persist as you navigate to different pages within the inventory module.

**Section 2: Valuation Section**

**2.1 Overview**

The Valuation section provides a quick check to confirm whether the perpetual inventory balance for the selected period matches the balance in the general ledger. The totals displayed will depend on the filter selections and period chosen.

| **Field**             | **Description**                                                                                                                                                               |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GL Balance**        | Derived from the F0902 balance table. Should match the trial balance report exactly.                                                                                          |
| **Perpetual Balance** | A summarized cardex total calculated from the balance forward records in RapidReconciler.                                                                                     |
| **Out of Balance**    | If this total is zero, inventory is in balance with the general ledger. Any non-zero amount represents variance that will be broken down in the Variance Calculation section. |

**Section 3: Variance Calculation**

**3.1 Overview**

The Variance Calculation section lists and quantifies all sources of variance. Each non-zero amount should be reviewed. The sum of all variances matches the out-of-balance amount shown in the Valuation section, confirming that all items are accounted for.

**3.2 Variance Sources**

- **Carry Forward** - The out-of-balance amount carried forward from the prior period. Return to the prior period to resolve, or offset with a manual journal entry in the current period if needed.
- **GL Batches** - GL batches that need to be posted. Work with the finance department to get these batches posted.
- **End of Day** - Work orders or sales orders that have not been processed to the general ledger. Get orders processed through manufacturing accounting or sales update.
- **Transactions** - Completed transactions with a discrepancy between the item ledger and the general ledger. These require an offsetting manual journal entry.
- **Cardex** - Items where the summarized cardex does not match the quantity or amount on hand. Quantity variances require an IT SQL correction. Amount variances require a dollars-only adjustment.
- **Manual Journal Entries** - Any manual entries made to the account(s) to correct out-of-balance amounts.

**3.3 GL Batches - Additional Information**

The GL Batches variance represents entries in the general ledger detail table F0911 where the posted code flag is not "P," meaning the detail line is not posted. Note that this may conflict with the batch header status, or the batch header itself may be missing.

If items appear in this list and the batch header cannot be located for posting, run the "Missing Batch Header" report provided by JD Edwards. The header must be rebuilt and the batch reposted to clear these entries.

**3.4 End of Day - Additional Information**

End of Day variances are item ledger records that do not contain a batch number. Ship confirmations, material issues, and completions generate item ledger records that initially do not have a batch number or GL date. These values are populated when the sales update program or manufacturing accounting program is run, typically once each night.

RapidReconciler uses the item ledger batch number to determine whether the transaction has been properly booked to the general ledger. If these programs complete successfully, the batch number and GL date are updated in the cardex, and the transaction will drop off the list after the next RapidReconciler refresh cycle.

**3.5 Transaction Variance - Additional Information**

Transaction variance is the difference in amounts between an item ledger (cardex) transaction and its corresponding entry in the general ledger. Transactions are matched based on the following fields: company number, account number, fiscal period, document type, document number, order number, and batch number. A difference in any one of these fields results in a mismatch, which may display on the grid as two rows.

**3.6 Cardex Variance - Additional Information**

Cardex variance is the result of an item's summarized cardex transactions not adding up to the balance in the item balance table. Refer to the Key Concepts training module for detailed information on analysis and correction.

**Section 4: Supporting Widgets**

**4.1 Drill Down Widget**

The Drill Down widget provides a visual aid for identifying where the largest out-of-balance amounts exist. This is especially useful in multi-company organizations with many business units being monitored.

- The chart follows the hierarchy of the account filters. The default starting point is the currency code.
- The legend on the right displays the items being shown.
- Hovering over a section of the chart displays the item name and variance amount.
- Clicking on a chart section drills down to the next level.
- The back arrow returns to the previous level.
- Filter selections automatically update as you click through levels.
- If there is no variance, no chart will be displayed.

**4.2 Offset Account Widget**

The Offset Account widget is represented by a star icon that appears when hovering over the End of Day or Transactions row in the Variance Calculation section. Clicking the icon opens a pop-up window listing the company, period, inventory account, and the offset account to be used for the applicable variance. The data can be exported to Excel and copied into the JD Edwards journal entry screen.

The exported data contains the following elements:

- **je_account column** - Contains one row for the perpetual inventory side, one row for "Tolerance Adjust," and one or more rows for any remaining variance.
- **Tolerance Adjust** - Accounts for the tolerance setting applied to transaction variances below 1 monetary unit. These rounding amounts still require adjustment.
- **TBD** - The default placeholder for any remaining variance. The administrator can configure specific offset accounts for different transaction types (e.g., sales order variances to COGS, manufacturing variances to WIP). When configured, the proper accounts will display in the data set.

**Note:** After exporting the data to Excel, manually replace "Tolerance Adjust" and "TBD" cells with the applicable GL account numbers, then copy the two rightmost columns and paste into JD Edwards. This feature is designed for use during the close. Entries made mid-period are not taken into account.

**4.3 Out of Balance History Graph**

The Out of Balance History graph displays variance trends over time.

- The most recent 14 period ending dates are displayed. If fewer than 14 periods exist, all available data is shown.
- A system in perfect balance would show all periods at \$0.
- Hovering over an individual period displays the date and variance total.
- Clicking on a data point changes the period filter to that period end date.

**4.4 Journal Entry Button**

Clicking the Journal Entry button produces an Excel report of the GL and perpetual balances for the selected accounts and single period. This is used to make journal entries at the account level when a more detailed review is not required.

**4.5 Audit Report Button**

The Audit Report documents the reconciliation results for the period being analyzed. The report contains the following sections:

| **Section**                | **Description**                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| **Accounts Summary**       | The valuation and variance calculation summary for each account.                           |
| **Unposted GL Batches**    | Details for any remaining unposted GL batches.                                             |
| **End of Day**             | Lists any remaining work orders or sales orders awaiting processing.                       |
| **Manual Journal Entries** | Lists any manual entries made to the account.                                              |
| **Variances**              | Lists transaction variances that occurred in the period, including any user-entered notes. |
| **Perpetual Details**      | A list of item balances and values at the end of the selected period.                      |

The report may be output in Excel or PDF format. You will be prompted to select a format after clicking the button.

**Important:** It is highly recommended that an audit report be produced and saved at the end of each period, as detail data may be removed during a purge.

**Section 5: Inventory Transactions Page**

**5.1 Overview**

The Transactions page lists documents where the data in the item ledger F4111 does not match the data in the general ledger F0911, per the matching criteria covered in the Key Concepts training. Only reconciling items are displayed. Any transaction that has been internally reconciled will not appear. Reviewing the transaction detail report is typically performed by a JDE business analyst or someone with a similar skill set.

**5.2 A Note About Rounding and Tolerance**

Due to decimal precision and other system factors, many transactions may fail by a penny or other very small amount. Displaying every such transaction could cause significant issues to become lost in the volume of data. RapidReconciler is designed with a tolerance setting that defaults to 1, meaning any transaction variance of less than 1 monetary unit will not be displayed.

**Important:** These sub-tolerance variances are still counted toward the total out-of-balance amount. As a result, the total shown on the Transactions line in the Variance Calculation section may differ slightly from the total displayed on the Transactions page. The tolerance setting may be changed by the RapidReconciler administrator if greater precision is required.

**5.3 Filters**

Filters are used to focus the variance investigation on specific types of transactions. The following filter types are available:

| **Field**         | **Description**                                                                                                                                                                         |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**          | Inventory, Sales, Manufacturing, or Purchasing - based on the batch type associated with the document.                                                                                  |
| **Sub Type**      | A value assigned by RapidReconciler. Options include: Accounts (account number mismatch), Periods (fiscal period mismatch), Transfers, Intercompany, Direct Ship, and Voucher Variance. |
| **Order Type**    | The JD Edwards order type of the transaction.                                                                                                                                           |
| **Document Type** | The JD Edwards document type of the transaction.                                                                                                                                        |

**Note:** It is recommended that direct ship orders be set to clear through a non-perpetual account.

**5.4 Subtotals**

The Subtotals widget works in conjunction with the filters to help prioritize which transactions to investigate. The widget contains four columns:

- **Column 1** - Defaults to "Type" but is selectable via the drop-down. Options include Type, Sub Type, Order Type, and Document Type.
- **Column 2** - The total cardex (F4111) amount for the rows being displayed.
- **Column 3** - The total GL (F0911) amount for the rows being displayed.
- **Column 4** - The variance between the cardex and GL amounts.

**5.5 Edit Notes and Worked Transactions**

Manual notes can be added to transactions in the grid to document corrective actions taken. These notes will appear on the period-end audit report.

Best practices for notes:

- Include your name and the date within the body of the note text.
- Notes can be deleted after the fact if necessary.
- Additional notes can be added to the same transaction at any time.

Flagging a transaction as "Worked" allows it to be filtered off the grid. This does not change variance totals or permanently remove transactions. The corrective action for any transaction on this page is an offsetting manual journal entry in JD Edwards, along with a note entry in RapidReconciler for audit purposes.

**5.6 Grid Column Definitions**

| **Column**                                                        | **Description**                                                                                              |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Worked**                                                        | Checked indicates the transaction has been cleared via the Edit Notes process.                               |
| **Note**                                                          | Hover to view any note that has been added.                                                                  |
| **Company Number**                                                | The company number associated with the transaction.                                                          |
| **Long Account**                                                  | The account number associated with the transaction.                                                          |
| **Offset Account**                                                | The account to be offset with the variance amount. Requires administrator setup. Default = "TBD".            |
| **Type**                                                          | Transaction type based on the JD Edwards batch type.                                                         |
| **Sub Type**                                                      | A value assigned by RapidReconciler.                                                                         |
| **Document Type**                                                 | The JD Edwards document type.                                                                                |
| **Document Number**                                               | The JD Edwards document number.                                                                              |
| **Order Type**                                                    | The JD Edwards order type.                                                                                   |
| **Order Number**                                                  | The JD Edwards order number.                                                                                 |
| **Cardex Amount**                                                 | The total from F4111.                                                                                        |
| **Ledger Amount**                                                 | The total from F0911.                                                                                        |
| **Variance**                                                      | Ledger Amount minus Cardex Amount.                                                                           |
| **Comment**                                                       | Helpful information provided by RapidReconciler.                                                             |
| **Currency**                                                      | The currency code of the transaction.                                                                        |
| **Batch Type**                                                    | The JD Edwards batch type.                                                                                   |
| **Batch Number**                                                  | The JD Edwards batch number.                                                                                 |
| **Period Ends**                                                   | The period ending date assigned by the date logic algorithm.                                                 |
| **Transaction Date**                                              | The creation date from the cardex, or the GL date for GL-only transactions.                                  |
| **Rel Type / Rel Order**                                          | The related order type and number, if applicable.                                                            |
| **Orig Comp / Orig Order / Orig Type / Orig Doc / Orig Doc Type** | Original company, order, type, document, and document type, if applicable.                                   |
| **GL Xref**                                                       | The matching document in the GL. Normally the same as the item ledger, except for work orders.               |
| **Group Code**                                                    | Concatenates codes from intercompany and transfer orders to allow related documents to be filtered together. |

**5.7 Producing a Transaction Detail Report**

Details for a specific transaction are accessed by clicking the **+** icon at the far left of the applicable grid row. Results are based on the company number, document type, and document number - the account, period, and order information are not passed, resulting in a complete data set for analysis.

The transaction detail report is organized into six sections:

| **Section**                        | **Description**                                                                                                                                                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Section 1 - Unassigned Account** | Lists cardex transactions with a GL class code not referenced in the model DMAAI table. If the item is a stock item, the GL class must be added to the model table. This section will not appear if all cardex records have stock GL class codes. |
| **Section 2 - F4111 Cardex**       | All F4111 rows for the selected company, document type, and document number.                                                                                                                                                                      |
| **Section 3 - F0911 GL**           | All F0911 rows for the selected company, document type, and document number. For work orders, the sub-ledger field and work order cross-reference table F3106 are also considered.                                                                |
| **Section 4 - RapidReconciler**    | Shows how RapidReconciler matches and summarizes the transaction data. One row indicates matching criteria are met; multiple rows indicate a mismatch.                                                                                            |
| **Section 5 - Order Data**         | For PO receipts and sales order shipments, contains all lines for the associated order. For intercompany orders, includes related order information.                                                                                              |
| **Section 6 - DMAAs**              | Lists all DMAAI entries for each GL class code in the transaction. The first row is from the model table.                                                                                                                                         |

**5.8 Analyzing the Transaction Detail Report**

Analyzing a failed transaction requires a thorough understanding of JD Edwards and is typically performed by a business analyst. The following tips are useful when reviewing the report:

- **Matching Criteria** - Verify that the company number, account number, and period ending date match for each row in Sections 2 and 3. Section 4 will show multiple rows if they do not.
- **Single-Sided Transfers** - "IT" transactions where the cardex shows only the "from" side without the "to" side. The GL will properly net to \$0.
- **Order Information Review** - Confirm that the unit cost for the item on the order matches Section 2. For sales orders, verify that the quantity shipped on the order line matches the quantity shipped in the cardex.
- **DMAAI Review** - If the account number in GL Section 3 differs from the account assigned in cardex Section 2, consult the DMAAI set up in Section 6 to determine the cause.

**Reminder:** The corrective action for any item on the Transactions page is an offsetting journal entry in JD Edwards and a note entry in RapidReconciler, as the transaction has already been completed and documentation is required for audit purposes.

**Section 6: Inventory As-Of Page**

**6.1 Overview**

The As-Of page provides a detailed listing of all branch plants, items, lots, and locations for the companies and accounts selected in the reconciliation page filters. It serves as the supporting detail for the perpetual balance amount shown in the Valuation section.

**Note:** Small differences between the As-Of page totals and the perpetual balance are common due to rounding and items with zero quantity and zero amounts. Large differences should be investigated.

The amounts shown on this page are calculated by summarizing cardex F4111 records from the balance forward set in RapidReconciler during installation. They are not a snapshot of item balances multiplied by unit costs. As a result, items may appear with an associated value but no quantity - this is the reason JD Edwards has a "zero balance adjustment" routing built into certain inventory transactions.

**Note:** If a value of -9999 is shown in the Quantity on Hand column, a UOM conversion factor is missing and RapidReconciler cannot properly roll up the quantities. This has no impact on amounts. Refer to the Integrity Report 4 training for further details.

**6.2 Impact of GL Class Code Changes**

Improperly changing a GL class code in JD Edwards without an intermediate inventory adjustment can result in multiple rows on the As-Of grid. The correct procedure is to:

- Adjust the inventory quantity to zero under the original GL class code.
- Change the code on the branch, locations, and open orders.
- Adjust the inventory back in under the new GL class code.

This ensures the value moves correctly from one account to the other in both the cardex and the general ledger.

**6.3 Grid Column Definitions**

| **Column**                                       | **Description**                                                                                       |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| **CompanyNumber**                                | The company number associated with the GL account.                                                    |
| **BranchCompany**                                | The company number associated with the branch plant. Typically the same as the company number.        |
| **LongAccount**                                  | The long account number assigned from the model DMAAI table.                                          |
| **Currency**                                     | The base currency code for the company number.                                                        |
| **Branch / BranchDesc**                          | The branch plant code and description from JDE.                                                       |
| **ShortItem / ItemNumber / ThirdItem**           | The three item number formats from JDE.                                                               |
| **Description**                                  | The item description from the item master.                                                            |
| **CurrCost**                                     | The current item cost from the cost ledger. This value is the same regardless of the period selected. |
| **UOM**                                          | The primary unit of measure from the item master.                                                     |
| **CalcCost**                                     | A calculated cost derived from Amount divided by Quantity on Hand. Zero if no quantity exists.        |
| **Location / Lot / Lot Status / Lot Expiration** | Location and lot details from JDE.                                                                    |
| **Quantity**                                     | The calculated quantity on hand in primary unit of measure.                                           |
| **Amount**                                       | The calculated amount on hand in base currency.                                                       |
| **GLClass**                                      | The GL class at the location/lot level.                                                               |
| **ST / CM**                                      | Stocking type and cost method.                                                                        |
| **Material / Labor / Overhead**                  | Cost components by type (A, B, and all others).                                                       |
| **QtyVar**                                       | Quantity variance between summarized item ledger F4111 and item balance F41021.                       |
| **AmtVar**                                       | Amount variance between summarized item ledger extended cost F4111 and on-hand amount.                |
| **Sales01-Sales10 / Purch01-Purch10**            | Sales and purchase category codes.                                                                    |

**6.4 Item Filters**

Reports can be filtered by item, branch, location, or lot by entering a value into the applicable filter field and clicking the green filter button. Each filter uses "starts with" functionality. A "Filters Applied" message will appear with a link to clear the filters when active.

**6.5 Filtered Totals**

| **Total**           | **Description**                                                                                                                                    |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Units**           | The quantity and monetary totals for all items currently displayed in the grid.                                                                    |
| **Cardex Variance** | A measure of accuracy between the summarized item ledger F4111 and item balance F41021. Small amounts are common, particularly in 24/7 operations. |

**6.6 Daily As-Of Drop-Down Selector**

Clicking the Daily As-Of drop-down produces a list of individual days within the selected period, in accordance with the fiscal calendar. Selecting an individual day changes the grid to show that day's ending inventory.

**Note:** If a day other than the period end is selected, the perpetual total on the Reconciliation page will not match the As-Of page totals. Ensure the filter is cleared before making that comparison by selecting the blank line at the top of the drop-down.

**6.7 Common Units of Measure**

Common units of measure can be configured by the RapidReconciler administrator to restate quantities in a single unit across all items. Once a common UOM is selected from the drop-down, two additional columns will appear on the far right of the grid:

- **CommonQty** - The quantity converted to the common unit of measure. If no conversion factor is set up in JDE, this field will be empty.
- **CommonUOM** - The common unit of measure selected. This value is the same in all rows.

**6.8 Summarize by Item**

The Summarize by Item button changes the display from branch/item/location/lot level to branch/item level, summarizing all locations and lots into a single row. This results in a smaller data set and nets out items with offsetting positive and negative quantities.

Things to note when using this toggle:

- Most grid columns will not be available, as detailed rows may contain different values.
- Access to cardex transaction details (the + sign) will be removed.
- Daily As-Of and Common UOM functionality will continue to operate normally.
- Clicking the button again restores the original level of detail.

**6.9 Cardex Transaction Details**

Individual cardex transactions that make up the balance can be accessed by clicking the **+** sign at the left of any row. The expanded grid shows the cardex details, which may be exported to Excel for analysis.

| **Column**                               | **Description**                                                            |
| ---------------------------------------- | -------------------------------------------------------------------------- |
| **CompanyNumber**                        | Company number of the transaction.                                         |
| **LongAccount**                          | GL account assigned from the model DMAAI table.                            |
| **UKID**                                 | Unique Key ID from JDE. Data is sorted in reverse order.                   |
| **Branch / ItemNumber / Location / Lot** | Branch plant, item number, location, and lot of the transaction.           |
| **GLClass**                              | GL class code. Check for changes.                                          |
| **Transdate**                            | The creation date of the transaction.                                      |
| **PeriodEnds**                           | The period ending date based on RapidReconciler date logic.                |
| **Comm**                                 | Comment. Contains row labels.                                              |
| **Runqty / RunAmt**                      | Running quantity and amount, summarized from the bottom up.                |
| **DT / Doc**                             | Document type and number.                                                  |
| **Qty / UOM**                            | Quantity in primary unit of measure and the unit of measure.               |
| **Cost / Val**                           | Unit cost and extended cost from the F4111 record.                         |
| **QtyVar / AmtVar**                      | Quantity and amount variance between F4111 total and current F41021 total. |

In addition to individual transactions, a balance forward row appears at the bottom of the report and a current balance row appears at the top.

**Section 7: Inventory Roll Forward Page**

**7.1 Overview**

The Roll Forward page lists item activity within a specified date range. Document and order types are assigned to report columns by the RapidReconciler administrator. This page requires ongoing maintenance if new document types or order types are added in JD Edwards.

**Note:** This report is provided as an information source and is not part of the normal reconciliation process. Its use is optional.

**7.2 Using the Roll Forward Report**

Follow these steps to generate the Roll Forward report:

- **Step 1** - Select the period end date in the top right corner. This acts as the ending date for the analysis.
- **Step 2** - Select the start date from the drop-down. A list of period start dates prior to the ending date will be displayed. Data will appear at this point.
- **Step 3** - If needed, add a common unit of measure as defined in the As-Of page training.
- **Step 4** - To view results in amount instead of quantity, change the "Type" drop-down.
- **Step 5** - If new document or order types have been added to the configuration since the report was last run, click the "Reset Table Changes" button to clear the cache.

**7.3 Validating the Roll Forward Report**

The Roll Forward report is validated by reviewing the Variance column on the far right of the grid. This column shows the difference between the closing balance and the sum of all preceding columns. Sort the data by clicking the column header to identify any non-zero quantities - sort in both directions to ensure accuracy. If any non-zero values exist, the report configuration must be reviewed. Contact the RapidReconciler administrator to check for any new document or order types that may need to be added.

**Section 8: Inventory Integrity Reports**

**8.1 Overview**

The perpetual inventory integrity reports are designed to identify potential discrepancies in the JD Edwards system setup that could lead to reconciling items. These reports should be reviewed and acted upon when RapidReconciler is first installed and then checked periodically thereafter.

Reports are accessed by clicking the "Select Report" drop-down box. Ensure you are logged in to RapidReconciler and can view your actual data while reviewing each report.

**8.2 Report 0 - JDE DMAAs**

This report is used primarily for debugging items listed on the Transactions page. It provides a quick method of analyzing DMAAI configuration through filtering, sorting, and Excel export. Flex accounting for inventory is supported. JDE data comes from tables F4095 and F4096.

**Note:** This report is used for researching configuration and does not need to be part of the periodic review.

**Grid Columns:**

| **Column**                      | **Description**                                                                      |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| **CompanyNumber**               | Company number from JD Edwards.                                                      |
| **System**                      | Assigned by RapidReconciler: Inventory, Purchasing, Manufacturing, Sales, or Other.  |
| **Type**                        | Assigned by RapidReconciler: Inv (inventory) or Exp (expense).                       |
| **TableNumber**                 | DMAAI table number from JD Edwards.                                                  |
| **OrderType**                   | Order type from JDE table F4095.                                                     |
| **DocType**                     | Document type from JDE table F4095.                                                  |
| **GLClass**                     | GL class from F4095. Value "\*\*\*\*" is a wildcard meaning all GL class codes.      |
| **Cost Type**                   | Cost type from JDE table F4095.                                                      |
| **BusinessUnit / Object / Sub** | Account fields from JDE table F4095.                                                 |
| **BUFlex / SubFlex**            | Indicates whether flex accounting is used for business unit or subsidiary.           |
| **BUSource / SubSource**        | Source of the business unit or subsidiary value: Hard Coded, Branch, or Table/Field. |

**8.3 Report 1 - Model AAI Table**

**Important:** This report must be reviewed for accuracy before using RapidReconciler to make GL adjustments. Verify that each GL class code has the proper business unit, object, and subsidiary specified. Integrity Report 3 can be used to identify any missing codes. Corrections must be made in JD Edwards and will appear after the next refresh cycle.

The Model AAI Table report lists entries in DMAAI table 4152 for the document type specified in the company setup. It is used during data import to assign each item ledger transaction and item balance record a GL account number based on the company number of the branch plant and GL class code. If using landed costs, those GL class codes must be included in the model table.

Grid columns are the same as Report 0, with the addition of **FlexBU** and **FlexSub** in place of **BUFlex** and **SubFlex**.

**8.4 Report 2 - DMAAI Entry Integrity**

**Important:** Each exception listed should be reviewed to determine if the DMAAI entry should be changed. Review this report each month, as system changes may occur at any time.

The DMAAI Entry Integrity report compares entries in the model table to other balance sheet DMAAI tables. The balance sheet tables reviewed are: 3110, 3130, 4122, 4126, 4134, 4172, 4240, and 4310.

The report identifies and lists the following exceptions by company number and GL class code:

- **Business Unit Mismatch** - The business unit in the table being analyzed does not match the business unit in model table 4152.
- **Object Account Mismatch** - The object account does not match model table 4152.
- **Subsidiary Mismatch** - The subsidiary does not match model table 4152.
- **Net Zero Accounts** - The debit and credit DMAAs for a given transaction reference the same account, resulting in no GL impact.

**8.5 Report 3 - Excluded GL Classes**

**Important:** This report should be reviewed each month for changes.

The Excluded GL Class report lists items where the GL class code is missing from model DMAAI table 4152. Any value for items listed here will not be counted in the reconciliation. For each item shown, verify:

- The proper GL class code is assigned to the item.
- The GL class should not count in the valuation (e.g., non-stock or expense items tracked for quantity purposes).
- The GL class is added to the model table if it should be counted in the reconciliation.

**Note:** Setting up document type "98" with entries in model table 4152 will prevent specified GL class codes from displaying. Use with discretion, as hiding entries may obscure items with incorrect GL class assignments.

**8.6 Report 4 - UOM Conversion Integrity**

**Important:** This report should be part of the monthly review process.

This report identifies items that have transaction units of measure in the item ledger (F4111) that differ from the current primary unit of measure, where RapidReconciler cannot find a conversion factor between the two.

RapidReconciler reads conversion tables from JDE and supports conversions up to 3 levels deep in either direction. It is best practice to add direct conversions to JDE for any items appearing on this list. The row will clear after the next refresh cycle once a conversion factor is in place.

The impact of a missing conversion factor is that the quantity on hand on the As-Of page cannot be rolled up properly. In this event, the quantity is replaced with a placeholder value of -9999.

**8.7 Report 5 - GL Class Integrity**

**Important:** This report should be part of the monthly review process.

The GL Class Integrity report lists items where the GL class code from the item branch record (F4102) does not match the GL class code in one or more associated location/lot records (F41021). Although this is sometimes intentional, it is more commonly desirable for these values to match.

RapidReconciler cannot determine which value is correct - the business must determine the proper value and make the necessary corrections in JD Edwards. The record will clear once the codes match and the data is refreshed.

**8.8 Report 6 - Frozen Cost Integrity**

**Important:** This report should be part of the monthly review process.

The Frozen Cost Integrity report lists items where the frozen cost in table F30026 does not match the ledger "07" cost in F4105. This can occur if ledger costs are manually overridden or improperly copied between branch plants. Corrections are made by having the item re-rolled by cost accounting.

**8.9 Report 7 - Duplicate Item Costs**

**Note:** This report will not contain data unless the RapidReconciler import fails due to cost data issues. A notification alert will be sent to users upon login directing them to review this report.

The Duplicate Cost Integrity report lists items where more than one cost method is designated as the "Inventory" valuation cost. RapidReconciler cannot determine which cost to use in this scenario and the import will fail. An alert is sent to users upon login.

Corrective action:

- Alert the IT department to use database tools to correct the issue, or
- In JD Edwards, navigate to the cost revision screen and change the Sales/Inventory value from its current setting to another value, then change it back.

The next RapidReconciler data refresh will proceed normally once the issue is resolved.

**8.10 Report 8 - Duplicate Sales Integrity**

**Note:** This report will normally not contain data. Duplicates are usually caused by system failures during sales update or other batch processes.

A sales order line number in JDE can only be ship-confirmed once. This report lists sales lines that appear in the item ledger table (F4111) more than once, excluding standard cost changes.

Corrective actions include cycle counting the affected items and making the appropriate manual journal entries. Rows on this report cannot be cleared by transactions in JDE. Date constraints can be added to the view to eliminate old data. Contact <rrsupport@getgsi.com> for assistance.

**8.11 Report 9 - Clean Cutoff Integrity**

**Note:** This report is for informational purposes. Review details to identify opportunities to improve batch job schedules.

The Clean Cutoff report lists items where the fiscal period associated with the creation date of the item ledger transaction does not match the fiscal period associated with the GL date of the transaction. Mismatches in period indicate that an accrual may be necessary to accurately state the inventory balance. Wherever possible, transactions should be posted to the GL in the same fiscal period in which the inventory quantity is changed.

**8.12 Report 10 - Items Missing Branch Records**

**Note:** This report will normally not contain data. Entries are typically due to inadvertent data purges.

The Items Missing Branch Records report lists items that have a quantity in the item balance table F41021 but no associated item branch record in table F4102. This represents a severe data integrity issue and is rare.

**Section 9: How to Reconcile Perpetual Inventory**

**9.1 Considerations**

Steps 1 and 2 below should be performed either daily or weekly, depending on business needs, outside of the closing process. Steps 3 and 4 should be performed as part of the period-end close.

**9.2 Step 1 - Select the Applicable Data Set**

- Log in to RapidReconciler.
- Confirm that both status lights are green.
- Select the period to be reconciled.
- Filter the applicable companies and accounts.

**9.3 Step 2 - Evaluate the Data**

- Review the Valuation section. If the out-of-balance amount is zero, inventory is fully reconciled. If not, proceed to the next step.
- Review the Variance Calculation section for sources of variance and address each non-zero amount:
  - **Carry Forward** - Address in the prior period or include in the month-end journal entry.
  - **GL Batches** - A bell icon indicates unposted batches greater than 2 days old. Review the details and investigate the cause. No bell icon means batch postings are current.
  - **End of Day** - A bell icon indicates open orders greater than 2 days old. Review the details and investigate the cause. No bell icon means sales update and/or manufacturing accounting orders are current.
  - **Transactions** - Navigate to the details, review the data, perform any preventative measures, and add notes to the transactions for audit purposes.
  - **Cardex** - Look for large item-level variances in the details and perform corrective actions as detailed in the Key Concepts training.

**9.4 Step 3 - Perform Closing Activities**

- Confirm the period being closed has no GL batch amount.
- Confirm the period being closed has no End of Day amount.
- Perform a final review of the transactional variance. Make any required adjusting entries using one of the following methods:
  - The Journal Entry button for account-level amounts.
  - The Offset Account icon for transaction-level amounts.
  - Manual calculations per business requirements.
- Include any carry-forward amounts in the manual entry as required.

The unreconciled variance should be zero once all entries have been made and the data has been refreshed. Once complete, produce the audit report and save it to a dedicated folder.

**9.5 Step 4 - Review Integrity Reports**

Review Integrity Reports 2 through 6 and apply any applicable updates. Detailed instructions are included in the individual integrity report training sections above.