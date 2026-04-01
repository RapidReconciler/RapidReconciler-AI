**Reference Guide: Tax in Procurement**

**Setup, AAIs, and General Ledger Tax Treatment**

**Section 1: Interfaces**

The Quantum Sales Tax Calculation Module by Vertex can be used with the procurement application as of release B73.3.1. The interface to Quantum is included as part of the EnterpriseOne procurement and address book applications. Vertex software is sold separately.

**Section 2: Tax Terms**

| **Term**                         | **Definition**                                                                                                                                                                                                                           |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sales Tax**                    | A tax paid to the supplier along with the cost of goods or services. The supplier collects the tax and remits it to the taxing authority.                                                                                                |
| **Use Tax**                      | A self-assessed tax on goods or services paid directly to the taxing authority by the buyer.                                                                                                                                             |
| **VAT (Value Added Tax)**        | A tax paid to the supplier that is subsequently recoverable by the buyer from the taxing authority.                                                                                                                                      |
| **GST (Goods and Services Tax)** | A Canadian Federal Government tax. GST is a recoverable VAT tax.                                                                                                                                                                         |
| **PST (Provincial Sales Tax)**   | A Canadian provincial tax. Can be applied to the value of goods or services before or after GST (inclusive of GST). PST can be payable to either the supplier (acts as sales tax) or directly to the taxing authority (acts as use tax). |

**Section 3: Tax Setup**

Tax setup is performed on menu **G0021** and includes the following programs:

- Tax Authorities
- Tax Rate/Areas
- Tax Explanation Codes
- Tax Rules by Company

**3.1 Tax Authorities**

All taxing authorities should be set up as regular Address Book records.

**3.2 Tax Rate/Areas**

Key fields in the Tax Rate/Area setup:

| **Field**             | **Description**                                                                                                                                                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Effective Date**    | Blank defaults to the current date.                                                                                                                                                                                                                    |
| **Expiration Date**   | If tax rates are indefinite, extend this date as far as possible. Once established, the expiration date cannot be changed.                                                                                                                             |
| **Item Number**       | A Tax Rate/Area can be applied to a group of items or a single item. Processing option 1 can suppress this field; processing option 3 controls how it is edited.                                                                                       |
| **Maximum Unit Cost** | The maximum amount an item can be taxed. Processing option 2 can suppress this field.                                                                                                                                                                  |
| **Address**           | The Address Book number for each taxing authority. Up to five taxing authorities can be defined per Tax Rate/Area.                                                                                                                                     |
| **GL Offset**         | The GL Class code used by the tax AAIs (4350 and 4355). Note: For procurement, the GL Offset for these AAIs comes from the Purchase Order Detail (F4311), not from the Tax Rate/Area.                                                                  |
| **Compound Tax**      | Controls the GST/PST calculation method. Checked = PST is calculated on item cost PLUS GST (tax-on-tax, typically used in Quebec). Unchecked = PST is calculated on item cost only.                                                                    |
| **VAT Expense**       | Identifies the percentage of VAT not eligible for input credits. Valid only with tax codes C, B, and V, and only for the third, fourth, and fifth tax authorities. Checked = not recoverable (expense); Unchecked = recoverable (receivable, default). |

**Compound Tax Calculation Example (GST = 4%, PST = 6%):**

|           | **Compound Tax Checked** | **Compound Tax Unchecked** |
| --------- | ------------------------ | -------------------------- |
| Item      | \$100.00                 | \$100.00                   |
| GST       | \$4.00                   | \$4.00                     |
| PST       | \$6.24 (\$104 × 6%)      | \$6.00 (\$100 × 6%)        |
| **Total** | **\$110.24**             | **\$110.00**               |

**Note:** The first line in the Tax Rate/Area is GST and the second line is PST when Tax Explanation Codes B and C are used on an order.

**3.3 Tax Explanation Codes**

The following hard-coded Tax Explanation Codes are most commonly used in procurement (defined in UDC 00/EX):

| **Code** | **Description**                                                |
| -------- | -------------------------------------------------------------- |
| **S**    | Sales Tax - seller-assessed                                    |
| **U**    | Use Tax - self-assessed by buyer                               |
| **V**    | VAT Tax - seller-assessed and recoverable                      |
| **C**    | GST/PST with PST paid to supplier                              |
| **B**    | GST/PST with PST accrued and paid directly to taxing authority |
| **E**    | Tax Exempt                                                     |

