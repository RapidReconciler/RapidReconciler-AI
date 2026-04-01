**JD Edwards In Transit**

**Training Guide: ST/OT Transfer Order Accounting (Part 4)**

**Topic: Standard Cost Variance on OT Receipt**

**Section 1: Overview**

This guide continues the series on ST/OT transfer order accounting in JD Edwards. Part 3 covered DMAAI setup for transferring goods at cost where the cost changes between order entry and shipment. This installment examines a related but distinct scenario - where the standard cost in the receiving branch has **not** been updated to match the shipping branch, and how DMAAI 4335 must be configured differently as a result.

**1.1 Background**

ST/OT transfer orders are used to move materials between branch plants (A to B) within the same company. A clearing account holds the value of goods while they are in transit. While in transit, quantities on hand are removed from the perpetual counts and exist only as a balance in the clearing account.

**Section 2: DMAAI Tables Involved in OT Receipt Processing**

Three DMAAI tables are involved during the receipt of an OT order:

| **DMAAI** | **Account**             | **Entry Type**             |
| --------- | ----------------------- | -------------------------- |
| **4310**  | Inventory               | Debit                      |
| **4320**  | RNV / Goods In Transit  | Credit                     |
| **4335**  | Purchased Part Variance | Debit or Credit (variance) |

**Section 3: Scenario - Standard Cost Not Updated in Receiving Branch**

**3.1 Setup**

The following example uses a transfer at cost where the standard cost has not been updated in the receiving branch:

- Standard cost in **Branch A**: **\$1.00 per unit**
- Standard cost in **Branch B**: **\$0.90 per unit** (not updated)
- Transfer: 10 units of the same item
- ST sales price: **\$1.00** (based on Branch A cost)
- OT purchase price: **\$1.00** (matches ST cost/price at time of order creation)

**3.2 Shipment from Branch A**

When the ST order is ship confirmed, the following entries are generated correctly:

- **\$10.00 credit** to the Inventory account (Branch A).
- **\$10.00 debit** to the Goods In Transit account.

The Goods In Transit account now carries a balance of **\$10.00**.

**Section 4: OT Receipt - Accounting Flow with DMAAI 4335**

At the time of receipt, the OT order is still expecting a **\$10.00** receipt. The standard cost in Branch B remains at **\$0.90** and has not been updated. The following entries are generated:

| **DMAAI** | **Account**          | **Amount**      | **Explanation**                                                                                                                    |
| --------- | -------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **4310**  | Inventory (Branch B) | +\$9.00 debit   | Branch B's standard cost is \$0.90 × 10 units = \$9.00. Inventory is correctly debited at the receiving branch's standard cost.    |
| **4320**  | Goods In Transit     | −\$10.00 credit | The OT purchase order unit cost is \$1.00 × 10 units = \$10.00. Goods In Transit is fully credited, clearing the clearing account. |
| **4335**  | PPV Expense Account  | +\$1.00 debit   | The \$1.00 variance (\$10.00 − \$9.00) is expensed to the Purchased Part Variance (PPV) account.                                   |

**Net result:** The Goods In Transit account is fully cleared, inventory in Branch B is recorded at the correct standard cost, and the \$1.00 variance is properly expensed to the PPV account.

**Section 5: Comparison to Part 3 - Why the DMAAI 4335 Setup Differs**

A critical point arises from comparing Part 3 and Part 4 of this series. In Part 3, DMAAI 4335 was configured to point to the **Goods In Transit account** to absorb a variance caused by a cost change that occurred after order entry. In this scenario, DMAAI 4335 must be configured to point to the **PPV Expense account**.

The reason for the difference is the nature of the variance:

| **Scenario**                                                       | **Variance Type**                                    | **DMAAI 4335 Configuration**                                         |
| ------------------------------------------------------------------ | ---------------------------------------------------- | -------------------------------------------------------------------- |
| **Part 3** - Cost changed after order entry; both branches updated | Timing variance between order cost and shipment cost | Point to **Goods In Transit** account to clear the remaining balance |
| **Part 4** - Standard cost not updated in receiving branch         | True standard cost variance between branches         | Point to **PPV Expense** account to properly expense the variance    |

**Section 6: Key Takeaway - There Is No Perfect DMAAI Setup**

DMAAI 4335 can only be configured one way in JD Edwards. Because different scenarios require different accounting treatment, there is no universally correct configuration for transfer order accounting.

**Best Practice Recommendation:** Analyze the transfer order scenarios that occur most frequently in your organization and configure DMAAI 4335 to handle those scenarios correctly. Document the configuration decision and the rationale so that any exceptions - where a different scenario occurs - can be identified and managed through manual journal entries or procedural controls.

Understanding the accounting impact of each scenario is essential for maintaining an accurate In Transit GL account and avoiding unexpected reconciling items at period end.