**Rapid Reconciler PO Receipts**

**Training Manual: Key Concepts**

**Section 1: Definition**

**PO Receipts, also known as "Received-Not-Vouchered" (RNV), is a balance sheet liability that accounts for goods and services received against a purchase order.**

**Important Distinction: PO Receipts should not be confused with an "Open PO," which refers to a purchase order or line where not all items have been received. These are two separate concepts.**

**Section 2: Process Flow**

**The PO Receipts process follows these steps:**

- **A receipt transaction is performed against an established purchase order. This transaction creates an "open receipt" pending a supplier invoice.**
- **Once the supplier invoice is received, it is matched to the receipt document(s) in JD Edwards via the voucher match process. This can be either a 2-way or 3-way match.**
- **The voucher transaction clears the open receipt and posts the applicable entries to the general ledger.**

**Section 3: Table F43121**

**Table F43121 is the table of record for purchase order receipts. It is important to understand that this table does not behave as a standard ledger, where each transaction associated with a receipt would have a unique record.**

**During a receipt or voucher reversal, the original receipt record is overwritten with new information. This behavior makes it impossible to generate an "As-Of" report from this table.**

**Section 4: Match Types**

**Table F43121 contains a "Match Type" column. There are four match types, defined as follows:**

| **Match Type** | **Description**                                                                                                                                                                                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**          | **A Match Type 1 record is created for each receipt document generated. This is the first step in the process. An "Open Receipts" report may be produced by selecting Match Type 1 records from the table.**                                                                      |
| **2**          | **Match Type 2 records are vouchers generated for Match Type 1 receipts. In an ideal scenario, the voucher will be for the same quantity and amount as the original receipt, with exceptions for pricing variances. This is typically the end of the process.**                   |
| **3**          | **Match Type 3 records are Match Type 1 receipts that have been reversed. The Match Type column changes from 1 to 3, and additional columns for quantities and amounts are updated accordingly. Reversals are the primary reason this table does not function as a true ledger.** |
| **4**          | **Match Type 4 records are the same as Match Type 3, except they represent voucher reversals rather than receipt reversals.**                                                                                                                                                     |

**Section 5: Accounting Flow**

**The following illustrates the accounting flow for a standard 3-way match process:**

- **Purchase Order Created - A purchase order is established in JD Edwards.**
- **Receipt Entered - Goods or services are received against the PO. A Match Type 1 record is created in table F43121. The RNV (Received-Not-Vouchered) account is credited and the inventory or expense account is debited.**
- **Supplier Invoice Received - The supplier invoice is matched to the receipt in JD Edwards via the voucher match process.**
- **Voucher Created - A Match Type 2 record is created. The RNV account is debited and Accounts Payable is credited, clearing the open receipt.**
- **Payment Processed - Accounts Payable is debited and cash or the bank account is credited, completing the process.**

**Section 6: Challenges**

**The following challenges are associated with the PO Receipts reconciliation process:**

- **System - The receipts table (F43121) is not a true ledger. Receipt and voucher reversals overwrite key data elements, making As-Of reporting impossible. This places additional importance on current-balance reconciliation methods.**
- **Process - Receipts routing, taxes, and landed cost configuration can add levels of complexity to the process. Reversals performed out of sequence may cause accounting discrepancies that are difficult to trace.**
- **Reconciliation - Because As-Of reporting is not available, reconciliation must be performed as a balance-to-balance comparison between the current open receipts report and the general ledger balance. This requires that the open receipts listing be carefully validated before any journal entries are made.**

**Training Manual: Preparing Item Data for Reconciliation**

**Section 1: The Model DMAAI Table**

**1.1 Overview**

The Model DMAAI (Distribution/Manufacturing Automatic Accounting Instructions) Table is a foundational concept within RapidReconciler. DMAAI table 4152, paired with document type PI, has been designated as the default model table. The document type may be modified by the RapidReconciler Administrator within the Companies settings.

**1.2 Purpose**

The Model DMAAI Table serves the following functions:

