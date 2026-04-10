**JD Edwards Inventory**

**Training Guide: Item Ledger (Table F4111)**

**Topic: Your Top 5 Questions Answered**

**Section 1: Overview**

The JD Edwards item ledger - table F4111, commonly referred to as "The Cardex" - contains the complete transaction history for items in the inventory system. All transactions that impact an item's quantity on hand are recorded in this table, including receipts, transfers, sales shipments, material issues, completions, and more.

This guide addresses the five most frequently asked questions about the item ledger.

**Section 2: Question 1 - Does the Item Ledger Contain Inventory Balances?**

**No.** The item ledger contains transactional data only - it does not store running balances.

To obtain the total on-hand quantity from this table, all qualifying transactions must be summarized. Note that transactions with a posting code of "X" must be excluded from this calculation (see Section 3 for details on posting codes).

The actual on-hand balance for each item is stored in table **F41021** - the Item Location table.

**Section 3: Question 2 - What Do the Posting Codes in the F4111 Table Mean?**

The posting code in F4111 is stored in column **ILIPCD**. There are four possible values:

| **Posting Code** | **Description**                                                                                                                                                                                                                               |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Blank**        | The initial value assigned to all qualifying transactions. Also used for IB transactions created when an item is added to the system.                                                                                                         |
| **Y**            | Posted by the Item Ledger As-Of Record Generation program (R41542) to the Item ASOF file (F41112).                                                                                                                                            |
| **S**            | The value of inventory has not yet been impacted by the transaction. Examples include a ship confirmation transaction before running Sales Update, or an IM document type before Manufacturing Accounting has been run.                       |
| **X**            | The transaction involved a movement of inventory only and had no effect on the general ledger. Examples include an IZ transaction created on a change of lot status. These transactions must be excluded when summarizing item ledger totals. |

**Section 4: Question 3 - How Can I Tell What Date a Transaction Was Entered Into the System?**

This is not straightforward, as there are two date fields in the JD Edwards item ledger to consider:

| **Date Field**       | **Description**                                                                                                                                                                                                                                                                                                                                                                  | **Reliability** |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **Transaction Date** | The date typically associated with when the transaction occurred. This field is available on some transaction entry screens and can be overridden by the user. Backdating for business process reasons and data entry errors are both common.                                                                                                                                    | Less reliable   |
| **Creation Date**    | The date the transaction record was created in the item ledger table. More reliable than the transaction date, with one notable exception: if Global Item Update is enabled and the second or third item number is changed, all item ledger records for that item will have their creation date updated to the date of the change. This scenario is rare but must be considered. | More reliable   |

**Recommendation:** Use the creation date when attempting to determine when a transaction entered the system. However, it should be noted that there is no 100% reliable method for obtaining this information in all scenarios.

**Section 5: Question 4 - Is There a Way to Determine Which DMAAs Were Used During a Transaction?**

**No.** The item ledger table does not store information about which DMAAI entries were used to process a transaction.

It is possible to make a reasonable assumption based on the following available data points:

- Company number
- Document type
- GL class code
- Knowledge of how JD Edwards transaction processing works

However, there is no way to retrieve this information directly from the F4111 table. For DMAAI analysis, the RapidReconciler Transaction Detail Report can provide this context by combining item ledger data with the applicable DMAAI configuration at the time of the transaction.

**Section 6: Question 5 - Should the Sum of the Item Ledger Always Equal the Item Balance Table?**

**Yes** - with the following important conditions all being met:

- All transactions with a posting code of **"X"** have been removed from the calculation.
- The transaction quantity is expressed in the item's **current primary unit of measure**.
- The item ledger table has not been purged without leaving a **balance forward record** to maintain continuity.
- No item **conversion factors** have been removed from the system.
- Any changes to an item's **primary unit of measure** were performed using the recommended procedures outlined in JD Edwards documentation.

If any of these conditions are not met, a discrepancy between the item ledger summary and the item balance table may exist that is not indicative of a true inventory integrity issue, but rather a data management consideration.
