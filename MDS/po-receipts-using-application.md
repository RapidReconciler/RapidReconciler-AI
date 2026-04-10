**Rapid Reconciler: PO Receipts**

**Training Manual: Using the Application**

**Section 1: PO Receipts Orders Page**

**1.1 Overview**

The Orders page lists all purchase orders - summarized to the order level - where one or more of the following conditions exist:

- **Open Receipts** - A receipt document has yet to be matched with a supplier invoice.
- **Variances** - A receipt or voucher in the receipts table F43121 contains an amount that does not match the corresponding GL entry in the RNV (Received Not Vouchered) account.

**Note:** If an order has been fully received and matched, and everything reconciles, it will automatically be removed from the list.

**1.2 Filtering Results**

Results on the Orders page can be filtered using the drop-downs at the top of the grid. Each drop-down offers a selection of All, Yes, or No:

- **Reconciled** - Show all orders (All), only reconciled orders (Yes), or only unreconciled orders (No).
- **Suspended** - Show all orders (All), only suspended orders (Yes), or only non-suspended orders (No).

**1.3 What Is a Suspension?**

A "suspension" in PO Receipts is equivalent to flagging an order as "Ignore Me." Suspending an order removes its amounts from any out-of-balance and variance calculations.

Common reasons to suspend an order include:

- When the receipts table was loaded into RapidReconciler by date, only the voucher was imported. The order is known to have been processed correctly and the record is simply a start-up issue in RapidReconciler. Suspending it cleans up the display.
- A supplier invoice was processed using standard voucher entry instead of being matched to the PO, leaving a paid receipt showing as open. This can be corrected directly in JD Edwards (preferred) or suspended in RapidReconciler.

**Notes:**

- If an order is suspended in error, it can be unsuspended.
- Suspension permission must be granted to your login ID for the process to be enabled.

**Section 2: Column Definitions - Orders Page**

The following columns are displayed on the Orders page:

| **Column**         | **Description**                                                                                                                                                                                      |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Suspended**      | Checkbox indicating the order has been suspended.                                                                                                                                                    |
| **Note**           | Icon indicating a text note has been entered for the order. Click "Edit Note" to view.                                                                                                               |
| **Company**        | The company number associated with the RNV account.                                                                                                                                                  |
| **Long Account**   | The RNV account number being reconciled.                                                                                                                                                             |
| **Supplier**       | The address book number associated with the PO. An order may show two addresses if landed costs are applied.                                                                                         |
| **Name**           | Name of the supplier on the row.                                                                                                                                                                     |
| **Order**          | Purchase order number.                                                                                                                                                                               |
| **Type**           | Purchase order type.                                                                                                                                                                                 |
| **MostRecReceipt** | The date of the most recent receipt.                                                                                                                                                                 |
| **UnitsRec**       | The number of units received.                                                                                                                                                                        |
| **AmtRec**         | The value of the units received.                                                                                                                                                                     |
| **UnitsVouch**     | The number of units vouchered.                                                                                                                                                                       |
| **AmtVouch**       | The value of units vouchered.                                                                                                                                                                        |
| **UnitsOpen**      | Units that have been received but not yet vouchered.                                                                                                                                                 |
| **AmtOpen**        | Value of units received but not yet vouchered. When Reconciled is set to "All" and Suspended is set to "No," the total of this column matches the "Open Receipt" balance on the Reconciliation page. |
| **RecTotal**       | Total value of all order transactions from the receipts table F43121.                                                                                                                                |
| **GLTotal**        | Total value of all order transactions posted to the general ledger RNV account.                                                                                                                      |
| **Variance**       | The difference between RecTotal and GLTotal. Ideally this is zero. Non-zero values indicate an issue to be resolved.                                                                                 |
| **ExclAmount**     | The exclusion amount for the order (explained in detail separately).                                                                                                                                 |
| **CurrCode**       | The currency code associated with amounts.                                                                                                                                                           |

**Important Reminder:** The reconciliation objective is to ensure that amounts on receipts and vouchers match between the receipts table F43121 and the general ledger. This process does not match vouchers to receipts. A receipt without a voucher constitutes an open receipt, which is displayed to support the "Open Receipts" balance on the reconciliation page.

**Section 3: Line Details**

**3.1 Accessing Line Details**

Line item details are accessed by clicking the **+** sign on the left side of any row on the Orders page.

- Details can be exported to Excel by clicking the green down arrow to the left of the data.
- Unreconciled lines are highlighted in grey.

**3.2 Line Analysis**