- Determine which GL accounts are perpetual inventory accounts, including business unit, object account, and subsidiary.
- Assign GL accounts to item ledger and location records during import from JD Edwards.
- Validate additional balance sheet DMAAI configurations.

**1.3 Key Concepts**

- DMAAI table 4152 is used as the model table. It is hard-coded in RapidReconciler and cannot be changed.
- Document type "PI" is the default document type used for the model. This may be changed by the RapidReconciler Administrator to meet specific business requirements.
- DMAAI tables 3110, 3130, 4122, 4126, 4134, 4172, 4240, and 4310 are designated for balance sheet perpetual accounts. Their configuration should closely resemble model table 4152.

**Section 2: Vetting the Model DMAAI Table**

**2.1 Overview**

The Model DMAAI Table must be vetted for accuracy in order to obtain correct results in RapidReconciler.

**2.2 Vetting Procedure**

Using the results from Inventory Integrity Report 1, verify the following:

- Ensure that individual entries for each company number and GL class code reference the correct business unit, object account, and subsidiary.
- Ensure that all GL class codes used for stock inventory are included in the model.
- Ensure that all GL class codes used for non-stock or expense items are excluded from document type PI where possible.

**Important Note:** If the document type PI contains GL class codes that are not intended to be valued but cannot be removed from the PI configuration, it is recommended that a dedicated document type (e.g., document type "I9") be created for RapidReconciler use. The RapidReconciler Administrator must update the default company configuration(s) in RapidReconciler for this change to take effect.

**2.3 Configuration Examples**

The following examples illustrate correct and incorrect DMAAI configurations. The scenario contains three inventory categories: Raw Materials, Sub-Assemblies, and Finished Goods. Each category has its own object account, and multiple GL class codes reference each category.

**2.3.1 Correct Configuration - DMAAI 4152 (Vetted)**

| **Company** | **Doc Type** | **GL Class** | **Business Unit** | **Object Account** | **Subsidiary** |
| ----------- | ------------ | ------------ | ----------------- | ------------------ | -------------- |
| 00001       | PI           | RM01         | 1                 | 1411               | 01             |
| 00001       | PI           | RM02         | 1                 | 1411               | 02             |
| 00001       | PI           | RM03         | 1                 | 1411               | 03             |
| 00001       | PI           | SA01         | 1                 | 1450               | 01             |
| 00001       | PI           | SA02         | 1                 | 1450               | 02             |
| 00001       | PI           | SA03         | 1                 | 1450               | 03             |
| 00001       | PI           | FG01         | 1                 | 1480               | 01             |
| 00001       | PI           | FG02         | 1                 | 1480               | 02             |
| 00001       | PI           | FG03         | 1                 | 1480               | 03             |

**2.3.2 Incorrect Configuration - DMAAI XXXX**

In the incorrect example, certain GL class codes are mapped to the wrong object account (e.g., RM03 mapped to object account 1480 instead of 1411, and SA02 mapped to 1411 instead of 1450). This mismatch demonstrates how errors in a non-model balance sheet DMAAI can occur.

**2.4 Key Concepts**

- It is imperative that DMAAI 4152 PI be vetted in order to produce correct results in RapidReconciler.
- If document type PI does not meet the needs of your business, a dedicated document type (e.g., "I9") should be established for use in RapidReconciler.
- If using a dedicated document type, the RapidReconciler Administrator must update the configuration in the RapidReconciler "Companies" settings accordingly.

**Section 3: Managing Inventory Accounts**

**3.1 Overview**

The Model DMAAI Table is also used to manage which accounts appear in the RapidReconciler inventory filters. Company numbers, business units, object accounts, and subsidiaries are pulled directly from this table and displayed in the filter widget on the reconciliation page.

**3.2 Key Concepts**

- The filters for the RapidReconciler inventory module are populated from data contained in the Model DMAAI Table.
- Account management occurs when the Model DMAAI Table is updated in JD Edwards. There is no direct account entry in RapidReconciler.

**Section 4: Assigning GL Account Information to Item Data**

**4.1 Overview**

Item ledger (cardex) and item location records in JD Edwards do not contain GL (General Ledger) account information. Each record does, however, contain the GL class code of the item being transacted. RapidReconciler uses this information to append GL account data to each item ledger (F4111) and item location (F41021) record during the import process.

