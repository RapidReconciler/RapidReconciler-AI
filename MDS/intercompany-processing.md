**Reference Guide: Sales Order Intercompany Processing**

**Section 1: Overview**

The Sales Order Intercompany process is used to fill a customer order from a branch plant other than the revenue/header branch, invoice the customer, and generate an intercompany sales order and purchase order between the two branch plants.

**1.1 Scenario Used in This Guide**

| **Role**             | **Company** | **Branch/Plant** | **Address Book Number** |
| -------------------- | ----------- | ---------------- | ----------------------- |
| **Revenue/Header**   | 00095       | 95               | 95                      |
| **Supplying/Detail** | 00085       | 85               | 85                      |

**Item:** Widget

|                | **Branch/Plant 95** | **Branch/Plant 85** |
| -------------- | ------------------- | ------------------- |
| **Base Price** | \$950.00            | \$850.00            |
| **Cost**       | \$95.00             | \$85.00             |

**1.2 Order Types Used**

| **Order Type** | **Description**                                                    |
| -------------- | ------------------------------------------------------------------ |
| **SI**         | Sales order from Header Branch/Plant 95 to Customer 54391          |
| **SK**         | Intercompany sales order - Branch/Plant 85 bills Branch/Plant 95   |
| **OK**         | Intercompany purchase order - Branch/Plant 95 owes Branch/Plant 85 |

**Note:** Item Widget must be set up in both Branch/Plant 95 and Branch/Plant 85. The SI base price defaults from the header Branch/Plant, not the detail Branch/Plant.

**Section 2: Basic Setup**

**2.1 Sales Order Entry (P4210) Processing Options for SI Creation**

**Interbranch tab:**

- **Processing option 1** - Set to **1** to enable intercompany sales order processing. If left blank, orders with Order Type SI will process as interbranch sales orders (not intercompany).
- **Processing option 2** - Enter the Order Type that triggers intercompany processing. In this example: **SI**.

**Process tab:**

- **Processing option 11 (Cost or Base Price)** - Determines how the cost on the SI is calculated. This is critical because the SI cost becomes the price on the SK and the cost on the OK.

| **Setting** | **Result**                                                  |
| ----------- | ----------------------------------------------------------- |
| **Blank**   | SI cost = cost of item in the Detail Branch/Plant           |
| **1**       | SI cost = cost of item in Detail Branch/Plant plus a markup |
| **2**       | SI cost = base price of the Detail Branch/Plant             |

**Section 3: Creating the SI Sales Order**

**3.1 Order Creation**

- Create the SI header with **Branch/Plant 95** as the Header Branch/Plant and **Customer 54391**.
- Create the SI detail with **Branch/Plant 85** as the Detail Branch/Plant and order 1 unit of Widget.

**Resulting values (with processing option 11 set to 2):**

- Price: **\$950.00** (base price of Widget in Header Branch/Plant 95)
- Cost: **\$850.00** (base price of Widget in Detail Branch/Plant 85)

**3.2 Inter Branch Sales Field (SDSO01)**

After the SI is created, the Inter Branch Sales field (SDSO01) in table F4211 is populated. For intercompany orders (processing option 1 = 1), only values 2 and 4 are used:

| **Value** | **Meaning**                                         |
| --------- | --------------------------------------------------- |
| **2**     | Cost or cost-plus-markup and intercompany invoicing |
| **4**     | Base price as cost and intercompany invoicing       |

In this example (processing option 11 = 2), SDSO01 = **4** because the Detail Branch/Plant base price is the cost. This field is used as data selection in the R4210IC program and also impacts how Sales Update (R42800) creates journal entries for the SI.

**Section 4: Creating the Intercompany SK and OK Orders with R4210IC**

**4.1 Program Overview**

The **Create Intercompany Sales Order (R4210IC)** batch program creates both the SK and OK from the SI:

- **SK** - Intercompany sales order where Detail Branch/Plant 85 bills Header Branch/Plant 95.
- **OK** - Intercompany purchase order where Header Branch/Plant 95 owes Detail Branch/Plant 85.

R4210IC calls a version of Sales Order Entry (P4210) to create the SK, which in turn calls a version of Purchase Order Entry (P4310) to create the OK.

**4.2 R4210IC Processing Options**

| **Tab**      | **Setting**                                                                   |
| ------------ | ----------------------------------------------------------------------------- |
| **Defaults** | Leave blank (reserved for future use).                                        |
| **Process**  | Set to Final mode for production processing.                                  |
| **Versions** | Enter the version of Sales Order Entry (P4210) to be called to create the SK. |

**4.3 Sales Order Entry (P4210) Version for SK Creation**

**Defaults tab:** Populate Order Type, Line Type, Beginning Status, and Line Number Increment.

**Versions tab:** Enter the version of Purchase Order Entry (P4310) to be called to create the OK. Leave all other processing options blank.

**Line Type for SK (IC):**

