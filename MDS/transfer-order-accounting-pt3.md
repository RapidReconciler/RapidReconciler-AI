**JD Edwards In Transit**

**Training Guide: ST/OT Transfer Order Accounting (Part 3)**

**Topic: OT Receipt Accounting and the Role of DMAAI 4335**

**Section 1: Overview**

This guide continues the series on ST/OT transfer order accounting in JD Edwards. Part 2 covered DMAAI setup when transferring goods with a markup. This installment focuses on the OT (purchase order) receipt side of a transfer at cost, and specifically how DMAAI 4335 is used to handle cost variances that arise between the time a transfer order is entered and when the shipment occurs.

**1.1 Background**

ST/OT transfer orders are used to move materials between branch plants (A to B) within the same company. The process uses a clearing account to hold the value of goods while they are in transit. While goods are in transit, quantities on hand are removed from the perpetual counts and exist only as a balance in the clearing account.

**Section 2: DMAAI Tables Involved in OT Receipt Processing**

Three DMAAI tables are involved during the receipt of an OT order:

| **DMAAI** | **Account**             | **Entry Type**             |
| --------- | ----------------------- | -------------------------- |
| **4310**  | Inventory               | Debit                      |
| **4320**  | RNV / Goods In Transit  | Credit                     |
| **4335**  | Purchased Part Variance | Debit or Credit (variance) |

**Section 3: Scenario - Transfer at Cost with No Cost Change**

**3.1 Setup**

The following example uses a straightforward transfer at cost with no cost changes:

- Item 123, 10 units at \$1 each, transferred from Branch A to Branch B.
- Standard cost in both branch plants: **\$1 each**.
- ST sales price: **\$10**.
- OT purchase price matches the sales cost: **\$1 each**.

**3.2 Accounting Flow - No Variance**

When the 10 units are shipped, a **\$10 debit** hits the Goods In Transit account as expected via DMAAI 4220.

Upon receipt, in a perfect scenario where nothing has changed between shipment and receipt:

- **DMAAI 4310** debits Inventory for **\$10**.
- **DMAAI 4320** credits Goods In Transit for **\$10**.

The Goods In Transit account clears perfectly with no variance, and DMAAI 4335 (Purchased Part Variance) is not needed.

**Section 4: Scenario - Standard Cost Change Between Order Entry and Shipment**

**4.1 The Problem**

A cost change occurring after the transfer order is entered but before the shipment is confirmed can cause the accounting to go out of sync.

**Updated scenario:**

- After the transfer order is entered, the standard cost in Branch A is updated from **\$1.00 to \$1.10**.
- The standard cost in Branch B is also updated to **\$1.10**.

**Important:** If Branch B's standard cost is not updated at the same time, an even more complicated scenario results.

The ST and OT orders still reflect the original **\$1.00** amounts. Here is what happens next:

**4.2 Shipment Confirmation**

When the ST order is ship confirmed, the ship confirmation program automatically updates to the new standard cost. This results in:

- A **\$11.00 credit** to the Inventory account (10 units × \$1.10).
- A matching **\$11.00 debit** to the Goods In Transit account.

**4.3 OT Receipt - The Variance Issue**

The OT purchase order is still expecting a **\$10.00** receipt, as the unit cost on the purchase order has not been updated to reflect the new \$1.10 standard.

Without DMAAI 4335, the accounting at receipt would be:

- **DMAAI 4310** - Branch B's standard is \$1.10, so Inventory is correctly debited **\$11.00**.
- **DMAAI 4320** - The OT unit cost is still \$1.00, so Goods In Transit is only credited **\$10.00**.
- This leaves a **\$1.00 variance** remaining in the Goods In Transit account.

**4.4 Resolution - Using DMAAI 4335**

DMAAI 4335 is designed to absorb this variance and keep the accounting clean. If DMAAI 4335 is configured to point to the **Goods In Transit account** for OT orders, the \$1.00 variance will also clear from Goods In Transit, resulting in a fully balanced accounting entry:

| **DMAAI**      | **Account**                    | **Amount**                |
| -------------- | ------------------------------ | ------------------------- |
| **4310**       | Inventory (Branch B)           | +\$11.00 debit            |
| **4320**       | Goods In Transit               | −\$10.00 credit           |
| **4335**       | Goods In Transit               | −\$1.00 credit (variance) |
| **Net result** | Goods In Transit fully cleared | \$0.00 remaining          |

**Section 5: Key Takeaway and Configuration Recommendation**

Configuring **DMAAI 4335** to point to the Goods In Transit account for OT orders ensures that standard cost variances arising between transfer order entry and shipment confirmation are properly absorbed, keeping the In Transit GL account clean.

**Configuration Recommendation:** Set DMAAI 4335 to the Goods In Transit account for OT order types. This will handle the cost variance scenario described above and prevent unresolved balances from accumulating in the In Transit clearing account.

**Note:** This configuration works correctly for the cost change scenario described in this guide. Additional scenarios - such as cases where the cost changes after shipment but before receipt - may produce different results and will be covered in the next installment of this series.
