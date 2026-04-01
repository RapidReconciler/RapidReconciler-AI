**JD Edwards Inventory Reconciliation**

**Training Guide: Resolving the Top 6 Issues (Part 2)**

**Topic: Controlling GL Class Code Changes for Items in Inventory**

**Section 1: Overview**

This guide continues the series on the top six issues with JD Edwards inventory reconciliation. Part 1 covered DMAAs. This installment focuses on the proper way to control GL class code changes for items that have quantity on hand in inventory.

**Section 2: What Is a GL Class Code?**

A GL class code is a 4-character code assigned at the item level in JD Edwards. Key characteristics include:

- It is assigned when a new item is created as part of the item master setup.
- Once assigned, it is propagated down to item branch, location, sales order, and purchase order records.
- It is an integral part of the Distribution/Manufacturing Automatic Accounting Instruction (DMAAI) configuration, which controls how inventory transactions are recorded in the general ledger.

**Section 3: The Problem - Changing GL Class Codes with Quantity on Hand**

JD Edwards allows changes to GL class code fields at any of the individual hierarchy levels without checking whether there is any quantity on hand for the item. This presents a significant risk.

**Critical Rule:** GL class codes should only be changed when the quantity on hand for the item is zero. Changing a GL class code while quantity exists in inventory can and will cause reconciling items at period end.

**Section 4: Scenario Examples**

**4.1 Scenario 1 - Incorrect Process (Code Changed with Quantity on Hand)**

In this scenario, an item was misclassified as a finished good and needed to be reclassified as a raw material. However, a receipt of \$100 had already occurred before the change was made.

**What happened:**

- A receipt (OV transaction) of \$100 posted to the Finished Goods account.
- The GL class code was changed from Finished Goods to Raw Materials **while quantity was still on hand**.
- A subsequent material issue (IM transaction) credited the **Raw Materials** account - because that was now the active GL class code.
- The **Finished Goods** account was never relieved.

**Result:** An account discrepancy exists. The Finished Goods account still carries the \$100 receipt with no corresponding relief, creating a reconciling item at period end.

**4.2 Scenario 2 - Correct Process (Quantity Zeroed Out Before Code Change)**

In this scenario, the same reclassification is needed, but the proper procedure is followed.

**What happened:**

- An inventory adjustment (IA transaction) was made to **zero out** the quantity on hand, properly relieving the Finished Goods account.
- The GL class code was then changed from Finished Goods to Raw Materials **after the quantity was at zero**.
- A second IA transaction debited the **Raw Materials** account, re-establishing the inventory under the correct classification.
- A subsequent material issue (IM transaction) correctly credited the Raw Materials account.

**Result:** All accounts reflect the correct balances with no discrepancies.

**Section 5: The Correct Procedure for Changing a GL Class Code**

When a GL class code change is required for an item that is or has been in inventory, follow this process:

- **Verify quantity on hand** - Confirm the current on-hand balance for the item across all locations and lots.
- **Adjust inventory to zero** - Perform an inventory adjustment (IA) to issue out all quantity on hand. This ensures the current account is properly relieved.
- **Change the GL class code** - Update the code at all applicable levels: item master, item branch, item locations, and any open orders.
- **Adjust inventory back in** - Perform a second inventory adjustment (IA) to re-establish the on-hand quantity under the new GL class code, ensuring the correct account is debited.
- **Verify account balances** - Confirm that the old account has been fully relieved and the new account reflects the correct balance.

**Section 6: Key Takeaway**

Changing a GL class code on an item while quantity is on hand disrupts the accounting flow between the item ledger and the general ledger, resulting in account discrepancies that surface as reconciling items at period end.

While the process of zeroing out inventory before making the code change requires additional steps, it ensures that inventory values move correctly from one GL account to another and prevents unnecessary reconciliation issues.

**Best Practice:** Establish a formal procedure within your organization that requires on-hand quantity to be at zero before any GL class code change is processed. This small discipline can prevent significant reconciliation headaches at month end.