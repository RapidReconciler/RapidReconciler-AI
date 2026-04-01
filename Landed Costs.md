**Reference Guide: Landed Costs**

**Functionality, Setup, and Journal Entries**

**Section 1: Overview**

Landed costs are used to automatically add additional fees to an item's cost to account for expected charges associated with the delivery or handling of a purchase order. Examples include:

- Harbor Fees
- Brokerage Fees
- Commissions
- Import Duties

**1.1 Key Rules**

- Landed costs are costs that **exceed** the purchase price of an item.
- Landed costs are applied to an **individual item line** - they cannot be applied to the total cost of a purchase order.
- Landed costs are **not taxable**.

**Section 2: Setup**

**2.1 Assignment Methods**

Landed costs may be assigned in two ways:

- By a **specific Item and Branch/Plant combination**.
- By a **Cost Rule** - a named group of landed costs that can be reused across items and suppliers.

**2.2 Required UDC Table Setup**

| **UDC Table** | **Purpose**                                                             |
| ------------- | ----------------------------------------------------------------------- |
| **41/P5**     | All Landed Cost Rules must exist in this table before they can be used. |
| **40/CA**     | Defines the Landed Cost Level, used to calculate additional fees.       |
| **41/9**      | All GL class codes used for landed costs must be included here.         |

**2.3 Assigning a Cost Rule**

After creating a Cost Rule, it can be assigned to any of the following:

- An inventory item (Item Branch/Plant Category Codes - P41026).
- A supplier (Supplier Master, Purchasing1 tab - P04012).
- A purchase order header (Additional Information form exit in P4310).
- A purchase order detail line (Additional Information in P4310).
- A processing option in Purchase Order Entry (P4310).

**2.4 Calculation Methods**

Landed costs can be calculated using any of the following methods:

| **Method**                   | **Description**                                                                                | **Example**                                          |
| ---------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Percentage of unit price** | Entered as a whole number (e.g., 5% entered as 5.00). Calculated as: % × quantity × unit cost. | 5% of a PO line with quantity 10 at \$10.00 = \$5.00 |
| **Fixed dollar amount**      | A flat fee applied per unit.                                                                   | -                                                    |
| **Rate × weight or volume**  | Rate entered as a whole number per unit of weight or volume.                                   | \$4.50/lb for a 10 lb item with quantity 1 = \$45.00 |

**2.5 Landed Cost Level and Basis**

All landed costs must be assigned a **Landed Cost Level** from UDC 40/CA. The **Based on Level** field controls what the landed cost is calculated against:

- The **purchase order line only**, or
- The **purchase order line plus a previously applied landed cost level** (cumulative calculation).

**2.6 GL Class Code**

The GL Class determines how landed costs are routed to the general ledger via AAIs 4385 and 4390. Different GL classes can direct landed costs to different accounts.

**Examples:**

- LC21 → Harbor Fees
- LC24 → Brokerage Fees

**Note:** If the GL class is left blank in Landed Cost Revisions, the system retrieves the GL class from the Item Location record.

**2.7 Landed Cost Configuration Options**

Each landed cost can also be configured with the following options:

| **Field**                 | **Description**                                                                                                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effective Dates**       | Limits the landed cost to a specific date range (e.g., Effective From 01/01/00 to Effective Thru 12/31/00).                                                                           |
| **Supplier**              | The landed cost can be paid to a different supplier than the one on the PO. The alternate supplier number is entered in the landed cost level.                                        |
| **Voucher (Y/N)**         | Determines whether the landed cost is eligible for voucher match processing. "Y" sets the PRLAND field to 2 (eligible); "N" sets it to 3 (not eligible - accrual only).               |
| **Include in Cost (Y/N)** | Determines whether the landed cost updates the item's unit cost. "Y" updates the Average Cost and Last-In buckets (UDC 40/AV applies). "N" does not update any inventory cost bucket. |

**Notes:**

- The purchasing bucket (08) is never updated by landed cost.
- The standard cost bucket (07) is never updated by landed cost.

**Section 3: Attaching a Landed Cost Rule - Hierarchy**

A Landed Cost Rule can be attached through multiple programs. When more than one assignment exists, the system follows this hierarchy (highest to lowest priority):

- Cost Rule - Item Branch/Plant combination (P41291)
- Purchase Order Header - Additional Information
- Processing option behind Purchase Order Entry P4310 (Landed Cost Rule)
- Purchasing Instructions from the Ship To address
- Landed Cost category code in the Item Branch/Plant Category Codes (P41026)

**Note:** Processing option #14 on the Defaults tab of Purchase Order Entry (P4310) in release 8.9 allows the Cost Rule Selection to default from either the Purchasing Instructions of the Ship To or the Supplier.

**Section 4: Applying Landed Costs**

Landed costs are applied and calculated using **Landed Cost Revisions (P41291)**. This program can be invoked at three points in the purchasing process:

