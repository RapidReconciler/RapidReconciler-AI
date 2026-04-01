**Reference Guide: Sales Update (P42800)**

**Frequently Asked Questions, Processing Information, and Error Resolution**

**Section 1: Overview**

Sales Update is the final step in the sales order process. It provides the interface between Sales Order Processing and other JD Edwards modules, including Inventory, Accounts Receivable, and the General Ledger.

**1.1 Purpose**

Sales Update serves four main purposes:

- **Updates the Financials systems** by creating journal entries in the General Ledger (F0911) and creating receivable records in Accounts Receivable (F0311).
- **Updates the item's on-hand quantity** if not previously done by Shipment Confirmation (P4205).
- **Closes out the sales order.**
- **Purges the sales order** to history files if records are not to be retained in the sales order header and detail files.

**1.2 Files Updated by Sales Update**

The update of the following files depends on line type setup, Branch/Plant setup, or processing options:

| **File**           | **Description**                                |
| ------------------ | ---------------------------------------------- |
| **F0311**          | Accounts Receivable Ledger                     |
| **F0911**          | General Ledger Account Ledger                  |
| **F41021 / F4111** | Item Location / Item Ledger (Cardex)           |
| **F4229 / F4115**  | Sales Summary History / Detailed Sales History |
| **F0018**          | Tax Reporting                                  |
| **F42005**         | Sales Commissions                              |
| **F4211**          | Sales Order Detail                             |
| **F4314**          | Text File                                      |
| **F42199**         | Sales Order Detail Ledger                      |

**Section 2: System Interfaces and File Updates**

**2.1 Accounts Receivable and General Ledger (F0311 / F0911)**

The Sales Order Invoice is a detailed list of all items sold to a customer. A/R entries may be created as either summarized or detailed:

- **Detailed** - A one-to-one relationship exists between invoice lines and A/R pay items.
- **Summarized** - One line is created for each line type/due date combination.

GL entries are created for inventory relief, cost of goods sold, and revenue. Additional entries may be created for freight, handling, and similar charges. Whether a line interfaces with the GL is controlled by either the Branch/Plant constants GL Interface flag or the Order Line Type setting.

To create a balanced GL entry when the A/R interface is active:

- If the A/R processing option is **blank** and the order line type has A/R Interface = Y, the A/R trade entry is created by the Post program (P09800) using the **RC AAI** (tied to the Customer Master GL Class Code).
- If A/R is bypassed, the A/R trade entry is created by sales update using **DMAAI 4245**.

**2.2 Inventory (F41021 / F4111)**

On-hand inventory can be relieved at either Ship Confirmation or Sales Update:

**At Ship Confirmation:**

- A cardex record is written with the sales order document type and number but no GL date.
- The on-hand quantity in F41021 is updated.
- During Sales Update, the sales order document number and type are replaced with the invoice document type and number, and the GL date is assigned.
- The order document type must be included in UDC table **40/IU** for ship confirmation relief to work.

**At Sales Update:**

- The cardex is updated only once.
- The invoice number is displayed in the Document Number and Type fields.
- The sales order number is displayed in the Document Number field of the Item Ledger Information video (V4111W).
- The order document type must **not** be in UDC table 40/IU.

**Inventory quantity impact example:**

|            | **On-Hand** | **Committed** | **Available** |
| ---------- | ----------- | ------------- | ------------- |
| **Before** | 100         | 10            | 90            |
| **After**  | 90          | 0             | 90            |

**2.3 Sales History (F4229 / F4115)**

Sales history is stored in two files:

| **File**                           | **Description**                                                                            | **Access**                      |
| ---------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------- |
| **F4115** - Detailed Sales History | Sales information by item number and business unit.                                        | Buyers Information (V4115)      |
| **F4229** - Summary Sales History  | Information by order type, line type, address book number, item number, and business unit. | Sales Analysis Summary (P42611) |

