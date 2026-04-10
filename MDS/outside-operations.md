**Reference Guide: Outside Operations**

**Explanation, Setup, Execution, and Accounting**

**Section 1: Overview**

An Outside Operation is Manufacturing's vehicle to interface with Accounts Payable, allowing a purchase order to be created in the system so that when a vendor sends an invoice for their services, a voucher match can be performed. An Outside Operation represents **payment for services rendered** - it is not an inventoried item.

**Important:** The setup of an outside operation is not complicated, but each step must be followed exactly. Deviating from the prescribed sequence will produce incorrect or incomplete results.

**Section 2: Item Master Setup (F4101)**

**2.1 Item Number Format**

The item number for an outside operation **must** follow this naming convention:

**Parent Item Number + \*OP + Operation Sequence Number**

Example: 333\*OP10

**Note:** JD Edwards World software supports decimal-separated operation sequence numbers (e.g., 333\*OP10.6). EnterpriseOne does **not** support this convention.

If the Short Item Number (ITM) or Catalog Number (AITM) is used instead of the formatted second item number, the following will fail:

- The Purchase Order will not be created.
- Product Costing will not generate a Dx cost on the parent item.
- A cost for the Outside Operation in F30026 will not be generated.

**2.2 Required Item Master Fields**

| **Field**                       | **Required Value** | **Notes**                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stocking Type (STKT)**        | X                  | The second description of the X stocking type must be **"P"** in UDC table 41/I.                                                                                                                                                                                                                                                                              |
| **Line Type (LNTY)**            | X                  | Maintains the link between the Purchase Order and the Work Order by controlling whether P3103 is displayed after PO receipt.                                                                                                                                                                                                                                  |
| **Inventory Cost Level (CLEV)** | 1 or 2             | Cost Level 3 is not supported. Outside Operations are non-inventory items (payment for services). Multi-Location, Lot Numbers, and Serial Numbers are not supported. Do not make the \*OP item lot-controlled - the OV will be written to the location in the PO fold, but the IM will always be written to the Primary Location, causing integrity problems. |

**Section 3: Item Branch Setup (F4102)**

- The Stocking Type and Line Type will default from the Item Master - **do not change them**.
- A value **must** be entered in the **Cost Revision (F4105)** table, because this is a purchased part with Stocking Type X and a second description of "P."

**Section 4: Work Center Setup (F3006)**

The following fields must be configured correctly for the outside operation work center:

| **Field**                | **Required Value**                                     | **Notes**                                                     |
| ------------------------ | ------------------------------------------------------ | ------------------------------------------------------------- |
| **Pay Point**            | 0 (zero)                                               | May be set to "M" if there are very long lead times.          |
| **Prime Load Code**      | O                                                      | Required for outside operation processing.                    |
| **Critical Work Center** | N (No)                                                 | -                                                             |
| **Move or Queue Hours**  | Populate if lead time should default into the routing. | Alternatively, populate these fields directly in the Routing. |

**Section 5: Routing Master Setup (F3003)**

**5.1 Operation Sequence**

The sequence number used in the item number must correspond to the **operation sequence of the Outside Operation** in the defined routing.

**5.2 Required Fields for the Outside Operation Routing Step**

| **Field**                  | **Requirement**                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Supplier Number (VEND)** | Must be a valid Address Book number. This is the supplier to whom the Purchase Order will be written.                                                                                                                                                                                                                                                                                                                                                                                     |
| **PO (POY)**               | Must be set to **Y**.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Cost Type (COST)**       | Must use a cost component starting with **"D"** (reserved by JD Edwards for Outside Operations). If multiple Outside Operations exist on the same routing, each must use a unique number (e.g., D1, D2, D3). Each cost type must be defined in UDC table **30/CA** with the Special Handling Code set to **"1"**. If outside operations are not being used, this field must be **blank** - if it is not blank, Manufacturing Accounting (R31802A) will generate a "Divide by Zero" error. |

**5.3 Position in the Routing**

The Outside Operation **cannot be the last step** on the routing for two reasons:

- If using Super Backflush, completion cannot occur to an outside operation work center because the pay point must be zero. The last routing operation must be a payable pay point.
- The purchasing receipt will not update the F43121, which prevents voucher match from being performed.

**Workaround:** Add an additional routing step after the outside operation (e.g., "Receive Outside Op") with no machine or labor hours. If using Super Backflush, this final step must be set as a pay point.

**Section 6: Standard Cost Simulation and Freeze**

**6.1 Standard Cost Simulation (R30812)**

