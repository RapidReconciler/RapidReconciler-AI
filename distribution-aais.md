**Reference Guide: Automatic Accounting Instructions (DMAAIs)**

**Setup, Configuration, and Complete AAI Listing**

**Section 1: Definition**

Automatic Accounting Instructions (AAIs) determine which account numbers will be affected when various transactions are created by JD Edwards programs. They serve as the mapping layer between business transactions and the general ledger.

**Section 2: Setup**

**2.1 Location and Access**

Distribution AAIs are stored in the **Distribution/Manufacturing AAI Values table (F4095)**. They can be set up from any distribution setup menu. The fast path is **DMAAI**.

**2.2 AAI Key Structure**

An AAI must be established for any unique combination of the following three fields:

- **Company Number**
- **Document Type**
- **GL Class Code**

A reference only matrix of AAIs by company, document type, and GL class code is available here:

[AAI Matrix](Docs/AAI%20Matrix.xls)

**2.3 Default Search Sequence**

If the system cannot find an AAI for a specific combination, it falls back through the following search sequence. The document type must match in all cases.

**Example:** For Company 00100 with GL Class code IN20, the system searches in this order:

| **Step** | **Search Criteria**                         | **Result if Not Found** |
| -------- | ------------------------------------------- | ----------------------- |
| 1        | Company 00100, GL Class IN20                | Proceed to Step 2       |
| 2        | Company 00100, GL Class \*\*\*\* (wildcard) | Proceed to Step 3       |
| 3        | Company 00000, GL Class IN20                | Proceed to Step 4       |
| 4        | Company 00000, GL Class \*\*\*\* (wildcard) | Proceed to Step 5       |
| 5        | Not found                                   | Error message generated |

**Note:** Financial AAIs are stored in the Automatic Accounting Instructions Master table **(F0012)**. The fast path for setup is **AAI**. Financial AAIs PC (A/P) and RC (A/R) follow a similar default search sequence, with a final default of Company 00000, item PC*\_\_\_or RC*\_\_\_ (which may be blank).

**Section 3: GL Class Codes**

**3.1 Source of GL Class Code by Transaction Type**

For inventory transactions, the GL class code is sourced from the **Item Location table (F41021)**, or for non-stock items, from the **Item Master table (F4101)**. For sales and purchasing transactions, the GL class code is determined by the inventory interface for the line type:

| **Inventory Interface** | **GL Class Code Source**                                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Y and D**             | Item Location table (F41021)                                                                                                         |
| **N**                   | The Line Type definition                                                                                                             |
| **A**                   | Debits the account number entered on the PO; pulls GL class code for RNV and Variances from the Line Type definition.                |
| **B**                   | Debits the account number entered on the PO; pulls GL class code for RNV and Variances from the Item Master Location table (F41021). |

**3.2 Exceptions**

| **Transaction Type**            | **GL Class Code Source**                                                                                                                                                                                                                                                                     |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Advanced Pricing**            | AAIs 4270 and 4280 pull GL class codes from the Advanced Pricing Adjustment Definition (P4071) off menu G42311. If blank, the code is pulled from the line item to which the adjustment applies.                                                                                             |
| **Taxes**                       | Tax AAIs pull the GL class code from the line type, the inventory item, or the GL Offset in the Tax Rate/Areas program (P4008) off menu G0021.                                                                                                                                               |
| **Landed Cost**                 | GL class code is pulled from the Landed Cost Revisions program (P41291) off menu G43A41.                                                                                                                                                                                                     |
| **Variance (Line Type A or B)** | If the Voucher Match Variance Account flag is checked ("Y") in the line type definition, amount differences at voucher match are written to a variance account using the GL class code in the fold. If unchecked ("N"), differences are written to the account number on the purchase order. |

**Section 4: Business Unit**

**4.1 Overview**

The Business Unit is optional in AAI setup. If left blank, the system generally pulls the business unit from the **Branch/Plant on the transaction**. Exceptions include:

**4.2 Project Number / Subsequent Cost Center**

A Project Number (also called Subsequent Cost Center) can be assigned to a business unit in Revise Single Business Unit (P0006) off menu G09411. If populated, it will be used as the business unit portion of the account when the AAI business unit is blank.

**4.3 Sales Update (R42800)**

Processing option 5 on the Defaults tab of Sales Update (R42800) controls where the Business Unit (or Cost Center) portion of the account is sourced from. Options include:

- Subsequent Cost Center (Project Number on Business Unit)
- Branch/Plant on the order
- Sold-To Address Book Number

**4.4 Flexible Sales Accounting**

The Business Unit portion of the account number can also be populated using Flexible Sales Accounting (P40296) off menu G4241.

**Section 5: Setup of Financial AAIs**

**5.1 Accessing Financial AAIs**

From the main Financials AAI screen (fast path **AAI**), take the Multiple AAIs form exit. Use the wildcard character **\*** to search - for example, entering **RT\*** will return every combination of RT\_\_\_\_ available.