| **Point**            | **Program**                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| **At Receipt**       | Purchase Order Receipts (P4312)                                           |
| **At Voucher Match** | Voucher Match to Open Receipt (P4314), called from P0411                  |
| **Stand-Alone**      | Stand Alone Landed Cost (P43214) - used between receipt and voucher match |

**4.1 Applying Landed Costs at Receipt (P4312)**

Processing option #6 on the Process tab of P4312 controls landed cost behavior at receipt:

| **Setting** | **Behavior**                                                                                                                                                                                                                                                                                         |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**       | Form W43291A displays after the receipt is accepted. Review and modify unit cost and extended cost as needed. Enter option **1** in the option column to include the landed cost. Click **OK** to create journal entries and F43121 records. Click **Cancel** to exit without applying landed costs. |
| **2**       | "Blind Landed Cost" - landed costs are applied and calculated automatically without displaying form W43291A. Used when landed cost fees are consistent and do not require review.                                                                                                                    |
| **Blank**   | No landed cost is applied or calculated.                                                                                                                                                                                                                                                             |

**Note:** If a purchase order receipt is reversed, any landed costs applied to those items - including journal entries, F43121 records, and F4111 (cardex) records - will also be reversed.

**4.2 Stand-Alone Landed Cost (P43214)**

Used to apply landed costs **after receipt and before voucher match**.

**Note:** Landed costs cannot be reversed through the Stand Alone program (P43214: ZJDE0003). Reversal is possible only if the purchase order itself is reversed using Open Receipts by Supplier (P43214: ZJDE0001).

**4.3 Landed Costs at Voucher Match (P0411 calling P4314)**

If landed costs were not applied at receipt, they can be applied during voucher match by executing the **Landed Cost Row exit** after bringing in the receipt to match. This calls the Stand Alone Landed Cost program (P43214).

**Section 5: Landed Cost Journal Entries**

**5.1 Setup for Example**

- Landed Cost Rule: 10% of cost
- Include in Cost: Y
- Purchase Order: \$100

**5.2 Journal Entries - Positive On-Hand Quantity**

| **Account**                  | **Debit** | **Credit** | **AAI** |
| ---------------------------- | --------- | ---------- | ------- |
| Inventory                    | \$100     |            | 4310    |
| RNV                          |           | \$100      | 4320    |
| Cost/Expense (landed cost)   | \$10      |            | 4385    |
| Cost/Liability (landed cost) |           | \$10       | 4390    |

**5.3 Journal Entries - Negative On-Hand Quantity**

With SAR #4375192, if the on-hand quantity is negative, the landed cost expense is split between AAI 4385 and AAI 4332. The cardex record and AAI 4385 are created only for the portion of landed cost applicable to the quantity on hand.

**Example:** On-hand quantity = -50; PO quantity = 100; PO cost = \$100.

| **Account**                  | **Debit** | **Credit** | **AAI** |
| ---------------------------- | --------- | ---------- | ------- |
| Inventory                    | \$100     |            | 4310    |
| RNV                          |           | \$100      | 4320    |
| Cost of Sales                | \$5       |            | 4332    |
| Cost/Expense (landed cost)   | \$5       |            | 4385    |
| Cost/Liability (landed cost) |           | \$10       | 4390    |

**Note:** Landed costs will **not** update the cardex (F4111) if the standard cost (07) rule is used for inventory.

**Section 6: Landed Cost F43121 Records**

**6.1 The PRLAND Field**

The PRLAND field in the F43121 table is the critical indicator for landed cost records. It determines whether the landed cost is eligible for voucher match or will only be accrued:

| **PRLAND Value** | **Meaning**                                                                    |
| ---------------- | ------------------------------------------------------------------------------ |
| **Blank**        | The record is not related to landed cost.                                      |
| **1**            | Product/item line.                                                             |
| **2**            | Landed cost record eligible for voucher match processing.                      |
| **3**            | Landed cost record that will only be accrued - not eligible for voucher match. |

**6.2 The PRLVLA Field**

The PRLVLA field stores the Landed Cost Level - a three-character value from UDC 40/CA that identifies the specific landed cost applied to the record.

**6.3 Multi-Currency Landed Costs**

Landed costs support multi-currency processing. A purchase order can be in one currency while one or more landed costs are in different currencies. When multi-currency is enabled:

- The currency field within the landed cost record becomes active.
- The currency defaults from the Supplier Master and **cannot be overridden**.
- Exchange rate variances for landed costs are tracked using **AAI 4340**.

**Section 7: Performance Issues with Landed Cost**

In releases B733.2 and Xe, performance issues have been identified with the landed cost functionality during the purchase order receipts process. The following ESUs (Electronic Software Updates) should be applied to resolve these issues:

| **Release** | **ESU Number** |
| ----------- | -------------- |
| **B733.2**  | 4951647        |
| **Xe**      | 4885774        |