Updates are applied only within RapidReconciler - never in JD Edwards.

**4.2 Cross-Reference Process**

To assign the correct account, the Model DMAAI Table is used as a cross-reference table. The company number and GL class code from each record are matched to the model table to retrieve the associated business unit, object account, and subsidiary.

**Example:** For an item ledger transaction for a purchase order receipt where the item belongs to company 00001 with a GL class code of IN30, RapidReconciler will append the following GL account data:

- Business Unit = 1
- Object Account = 1411
- Subsidiary = Blank

Using this approach, filtering by account in RapidReconciler will return both general ledger balances and the related perpetual inventory balances and details.

**4.3 Key Concepts**

- Item ledger and location records in JD Edwards do not contain GL account information, but do carry the GL class codes of the items.
- RapidReconciler appends these records with GL account data by using the Model DMAAI Table as a cross-reference.
- GL account and perpetual inventory balances can then be viewed by business unit, object account, and subsidiary.

**Section 5: Assigning Period End Information to Item Ledger Records - Initial Load**

**5.1 Overview**

In order to perform a proper reconciliation, each item ledger record must be allocated to a fiscal period. This allocation is performed in accordance with the fiscal date patterns established for your company in the JD Edwards system.

**5.2 Date Options**

There are three date fields in the item ledger table that may be used to determine the period in which a transaction occurred:

- **Transaction Date** - The date the transaction is recorded in the system. This date appears on many transaction screens and can be manipulated by system users. Due to the potential for human error, this is considered an undesirable option.
- **General Ledger Date** - The date the transaction is booked to the general ledger. While this date can also be manually adjusted, it is typically handled with greater care as it directly impacts financial statements.
- **Creation Date** - The system-generated date of when the transaction occurred. It cannot be altered by end users; however, it can be overwritten by the global item update program.

**5.3 RapidReconciler Date Logic**

Because no single date field is universally optimal, RapidReconciler employs its own internal date logic to determine the fiscal period of each transaction. During the initial load, the following logic is applied:

- **GL Date** - If the GL date on the item ledger record exists and is greater than or equal to January 1st of the current fiscal year, the period is assigned using the GL date.
- **Creation Date** - If the GL date has not been populated (which may occur due to unprocessed End of Day transactions), the period is assigned using the creation date.

**Note:** This logic applies during the initial load only. These rules exist because the original creation date may have been updated by the Global Item Update program in JD Edwards. Refer to Oracle documentation for further detail. The "go forward" strategy for period assignment is covered in the following section.

**Section 6: Assigning Period End Information to Item Data - Post Initial Load**

**6.1 Overview**

Following the initial load from JD Edwards into RapidReconciler, subsequent nightly imports use a different rule set for assigning fiscal periods to item ledger records.

**6.2 Cardex Accounting Method**

The diagram below illustrates the Cardex Accounting Method, which governs how period assignments are handled going forward after installation or a partial reset.

**Scenario Example:**

- The system is currently in Period 5 of the fiscal year.
- In Period 3, a sales order shipment occurred, but line items were failing unnoticed during the sales update.
- This would appear as an End of Day variance in RapidReconciler.
- The error was subsequently corrected in Period 5 or 6.
- The sales update is configured to use the system date when booking the GL entry.

The question of how to handle such a variance - and whether to reopen the Period 3 reconciliation - leads to the use of Cardex Accounting Methods, which will be addressed in the next section.

**Section 7: Inventory Reconciliation - Overview and Sources of Variance**

**7.1 What Is Inventory Reconciliation?**

There are two types of inventory reconciliation processes:

- **Physical Count Reconciliation** - Matching physical count items to perpetual balances in the system (e.g., cycle counts or physical inventories).
- **Accounting Reconciliation** - Matching calculated perpetual balances to general ledger account balances (monthly accounting process).

**Note:** RapidReconciler, like all computer-based software, can only address the monthly **accounting** reconciliation process.

**7.2 Importance of Reconciliation**

