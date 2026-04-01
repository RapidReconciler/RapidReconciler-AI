**Reference Guide: Zero Balance Adjustments**

**Purpose, Purchasing, Inventory, and Sales**

**Section 1: Purpose**

A Zero Balance Adjustment is automatically created in the General Ledger when the inventory quantity for an item goes to zero while a cost value remains associated with that item. This occurs regardless of which inventory cost method is selected in the Cost Revisions file (F4105).

Both inventory and purchasing programs include AAIs that automatically generate a zero balance adjustment when this scenario occurs. The underlying reason is that **an inventory value cannot exist if there is no quantity on hand**. The system generates the adjustment to bring the inventory value to exactly zero.

**Section 2: Zero Balance Adjustments in Purchasing**

**2.1 AAIs Used**

| **AAI**  | **Account**     |
| -------- | --------------- |
| **4400** | Inventory       |
| **4405** | COGS or Expense |

**2.2 Program**

- **P4312** - Enter Receipts by Purchase Order or by Item

**2.3 Conditions That Trigger the Adjustment**

- The inventory quantity goes to zero as a result of a negative quantity purchase order receipt or a receipt reversal.
- A positive or negative cost value still exists for the item after the transaction.

**2.4 Why the Cost in F4105 Changes**

The cost at which inventory was removed is different from the cost that was in the F4105 Cost Revisions file prior to the transaction.

**2.5 Purchasing Example**

**Starting position:**

- Quantity on Hand: **25**
- Unit Cost (cost method 02 - Weighted Average): **\$5.00**
- Total Inventory Value: **\$125.00** (25 × \$5.00)

**Transaction entered:** A purchase order for a quantity of **−25** at a cost of **\$4.00 each** is received.

**Impact:**

|                            | **Quantity on Hand** | **Value** |
| -------------------------- | -------------------- | --------- |
| **Before the transaction** | 25                   | \$125.00  |
| **Transaction amount**     | −25                  | −\$100.00 |
| **After the transaction**  | 0                    | \$25.00   |

After the transaction, the quantity is zero but a value of **\$25.00** still remains. Since an inventory value cannot exist with no quantity on hand, the system automatically generates a zero balance adjustment to reduce the value to zero.

**Journal entries for the receipt transaction:**

| **Entry**              | **Debit** | **Credit** | **AAI** |
| ---------------------- | --------- | ---------- | ------- |
| Inventory              | −\$100.00 |            | 4310    |
| Received Not Vouchered |           | \$100.00   | 4320    |

**Journal entries for the zero balance adjustment:**

| **Entry**       | **Debit** | **Credit** | **AAI** |
| --------------- | --------- | ---------- | ------- |
| Inventory       | −\$25.00  |            | 4400    |
| COGS or Expense |           | \$25.00    | 4405    |

**Resulting Cardex (F4111):**

- Record for PO 5638 (OP): Quantity −25 at \$4.00 each = −\$100.00 extended cost (the receipt).
- Zero balance adjustment record: −\$25.00 to bring inventory value to zero.

The Explanation field on the zero balance adjustment record in the Item Ledger will read **"Zero Balance Adjustment."**

**Section 3: Zero Balance Adjustments in Inventory**

**3.1 AAIs Used**

| **AAI**  | **Account**     |
| -------- | --------------- |
| **4126** | Inventory       |
| **4128** | COGS or Expense |

**3.2 Programs**

- **P4112** - Inventory Issues
- **P4113** - Inventory Transfers
- **P4114** - Inventory Adjustments

**3.3 Conditions That Trigger the Adjustment**

- The inventory quantity goes to zero as a result of an inventory issue, inventory transfer, or negative inventory adjustment.
- A positive or negative cost value still exists for the item after the transaction.

**3.4 Why the Cost in F4105 Changes**

The cost at which inventory was removed is different from the cost that was in the F4105 Cost Revisions file prior to the transaction.

**3.5 Inventory Example**

**Starting position:**

- Quantity on Hand: **30**
- Unit Cost (cost method 02 - Weighted Average): **\$10.00**
- Total Inventory Value: **\$300.00** (30 × \$10.00)

**Transaction entered:** An inventory issue (P4112) for all 30 units at a unit cost of **\$12.00** each.

**Impact:**

|                            | **Quantity on Hand** | **Value** |
| -------------------------- | -------------------- | --------- |
| **Before the transaction** | 30                   | \$300.00  |
| **Transaction amount**     | −30                  | −\$360.00 |
| **After the transaction**  | 0                    | −\$60.00  |

After the transaction, the quantity is zero but a value of **−\$60.00** remains. Since an inventory value cannot exist with no quantity on hand, the system automatically generates a zero balance adjustment to increase the value back to zero.

**Journal entries for the inventory issue:**

| **Entry**       | **Debit** | **Credit** | **AAI** |
| --------------- | --------- | ---------- | ------- |
| Expense or COGS | \$360.00  |            | 4124    |
| Inventory       |           | −\$360.00  | 4122    |

**Journal entries for the zero balance adjustment:**

| **Entry**       | **Debit** | **Credit** | **AAI** |
| --------------- | --------- | ---------- | ------- |
| Expense or COGS | \$60.00   |            | 4128    |
| Inventory       |           | −\$60.00   | 4126    |

**Section 4: Zero Balance Adjustments in Sales**

The Sales system was **not designed** to use Zero Balance Adjustments. This functionality applies only to the Purchasing and Inventory modules as described above.

**Section 5: AAI Reference Summary**

| **Module**     | **AAI** | **Account**     | **Direction** |
| -------------- | ------- | --------------- | ------------- |
| **Purchasing** | 4400    | Inventory       | Debit         |
| **Purchasing** | 4405    | COGS or Expense | Credit        |
| **Inventory**  | 4126    | Inventory       | Credit        |
| **Inventory**  | 4128    | COGS or Expense | Debit         |