Clicking the **Line Analysis** button within the expanded row will navigate directly to the Line Analysis page with the filter information pre-populated. Line Analysis functionality is detailed in Section 5.

**Section 4: Things to Check on the Orders Page**

When reviewing the Orders page, the following checks are recommended:

- Identify the order with the oldest "most recent receipt" date. Confirm whether it is still active or consider closing it in JDE or suspending it in RapidReconciler.
- Set the Reconciled filter to ALL and Suspended to YES. Confirm that all suspended orders genuinely warrant suspension.
- Set the Reconciled filter to NO and Suspended to NO. This displays all orders requiring review.
- Expand line details for any order to identify which lines are unreconciled (highlighted in grey).
- Click the Line Analysis button on an unreconciled line for more detailed information.

To obtain the most accurate "Open Receipts" balance, this order list must be validated before proceeding with the reconciliation process.

**Section 5: PO Receipts Reconciliation Page**

**5.1 Definition and Considerations**

The Reconciliation page is the default page that appears upon logging into the PO Receipts module. This is where all detailed data is summarized. It is important to review each section carefully, as understanding what is displayed here makes working with the supporting details far easier.

**5.2 Status Indicators**

Two status indicators are displayed at the top center of the screen:

- **PO Receipt Validation (Green)** - Ensures the carry-forward amount from the general ledger matches the out-of-balance amount from the previous period. If red, hover the cursor over the indicator for more information.
- **System Status (Green)** - Ensures the import from JD Edwards has completed without error. If red, hover the cursor over the indicator for more information.

**Important:** Both status lights must be green before making any adjustments to the general ledger.

**5.3 Period Selector**

Unlike the Inventory and In Transit modules, there is no period selector for PO Receipts. The reasoning for this is explained in the Key Concepts section of this training.

**5.4 Account Filters**

The account filters operate intuitively using a hierarchy from left to right. Key behaviors include:

- Check items to include in the reconciliation; uncheck to exclude.
- Removing a company will automatically remove its associated business units, objects, and subsidiaries.
- Each column has a search row at the top to filter individual column entries.
- If display issues occur, click the refresh icon in the top right corner.
- Filter selections persist as you navigate between pages within the PO Receipts module.

**5.5 Calculation Section**

The Calculation section provides a quick check to confirm whether the open receipts balance matches the general ledger balance.

| **Field**           | **Description**                                                                                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GL Balance**      | Derived from the F0902 balance table. Should match the trial balance report exactly. Represents the posted GL balance at the time of the last RapidReconciler import.      |
| **Open Receipts**   | Calculated from the receipt table F43121, match type 1 records.                                                                                                            |
| **Out of Balance**  | Difference between GL Balance and Open Receipts. If zero, open receipts are in balance with the general ledger.                                                            |
| **Unreconciled**    | Unreconciled amount details are available on the Orders page via the link.                                                                                                 |
| **Batches**         | Any GL batches waiting to be posted.                                                                                                                                       |
| **Total Variance**  | Sum of Unreconciled and Batches amounts.                                                                                                                                   |
| **Suggested Entry** | Out of Balance minus the Unreconciled amount, excluding any posted batches. Before making any entry, it is highly recommended that unreconciled amounts be resolved first. |
| **Manual Entries**  | Manual adjustments made to the selected account(s).                                                                                                                        |

**5.6 PO Receipts Aging**

The PO Receipts Aging chart is a visual representation of open receipts aging, bucketed by period.

**Section 6: PO Receipts Line Analysis Page**

**6.1 Overview**

The Line Analysis page is accessed from the Orders page by clicking the Line Analysis button on the left side of the grid. This action navigates to the Line Analysis page with filter data pre-populated for the selected order.

**Note:** Clicking the Line Analysis link in the Main Navigation pane will not populate or update the filter data and may cause confusion. It is always best to click the button on the Orders page to access precise PO data.

**6.2 Edit Note Button**

The Edit Note button is used to:

- Exclude a document (receipt or voucher) from variance calculations.
- Add a note for future reference or audit purposes.

**Procedure:**

- Click on the grid row(s) to be edited.
- Type in the text box to add a note.
- Check the Excluded box to remove amounts from variance after a recalculation or nightly refresh.
- Click Save when finished.

**Note:** If an exclusion is made in error, unchecking the box will reinstate the document in calculations. Exclusion permission must be granted to your login ID for this process to be enabled.

**6.3 Document Button**

The Document button displays a pop-up list of all documents associated with the PO line being analyzed. Data is combined from the receipts table F43121 and the GL table F0911.