**5.2 Accounts Payable AAIs**

| **AAI**     | **Purpose**                         | **GL Class Code Source**                                                                                                                                                                                                                                                                                                               |
| ----------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PC xxxx** | Financial AAI for payables.         | Assigned in Supplier Master Information (P04012). PC\_\_\_\_ is valid (may be blank).                                                                                                                                                                                                                                                  |
| **PT xxxx** | Financial AAI for purchasing taxes. | Four-character GL Offset from Tax Rate/Area (P4008), except for "U" and "B" tax explanation codes (self-assessed taxes), which use PT\_\_\_\_. The subsidiary is the Tax Rate/Area. If the account does not exist with a subsidiary, the system defaults to the account without the subsidiary (e.g., 10.4423.CO defaults to 10.4423). |

**5.3 Accounts Receivable AAIs**

| **AAI**     | **Purpose**                    | **GL Class Code Source**                                                       |
| ----------- | ------------------------------ | ------------------------------------------------------------------------------ |
| **RC xxxx** | Financial AAI for receivables. | Assigned in Customer Billing Instructions (P03013) on the GL Distribution tab. |
| **RT xxxx** | Financial AAI for sales taxes. | Four-character GL Offset from Tax Rate/Area (P4008) off menu G0021.            |

**Section 6: AAI Error Messages**

| **Error #** | **Message**                            | **Resolution**                                                                                                           |
| ----------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **0381**    | AAI not set up                         | Error at Sales Update (R42800). The message specifies which AAI is missing. Set up the missing entry in the DMAAI table. |
| **3429**    | Invalid Distribution/Manufacturing AAI | Interactive error for inventory or purchasing transactions. Specifies which AAIs are not configured.                     |
| **0028**    | Account number invalid                 | The AAI is pointing to an account number not in the chart of accounts. Set up a valid account off menu G09411.           |
| **1829**    | Record not set up in AAI file          | Tax AAI is not configured. Set up RT xxxx, PT xxxx, PT\_\_\_\_, or GT xxxx in the financial AAI schedule.                |

**Section 7: Inventory AAIs**

| **AAI**         | **Account**                 | **Purpose**                                                                                              | **Programs**                                                                                                              |
| --------------- | --------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **4122 / 4124** | Inventory / Expense or COGS | Journal entry for issues, adjustments, and transfers.                                                    | Inventory Issues (P4112), Inventory Transfers (P4113), Inventory Adjustments (P4114), Inventory Reclassifications (P4116) |
| **4126 / 4128** | Inventory / Expense or COGS | Zero balance adjustment - used when quantity equals zero but dollars remain.                             | Inventory Issues (P4112), Inventory Transfers (P4113), Inventory Adjustments (P4114), Inventory Reclassifications (P4116) |
| **4134 / 4136** | Inventory / Expense or COGS | Records change to COGS when the cost of an item changes.                                                 | Quantity Revisions (P41022), Item Branch/Plant Information (P41026), Batch Cost Maintenance (R41802)                      |
| **4141**        | COGS                        | Variance when a transaction has a different standard cost than what is in the Item Cost (F4105) file.    | Inventory Issues (P4112), Inventory Transfers (P4113), Inventory Adjustments (P4114), Inventory Reclassifications (P4116) |
| **4152 / 4154** | Inventory / COGS            | Change to inventory value when quantity counted does not equal quantity on hand in a physical inventory. | Cycle Count Update (R41413), Tag Count Update (R41610)                                                                    |
| **4172 / 4174** | Inventory / Expense or COGS | Change in inventory value when the unit cost of an item is changed through Future Cost Update.           | Future Cost Update (R41052)                                                                                               |

**Section 8: Sales AAIs**

| **AAI**  | **Account**                 | **Purpose**                                                                                                         | **GL Class Code Source**      |
| -------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **4220** | COGS                        | Standard sales transaction journal entry.                                                                           | Item Location                 |
| **4230** | Sales/Revenue               | Standard sales transaction journal entry.                                                                           | Item Location                 |
| **4240** | Inventory                   | Standard sales transaction journal entry.                                                                           | Item Location                 |
| **4245** | Accounts Receivable (Trade) | Standard sales transaction journal entry.                                                                           | Customer Master               |
| **RC**   | Accounts Receivable         | Standard sales transaction journal entry.                                                                           | Customer Master               |
| **4250** | Sales Tax Liability         | Standard sales transaction journal entry.                                                                           | Tax Rate/Area                 |
| **4260** | Interbranch Revenue         | Records interbranch revenue when processing options are set in Sales Order Entry (P4210) and Sales Update (R42800). | Item Location                 |
| **4270** | Advanced Price Adjustment   | Records discount or markup for advanced price adjustments.                                                          | Price Adjustment Type (P4071) |
| **4280** | Advanced Price Accruals     | Records the offset to 4270 for accruals in Advanced Pricing.                                                        | Price Adjustment Type (P4071) |

**Section 9: Purchasing AAIs**