Processing options in Sales Update control whether these files are updated. At least one year of history must be available for trend comparisons to function correctly. Additional reports can be created using World Writer over these files.

**2.4 Commissions (F42005)**

Commission information is written to the Commissions file only at Sales Update. No A/P or GL records are created for accrued commissions - these entries must be created manually. Commission data is accessed through the Commission/Royalty Inquiry (V42120) or through a user-defined report.

**2.5 Sales Order Detail History (F42119)**

Contains a one-to-one record of all lines processed by Sales Update when processing option 16 is blank. Also stores records created by Purge Details to History (P42996). This file can be written to tape or disk to free the system for current activity.

**2.6 Sales Order Header History (F42019)**

Contains a one-to-one record of each order header purged during Sales Update or through the standalone purge program. Writing to this file is controlled by processing option 17.

**2.7 Tax File (F0018)**

The tax file is not written to until the GL transactions (F0911) are posted to the Account Balance file (F0902). Tax entries print on the Sales Update report (R42800) without specific GL account numbers. Processing option behind the Post program (P09800) controls whether and how tax entries are written:

| **Setting** | **Behavior**              |
| ----------- | ------------------------- |
| **1**       | VAT or Use Tax            |
| **2**       | All Tax Amounts           |
| **3**       | All Tax Explanation Codes |
| **Blank**   | No update to the file     |

**2.8 Sales Order Detail File (F4211)**

Sales Update advances the sales order line status to **999** (or to the status set in processing option 6). It also updates the GL date, invoice number, invoice type, and date (if Invoice Print was not previously run).

**2.9 Associated Text (F4314)**

Text lines associated with an order line will be purged if processing option 15 is set appropriately. There is no Text History file - once purged, text cannot be recovered.

**2.10 Price Adjustments History (F4074)**

Maintains a record of pricing applied to specific order lines. If processing option 18 is set to purge this file, the records are permanently deleted. There is no related history file for this data.

**Section 3: Processing Order**

Sales Update processes all selected F4211 records in two or three major cycles:

**First (if applicable):** If processing option 22 is set, the Update Sales Price/Cost program (P42950) processes all F4211 records.

**Second:** After P42950 completes, Sales Update creates records in the following files, processing one F4211 record at a time:

- F0311 - Accounts Receivable Ledger (dependent on processing option 14)
- F0911 - Account Ledger (requires both the GL Interface flag in the line type AND the Interface with GL flag in Branch/Plant Constants to be set)

**Third:** After all F0311 and F0911 records are created, Sales Update updates or creates records in the following order, processing one F4211 at a time:

- F41021 - Item Location file
- F4111 - Item Ledger file
- F4115 - Item History file (dependent on processing option 14)
- F4229 - Sales Summary History file (dependent on processing option 14)
- F42005 - Sales Commission file
- F4314 - Text file (dependent on processing option 15) - purges header and detail text
- F4211 - Sales Order Detail file (advances status to 999 or processing option 6 value)
- F42199 - Sales Order Detail Ledger file
- F4074 - Price Adjustment History file (dependent on processing option 18) - **no flex file; once purged, cannot be retrieved**
- F42119 - Sales Order Detail History file (dependent on processing option 16)
- F42019 - Sales Order Header History file (dependent on processing option 17)

**Note:** F4201 records will not purge to F42019 until all associated F4211 records have been purged to F42119.

**Section 4: Reports Generated by Sales Update**

| **Report**                   | **Program** | **Description**                                                                                                                                                                     |
| ---------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Invoice Journal**          | P42800      | Shows journal entry account numbers and amounts for all invoices processed. Displays batch number, batch type, batch date, and invoice number. Prints in both proof and final mode. |
| **Error Report**             | P42801      | Generated automatically. Lists errors encountered during processing. See Section 9 for error details.                                                                               |
| **Sales Journal** (optional) | P42810      | Controlled by processing option 8. Categorizes sales into stock, non-stock, or miscellaneous and displays gross profit percent. Can also be run independently from menu G42111.     |