**3.4 Tax Rules by Company**

Access Tax Rules by Company for Procurement with **System = 2**.

| **Field**                                       | **Description**                                                               |
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| **Tolerances**                                  | Not used by Purchase Order Processing or Sales Order Processing.              |
| **Calculate Tax on Gross (Including Discount)** | Choose to calculate tax on gross including or excluding discount.             |
| **Calculate Discount on Gross (Including Tax)** | Check to calculate the discount on item cost plus tax. Defaults to unchecked. |

**Section 4: Automatic Accounting Instructions**

| **AAI**  | **Account**                       | **Description**                                                                |
| -------- | --------------------------------- | ------------------------------------------------------------------------------ |
| **4310** | Inventory                         | Directs the procurement application to the Inventory GL account.               |
| **4320** | Received Not Vouchered (RNV)      | Directs the procurement application to the temporary liability GL account.     |
| **4350** | Tax Expense                       | Directs the procurement application to the Tax Expense GL account.             |
| **4355** | RNV Tax (Temporary Tax Liability) | Directs the procurement application to the temporary tax liability GL account. |
| **PT**   | Tax-Related A/P                   | Financial AAI that directs tax-related accounts payable entries.               |
| **PC**   | AP Trade                          | Financial AAI that directs trade accounts payable entries.                     |

**Note:** In a 2-way match, the temporary liability AAIs 4320 and 4355 are not used.

**Section 5: Default Codes and Rates**

Default tax information (Tax Explanation Code and Tax Rate/Area) is specified in **Supplier Master Information (P04012)** off menu G0411. These defaults populate the Purchase Order Entry screen and can be overridden at order entry.

**Important:** If tax information is not entered during purchase order entry, taxes will not be accrued at PO Receipt. Tax codes can be entered at Voucher Match, and the resulting journal entries will resemble those for a 2-way match.

**5.1 Purchase Order Entry (P4310) Processing Option**

Processing option #7 on the Defaults tab controls the default source for the tax code and rate:

| **Setting** | **Behavior**                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------ |
| **1**       | Defaults Tax Explanation Code and Tax Rate/Area from the Supplier Master of the Ship-To Address Book.  |
| **Blank**   | Defaults Tax Explanation Code and Tax Rate/Area from the Supplier Master of the Supplier Address Book. |

**Note:** PO Receipts (P4312) and Voucher Match (P4314) have no processing options specific to taxes.

**Section 6: General Ledger Tax Treatment**

The accounting treatment of taxes in the procurement application varies based on three factors:

- **Tax Explanation Code**
- **Inventory vs. Non-Inventory purchase order** - "Inventory" = line type with inventory interface of "Y"; "Non-Inventory" = line type with inventory interface of "N" or "A"
- **Two-way match vs. three-way match**

**Note:** All entries marked with \* are made by the GL Post program (R09801).

**Section 7: Tax Code "S" - Simple Sales Tax**

**Purpose:** Used when purchasing items where tax is remitted to the supplier with the cost of the goods.

**7.1 Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**          | **Debit** | **Credit** |
| ------------------ | --------- | ---------- |
| 4310 - Inventory   | Item      |            |
| 4350 - Tax Expense | Tax       |            |
| 4320 - RNV         |           | Item       |
| 4355 - RNV Tax     |           | Tax        |

**Voucher Match (P4314):**

| **Entry**        | **Debit** | **Credit** |
| ---------------- | --------- | ---------- |
| 4320 - RNV       | Item      |            |
| 4355 - RNV Tax   | Tax       |            |
| PC - AP Trade \* |           | Item + Tax |

**7.2 Non-Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**             | **Debit**  | **Credit** |
| --------------------- | ---------- | ---------- |
| Account entered on PO | Item + Tax |            |
| 4320 - RNV            |            | Item       |
| 4355 - RNV Tax        |            | Tax        |

**Voucher Match (P4314):**

| **Entry**        | **Debit** | **Credit** |
| ---------------- | --------- | ---------- |
| 4320 - RNV       | Item      |            |
| 4355 - RNV Tax   | Tax       |            |
| PC - AP Trade \* |           | Item + Tax |

**7.3 Non-Inventory - 2-Way Match**

**Receive and Voucher (P4314):**