- Inventory Interface: **N**
- Edits against the item master - allows the item's GL Offset to be used on the SK.
- The Generate Purchase Order flag does not need to be set; R4210IC creates both SK and OK automatically.
- Order Activity Rules must be set up for Order Type SK and Line Type IC.

**Note:** The Header Branch/Plant Address Book Number must be set up as a **customer** in the Customer Master and Customer Billing Instructions, as the SK bills the Header Branch/Plant.

**4.4 Purchase Order Entry (P4310) Version for OK Creation**

**Defaults tab:** Populate Order Type, Line Type, Beginning Status, and Line Number Increment. Leave all other processing options blank.

**Line Type for OK (D):**

- Inventory Interface: **D**
- Supports a two-way voucher match process.
- The Generate Purchase Order flag setting is not considered by R4210IC.
- Order Activity Rules must be set up for Order Type OK and Line Type D.

**Note:** The Detail Branch/Plant Address Book Number must be set up as a **supplier** in the Supplier Master and Supplier Instructions, as the OK creates a payable to the Detail Branch/Plant.

**4.5 Data Selection for R4210IC**

| **Field**                             | **Condition**   | **Purpose**                                                                                                                                     |
| ------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **BC Document-Original (SDODOC)**     | Equal to zero   | Prevents SI lines already processed by R4210IC from being reprocessed (SDODOC is updated with the SK order number after successful processing). |
| **BC Sales Order Status 15 (SDSO15)** | Not equal to 1  | This field is for future use and will be blank on SI records.                                                                                   |
| **BC Inter Branch Sales (SDSO01)**    | Equal to 2 or 4 | Ensures only intercompany SI orders are processed.                                                                                              |

**Best Practice:** Include the ship confirm next status code in data selection so only ship-confirmed SIs are processed by R4210IC.

**Section 5: Submitting the R4210IC**

**5.1 Automatic Submission via Ship Confirm**

When the SI is ship confirmed using Confirm Shipments (P4205), the program can automatically submit R4210IC to create the SK and OK.

**Interbranch tab of P4205:**

- **Processing option 1** - Enter the version of R4210IC to be submitted.
- **Processing option 2** - Controls how R4210IC is submitted:
  - **Blank** - R4210IC will not be submitted by ship confirm (must be submitted manually).
  - In **Xe**, ship confirm can only submit R4210IC in **subsystem mode** due to transaction processing.
  - In **B733 cum 2**, ship confirm can submit R4210IC in either batch or subsystem mode.

**5.2 Order Cross-Reference**

After R4210IC completes, the SK and OK are linked to the SI through the following fields:

| **Order** | **Field** | **Stored Value**       |
| --------- | --------- | ---------------------- |
| SI (6131) | SDODOC    | SK order number (260)  |
| SI (6131) | SDODCT    | SK order type (SK)     |
| SK (260)  | SDOORN    | SI order number (6131) |
| SK (260)  | SDRORN    | OK order number (5114) |
| OK (5114) | PDRORN    | SK order number (260)  |

**To view cross-reference information:**

- **SI → SK:** Customer Service Inquiry (P4210), inquire on the SI, take the Additional Information row exit.
- **SK → SI and OK:** Customer Service Inquiry (P4210), inquire on the SK, take the Additional Information row exit.
- **OK → SK:** Open Order Inquiry (P4310), inquire on the OK, take the Order Detail row exit, then the Additional Information form exit.

**Section 6: Invoicing the SI and SK**

Both the SI customer invoice and the SK intercompany invoice can be generated through **Print Invoices (R42565)**. Different versions can be configured to assign separate Invoice Document Types to each:

| **Order** | **Invoice Document Type** | **Invoice Number (Example)** |
| --------- | ------------------------- | ---------------------------- |
| SI (6131) | RI                        | 6418 RI 00095                |
| SK (260)  | RT                        | 6419 RT 00085                |

**Section 7: Running Sales Update (R42800) for SI, SK, and OK**

**7.1 Overview**

Sales Update (R42800) must process all three orders to:

- Create an A/R invoice for the SI customer.
- Create an A/R invoice for the SK customer (Header Branch/Plant 95).
- Create an A/P voucher for the OK supplier (Detail Branch/Plant 85).

**7.2 Interbranch Tab Processing Options for R42800**

| **Option**   | **Setting**      | **Purpose**                                                                                                                                                                                         |
| ------------ | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Option 1** | SK               | Order Type created by R4210IC to be processed.                                                                                                                                                      |
| **Option 2** | 1                | Creates the A/R batch for SK/RT and the A/P batch for OK/PV. This must be set - unlike interbranch processing, intercompany requires both an SK invoice and an OK voucher to be created and closed. |
| **Option 3** | Version of P4314 | Version of Voucher Match to use for OK voucher creation.                                                                                                                                            |

**7.3 Voucher Match (P4314) Setup**

**Defaults tab:** Set Order Type to **OK** and Voucher Type to **PV**.

**Process tab:** Define the allowable From and Through Status Code ranges for the OK. In this example, the OK is at status 440 after creation by R4210IC.

**Section 8: Journal Entries for SI, SK, and OK**