**Section 5: AAIs Used by Sales Update**

| **AAI**  | **Description**                                     |
| -------- | --------------------------------------------------- |
| **4220** | Cost of Goods Sold                                  |
| **4230** | Revenue                                             |
| **4240** | Inventory                                           |
| **4245** | Accounts Receivable Trade (used when bypassing A/R) |
| **RC**   | Accounts Receivable Trade                           |
| **4250** | Tax Liability                                       |
| **4260** | Interbranch Revenue                                 |
| **4270** | Price Adjustments                                   |
| **4280** | Rebates Payable                                     |

**Note:** AAI table numbers are hard-coded within Sales Update.

**5.1 Tax AAIs**

| **AAI**  | **When Used**                                                                                                                                                                                                   |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RT**   | Used by the Post program (P09800) for PST (Provincial Sales Tax) and VAT taxes. Sales Update validates the RT AAI even if it is not used in a transaction - a missing or invalid RT AAI will generate an error. |
| **4250** | Used by Sales Update for all other tax types.                                                                                                                                                                   |

**5.2 Bypassing Accounts Receivable**

Setting processing option 14 prevents the creation of F0311 records. F0911 records are still created to maintain a balanced entry. AAI 4245 is used for the A/R entry when bypassing A/R.

|                              | **Bypassing A/R**             | **Not Bypassing A/R**         |
| ---------------------------- | ----------------------------- | ----------------------------- |
| **At Sales Update - Debit**  | COGS \$60; 4245 A/R \$100     | COGS \$60                     |
| **At Sales Update - Credit** | Revenue \$100; Inventory \$60 | Revenue \$100; Inventory \$60 |
| **At Post - Debit**          | -                             | RC A/R \$100                  |

**Important:** You cannot bypass A/R by setting the A/R flag in the order line type to N. This creates a three-way journal entry that will not post because it is out of balance.

**Section 6: Batch Types Created by Sales Update**

| **Scenario**                                                                         | **Batch Types Created**                                                        |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Running in detail (not summarizing Inventory/COGS to separate batch)                 | All entries in **I-batch**                                                     |
| Summarizing Inventory and COGS to separate batch (processing option 12 = 1)          | Sales entries in **I-batch**; Inventory and COGS in **G-batch**                |
| Interbranch orders - not creating A/R and A/P batches (processing option 26 = blank) | Regular entries in **I-batch**; interbranch settlement entries in **ST batch** |
| Interbranch orders - creating A/R and A/P batches (processing option 26 = 1)         | Regular entries in **I-batch**; creates **V batch**                            |

**Section 7: Summary vs. Detail Mode**

**7.1 Accounts Receivable Entries**

**Detail:** Creates a separate F0311 record for each F4211 record with a particular invoice number. Pay items increment by 001 for each subsequent line.

**Summary:** Summarizes F4211 records by invoice number into one pay item. Records will only summarize if all of the following fields are identical:

| **Field** | **Description**                                   |
| --------- | ------------------------------------------------- |
| KCO       | Document Key Company                              |
| DOC       | Document Number                                   |
| DCT       | Document Type                                     |
| CO        | Company                                           |
| TXA1      | Tax Area                                          |
| EXR1      | Tax Explanation                                   |
| PTC       | Payment Terms                                     |
| ITM       | Item Number (if specified in tax rate/area setup) |

**Notes:**

- Lines with different Tax Explanation Codes or Tax Rate/Areas will not summarize.
- Lines where the calculated Due Dates or Discount Due Dates differ will not summarize, even if Payment Terms are the same.

**7.2 General Ledger Entries**

**Detail:** Creates a separate F0911 record for each F4211 record with a particular invoice number.

**Summary:** Summarizes F4211 records by invoice number using the following fields: Short Account ID (AID), Subledger (SBL), Subledger Type (SBLT).

**Section 8: Proof vs. Final Mode**