| **Entry**             | **Debit**  | **Credit** |
| --------------------- | ---------- | ---------- |
| Account entered on PO | Item + Tax |            |
| PC - AP Trade \*      |            | Item + Tax |

**Section 8: Tax Code "U" - Use Tax**

**Purpose:** Used when the buyer calculates, accrues, and remits the tax amount directly to the taxing authority.

**8.1 Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**          | **Debit** | **Credit** |
| ------------------ | --------- | ---------- |
| 4310 - Inventory   | Item      |            |
| 4350 - Tax Expense | Tax       |            |
| 4320 - RNV         |           | Item       |
| 4355 - RNV Tax     |           | Tax        |

**Voucher Match (P4314):**

| **Entry**        | **Debit** | **Credit** |
| ---------------- | --------- | ---------- |
| 4320 - RNV       | Item      |            |
| 4355 - RNV Tax   | Tax       |            |
| PC - AP Trade \* |           | Item       |
| PT AAI \*@       |           | Tax        |

**8.2 Non-Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**             | **Debit**  | **Credit** |
| --------------------- | ---------- | ---------- |
| Account entered on PO | Item + Tax |            |
| 4320 - RNV            |            | Item       |
| 4355 - RNV Tax        |            | Tax        |

**Voucher Match (P4314):**

| **Entry**        | **Debit** | **Credit** |
| ---------------- | --------- | ---------- |
| 4320 - RNV       | Item      |            |
| 4355 - RNV Tax   | Tax       |            |
| PC - AP Trade \* |           | Item       |
| PT AAI \*@       |           | Tax        |

**8.3 Non-Inventory - 2-Way Match**

**Receive and Voucher (P4314):**

| **Entry**             | **Debit**  | **Credit** |
| --------------------- | ---------- | ---------- |
| Account entered on PO | Item + Tax |            |
| PC - AP Trade \*      |            | Item       |
| PT AAI \*@            |            | Tax        |

**@ PT AAI Logic for Use Tax:** The system first looks for AAI PT\_\_\_\_ (literal blank) to find the cost center and object account. It then looks for an account whose cost center, object, and subsidiary name match the Tax Rate/Area name. If a subsidiary account is not found, only the cost center and object are used. The GL Offset in the Tax Rate/Area is ignored.

**Section 9: Tax Code "V" - Value Added Tax**

**Purpose:** Used when the buyer pays tax to the supplier that is later recoverable from the taxing authority.

**9.1 Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**        | **Debit** | **Credit** |
| ---------------- | --------- | ---------- |
| 4310 - Inventory | Item      |            |
| 4320 - RNV       |           | Item       |

**Voucher Match (P4314):**

| **Entry**           | **Debit** | **Credit** |
| ------------------- | --------- | ---------- |
| 4320 - RNV          | Item      |            |
| VAT Recoverable \*@ | Tax       |            |
| PC - AP Trade \*    |           | Item + Tax |

**9.2 Non-Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**             | **Debit** | **Credit** |
| --------------------- | --------- | ---------- |
| Account entered on PO | Item      |            |
| 4320 - RNV            |           | Item       |

**Voucher Match (P4314):**

| **Entry**           | **Debit** | **Credit** |
| ------------------- | --------- | ---------- |
| 4320 - RNV          | Item      |            |
| VAT Recoverable \*@ | Tax       |            |
| PC - AP Trade \*    |           | Item + Tax |

**9.3 Non-Inventory - 2-Way Match**

**Receive and Voucher (P4314):**

| **Entry**             | **Debit** | **Credit** |
| --------------------- | --------- | ---------- |
| Account entered on PO | Item      |            |
| VAT Recoverable \*@   | Tax       |            |
| PC - AP Trade \*      |           | Item + Tax |

**@ VAT Recoverable AAI Logic:** The system looks up the GL Offset from the Tax Rate/Area and then searches for an AAI of PT followed by the GL Offset (e.g., PTTXTX).

**Section 10: Tax Code "C" - GST/PST with PST Paid to Supplier**

**Purpose:** Used in Canada for a combination of GST and PST, both paid to the supplier. The PST portion behaves like a "S" (seller-assessed) sales tax; the GST portion behaves like a "V" (recoverable VAT).

**10.1 Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**          | **Debit** | **Credit** |
| ------------------ | --------- | ---------- |
| 4310 - Inventory   | Item      |            |
| 4350 - Tax Expense | PST Tax   |            |
| 4320 - RNV         |           | Item       |
| 4355 - RNV Tax     |           | PST Tax    |

