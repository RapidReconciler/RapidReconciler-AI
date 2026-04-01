**JD Edwards EnterpriseOne - Distribution**

**Reference Guide: Flexible Accounting for Distribution**

**Sales and Purchasing Processes**

|                       |            |
| --------------------- | ---------- |
| **Solution ID**       | 200782056  |
| **Date Last Revised** | 03/28/2008 |

**Section 1: Background**

Flexible Accounting was created to provide users greater flexibility in how accounting information is recorded for sales and purchasing transactions. Prior to Flexible Accounting, the only way to pass detailed information to the general ledger was through the subledger field, which could only capture one piece of information.

With Flexible Accounting, the business unit portion of an account number can be defined based on a combination of fields - for example, a sold-to address number, an address book category code, and an item category code. This allows organizations to be highly specific in their accounting for who, where, and what is being sold or purchased.

Flexible Accounting can be used across Manufacturing, Cost Accounting, and Distribution applications in EnterpriseOne. This guide addresses Flexible Accounting for the **Distribution** applications - specifically the Sales and Purchasing processes:

- **Sales** - Flexible Accounting is applied during Sales Update (R42800).
- **Purchasing** - Flexible Accounting is applied during Purchase Receipts (P4312) and Match Voucher to Open Receipts (P4314).

**Important:** Setting up the account structure is a business decision that should be made during the implementation and planning phase. While it is technically possible to switch between standard accounting and Flexible Accounting mid-stream, this is not a process that is easily accomplished and should be carefully evaluated before proceeding.

**Section 2: Requirements**

Three steps must be completed to activate Flexible Accounting:

- **Enable Flexible Accounting** - Define the Rule Setup Method and associate programs with tables.
- **Identify the AAIs to be flexed** - Determine which AAI table numbers will use Flexible Accounting.
- **Define the Flexible account rules** - Specify how account components will be constructed from combinations of fields.

**Section 3: Enabling Flexible Accounting**

**3.1 Overview**

Two steps are required to enable Flexible Accounting. Both are performed from menu **G1631** using the **Enable Functionality by Application** option (P16902).

**3.2 Step 1 - Establishing the Rule Setup Method**

The Rule Setup Method defines how the system creates Flexible Accounting entries. If the Rule Method is not already in the table (i.e., SM type of functionality is not listed for the application being set up), it must be added:

- Click **Add**.
- Enter **SM** in the Type of Functionality field, then tab.
- The Setup Method and Application Name fields will appear.
- Enter **A** in the Setup Method field and the relevant application name (e.g., R42800, P4312, or P4314).

**Available Setup Methods:**

| **Code** | **Method**                    |
| -------- | ----------------------------- |
| **O**    | Object                        |
| **A**    | AAI                           |
| **C**    | Combination of Object and AAI |

**Note:** If the Setup Method is set to "C" (Combination) and flex information is configured to flex a specific field differently based on Object vs. AAI, **Object will take precedence**.

**3.3 Step 2 - Establishing Program/Table Relationships**

The second step is to associate the program using Flexible Accounting with the tables it will access. If the relationship has not already been defined, it must be added using the Enable Functionality form.

**Tables accessed by Sales Update (R42800):** The last line on the form is the Rule (SM).

**Tables accessed by Purchasing processes (P4312 and P4314):** A separate list of tables applies to purchase receipts and voucher match.

**Important:** As of release B733.2, only the tables that are listed for an application are supported. Adding a new table to the Enable Functionality form would be considered a modification and is not supported by GSC.

**Section 4: Determining the AAIs to Be Flexed**

**4.1 Sales Order Processing**

For Sales Order Processing, only the following AAIs can be flexed:

| **Category**         | **AAIs**                         |
| -------------------- | -------------------------------- |
| **Sales**            | 4220, 4230, 4240, 4250, and 4245 |
| **Advanced Pricing** | 4270 and 4280                    |

**Note:** AAI 4245 is invoked when accounts receivable is bypassed by setting processing option #2 on the Update tab of Sales Update (R42800) to "1."

**4.2 Purchasing**

With the advent of Product Costing, **all AAIs** can be flexed for Purchasing processes.

