**Reference Guide: Tax in Sales**

**Setup, Functionality, and Sales Tax AAIs**

**Section 1: Tax Setup**

Tax setup is accessed from menu **G0021**, which is shared with Financials for all tax setup and reporting. The following options on this menu are used by Distribution:

- Tax Authorities
- Tax Rates & Areas
- Tax Explanation Codes
- Tax Rules by Company

**Section 2: Tax Explanation Codes**

Tax Explanation Codes are defined in UDC table **00/EX**. The code tells the system what type of tax to apply to the order.

**Valid values for Sales:**

| **Code** | **Description**                         |
| -------- | --------------------------------------- |
| **S**    | Standard sales tax                      |
| **V**    | VAT Tax                                 |
| **V+**   | VAT Tax with tax-on-tax capability      |
| **C**    | Canadian Tax with tax-on-tax capability |
| **E**    | Exempt from tax                         |

**2.1 Custom Tax Explanation Codes**

New tax explanation codes can be created, but they must begin with **S**, **V**, **C**, or **E** to write a valid record to the tax file (F0018) at post. The tax calculator program (X4008C) is hard-coded to recognize the first character.

| **Example** | **Behavior**               |
| ----------- | -------------------------- |
| **S1**      | Behaves identically to "S" |
| **V1**      | Behaves identically to "V" |

**Important:** Do **not** create a code of "TX." Although the system will accept it on the UDC table and on an order, no tax amount will be written to the F0018 tax file.

**Section 3: Tax Rate/Area**

The Tax Rate/Area identifies a geographic or tax area and defines the tax percentage to be accrued.

**3.1 Key Fields**

| **Field**               | **Description**                                                                                                                                                                                                                                                                         |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tax Authority**       | The Address Book number of the municipality to whom the tax is remitted. Up to five tax authorities can be defined per Tax Rate/Area.                                                                                                                                                   |
| **Tax Rate**            | The tax percentage for a particular tax authority.                                                                                                                                                                                                                                      |
| **GL Offset**           | The GL Class code used by the tax AAIs.                                                                                                                                                                                                                                                 |
| **Calc Method**         | Indicates whether tax-on-tax applies. Primarily used with Canadian taxes.                                                                                                                                                                                                               |
| **VAT Exp**             | Identifies the percentage of VAT not eligible for input credits. Valid values: **R** (not recoverable - treated as an expense), **Blank** (default - tax is a receivable). Valid only for the third, fourth, and fifth tax authorities and only with tax explanation codes C, V, and B. |
| **Total Area Tax Rate** | The sum of all tax authorities' tax rates, including tax-on-tax where applicable.                                                                                                                                                                                                       |

The Tax Explanation Code and Tax Rate/Area are assigned in the Customer Master and default into the sales order.

**Section 4: Tax Rules by Company**

To access Tax Rules by Company for Sales, inquire on the company with **System = 1 (A/R)**.

The **Calculate Sales Order Taxes on Summary** flag determines whether taxes are calculated at the detail line level or at the order level. This setting should correspond to whether entries are being summarized at Sales Update.

**Section 5: Other Tax Setup**

**5.1 Item Branch - Sales Taxable Field**

The Sales Taxable field in Item/Branch determines taxability by item. This value defaults into the detail line for the item on the sales order and can be overridden at the order level.

**5.2 Line Type Definition - TX01 Flag (Include Tax)**

The TX01 flag (field TAX1) in the line type definition (G4241, option 2) controls taxability for non-stock lines. The taxability for stock lines is determined by the Sales Taxable field in Item/Branch.

| **Value** | **Description**                                                                                                  |
| --------- | ---------------------------------------------------------------------------------------------------------------- |
| **Y**     | The line is subject to applicable taxes.                                                                         |
| **N**     | The line is not subject to applicable taxes.                                                                     |
| **3-8**   | The line is subject to taxes at the rate indicated by the group number. Used for VAT (Value Added Tax) grouping. |

**Section 6: Entering Tax Information on a Sales Order**

The Tax Explanation Code and Tax Rate/Area default into the **sales order header** from the Customer Master records of the Sold-To and Ship-To customers, or they can be entered manually. Both fields must be populated. These values default down to the detail lines.

**Defaulting rules:**

- The **Tax Explanation Code** comes from the **Sold-To** customer.
- The **Tax Rate/Area** comes from the **Ship-To** customer.
- If no Tax Explanation Code exists on the Sold-To, both the Tax Explanation Code and Tax Rate/Area are taken from the **Ship-To**.

**6.1 Viewing Tax Online**

Tax can be viewed using **On-Line Invoice (P42230)**, accessed with **F6** from the detail. The taxable amount, tax percentage, and total tax display at the bottom. If lines are taxed at different rates, "N/A" may appear as the tax percentage.

Pressing **F15** from this screen displays detailed tax information (V42235). Setting the Tax Summary field to 1, 2, or 3 provides additional levels of detail.

**Section 7: Tax Explanation Code Examples**

**7.1 "S" - Standard U.S. Sales Tax**