**Voucher Match (P4314):**

| **Entry**           | **Debit** | **Credit**       |
| ------------------- | --------- | ---------------- |
| 4320 - RNV          | Item      |                  |
| 4355 - RNV Tax      | PST Tax   |                  |
| VAT Recoverable \*@ | GST Tax   |                  |
| PC - AP Trade \*    |           | Item + PST + GST |

**10.2 Non-Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**             | **Debit**  | **Credit** |
| --------------------- | ---------- | ---------- |
| Account entered on PO | Item + PST |            |
| 4320 - RNV            |            | Item       |
| 4355 - RNV Tax        |            | PST Tax    |

**Voucher Match (P4314):**

| **Entry**           | **Debit** | **Credit**       |
| ------------------- | --------- | ---------------- |
| 4320 - RNV          | Item      |                  |
| 4355 - RNV Tax      | PST Tax   |                  |
| VAT Recoverable \*@ | GST Tax   |                  |
| PC - AP Trade \*    |           | Item + PST + GST |

**10.3 Non-Inventory - 2-Way Match**

**Receive and Voucher (P4314):**

| **Entry**             | **Debit**  | **Credit**       |
| --------------------- | ---------- | ---------------- |
| Account entered on PO | Item + PST |                  |
| VAT Recoverable \*@   | GST Tax    |                  |
| PC - AP Trade \*      |            | Item + PST + GST |

**@ VAT Recoverable AAI Logic:** The system uses the GL Offset from the first line of the Tax Rate/Area table and looks for an AAI of PT followed by the GL Offset (e.g., PTTXTX).

**Section 11: Tax Code "B" - GST/PST with PST Withheld**

**Purpose:** Used in Canada for a combination of GST paid to the supplier and PST withheld and paid directly to the Provincial tax authority. The PST portion behaves like a "U" (self-assessed) use tax.

**11.1 Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**          | **Debit** | **Credit** |
| ------------------ | --------- | ---------- |
| 4310 - Inventory   | Item      |            |
| 4350 - Tax Expense | PST Tax   |            |
| 4320 - RNV         |           | Item       |
| 4355 - RNV Tax     |           | PST Tax    |

**Voucher Match (P4314):**

| **Entry**           | **Debit** | **Credit** |
| ------------------- | --------- | ---------- |
| 4320 - RNV          | Item      |            |
| 4355 - RNV Tax      | PST Tax   |            |
| VAT Recoverable \*@ | GST Tax   |            |
| Tax Payable \*#     |           | PST Tax    |
| PC - AP Trade \*    |           | Item + GST |

**11.2 Non-Inventory - 3-Way Match**

**PO Receipt (P4312):**

| **Entry**             | **Debit**      | **Credit** |
| --------------------- | -------------- | ---------- |
| Account entered on PO | Item + PST Tax |            |
| 4320 - RNV            |                | Item       |
| 4355 - RNV Tax        |                | PST Tax    |

**Voucher Match (P4314):**

| **Entry**           | **Debit** | **Credit** |
| ------------------- | --------- | ---------- |
| 4320 - RNV          | Item      |            |
| 4355 - RNV Tax      | PST Tax   |            |
| VAT Recoverable \*@ | GST Tax   |            |
| Tax Payable \*#     |           | PST Tax    |
| PC - AP Trade \*    |           | Item + GST |

**11.3 Non-Inventory - 2-Way Match**

**Receive and Voucher (P4314):**

| **Entry**             | **Debit**      | **Credit** |
| --------------------- | -------------- | ---------- |
| Account entered on PO | Item + PST Tax |            |
| VAT Recoverable \*@   | GST Tax        |            |
| Tax Payable \*#       |                | PST Tax    |
| PC - AP Trade \*      |                | Item + GST |

**@ VAT Recoverable AAI Logic:** The system uses the GL Offset from the first line of the Tax Rate/Area table and uses the financial AAI of PT followed by the GL Offset (e.g., PTTXTX).

**\# Tax Payable AAI Logic for PST:** The system first looks for AAI PT\_\_\_\_ (literal blank) to find the cost center and object account. It then looks for an account whose cost center, object, and subsidiary name match the Tax Rate/Area name. If a subsidiary account is not found, only the cost center and object are used. The GL Offset in the Tax Rate/Area is ignored.