| **Mode**  | **Behavior**                                                                                                                                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Proof** | Generates Invoice Journal (P42800) and Error Report (error report may not be complete). Does not update status codes or any files. Use to preview journal entries and identify errors.                              |
| **Final** | Generates Invoice Journal, Error Report (P42801), and Sales Journal (if selected). Updates status codes and files. Performs edits against the GL functional server (XT0911Z1) and A/R functional server (XT0311Z1). |

**Section 9: Versions of Sales Update**

Two versions of Sales Update exist. The data sequencing for either version should not be changed.

**9.1 Sales Update - Proof or Final**

**Use when:** The order has been run through Invoice Print (P42565) and contains a document number and type in F4211.

- Data selection: Invoice NE \*BLANKS (only processes F4211 records with an invoice number in SDDOC).
- Required sequencing: Document Number (DOC) → Document Type (DCT) → Document Company (KCO).

**9.2 Sales Update - Assign Invoice No. - Proof or Final**

**Use when:** The order has not been run through Invoice Print and does not contain a document number or type in F4211.

- A next number bucket for the invoice can be selected using system 03 (processing option 21).
- A document type other than RI can be chosen (processing option 22) - value must be set up in UDC 00/DI.
- Data selection: \*ALL except Invoice Date NE \*ZEROS.
- Required sequencing: Order Number (DOCO) → Order Type (DCTO) → Order Number Document Company (KCOO).

**To determine if an invoice has been assigned:** Inquire on the order using On-line Invoice or Customer Service Inquiry (option 5 on the detail line). If an invoice has been printed, the Invoice Number and Type fields will be populated.

**Section 10: Common Problems and Resolutions**

**10.1 Multiple F0311 and F0911 Records**

**Cause:** Running the wrong version of Sales Update - specifically, running the version that assumes an invoice number exists when one has not been assigned. This results in incorrect sequencing by DOC/DCT/KCO instead of DOCO/DCTO/KCOO.

**Resolution:** Confirm the version being used and match it to whether an invoice number has been assigned.

**10.2 F0311 Records Created but No F0911 Records**

**Cause:** GL interface flags are not set correctly.

**Resolution:** Check both the GL Interface flag in the order line type AND the Interface with GL flag in the Branch/Plant Constants. Both must be set for F0911 records to be created.

**10.3 A/R Records Not Summarizing Despite Processing Option 10 Being Set**

**Cause:** One or more of the seven required fields (see Section 7.1) differ between lines, or the line types are different with different Credit/Debit (C/D) flags causing different due dates.

**Resolution:** Review all summarization fields across the lines in question. Check C/D flag settings in the applicable line types.

**10.4 Sales Update Stopped in the Middle**

- Identify which F4211 record the update stopped on using the job log and formatted dump.
- Clean up the problem record using a file manipulation utility (DFU, DBU, QuestView, or SQL).
- Verify that all files were properly updated for the record prior to the one where processing stopped.
- If F0311 and F0911 records have been created but F41021 or F4111 have not been updated, determine which cardex records exist.
- If only F0311 and F0911 records were created, delete all records for that batch number and re-run Sales Update.
- For more complex situations, seek second-level support.

**10.5 Tax File (F0018) Not Populating**

Sales Update does not write to the Tax Work File (F0018). Entries are created by the Post program (P09800). Check processing option 9 in P09800. If the processing option needs to be changed, note that entries will only be made from that point forward - historical entries must be entered manually using Tax File Revisions (P0018). This processing option must be set for each Post version used.

**10.6 Status Advanced to 999 but No F0311, F0911, F41021, or F4111 Records Created**

**Most likely cause:** The detail line was already at status 999 before Sales Update ran (e.g., from a reprint or rerun where the override next status processing option was not populated).

**Resolution:** View the F4211 record and check the SDPID (Program ID) field to identify the last program that processed the record. Use a file manipulation utility to change the last and next status back to allow the record to process through Sales Update.

**10.7 Purging Records During Sales Update**

