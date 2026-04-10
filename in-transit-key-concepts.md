**Rapid Reconciler In Transit**

**Training Manual: Key Concepts**

**Section 1: What Is "In Transit"?**

**1.1 Definition**

In Transit reconciliation in RapidReconciler refers to the movement of inventory via the ST/OT (Stock Transfer/Order Transfer) process. The following conditions typically apply:

- Inventory is moved from branch plant "A" to branch plant "B."
- There is sufficient distance between the branches to warrant physical transportation.
- Both branch plants are in the same company, with rare exceptions. If branch plants are in different companies, consider using an intercompany sale instead.
- The time between shipment and receipt is within a few weeks maximum.

**1.2 Key Considerations**

Before working with the In Transit module, be aware of the following:

- The process is not limited to ST/OT order types. Other order types can be configured, and RapidReconciler will identify them based on flags in the detail data.
- Goods may be transferred at cost or with a markup. The accounting rules (DMAAs) must be configured accordingly.

**Important:** Do not mix costing methods on the same order type, as this will cause accounting issues.

- In Transit accounts are tracked in dollars only. RapidReconciler calculates inventory in transit using the following formulas:
  - **In Transit Quantity** = Quantity Shipped − Quantity Received
  - **In Transit Amount** = Amount Shipped − Amount Received
- The item number and line number on the shipment (ST sales order) must have a matching item number and line number on the receipt (OT purchase order).
- There are typically no invoices generated for the ST order.
- The Sales Update program P42800 has a dedicated version set up for transfer orders. In this version, the interface to A/R is turned off to avoid generating receivables.

**Reminder:** You should be fully aware of the order types used by your organization for transfers, and whether goods are transferred at cost or with a markup.

**Section 2: In Transit Accounting Setup**

**2.1 Transfer Without Markup**

When goods are transferred at cost with no markup, the DMAAI configuration is as follows:

**Shipping Entries:**

| **AAI** | **Account** | **Debit** | **Credit** |
| ------- | ----------- | --------- | ---------- |
| 4230    | Clearing    |           | Price      |
| 4245    | Clearing    | Price     |            |
| 4240    | Inventory   |           | Cost       |
| 4220    | In Transit  | Cost      |            |

**Receiving Entries:**

| **AAI** | **Account** | **Debit** | **Credit** |
| ------- | ----------- | --------- | ---------- |
| 4310    | Inventory   | Cost      |            |
| 4320    | In Transit  |           | Cost       |

**How this configuration works:**

- **DMAAI 4245** is used when the A/R interface is turned off in the Sales Update program P42800.
- **DMAAs 4245 (A/R) and 4230 (Revenue)** are populated with a "wash" account. This negates any pricing issues on the ST order - regardless of whether the price is \$0 or \$1,000,000, there will be no impact on the general ledger.
- **DMAAI 4240 (Inventory)** is credited with the inventory value at time of shipment confirmation. This comes from the COST field on the ST order.
- **DMAAI 4220 (Cost of Goods Sold/In Transit)** is debited with the same inventory value.
- **DMAAI 4310 (Inventory)** is debited with the inventory cost of the item in the receiving branch.
- **DMAAI 4320 (Received-Not-Vouchered/In Transit)** is credited with the cost on the OT order.

Variances generated at the time of receipt are handled depending on the cost method of the item (standard cost vs. weighted average).

**2.2 Transfer With Markup**

When goods are transferred with a markup, the DMAAI configuration differs as follows:

**Shipping Entries:**

| **AAI** | **Account**         | **Debit** | **Credit** |
| ------- | ------------------- | --------- | ---------- |
| 4230    | Interbranch Revenue |           | Price      |
| 4245    | In Transit          | Price     |            |
| 4240    | Inventory           |           | Cost       |
| 4220    | Cost of Goods Sold  | Cost      |            |

**Receiving Entries:**

| **AAI** | **Account** | **Debit** | **Credit** |
| ------- | ----------- | --------- | ---------- |
| 4310    | Inventory   | Cost      |            |
| 4320    | In Transit  |           | Cost       |

**How this configuration works:**

