**JD Edwards In Transit**

**Training Guide: ST/OT Transfer Orders**

**Topic: Exclusion Variance Added to the Orders List**

**Section 1: Overview of ST/OT Transfer Orders**

ST/OT transfer orders in JD Edwards are used to move materials between branch plants (A to B) within the same company. The process uses a clearing account to hold the value of goods while they are in transit.

The standard process flow is as follows:

- A shipment confirmation is performed for one or more items from branch "A."
- Those items are received at branch "B."
- Ideally, the received items match the shipment in both quantity and cost between the two branches, resulting in a clean reconciliation of the In Transit account.

In practice, however, the ideal scenario is not always achieved.

**Section 2: The Problem - Processing Discrepancies on Transfer Orders**

**2.1 Common Scenario**

It is common to have multiple transfer orders in process for the same item number simultaneously. This creates the potential for processing discrepancies that complicate reconciliation.

**Example:**

- Two transfer orders are in process for the same item, each for 50 units, scheduled to ship within a week of each other.
- Due to delays or scheduling changes, all 100 units are shipped together. Ship confirmations are processed correctly - 50 units on each order.
- At the receiving dock, the operator counts 100 units in the same box, looks up the item, and receives all 100 units against **one** of the two open purchase orders.
- One order is closed. The other remains open in JD Edwards - theoretically never to be received against.

**2.2 The Exclusion Process**

When reviewing the open purchase order in RapidReconciler, the order must be **excluded** from the In Transit calculations. Once excluded, the In Transit account balances correctly and the reconciliation is clean.

However, a new risk is introduced: because there is still an open purchase order in JD Edwards, it remains possible for items to be received against it - even from an **unrelated shipment**. If this occurs, the new receipt activity will not be reflected in RapidReconciler because the purchase order was previously excluded.

This is where **Exclusion Variance** becomes important.

**Section 3: Exclusion Variance - New Columns on the Orders Tab**

To address this risk, four new columns have been added to the Orders tab in the In Transit module:

| **Column**     | **Description**                                                                                    |
| -------------- | -------------------------------------------------------------------------------------------------- |
| **ExclQty**    | The quantity excluded on the order.                                                                |
| **ExclAmt**    | The amount excluded on the order.                                                                  |
| **ExclVarQty** | The exclusion quantity variance - identifies any quantity activity on a previously excluded order. |
| **ExclVarAmt** | The exclusion amount variance - identifies any dollar activity on a previously excluded order.     |

**Section 4: How to Use the Exclusion Variance Columns**

The **ExclVarQty** and **ExclVarAmt** columns are the key fields to monitor. Any non-zero value in either of these columns indicates that transaction activity has occurred on an order that was previously excluded from the In Transit calculations.

**4.1 Required Action**

If non-zero values appear in the exclusion variance columns, the affected lines must be processed as follows:

- **Unexclude** the order pair to reinstate it in the In Transit calculations.
- **Re-exclude** the order pair so that the quantities and amounts are recalculated correctly based on all activity, including the new transactions.

This ensures that the In Transit reconciliation reflects an accurate and complete picture of all activity on the order.

**Section 5: Key Takeaway**

In theory, if In Transit orders are processed correctly, exclusion variances should never occur. In practice, however, receiving discrepancies and unrelated receipts against open purchase orders do happen. The Exclusion Variance columns provide an important safeguard - surfacing any activity on previously excluded orders so that no transactions are inadvertently omitted from the In Transit reconciliation.

**Best Practice:** As part of the periodic In Transit reconciliation review, always check the ExclVarQty and ExclVarAmt columns on the Orders tab for any non-zero values and address them promptly using the unexclude and re-exclude process.