Accurate physical counts are essential for identifying human error, fraud, and material excesses or shortages. Accurate general ledger balances are equally critical for financial considerations such as tax calculations and borrowing power.

**7.3 How RapidReconciler Identifies Variance**

Inventory reconciliation in RapidReconciler is based on identifying and quantifying all sources of variance. The system represents two entities that must remain in equilibrium: the perpetual inventory system and the general ledger. Each entity has two components - balances and details.

If the net amount of each variance source equals zero, then balances must be equal. Any transaction processed in JD Edwards that does not keep these two entities in balance indicates an issue with that transaction.

**Important:** Transactions must match on the same company, GL account, and fiscal period in order to balance.

**7.4 The Four Sources of Variance**

- **GL Batches** - A difference between the sum in the F0911 GL details table and the F0902 account balance table.
- **End of Day** - Transactions in the F4111 item ledger table that have not yet been created in the general ledger F0911.
- **Transactional** - Transactions that have been fully processed, but where a mismatch exists between the item ledger F4111 and general ledger table F0911.
- **Cardex** - The sum of the quantity and/or amount of a given item in the item ledger F4111 does not match the balance on hand in table F41021.

**7.5 Perpetual Balance Forward Calculation**

The perpetual balance forward is calculated as follows:

- For the initial production import from JD Edwards, it is essential that no inventory transactions are being performed. This allows stable item balances to be retrieved from the item location table F41021 as a starting point.
- All item ledger transactions already assigned to a fiscal period are used to back-calculate to the first period to be reconciled.
- This balance forward serves as the starting point. Period end perpetual balances are then calculated by summarizing item ledger transactions. These calculated balances are reported in the RapidReconciler "Valuation" section.
- Any difference between this summarization and the latest inventory snapshot is reported as a cardex variance in the current period only.

**Section 8: Variance Source 1 - GL Batch Postings**

**8.1 Overview**

GL batch postings represent the smallest cause of reconciliation variances. Due to on-site expertise and the robust JD Edwards toolset, batch postings are normally completed without significant issues. The information in this section is provided for informational purposes.

**8.2 What Are Batch Postings?**

As inventory transactions are entered into the system, GL batches are created either immediately (for receipts, issues, adjustments, and transfers) or later (for work orders or sales orders). In either case:

- Batches must be approved, either manually or through auto-approval.
- Batches must be posted to update account balances in table F0902.
- Account balances must be current before reconciling.
- This variance source checks F0911 to F0902 integrity for the applicable accounts.

GL batch postings are part of routine JD Edwards daily processing managed by the financial department.

**8.3 Common Batch Posting Errors**

| **Error**              | **Description**                                                                    |
| ---------------------- | ---------------------------------------------------------------------------------- |
| Missing Batch Headers  | A batch header record in table F0011 is missing.                                   |
| Invalid Object Account | The object account used for posting is either invalid or is not a posting account. |
| Invalid Business Unit  | The business unit is not in the business unit master F0006 table.                  |
| Amounts Out of Balance | Debits and credits in the batch do not balance.                                    |
| GL Date Invalid        | The batch is attempting to post to a closed period.                                |

Each of these errors can lead to an integrity issue between general ledger details F0911 and general ledger balances F0902. Contact your financial department to resolve any discrepancies.

**8.4 Missing Batch Headers**

Any batch lacking a header record in table F0011 must have one added before the batch can be posted. Missing headers can be recreated in the following ways:

- Manually, using the Batch Header Revisions program.
- Using Program R007021.

RapidReconciler will identify inventory transactions with missing batch headers using an internal status code of "MH" (missing header). This code appears in the Approval_Status and Posting_Status columns on the GL Batches variance preview screen.

**8.5 Reposting an Account**

If an account balance in table F0902 becomes damaged, it can be reposted using program R099102. Refer to the relevant Oracle documentation for further information.

**Section 9: Variance Source 2 - End of Day Transactions**

**9.1 What Is an End of Day Transaction?**

An "End of Day" transaction is defined as a transaction where the general ledger system is updated at a later time than the item ledger/location record. General ledger updates occur during a batch process, typically scheduled to run at the end of the day.