Key column definitions:

| **Column**       | **Description**                                                                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cutoff Date**  | The earliest date considered when importing data. RapidReconciler does not import all historical data - it is limited by date.                        |
| **Capture Date** | The date the data was imported into RapidReconciler. The further this is from the cutoff date, the less likely a discrepancy is caused by the cutoff. |
| **Variance**     | The difference between the F43121 amount and the GL amount by document.                                                                               |

Document data can be exported to Excel by clicking the green export button in the bottom right corner.

**6.4 Filter Drop-Downs - Exc, Rec, and Doc**

These drop-downs filter the grid rows on the Line Analysis page:

- **Exc (Excluded Docs):** ALL = Show all documents; YES = Show only excluded documents; NO = Show only unexcluded documents.
- **Rec (Reconciled Docs):** ALL = Show all documents; YES = Show only reconciled documents; NO = Show only unreconciled documents.
- **Doc:** An individual document may be selected from the list.

**6.5 Account, PO Data, and Query Button**

This filter data is pre-populated when navigating from the Orders page. It can be manually adjusted as needed.

**Helpful Trick:** Changing the line number to 0 and clicking the Query button will display data for all lines on the PO. This is extremely helpful when diagnosing variance. The Document button will then display all documents for the entire purchase order.

**6.6 Recalc and Export Buttons**

- **Recalc** - Recalculates variances after documents have been excluded. Results are available within a few minutes. A gear icon will appear in the top right corner while the recalculation is running.
- **Export** - Grid data may be exported to Excel by clicking the export button (down arrow).

**6.7 Documents Grid Overview**

The Documents Grid lists all transactions for the PO line(s) being filtered. Each document is split by data source - receipts table F43121 and general ledger table F0911. Reconciled rows are displayed in light color; unreconciled rows appear in grey.

For a side-by-side comparison of receipts and GL data, click the Documents button.

**Section 7: How to Reconcile PO Receipts**

**Step 1 - Validate the Open Amount**

Reconciling the RNV (Received Not Vouchered) account depends heavily on the value of Amount Open on the Orders page.

- Set the Reconciled and Suspended filters as follows: Reconciled = All; Suspended = No. This displays all orders contributing to the Open Receipts amount on the reconciliation page, including both reconciled and non-reconciled orders.
- Review the order listing to ensure accuracy. Focus especially on older orders. Sort by the most recent receipt date column to identify candidates for review.
- If an order is found to be on the list in error, either make the appropriate correction in JD Edwards or suspend the order in RapidReconciler.

**Step 2 - Make Any Necessary Adjustment**

When adjusting the GL balance, consider the following:

- The GL balance comes directly from table F0902 and will match JD Edwards exactly.
- The Open Receipts balance should match any Open Receipts report obtained directly from JD Edwards. Resolve any discrepancies first. Timing is important - RapidReconciler updates once a day, so any JD Edwards report used for comparison should be run at approximately the same time.
- The Suggested Entry is the Out of Balance amount, excluding any unreconciled orders or unposted batches.
- Determine whether to work the Unreconciled orders before or after closing the period. Once decided:
  - a. Work the Unreconciled orders to zero. Refer to the next section for details.
  - b. Ensure all batches have been posted accordingly.
  - c. Adjust the GL balance:
    - i. To include any Unreconciled orders, use the Out of Balance amount.
    - ii. To temporarily exclude variances, use the Suggested Entry amount.

**Section 8: Working Unreconciled Purchase Orders**

**8.1 Display Unreconciled Orders**

Click the Unreconciled link on the Reconciliation page. This displays the Orders page with filters preset to: Reconciled = No; Suspended = No.

**8.2 Select the Order to Work**

Expand the order by clicking the **+** icon on the left of the row. This displays each line that has an open receipt amount or a variance. Once expanded, the icon changes to a **-**.

Unreconciled lines are displayed in grey; reconciled lines are displayed in white. Click the Line Analysis button for the line to be analyzed to navigate to the Line Analysis page with filters pre-selected.

**8.3 Perform Order/Line Analysis**

On the Line Analysis page:

- The page displays unreconciled documents only by default. To view all transactions, change the Rec filter to ALL and the Line filter to 0, then click Query.
- Note that rows are separated by data source - data from receipts table F43121 and GL table F0911 appear on separate rows for the same transaction document.
- For a side-by-side comparison, click the Document icon to the right of the Edit Note button.
- Review the Documents pop-up. The Variance column will indicate which documents have discrepancies between F43121 and F0911 amounts.