| **AAI**         | **Account**                                                                   | **Purpose**                                                                                                                                                            | **Programs**                                                                                                   |
| --------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **4310**        | Inventory                                                                     | Journal entry for receipt.                                                                                                                                             | Receipts by PO (P4312), Receipts by Item (P4312)                                                               |
| **4315**        | Non-stock asset                                                               | Journal entry for receipt of non-stock assets.                                                                                                                         | Receipts by PO (P4312), Receipts by Item (P4312), Match Voucher to Open Receipt (P0411) - for 2-way match      |
| **4320**        | Temporary Liability - Received Not Vouchered (RNV)                            | Journal entry for receipt.                                                                                                                                             | Match Voucher to Open Receipt (P0411)                                                                          |
| **4330**        | Variance Account or Inventory (written to F4111)                              | Records variance when invoice amount at voucher match differs from receipt amount. Requires Voucher Match Variance Account flag to be checked in Line Type definition. | Match Voucher to Open Receipt (P0411)                                                                          |
| **4332**        | Cost Variance (not written to F4111)                                          | Records variance to Cost of Sales when quantity on hand is less than quantity vouchered. Requires Voucher Match Variance Account flag to be checked.                   | Match Voucher to Open Receipt (P0411); if quantity on hand is less than zero: Stand Alone Landed Cost (P43214) |
| **4335**        | Variance Account (not written to F4111)                                       | Records standard cost variance.                                                                                                                                        | Match Voucher to Open Receipt (P0411)                                                                          |
| **4337**        | Material Burden                                                               | Accounts for all costs in addition to purchase price.                                                                                                                  | Receipts by PO (P4312), Receipts by Item (P4312)                                                               |
| **4340**        | Variance Account (not written to F4111)                                       | Records exchange rate variance.                                                                                                                                        | Match Voucher to Open Receipt (P0411)                                                                          |
| **4350 / 4355** | Tax Expense or Inventory (written to F4111) / Temporary Tax Liability         | Records tax during receipt or voucher match. AAI 4355 is not used if taxed at voucher match.                                                                           | Receipts by PO (P4312), Receipts by Item (P4312), Match Voucher to Open Receipt (P0411)                        |
| **4365 / 4370** | Prior to Receipt/Completion Liability / Routing Operation                     | Records journal entries at specified steps in a receipt route. (As of Xe release.)                                                                                     | Movement & Disposition (P43250)                                                                                |
| **4375**        | Expense                                                                       | Debits expense account for items dispositioned off during receipt routing.                                                                                             | Movement & Disposition (P43250)                                                                                |
| **4385 / 4390** | Inventory or Landed Cost (written to F4111) / Landed Cost Temporary Liability | Records landed costs.                                                                                                                                                  | Receipts by PO (P4312), Receipts by Item (P4312), Stand Alone Landed Cost (P43214)                             |
| **4400 / 4405** | Inventory / COGS or Expense                                                   | Zero balance adjustment - used when quantity equals zero but dollars remain.                                                                                           | Receipts by PO (P4312), Receipts by Item (P4312)                                                               |

**Section 10: Change to DMAAI Key Structure in Xe Release**

**10.1 Key Structure Change**

Prior to the Xe release, the keys for the F4095 table were: ANUM, CO, DCTO, DCT, GLPT, COST, **MCU, OBJ, and SUB**.

In Xe and later releases, the keys are: **ANUM, CO, DCTO, DCT, GLPT, COST** only. The account number components (MCU, OBJ, and SUB) were removed as key fields.

**10.2 Table Conversion - R894095A**

To support the upgrade to Xe, a table conversion program **R894095A** was created. This conversion:

- Eliminates duplicate records from F4095 using the new key values (ANUM, CO, DCTO, DCT, GLPT, COST).
- Retains only the first record when duplicates are identified.
- Stores all subsequent duplicate records in the temporary table **F4095TEM** for client review.

Clients must evaluate the records stored in F4095TEM to determine which AAIs will be used going forward.

**10.3 Consolidating or Closing Accounts No Longer Referenced in F4095**

For accounts that are no longer referenced after the conversion:

- Run **P0902P1 (Account Balance by Month)** to determine the total amounts booked to the account across all fiscal years.
- Run **Journal Entry application P0911** to move amounts from the closed account to the remaining active account.

**10.4 Maintaining Accounts from the Previous Release**

If multiple accounts need to be maintained that were previously driven by MCU, OBJ, and SUB key fields, these must now be managed through **GL class codes**:

- Maintain one wildcard GL class code pointing to one account.
- Create additional AAI records with specific GL class codes pointing to the remaining accounts.
- Update the GL class code on the applicable items to align with the new AAI structure.

**Note:** In the AAI setup, the MCU field may be left blank. In that case, the MCU from the purchase order detail line is used to construct the account, with the object and subsidiary sourced from the company, document type, and GL class code.

After the conversion is complete and all records in F4095TEM have been evaluated and addressed, the F4095TEM table may be deleted.