Sales Update can purge the following files when processing options are configured correctly:

- Price Adjustment History (F4074) - permanently deleted; no recovery possible.
- Sales Detail (F4211) - purged to F42119.
- Sales Header (F4201) - purged to F42019.
- Text Detail (F4314) - permanently deleted.

**Note:** Records that reached status 999 prior to running Sales Update will not be included in the programmatic purge. Use specific purge programs (P00PURGE and others) for records not purged through Sales Update.

**10.8 Re-Running Sales Update**

**Changing GL or Invoice Dates:** There is no programmatic way to reverse Sales Update. The recommended approach is to create a correcting journal entry to move summary dollars between periods. Restoring from backup tape is the only other option but requires re-entering all data entered after the backup was created.

**Records Not Included:** Create a version of Sales Update that selects only the missing records. Run in proof mode first to verify selection, then run in final mode.

**Data Purged Erroneously:** Short of restoring all files from backup, there is no easy way to restore purged data.

**Data Not Purged:** Use the appropriate standalone purge programs rather than re-running Sales Update.

**Section 11: Error Messages - Causes and Resolutions**

**11.1 How to Read the Error Report**

The Sales Update Error Report (R42801) provides the following information for each error:

- **Data Type** - 0311 (A/R) or 0911 (GL)
- **Data Item** - The field in error
- **Field Value** - The value that caused the error
- **Code** - The error code number
- **Message Description** - Brief description (inquire on the error code in the data dictionary for full details)

**Note:** Some problems generate multiple errors. Focus on the lowest-numbered error in a group - resolving it will often clear the others automatically.

**11.2 Error Reference**

