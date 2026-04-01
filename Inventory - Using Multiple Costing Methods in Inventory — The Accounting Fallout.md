**JD Edwards Inventory Reconciliation**

**Training Guide: Product Costing**

**Topic: Using Multiple Costing Methods in Inventory - The Accounting Fallout**

**Section 1: Overview**

When setting up inventory items in JD Edwards, one of the most critical decisions is assigning the cost method used for valuation. Common options include:

| **Cost Method** | **Description**       |
| --------------- | --------------------- |
| **01**          | Last-In Cost          |
| **02**          | Weighted Average Cost |
| **07**          | Standard Cost         |

Most organizations select a single cost method and apply it consistently across all inventory items. However, in some environments, standard costing is used for certain items while actual costing (weighted average) is used for others. This mixed approach can create accounting discrepancies in the general ledger that are important to understand and manage.

**Section 2: DMAAI Tables Involved in Purchase Order Receipts**

Three primary DMAAI tables control the accounting for purchase order receipts:

| **DMAAI** | **Account**                   | **Description**                                                                   |
| --------- | ----------------------------- | --------------------------------------------------------------------------------- |
| **4320**  | Received Not Vouchered (RNV)  | Accrues the entire liability owed to the vendor.                                  |
| **4310**  | Perpetual Inventory           | Records the value of units received into on-hand inventory.                       |
| **4335**  | Purchased Part Variance (PPV) | Records any cost difference between the standard cost and the actual amount paid. |

**Section 3: Scenario - Mixed Cost Methods on the Same Purchase Order**

**3.1 Setup**

The following example illustrates the accounting fallout that occurs when standard cost and actual cost items share the same DMAAI configuration:

- **Part 123** - Standard cost item, standard cost = **\$1.00 per unit**, no units on hand.
- **Part 456** - Actual cost (weighted average) item, current cost = **\$10.00 per unit**, no units on hand.
- A purchase order is issued to the same vendor for both parts.
- Vendor charges: **\$1.10** for Part 123 and **\$11.00** for Part 456.

**3.2 General Ledger Entries at Receipt**

**Part 123 - Standard Cost Item:**

| **Account**                    | **Debit** | **Credit** |
| ------------------------------ | --------- | ---------- |
| Perpetual Inventory (4310)     | \$1.00    |            |
| Purchased Part Variance (4335) | \$0.10    |            |
| Received Not Vouchered (4320)  |           | \$1.10     |

This is correct. The inventory is recorded at the standard cost of \$1.00, and the \$0.10 difference between the standard cost and the vendor price is posted to the PPV account.

**Part 456 - Actual Cost Item:**

| **Account**                    | **Debit** | **Credit** |
| ------------------------------ | --------- | ---------- |
| Perpetual Inventory (4310)     | \$10.00   |            |
| Purchased Part Variance (4335) | \$1.00    |            |
| Received Not Vouchered (4320)  |           | \$11.00    |

This is **incorrect**. Because Part 456 is an actual cost item, the inventory value should reflect the actual purchase price of **\$11.00**, not the prior cost of \$10.00. There should be no PPV variance for an actual cost item - the full vendor price should flow directly into inventory.

**Section 4: Why the Issue Cannot Be Resolved with a Single DMAAI Change**

It may seem that the problem could be resolved by changing DMAAI 4335 to point to the Inventory account (4310) instead of the PPV expense account. However, this creates a new problem:

- If DMAAI 4335 points to the **Inventory account**, actual cost items will be handled correctly - the full vendor price will flow into inventory with no variance.
- However, standard cost items will then also post the cost difference to the Inventory account rather than the PPV account, which is **incorrect** for standard costing.

There is no single DMAAI configuration that correctly handles both standard cost and actual cost items simultaneously when they share the same GL class code.

**Section 5: The Correct Solution - Separate GL Class Codes**

The only reliable solution is to assign **separate GL class codes** to standard cost items and actual cost items, ensuring that each group has its own dedicated DMAAI configuration.

| **Item Type**           | **GL Class Code**            | **DMAAI 4335 Configuration**  |
| ----------------------- | ---------------------------- | ----------------------------- |
| **Standard Cost Items** | Dedicated code (e.g., STD01) | Points to PPV Expense account |
| **Average Cost Items**  | Dedicated code (e.g., AVG01) | Points to Inventory account   |

This separation allows each cost method to have the correct accounting treatment without interference from the other.

**Important:** While this is the correct approach, maintaining separate GL class codes for different cost methods requires ongoing discipline in item setup and maintenance. Care must be taken to ensure that new items are assigned the correct GL class code at the time of creation and that the codes are never mixed.

**Section 6: Key Takeaway**

Mixing standard cost and actual cost items under the same GL class code and DMAAI configuration will produce incorrect general ledger entries for one or both item types. This will result in inventory account discrepancies and reconciling items that cannot be resolved without a configuration change.

**Best Practice:** If your organization uses both standard cost and actual cost items, establish and enforce separate GL class codes for each cost method. Document the distinction clearly in your item setup procedures to prevent incorrect assignments and the accounting fallout that follows.