Sales Update (R42800) creates three batches: an IB batch for the SI, an IB batch for the SK, and a V batch for the OK.

**8.1 SI Journal Entries (Invoice 6418 RI 00095)**

| **Account**                    | **Debit** | **Credit**   | **AAI**                  |
| ------------------------------ | --------- | ------------ | ------------------------ |
| A/R 00095                      | \$950.00  |              | RC                       |
| Revenue 00095                  |           | \$950.00     | 4230 (00095 SI IN30)     |
| COGS 00095                     | \$850.00  |              | 4220 (00095 SI IN30)     |
| **In Transit/Inventory 00095** |           | **\$850.00** | **4240 (00095 SI IN30)** |

**8.2 SK Journal Entries (Invoice 6419 RT 00085)**

| **Account**     | **Debit** | **Credit** | **AAI**              |
| --------------- | --------- | ---------- | -------------------- |
| A/R 00085       | \$850.00  |            | RC                   |
| Revenue 00085   |           | \$850.00   | 4230 (00085 SK IN30) |
| COGS 00085      | \$85.00   |            | 4220 (00085 SK IN30) |
| Inventory 00085 |           | \$85.00    | 4240 (00085 SK IN30) |

**8.3 OK Journal Entries (Voucher 7428 PV 00095)**

| **Account**                    | **Debit**    | **Credit** | **AAI**                  |
| ------------------------------ | ------------ | ---------- | ------------------------ |
| **In Transit/Inventory 00095** | **\$850.00** |            | **4310 (00095 OK IN30)** |
| A/P 00095                      |              | \$850.00   | PC                       |

**8.4 In Transit Account Explanation**

Sales Update hits the 4240 (Inventory) AAI with Company 00095 for the SI because Company 00095 is the header company. Since Company 00095 did not physically ship any product, this journal entry must be washed out. The SI credit to AAI 4240 in Company 00095 is offset by the debit to AAI 4310 in Company 00095 when the OK is processed.

**Recommendation:** Configure DMAAI 4240 for Company 00095 and Order Type SI to point to an **In Transit account**. Configure DMAAI 4310 for Company 00095 and Order Type OK to point to the same In Transit account, effectively clearing it when the OK voucher is created.

**8.5 Key Principle - Cost Alignment**

The cost on the SI must equal the price on the SK and the cost on the OK. This is because:

- The SI cost credit must be washed out by the OK cost debit.
- The OK cost and SK price must be equal so the OK A/P voucher can pay the SK A/R invoice.

Advanced pricing and price discounting do not affect the price on the SK. The SK line is a non-stock line with a price derived from the SI cost. One recommended approach for applying discounts is through **payment terms** on the SK and OK, which can carry discount amounts to be applied during A/P check creation and A/R cash receipts processing.

**Section 9: Cost or Base Price Markup Processing Option**

**9.1 Using Cost Plus Markup (Processing Option 11 = 1)**

When processing option 11 is set to 1, the SI cost is calculated as the Detail Branch/Plant item cost plus a configured markup percentage.

**Setting Up Branch Markup:**

Access **Branch Sales Markup (P3403)** on menu G4241 and configure the markup from Branch/Plant 85 to Branch/Plant 95 for the applicable item. Markups can also be defined based on the item's sales catalog section category code (UDC table 41/S1).

**Example:** Item Widget cost in Branch/Plant 85 = \$85.00 with 100% markup:

- SI Cost = \$85.00 + \$85.00 = **\$170.00**
- SI Price = **\$950.00** (base price in Header Branch/Plant 95)
- SDSO01 field = **2** (cost or cost-plus-markup, intercompany invoicing)
- SK Price = **\$170.00** (SI cost)
- OK Cost = **\$170.00** (SI cost)
- SK Cost = **\$85.00** (item cost in Branch/Plant 85)

**9.2 Using Item Cost (Processing Option 11 = Blank)**

When processing option 11 is blank, the SI cost equals the item cost in the Detail Branch/Plant with no markup.

**Example:**

- SI Cost = **\$85.00** (item cost in Branch/Plant 85)
- SI Price = **\$950.00** (base price in Header Branch/Plant 95)
- SDSO01 field = **2**
- SK Price = **\$85.00**
- OK Cost = **\$85.00**

**Section 10: Intercompany Settlements**

Sales Order Intercompany processing follows the same rules as all other multi-company journal entries with respect to the **Intercompany Settlements flag** in the General Accounting constants.

When a journal entry spans multiple companies, the Post program (R09801) balances the entries between companies based on this flag. Two flags are relevant:

| **Flag**                                           | **Description**                                                                                                                                                                                         |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Intercompany Settlements**                       | Balances journal entries that span multiple companies upon posting.                                                                                                                                     |
| **Allow Multi-Currency Intercompany Transactions** | Determines whether journal entries can be created across companies with different base currencies. If set to No, intercompany orders between companies with different currencies will not be permitted. |

General Accounting Intercompany setup is managed as part of General Accounting processing and applies uniformly to all multi-company transactions, including intercompany sales orders.