| **Error(s)**         | **Data Item**         | **Type** | **Cause**                                                                                                                                 | **Resolution**                                                                                                                                               |
| -------------------- | --------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **0000**             | DG                    | 0911     | A/R and GL date from processing options 1 and 3 are in a future fiscal year.                                                              | Check the fiscal date pattern for the company. Note: A batch is still created and will post.                                                                 |
| **0002**             | DCT, DOC, SFX         | 0311     | (1) Line did not close to 999 and keeps processing. (2) Invoice already processed but pay item not incremented in F0311.                  | (1) Change status to 999. (2) Change the pay item of the existing F0311 record to a different value to allow the new record to write.                        |
| **0025 / 2362**      | DCT                   | 0311     | Invoice document type in processing option 21 is not defined in UDC 00/DI (error 0025) or 00/DT (error 2362).                             | Add the document type to the applicable UDC tables.                                                                                                          |
| **0027**             | PDCT                  | 0311     | A related order number exists without an order type in the details behind the details.                                                    | Check the related order type. Verify that blanks is a valid value in UDC 00/DT.                                                                              |
| **0028 / 0381**      | ANI, AAI              | 0911     | Error 0381: AAI not set up in F4095. Error 0028: Account number in the AAI is incorrect or not in the chart of accounts.                  | 0381: Add the AAI for the specific company, document type, and GL class code. 0028: Verify the account in the AAI table and set up in the chart of accounts. |
| **0064**             | DGJ                   | 0311     | GL/A/R date is less than the beginning fiscal date in the company constants.                                                              | Check the fiscal date pattern. Either change the company fiscal date or enter a valid date in processing options.                                            |
| **0065**             | DG                    | 0911     | Fiscal date pattern is set to a current period in the future relative to the order date.                                                  | Check the fiscal date pattern. If prior period posting is needed, confirm PBCO postings are allowed in General Accounting Constants (P00909).                |
| **0066**             | DGJ                   | 0311     | GL/A/R date is in a future month beyond the current and next period. Warning only - batch will post.                                      | No action required. Check fiscal date pattern.                                                                                                               |
| **0069**             | ANI                   | 0911     | Account being booked has a posting edit code that does not allow entry.                                                                   | Change the posting edit code in the chart of accounts (G09411) or in Revise Single Business Unit (G09411).                                                   |
| **0272**             | TXA1                  | 0311     | Tax Rate/Area not set up or not set up correctly, or detail line has a Tax Explanation Code but no Tax Rate/Area.                         | Verify Tax Rate/Area setup and effective dates. Check the RT AAI for the GL Class Code from the Tax Rate/Area.                                               |
| **0272 / 2367-2370** | TXA1, DG, DI, DSV, DD | 0311     | Invoice not printed but processing options 2 and 4 are set to use invoice date.                                                           | Set processing options 2 and 4 to use the sales update execution date, or specify a date in processing options 1 and 3.                                      |
| **0748**             | EXR1                  | 0311     | Tax Explanation Code was valid when the order was entered but was removed from UDC 00/EX before Sales Update ran.                         | Add the code back to UDC 00/EX or change the F4211 record to the correct code.                                                                               |
| **0812**             | -                     | -        | Tax amount is incorrect, usually a result of other tax errors.                                                                            | Resolve the other tax errors; error 0812 will clear automatically.                                                                                           |
| **1002 / 2106**      | -                     | -        | Allow Understatement of Tax Amount = Y, but the Tolerance Percentage or Amount is less than the change in the tax rate.                   | Temporarily increase the Tolerance Percentage to above the rate change, run Sales Update, then restore the original tolerance.                               |
| **1480 / 2106**      | -                     | -        | Allow Understatement of Tax Amount = N.                                                                                                   | Change the field to Y.                                                                                                                                       |
| **1614**             | -                     | -        | Order has two or more lines where a taxable line is followed by a non-taxable line (releases prior to A73 cum7 / A72 cum9).               | Run the non-taxable line through Sales Update separately.                                                                                                    |
| **1829**             | TXA1                  | 0311     | RT AAI is not set up. Sales Update validates RT AAI for all transactions including non-taxable lines.                                     | Set up the RT AAI using the GL Class Code from the GL Offset in Tax Rates and Areas (P4008) for the specific company.                                        |
| **1837**             | AN8                   | 0311     | Hold Invoice flag in the customer master is set to Y.                                                                                     | Change the customer's Hold Invoice flag to N.                                                                                                                |
| **2527 / 2528**      | AG                    | 0311     | Tax rate is a negative value (e.g., -7.75%).                                                                                              | Sales Update cannot process negative tax amounts. This requires a configuration review.                                                                      |
| **2528**             | AG, ATXA              | 0311     | Tax rate changed between order date and invoicing/Sales Update, causing taxable amount to exceed the gross amount.                        | In A8.1, use the processing option to specify which date (order, ship, or invoice) is used for tax calculation.                                              |
| **3475**             | KCO                   | 0911     | Key Company number is not the same across F4211, F4311, F0311, and F0911. Note: Errors appear only in proof mode; final mode will update. | Change the KCO to be consistent across all four files.                                                                                                       |
| **3479**             | CRR                   | 0311     | Multiple orders with different exchange rates were consolidated by customer through Invoice Print.                                        | Change exchange rates to be consistent in F4211, or configure the customer to not consolidate invoices.                                                      |
| **3481 / 3483**      | DG, DI                | 0311     | Invoice dates are not consistent across lines (caused by DFU or modification) and processing options 2 and 4 are set to use invoice date. | Specify a date in processing options 1 and 3, or use DFU to make invoice dates consistent.                                                                   |
| **3482**             | AN8                   | 0311     | Sold-to address numbers are not consistent across all lines of an order (caused by DFU or modification).                                  | Use DFU to make the Sold-to address consistent for all lines.                                                                                                |
| **3490**             | AN8                   | 0311     | Address Book number is valid but no Customer Master record exists.                                                                        | Add the Customer Master record.                                                                                                                              |
| **3740**             | -                     | -        | No currency code for the customer in the customer master in a multi-currency environment.                                                 | Add the currency code to the Customer Master (G0311).                                                                                                        |