The "S" Tax Explanation Code is the standard for United States sales tax. The customer pays the item price plus tax, and the supplier remits the tax to the tax authorities.

**AAI used:** DMAAI **4250**

- The Company defaults from the detail Branch/Plant on the sales order.
- The GL Class code comes from the GL Offset in the Tax Rate/Area setup.

**The tax amount and account are visible on the Sales Update report.**

**Example:** On a \$100 order with a 5% tax rate:

- A/R = \$105
- Revenue = \$100
- Tax Payable (4250) = \$5

**7.2 "V" - VAT Tax**

The "V" Tax Explanation Code is commonly used in Canada and Europe.

**AAI used:** Financial AAI **RT** (accessed via fast path AAI, then F16 for table format)

The RT AAI is structured as the base "RT" plus the GL Class Code from the Tax Rate/Area setup (e.g., RTTAXX).

**The VAT tax amount appears on the Sales Update report, but the GL account distribution is not visible until the batch is posted.** It is written as an automatic entry (AE) at post.

**7.3 "C" - Canadian Tax with Tax-on-Tax**

The "C" Tax Explanation Code is primarily used in Canada for tax-on-tax scenarios.

**AAIs used:** Both **RT** and **4250**

The key difference from "V" is the Tax Rate/Area setup:

- The tax-on-tax percentage uses the **4250 AAI**.
- The base tax percentage uses the **RT AAI**.

**Example:** Tax Rate/Area with 7% base tax and 8.56% tax-on-tax = 15.56% Total Area Tax Rate.

**Sales Update example on a \$100 order:**

- Base tax (7%) → RT AAI
- Tax on tax (8.56%) → 4250 AAI

**7.4 "E" - Exempt from Tax**

The "E" Tax Explanation Code is used for customers who are exempt from tax. No tax is written, but the system **still validates** the RT AAI for exempt orders.

**Important:** Due to Vertex integration changes, the system checks that the RT AAI is configured with a valid account number even for exempt orders. If the RT AAI is not set up, **error 1829** (Record not set up in Auto Acct Inst File) will be generated at Sales Update.

**Section 8: Tax Work File (F0018)**

Tax amounts are written to the Tax Work File (F0018) at post, provided the Post program (P09800) processing options are configured:

| **Processing Option** | **Function**                                                                   |
| --------------------- | ------------------------------------------------------------------------------ |
| **Option 9**          | Controls whether tax entries are written to F0018. If blank, no updates occur. |
| **Options 10 and 11** | Additional tax-related controls in the Post program.                           |

**Section 9: Sales Tax AAIs**

**9.1 DMAAI 4250 vs. Financial AAI RT**

| **AAI**  | **Used With**                                                                  | **Key Behavior**                                                                                                                                                                                                                                        |
| -------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **4250** | "S" tax explanation code only                                                  | Searches for a combination of company number, order type, and GL Class Code (from the GL Offset in the Tax Rate/Area). Tax amount and account visible at Sales Update. If not set up, generates **error 0381** (AAI Account Not Setup) at Sales Update. |
| **RT**   | "V", "C", and "E" tax explanation codes; also used for non-taxable items/lines | Tax amount visible on the Sales Update report, but GL distribution not visible until post (written as an automatic entry). Also validated for exempt orders and non-taxable lines - if not set up, generates **error 1829** at Sales Update.            |

**9.2 RT AAI Setup**

The RT AAI is structured as **RT + GL Class Code** from the Tax Rate/Area GL Offset.

**Example:** For Tax Rate/Area "COLO" with GL Offset "TAXX," the correct RT AAI setup would be **RTTAXX** for Company 00001.

**Note:** The data item and field value in error 1829 reference the Tax Rate/Area name. The resolution is to set up the RT AAI in the Financial AAIs using the GL Class Code from the Tax Rate/Area GL Offset - not the Tax Rate/Area name itself.

**9.3 Non-Taxable Lines and the RT AAI**

When an item or line type has "N" in the taxable field, the system passes an "E" (exempt) for the tax explanation code. Even though no tax is charged, Sales Update still validates that the RT AAI is set up. If it is not, error 1829 will be generated.

**Section 10: Tax Calculation Date**

**10.1 Release A7.3**

In A7.3, tax in the sales system is calculated based on the **order date**.

**Planned Enhancement (SAR 6361376):** A processing option will be added to allow a choice between Invoice Date and Order Date for tax calculation in A7.3.

**10.2 Release A8.1**

In A8.1, the **Tax Service Date Selection (TXSD)** field was added, allowing the user to specify which date is used for tax calculation.

| **Value** | **Tax Service Date** |
| --------- | -------------------- |
| **1**     | Order date           |
| **2**     | Invoice date         |
| **3**     | Ship date            |
| **Blank** | Order date (default) |

**Where to configure:**

- At the ship-to address number level: **Customer Billing Instructions** (page 2)
- At the header Branch/Plant company level: **Tax Rules by Company** (inquire on System A/R)

**Priority:** If the ship-to address number value is blank, the header Branch/Plant company value is used. If both are blank, the order date defaults as the tax service date.