**9.2 End of Day Transaction Types**

There are two transaction types that fall into the End of Day category (using standard JD Edwards document types):

- **Work Orders** - Includes work order completions (IC's) and material issues (IM's).
- **Sales Orders** - Shipment confirmations (RI's).

**9.3 Additional Information**

- Item Ledger and Location records are always updated at the time the transactions occur.
- General Ledger update means records are created in the GL detail table but are not yet posted.
- Other transaction types (e.g., PO receipts, issues, adjustments, and transfers) update the general ledger simultaneously with the item ledger/location.

**9.4 Impact on Inventory Reconciliation**

The timing differences between item ledger/location creation and general ledger creation for End of Day transactions directly impact the reconciliation process. Reconciliation begins by comparing the perpetual inventory calculated value to the amount balance in the corresponding general ledger account(s). If the balances do not match - which they rarely do - investigation is required.

**9.5 Key Concepts**

- End of Day transactions impact perpetual balance valuation reports immediately.
- If the perpetual inventory valuation report is generated while End of Day transactions are still in process, reconciling items will appear.
- Additional processing must occur to generate and post general ledger batches for End of Day transactions.
- It is highly recommended that all End of Day transactions be identified and fully completed before reconciling.

**9.6 Validating End of Day Items in the JDE Item Ledger**

If the validity of items listed on the report is in question (e.g., a status code of 99 or 999), validate by locating the transaction on the JDE Item Ledger inquiry screen and drilling into the details to review the batch number.

If the batch number is present but an issue remains, locate the oldest transaction date and use the cardex deletion tool in the Administrator section. Administrator permissions in RapidReconciler are required to use this tool.

**Section 10: Variance Source 3 - Transactional Variances**

**10.1 What Are Transactional Variances?**

Transactional variances represent differences between the item ledger table F4111 and the general ledger detail table F0911 for transactions that have been fully processed. RapidReconciler only displays transactions with discrepancies - it functions as an exception list.

**10.2 Transaction Matching Criteria**

For an item ledger F4111 transaction to be matched to its general ledger F0911 counterpart, the following seven fields must be identical in both tables:

- Company Number
- Batch Number
- Document Type
- Document Number
- Order Type
- Account Number
- Period Ends

**Note:** The item ledger company number is fetched from the F0006 business unit master table based on the branch plant used. Work order document numbers in the general ledger differ by design from those in the item ledger and are cross-referenced from table F3106 and/or the GL subledger. Account number and period information are appended to item ledger data during the import process from JD Edwards.

**10.3 Transactional Scenarios Identified by RapidReconciler**

| **Scenario**            | **Description**                                                                                                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Company Number Mismatch | The branch company from the item ledger does not match the company number in the GL. The transaction is not considered the same, even if the document number and type match.                                                  |
| Account Number Mismatch | The assigned account number in the item ledger does not match the account in the general ledger. RapidReconciler notes this as an "Account Mismatch" and displays two offsetting detail lines with different account numbers. |
| Fiscal Period Mismatch  | The assigned fiscal period in the item ledger does not match the period in the general ledger. RapidReconciler notes this as a "Period Mismatch" and displays two offsetting detail lines with different periods.             |
| Amount Discrepancy      | Matching criteria are met, but the amount in the item ledger differs from the amount in the general ledger. A single line is displayed quantifying the variance.                                                              |

If matching criteria are met and there is no amount discrepancy, the transaction is considered reconciled and will not be displayed.

**Section 11: Variance Source 4 - Cardex Variance**

**11.1 What Is Cardex Variance?**

Cardex variance is the difference between an item's transaction amount summary and its on-hand value. This represents the F41021 to F4111 integrity check. For standard cost items, the item ledger transactional summary for each branch plant, item number, location, and lot must equal the on-hand balance in both units and amounts.

**11.2 Investigating Cardex Variance in JD Edwards**

To investigate a cardex variance from the item ledger screen in JD Edwards:

- Inquire on the item to be analyzed. Be as specific as possible - input the item number and branch plant at a minimum. For standard cost items, add location and lot.
- Note the balances at the top of the screen. The quantity on hand comes from item balance table F41021. The value equals quantity on hand multiplied by unit cost from F4105.
- Detail transactions come from table F4111. Navigate to the bottom of the list and export all transactions to Excel.
- Ensure all quantities are stated in primary unit of measure.
- Delete any memo transactions (typically work order scrap "IS" and lot releases "IZ").
- The sum of primary quantities from the detail must match the quantity on hand in the header. If not, an IT update to the quantity on hand may be required.
- The sum of the extended amount column must equal the amount shown in the value field in the header. If not, a dollars-only inventory adjustment is needed.

**11.3 New Re-Roll Feature**

As of November 2023, the item re-roll feature was updated to address invalid cardex variances or problems with roll-forward totals. On the As-Of page, a button is available in the far-right column for each item. Clicking this button presents three options:

- **ReRoll Item** - Use this option when there are issues with the quantity on hand due to changes in the primary unit of measure. This option retains the current balance forward, adjusts transactions as needed, and recalculates each period ending total through the current period. This has no impact on amounts - only quantity.
- **Zero Beg Balance** - Use this option only if the first available period should have a beginning balance of zero. The beginning balance will be forced to zero and each period total will be recalculated. Since perpetual amount totals for all periods may change, confirm this is correct before executing.
- **Remove CX Var** - Use this option to remove any erroneous cardex variance for the item in RapidReconciler. Validate that the summarized cardex quantity total matches the total quantity on hand in JDE before proceeding. If JDE is correct and RapidReconciler is showing a cardex variance, selecting this option will remove it.

**Important:** There is no undo process. Review each option carefully before executing. Once complete, the As-Of totals will be adjusted; however, reconciliation summary totals will not be updated until the next refresh cycle.

**Section 12: GL Class Codes**

**12.1 Hierarchy Overview**

GL class codes are assigned to items in JD Edwards and define how inventory transactions are recorded in the general ledger. Transaction mapping is defined in the Distribution/Manufacturing Automatic Accounting Instructions (DMAAs), which are covered separately.

The GL class code hierarchy consists of four levels:

- **Item Master Level** - The GL class code is assigned during the new item creation process.
- **Item Branch Level** - The code is copied from the item master. Each branch may have a different value, although this is uncommon.
- **Item Location Level** - The code is copied from the item branch. Each location may have a different value, although this is also uncommon.
- **Sales Order / Purchase Order Level** - The code is copied from the location record.

**12.2 Changing a GL Class Code**

When a GL class code needs to be changed, each tier in the hierarchy must be updated manually - changes to the item master do not automatically propagate to lower tiers.

An additional consideration is inventory on hand. The old code must be closed out before changing to the new code. The correct process is as follows:

- Adjust inventory on hand to zero under the old GL class code.
- Change the code on the branch, locations, and open orders.
- Adjust inventory back in under the new GL class code.

**Why is this necessary?** If the old GL class code is not zeroed out first, the value of any existing inventory will remain in the original general ledger account. There will be no transaction to move the value to the new account. By adjusting the inventory out first and back in after the code change, the value correctly moves from one account to the other.

**12.3 Transaction Usage**

GL class codes are used when processing inventory transactions. Each transaction type is programmed to use specific entries from the DMAAI tables to create the applicable journal entries.

Different transaction types source GL class codes from different hierarchy levels:

- **Work Orders** - Material issues and completions source the GL class code from the **item branch level**.
- **Sales and Purchase Orders** - Shipments and receipts source the GL class code from the **order level**.
- **Inventory Transactions** - Issues, adjustments, transfers, and cycle counts source the GL class code from the **location level**.

**Note:** It is uncommon for the GL class code value to vary for a given item across different levels. From a valuation perspective, the accounting rule for an item should not change with the transaction type.

**12.4 Integrity Report 5 - GL Class Code Consistency**

Inventory Integrity Report 5 identifies items where the GL class code on the item branch level does not match the GL class code on one or more corresponding item location records. It is generally desirable that these values be consistent.

Any item appearing on this report should be reviewed for accuracy and adjusted in JD Edwards as applicable.
