**Reference Guide: Weighted Average Cost**

**Overview, Setup, and Functionality**

**Warning:** Weighted Average Cost is not designed to be used in an environment where the Inventory On Hand Quantity is allowed to go negative.

**Section 1: Overview**

Weighted Average Cost is **cost method 02** in JD Edwards. The system uses a weighted average formula to recalculate an item's per-unit average cost. The recalculation can occur in two ways:

- **Online** - Recalculated automatically after each transaction is completed.
- **Batch mode** - Recalculated by running the Update Average Cost program (R41811).

The programs that impact weighted average cost can be individually configured. The system will calculate weighted average costs whether or not cost method 02 is designated as the current sales/inventory cost method.

**Section 2: Weighted Average Cost Calculation Formula**

The weighted average cost is calculated using the following formula:

**New Average Cost = (Quantity on Hand × Current Average Cost + Transaction Quantity × Transaction Cost) ÷ (Quantity on Hand + Transaction Quantity)**

The final weighted average cost resulting from a series of transactions will be the same regardless of whether the recalculation is performed online or in batch mode. The order in which transactions are processed does not affect the final result.

**Section 3: Recalculation vs. Changing Weighted Average Cost**

**3.1 Recalculation (Online or Batch)**

Recalculating the weighted average cost - either online or in batch - does **not** create an IB transaction (inventory re-evaluation adjustment) and does **not** generate any journal entries. The inventory value has not changed; the system has simply averaged the per-unit cost of existing inventory with the per-unit cost of the new transaction(s).

**3.2 Manual Change via Cost Revisions (P4105)**

If the weighted average cost is manually changed in the **Cost Revisions program (P4105)**, an **IB transaction** will be created and will appear in the Cardex (F4111). This occurs because the value of the inventory has changed as a direct result of the manual modification.

**Section 4: Setup**

**4.1 Setting the Sales/Inventory Cost Method**

To use weighted average cost as the sales/inventory cost method:

- Navigate to **Cost Revisions (P4105)** on menu **G4112**.
- Set the **Sales/Inventory cost method** to **"02"**.

All costs are stored in the Item Cost file (F4105) in the primary unit of measure.

**4.2 UDC Table 40/AV - Controlling Which Programs Affect Weighted Average Cost**

UDC table **40/AV** lists every program that can affect weighted average cost. The **Description 02** column controls whether each program participates in the recalculation:

| **Description 02 Value** | **Behavior**                                           |
| ------------------------ | ------------------------------------------------------ |
| **Y**                    | The program will affect the weighted average cost.     |
| **N**                    | The program will not affect the weighted average cost. |

**Note:** Adding programs to UDC 40/AV that were not included when the table shipped will have no effect on weighted average cost processing.

**4.3 Configuration Considerations by Transaction Type**

The following guidance may assist in determining configuration. One setup is not recommended over another - these are business decisions:

**Inventory Transactions (Issues, Transfers, Adjustments, Reclassifications):** To prevent inventory transactions from affecting weighted average cost, set Description 02 to **"N"** for programs P4112, P4113, P4114, and P4116 in UDC 40/AV.

**Sales Transactions:**

- If the order type is set up in UDC **40/IU**, weighted average cost is calculated at **Shipment Confirmation (P4205)** - not at Sales Update (R42800).
- If the order type is not in UDC 40/IU, weighted average cost is calculated at **Sales Update (R42800)**.
- Because inventory can only be relieved once per sales detail line, the weighted average cost calculation will only be performed once - even if both P4205 and R42800 are set to "Y" in UDC 40/AV.

**Purchasing Transactions:**

- If both PO Receipt (P4312) and Voucher Match (P0411/P4314) are set to "Y" in UDC 40/AV, the recalculation will only be done at **receipt** unless a different cost is used at Voucher Match.
- If Voucher Match uses a different cost than the Receipt, the calculation done at receipt is ignored and the recalculation is based on the cost at Voucher Match.

**Example:**

| **Step**                                        | **Quantity on Hand** | **Average Cost** | **Calculation**           |
| ----------------------------------------------- | -------------------- | ---------------- | ------------------------- |
| Initial state                                   | 50                   | \$10.00          | -                         |
| PO Receipt: 50 units at \$20                    | 100                  | **\$15.00**      | (50×\$10 + 50×\$20) ÷ 100 |
| Voucher Match: same PO at \$25 (different cost) | 100                  | **\$17.50**      | (50×\$10 + 50×\$25) ÷ 100 |

**Transfer Orders:** If different costs are used in different branch plants, the price on the sales order becomes the cost on the purchase order and will affect the weighted average cost in the receiving branch plant - unless both P4312 and P0411/P4314 are set to "N" in UDC 40/AV.

**Important:** If UDC 40/AV is configured so that neither PO Receipt nor Voucher Match affects weighted average cost, **no** purchasing receipts or voucher matches will affect weighted average cost - regardless of whether the purchase order was created through the transfer order program, purchase order entry, or released from a blanket or quote.

**Section 5: Online vs. Batch Mode**

**5.1 Online Recalculation**

To have weighted average cost recalculated automatically after each transaction:

- Navigate to **System Constants** by taking the form exit from Branch/Plant Constants (P41001).
- Check the **"Update Average Cost On-Line"** option.

**5.2 Batch Mode Recalculation**

The **Update Average Cost (R41811)** program is the batch mode alternative. Key characteristics:

- The program has no processing options.
- It is based on the **Average Cost Work File (F41051)**.
- Data selection can be used to target specific items or branch plants.
- When System Constants is **not** set to update online, each transaction completed by a program listed in UDC 40/AV will create a record in F41051 - regardless of whether cost method 02 is the current sales/inventory cost method.
- When R41811 is run, it processes and **purges** the records from F41051 that it has processed.

**Section 6: Alternative Language Consideration**

If a user is operating in an alternative language and weighted average cost is not updating despite correct setup, verify whether the alternative language version of UDC 40/AV has been enabled:

- Enter **UDC** on the fast path.
- Enter **40/AV** and click **Find**.
- Highlight a program and take the **Language** row exit to verify the alternative language settings.

**Section 7: Impact of Landed Cost**

Landed Cost Rules can be configured to be included in or excluded from weighted average cost calculations. Setup must be completed in two places:

- **UDC 40/AV** - Program **P43291** must have Description 02 set to **"Y"**. If this is not set to "Y," the second configuration step will have no effect.
- **Landed Cost Revisions (P41291)** off menu G43A41 - The **"Include in Unit Cost Y/N"** field must be set:
  - **Y** - The landed cost is included in the transaction cost and will affect the weighted average cost.
  - **N** - The landed cost will not affect the weighted average cost.