- **DMAAI 4245** is used when the A/R interface is turned off in Sales Update program P42800.
- **DMAAs 4245 (A/R) and 4230 (Revenue)** are populated with interbranch revenue and the In Transit account as depicted. Price management on the ST order becomes critical in this configuration.
- **DMAAI 4240 (Inventory)** is credited with the inventory value at time of shipment confirmation, sourced from the COST field on the ST order.
- **DMAAI 4220 (Cost of Goods Sold)** is debited with the same inventory value.
- At the time of entry, the cost on the OT order matches the price on the ST order.
- **DMAAI 4310 (Inventory)** is debited with the inventory cost of the item in the receiving branch.
- **DMAAI 4320 (Received-Not-Vouchered/In Transit)** is credited with the cost on the OT order.

Variances generated at the time of receipt are handled depending on the cost method of the item (standard cost vs. weighted average).

Here are some examples of how the T accounts would look for both scenarios:

[Trans Cost Difference T Accounts](Docs/Trans%20Cost%20Difference%20T%20Accounts.xlsx)

**Section 3: In Transit Glossary of Terms**

**3.1 Orders Page**

The Orders page for the In Transit module lists the following:

- All order pairs (explained in the next section) that have either an open quantity or open amount.
- The current In Transit balance, regardless of the period selected. Note that changing the period while on this page will not change the information displayed.
- A new order pair will appear once a new shipment occurs on a transfer order.
- A receipt that matches the shipment in both units and amount will automatically remove the order pair from the page.
- Any remaining balances that cannot be cleared through JDE processing must be removed using the "Exclusion" process within RapidReconciler.

**3.2 Order Pairs**

In JD Edwards, a transfer order is broken down into line numbers. An item can be entered on more than one line due to delivery date or lot number variations. In RapidReconciler, In Transit entries are based on an "order pair" concept.

An **Order Pair** is a summarized item number at the ST sales order, OT purchase order, and item number level. Lines and lots are eliminated in this summarization. All order pairs are listed on the Orders page in the In Transit module.

**Example Scenario:**

| **Event**         | **Detail**                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------ |
| Monday morning    | Transfer order shipped from Branch A for 100 EA at \$100                                   |
| Monday evening    | Sales update debits In Transit for \$100; ST status = 999                                  |
| Tuesday afternoon | Items arrive at Branch B; 94 received, OT status = 999; In Transit account has \$94 credit |

**Resulting Order Pair:**

| **From** | **To** | **Item** | **Ship Qty** | **Rec Qty** | **TranQty** | **Ship Amt** | **Rec Amt** | **TranAmt** | **Ship Sts** | **Rec Sts** |
| -------- | ------ | -------- | ------------ | ----------- | ----------- | ------------ | ----------- | ----------- | ------------ | ----------- |
| A        | B      | 12345    | 100          | 94          | 6           | \$100        | \$94        | \$6         | 999          | 999         |

In this scenario, both the shipment and receipt are complete, but a remaining balance of 6 units valued at \$6 exists. Since both status codes are 999, no further transactions can be performed for this item on that order pair. The \$6 amount remains on the In Transit account balance sheet.

**3.3 Exclusions**

When an order pair has a minimum status code of 999 for both the sales order (Ship Sts) and the purchase order (Rec Sts), no additional transactions can be performed. Any remaining balance must be cleared using the **Exclusion** process in RapidReconciler.

Excluding an order pair removes its balance from the In Transit balance calculation. The excluded amount is added to the "Exclusions" total in the Variance Calculation section, as shown in the example below:

| **Variance Calculation**  | **Amount**   |
| ------------------------- | ------------ |
| Carry Forward             | (750.10)     |
| GL Batches                | 0.00         |
| End of Day                | 0.00         |
| Transactions              | 0.00         |
| **Exclusions**            | **(23.31)**  |
| Manual Journal Entries    | 0.00         |
| **Unreconciled Variance** | **(773.41)** |

The corrective action for an excluded order pair is an offsetting journal entry in JD Edwards. The Exclusion process will be explained in further detail within the In Transit user training module.