On the Processing tab, enter a valid F4105 cost method that has a cost value associated with it for the Outside Operation in **option 3b**.

A successful R30812 run will produce:

- An **A1 cost** for the \*OP item.
- A **"D" type cost component** on the parent item for the Outside Operation.

**6.2 Frozen Update (R30835)**

After simulation, run the Frozen Standard Update (R30835) to freeze the costs.

**Section 7: Generate and Print Work Orders (R31410)**

**7.1 Processing Options**

**Process tab - Generate Parts List and Routing Instructions:**

- Enter **2** or **3** to attach a routing.

**Routing tab - Purchase Order Information (options 2, 3, and 4):**

- Enter the Document Type to be used for the Purchase Order.
- Set the Line Type to **X**.
- Enter a beginning status corresponding to the Order Activity Rules for Purchasing.

**Important:** The work order routing must be attached using R31410. Without this, no Outside Operation Purchase Order will be generated. R31410 calls P3420 (Write Purchase Order) to create the PO.

**7.2 Results**

When R31410 completes successfully:

- The **Related PO fields** in the fold are populated with the Related Purchase Order Number and Document Type.
- An **F3112 record** is created for the Outside Operation with the Quantity (UORG) and Quantity at Operation (QMTO) populated with the quantity for which the PO was issued.

**Note:** An enhancement introduced in EnterpriseOne release 8.9 supports interactive attachment of routings with outside operation PO generation.

**Section 8: Purchase Order Receipt (P4312 - G43A11)**

**8.1 Receipt Procedure**

- Receive the Outside Operation Purchase Order by entering **1** in the REC OPT field and clicking OK.
- Ensure the **Location (LOCN)** and **Lot/SN (LOTN)** fields are **blank** in the line detail of the Purchase Order.
- Confirm that the beginning status and document type match the processing option values in R31410, P4311, and P4312.
- Confirm that Order Activity Rules are set up for **Line Type X** (accessed from G43A41).

**8.2 What Happens at Receipt**

When the Purchase Order is received:

- An **OV transaction** is written to the cardex, increasing the on-hand balance.
- The **P3103 window** displays immediately after entering the receipt. This window creates an **IM record** in the cardex for the opposite amount of the OV. The net effect is a **zero on-hand balance**.
- The IM will always be written to the **primary location**.
- In the F3112 record: Quantity (UORG) remains the same; Quantity at Operation (QMTO) is decreased by the quantity received; Quantity Shipped (SOQS) is increased by the quantity received.

**8.3 Journal Entries at Receipt**

Three purchasing AAIs are used at receipt:

| **AAI**  | **Entry** | **Account**                  | **Notes**                                                                       |
| -------- | --------- | ---------------------------- | ------------------------------------------------------------------------------- |
| **4310** | Debit     | Inventory                    | Should be an offsetting account with AAI 3401. Balances the 4320 journal entry. |
| **4320** | Credit    | Received Not Vouchered (RNV) | Interfaces with Accounts Payable.                                               |
| **4335** |           | Standard Cost Variance       | Used when a standard cost variance exists.                                      |

**Section 9: Manufacturing WIP Journal Entries (R31802A)**

**9.1 Overview**

After the Outside Operation Purchase Order has been fully or partially received, R31802A can be run to produce **IH journal entries** related to the Outside Operation.

**9.2 Journal Entries Produced**

| **AAI**  | **Entry** | **Account**           | **Notes**                                                                                                                                                                    |
| -------- | --------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **3120** | Debit     | Work In Process (WIP) | Represents the value of the Outside Operation incorporated into the parent cost.                                                                                             |
| **3401** | Credit    | Accruals              | Should use the same account number as AAI 4310 - both accounts are primarily used to balance 3120 and 4320 and are otherwise relatively meaningless as stand-alone balances. |

**9.3 R31802A Calculation**

R31802A performs the following calculation to determine the IH journal entry amount:

**(SOQS − CLUN) × F30026 cost of the Outside Operation**

| **Field** | **Description**  | **Source Table** |
| --------- | ---------------- | ---------------- |
| **SOQS**  | Quantity Shipped | F3112            |
| **CLUN**  | Actual Units     | F3102            |

An **IH document type** journal entry is created for the resulting amount. After the calculation, the system updates CLUN in F3102 to match SOQS in F3112, ensuring that duplicate IH journal entries are not created for the Outside Operation.

**Note:** The Batch Number, GL Date, User ID, and Program ID are **not** updated in the cardex for the IM entry that corresponds to the Outside Operation.