**Note:** Flex accounts can be set up using either a To/From Object account **or** a specific AAI in Flex Accounting rules - but not both simultaneously.

**Section 5: Establishing Flexible Accounts**

**5.1 Principle**

The core principle of Flexible Accounting is that various fields from various tables can be combined to create individual components of an account number. Setup is performed using the **Flexible Sales Accounting program (P40296)** off menu G4241.

The account components that can be "flexed" are:

- **Business Unit** - Can be broken into up to **6 segments** with a total of **12 characters**.
- **Subsidiary** - Can be broken into up to **4 segments** with a maximum of **8 characters**.
- **Subledger**

**Important Constraint:** The **object account cannot be flexed**.

**5.2 Account Structure Requirements**

A consistent account structure must be used across all companies and all business units in the organization. This is required for multi-company consolidations and automated intercompany settlements. If Flexible Accounting is also used on the financials side of the system, the distribution business units and subsidiary must use the same number of characters as the financials flexible accounting configuration.

**Note:** Because Flexible Accounting can consume significant space in the financials tables, it is common for organizations to track Flexible Accounting information for only a select group of customers and/or items. This requires creating a separate version of the applicable programs (R42800, P4312, and/or P4314).

**5.3 Step-by-Step Setup Procedure**

Follow these steps to set up Flexible Accounting:

**Step 1 - Identify the AAI to be flexed and define the Flexible account**

Identify which AAI table number will be flexed and define the Flexible definition for that AAI. For example, to flex the Revenue AAI (4230) using an address book number and an item category code:

- The Business Unit field is constructed from a combination of the sold-to address book number and an item category code (e.g., SRP4 from F4211/F4102).
- The Data Type field determines which address book record is used (options: Sold To, Ship To, or Parent Address Number).
- This setup is specific to AAI 4230. Each additional AAI to be flexed requires its own separate setup.

**Step 2 - Define valid combinations in the Branch/Plant**

Define the valid combinations of values that can result from the Flexible configuration. For the revenue account example, the applicable value would be **4242ACC** (address book number 4242 combined with category code ACC).

**Step 3 - Verify chart of accounts**

Confirm that the appropriate chart of accounts information has been established for the flexed branch/plant value.

**Step 4 - Configure the DMAAI correctly**

When using Flexible Accounting, the field being flexed (business unit or subsidiary) must be left **blank** in the DMAAI setup. Entering a hard-coded value would override the Flexible Accounting configuration.

**Example DMAAI configuration:**

- Company: 50000
- Document Type: LM
- GL Class: IN30
- Business Unit: **Blank** (allows Flexible Accounting to populate this field)
- Object Account: 5020

**Step 5 - Activate via processing options**

Set the processing options behind the applicable programs to validate and create Flexible Accounting entries:

- Sales Update (R42800)
- Purchase Order Receipts (P4312)
- Voucher Match (P0411 / P4314)

**Note:** If using both Landed Cost and Flexible Accounting, ensure that the processing option for Landed Cost Selection (P43291) is also configured correctly.

**Section 6: Inventory Applications and Flexible Accounting**

**6.1 Partial Support**

Flexible Accounting is only **partially supported** within the following Inventory programs:

- Issues (P4112)
- Transfers (P4113)
- Adjustments (P4114)
- Reclassification (P4116)

There is no processing option to turn Flexible Accounting on or off for these programs. If AAIs 4122 or 4124 are set up in the Flexible Accounting tables, they will be used automatically.

**6.2 Enabling Flexible Accounting for Inventory Programs**

To enable Flexible Accounting for inventory programs, set up **SM** and **FA** for **XT4111Z1** in the Enable Functionality by Application program (P16902) off menu G1631.

**6.3 Inventory Issues (P4112) - Special Consideration**

Processing options 1 and 2 on the Process tab of Inventory Issues (P4112) control whether a manual account can be entered for the transaction:

- If a manual account is entered, it will be used **in place of** the 4124 AAI.
- Flexible Accounting will **not** be applied to manually entered accounts.
- Flexible Accounting can be set up by object - this works correctly for AAIs 4122 and 4124, but will have **no effect** on manually entered accounts.
