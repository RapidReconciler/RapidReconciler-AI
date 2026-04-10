**GL Class Codes - Professional Training Guide**

**Overview**

GL Class Codes are item attributes assigned in JD Edwards (JDE) that determine how inventory transactions are recorded in the General Ledger. The mapping between GL Class Codes and journal entries is defined in the Distribution/Manufacturing Automatic Accounting Instructions (DMAIIs), which are covered separately.

This guide covers four topics:

- The GL Class Code hierarchy
- How to change a GL Class Code correctly
- How GL Class Codes are used in transactions
- Integrity Report 5

**1\. The GL Class Code Hierarchy**

GL Class Codes exist at four levels in JDE. Understanding this hierarchy is essential for maintaining accurate and consistent accounting records.

**Level 1 - Item Master**

The GL Class Code is first assigned when a new item is created in the Item Master. This is the foundation of the hierarchy.

**Level 2 - Item Branch**

When branch plant records are created for an item, the GL Class Code is copied from the Item Master to each branch plant record. While each branch plant may technically carry a different value, this is uncommon and generally not recommended.

**Level 3 - Item Location**

Each branch plant must have at least one primary location assigned to an item before any transactions can be processed. Additional secondary locations may also be defined. When locations are created, the GL Class Code is copied from the Item Branch record. Again, different values per location are possible but uncommon.

**Level 4 - Sales Order / Purchase Order**

When a purchase order or sales order is entered, the GL Class Code is copied from the item's location record to each order line via the **Additional Info** form.

**Key Takeaway:** The GL Class Code flows downward through the hierarchy - from Item Master → Item Branch → Item Location → Order Line - but it does **not** update automatically. Each level must be maintained independently.

**2\. Changing a GL Class Code**

**Important: Changes Do Not Cascade**

A common misconception is that updating the GL Class Code at the Item Master level will automatically update all lower levels. **This is not the case.** Each level must be updated manually, which can be a time-consuming process depending on the number of branch plants and locations involved.

**Handling Inventory On Hand**

Before changing a GL Class Code, any existing on-hand inventory must be addressed. Failing to do so will result in the item's value remaining in the old GL account, with no transaction created to move it to the new account.

**The correct process is:**

- **Adjust out** all on-hand quantity under the current GL Class Code.
- **Update** the GL Class Code at all applicable levels (Item Master, Item Branch, Item Location, and any open order lines).
- **Adjust in** the quantity under the new GL Class Code.

**Why This Matters - An Example**

Suppose an item is incorrectly coded as a raw material, and inventory is received against it. The dollar value of that receipt posts to the raw material account in the General Ledger. When the error is discovered and the code is changed to finished goods - without first adjusting the inventory out - the value remains in the raw material account. There is no transaction to trigger a reallocation.

By adjusting the quantity out first, then changing the code, then adjusting back in, the system generates the appropriate journal entries to move the value from the raw material account to the finished goods account.

**Key Takeaway:** Always adjust inventory out before changing a GL Class Code, then adjust it back in after the code has been updated at all levels.

**3\. Transaction Usage**

Different transaction types retrieve the GL Class Code from different levels of the hierarchy. This is summarized below:

| **Transaction Type**                                                  | **GL Class Code Source** |
| --------------------------------------------------------------------- | ------------------------ |
| Work Orders (material issues & completions)                           | Item Branch level        |
| Sales Orders & Purchase Orders (shipments & receipts)                 | Order line level         |
| Inventory Transactions (issues, adjustments, transfers, cycle counts) | Item Location level      |

Journal entries for work order transactions are created during the manufacturing accounting batch process, while sales/purchase order and inventory transactions are processed in real time.

**Why Consistency Matters**

Because different transaction types pull the GL Class Code from different levels, it is critical that the code is **consistent across all levels** for a given item. If the values differ, the same item could post to different GL accounts depending on the transaction type - creating inconsistencies in financial reporting and inventory valuation.

**Key Takeaway:** GL Class Codes should always be the same across all levels for a given item. Inconsistencies can lead to incorrect journal entries and valuation errors.

**4\. Integrity Report 5**

**Integrity Report 5** identifies items where the GL Class Code at the Item Branch level does not match the GL Class Code on one or more of its corresponding Item Location records.

Since these values are expected to be the same, any item appearing on this report should be reviewed promptly and corrected in JD Edwards as appropriate.

**How to Run Integrity Report 5**

_(Follow your organization's standard instructions for accessing and running this report in JDE.)_

**Key Takeaway:** Run Integrity Report 5 regularly to proactively identify and resolve GL Class Code mismatches before they affect transaction accuracy.