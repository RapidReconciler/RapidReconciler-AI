**JD Edwards Inventory Reconciliation**

**Training Guide: GL Class Code Management**

**Topic: Considerations When Changing a GL Class Code**

**Section 1: Overview**

The recommended procedure for changing a GL class code in JD Edwards is well established:

- Adjust any quantity on hand to zero.
- Change the GL class code in all required locations.
- Adjust the inventory back in under the new GL class code.

This guide expands on that procedure by addressing the key considerations that must be evaluated before and during the change process to avoid potential reconciliation issues.

**Section 2: Consideration 1 - Who Can Perform All Required Transactions?**

Changing a GL class code is not typically a single-person task. The process involves both system configuration changes (e.g., updating the item master) and inventory transactions (e.g., adjusting on-hand quantities). In most organizations, these functions are controlled by different users with different system authorities.

For example, the person responsible for maintaining item master records may not have the authority to post inventory adjustments, and vice versa.

**2.1 Automating the Process**

To ensure the steps are performed in the correct sequence and by the right parties, some organizations have developed automated logic to:

- Perform the inventory adjustment to zero.
- Change the GL class code in all required locations.
- Adjust the inventory back in under the new code.

Maintaining the correct sequence of events is critical to keeping the item ledger clean, which directly impacts the accuracy of the reconciliation.

**Section 3: Consideration 2 - All Locations Where the GL Class Code Must Be Changed**

It is essential to update the GL class code in every location within JD Edwards where it is stored. The following locations must all be addressed:

| **Location**                  | **Notes**                                                                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Item Master**               | Optional - the GL class code at the item master level is not always used for transaction routing, but should be updated for consistency.                     |
| **Item Branch Record**        | Required - this is the primary level used for most transaction types.                                                                                        |
| **Item Location Record**      | Required - each location record carries its own copy of the GL class code.                                                                                   |
| **Open Purchase Order Lines** | Required - frequently overlooked. Receipts against orders created before the change will use the old GL class code, generating incorrect financial entries.  |
| **Open Sales Order Lines**    | Required - frequently overlooked. Shipments against orders created before the change will use the old GL class code, generating incorrect financial entries. |

**Important:** Open purchase and sales order lines are the most commonly missed update points. Any receipt or shipment transacted against an order created prior to the change will carry the old GL class code, resulting in incorrect general ledger entries and reconciling items at period end.

**Section 4: Consideration 3 - Why the Inventory Adjustment Steps Are Essential**

Skipping the inventory adjustment steps - even when the quantity eventually reaches zero through normal transactions - will leave the item ledger in an unreconcilable state.

**4.1 Example Scenario - Incorrect Process**

- A purchased item is set up with an incorrect GL class code of **FG01** (Finished Goods) instead of **RM01** (Raw Materials).
- One unit is received at **\$10**. This creates:
  - A **\$10 debit** to the Finished Goods account.
  - An item ledger record (OV) for \$10 with GL class **FG01**.
- The error is recognized. The GL class code is corrected to **RM01** in all required locations - but the unit is not adjusted out first.
- The unit is issued to a work order. This creates:
  - A **\$10 credit** to the Raw Materials account.
  - An item ledger record (IM) for \$10 with GL class **RM01**.

**Result:**

- Perpetual inventory: \$0 (correct).
- Finished Goods account: **\$10 debit remaining** (incorrect).
- Raw Materials account: **\$10 credit remaining** (incorrect).
- Both GL accounts are out of balance.

**4.2 Why a Journal Entry Alone Is Not Sufficient**

While a journal entry can correct the GL account balances, it does not resolve the item ledger. Each transaction in the item ledger must be summarized by GL class code in order to balance to the correct account. In the example above, the item ledger contains:

- An OV transaction with GL class **FG01** (receipt into Finished Goods)
- An IM transaction with GL class **RM01** (issue from Raw Materials)

These two transactions reference different accounts and cannot net to zero in a reconciliation. The correct approach would have been to create:

- An inventory adjustment (IA) to zero out the quantity under GL class **FG01**, properly relieving the Finished Goods account.
- After the GL class change, a second IA to re-establish the quantity under **RM01**, properly funding the Raw Materials account.
- The subsequent IM transaction would then correctly credit the Raw Materials account, and all ledgers would balance.

**Section 5: Summary**

The following table summarizes the three key considerations when changing a GL class code:

| **Consideration**                          | **Key Point**                                                                                                                                       |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Who performs the change**                | Ensure the correct users are involved at each step, or automate the process to enforce the proper sequence.                                         |
| **Where the code must be changed**         | Update the item master, item branch, item location, open purchase order lines, and open sales order lines. Do not overlook open orders.             |
| **Why inventory adjustments are required** | Skipping the adjust-out and adjust-in steps leaves the item ledger with mismatched GL class codes that cannot be resolved by a journal entry alone. |

Following the complete recommended procedure - adjust out, change the code, adjust back in - in the correct sequence and across all required locations ensures a clean item ledger and prevents unnecessary reconciling items at period end.