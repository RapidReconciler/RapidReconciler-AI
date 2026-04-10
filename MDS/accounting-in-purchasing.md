**Reference Guide: Accounting in Purchasing**

**File Updates and Journal Entries by Transaction Type**

**Section 1: Stock Purchase - 3-Way Match**

**1.1 Step 1 - Purchase Order Entry (P4311)**

**Files created/updated:**

| **File**   | **Action**                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------- |
| **F4301**  | PO Header record created                                                                     |
| **F4311**  | PO Detail record created                                                                     |
| **F43199** | Purchasing Ledger record created (only if Order Activity Rules have "Y" in the Ledger field) |
| **F41021** | Item Location file updated                                                                   |

**No journal entries are created at Purchase Order Entry.**

**1.2 Step 2 - Enter Receipt by Purchase Order (P4312)**

**Files created/updated:**

| **File**   | **Action**                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------- |
| **F4311**  | PO Detail record closed (Status Codes, received and open quantity and amount fields updated) |
| **F43121** | PO Receiver file - Match Type 1 record created                                               |
| **F4111**  | Item Ledger file - OV (receipt) document type created                                        |
| **F0911**  | Account Ledger - OV document type created                                                    |
| **F41021** | Item Location file - On Hand Quantity and On PO fields updated                               |
| **F4105**  | Item Cost file - Last-In, Average, and Purchase cost buckets updated                         |

**Journal entries created at receipt:**

| **Entry**                    | **Debit** | **Credit** | **AAI**  |
| ---------------------------- | --------- | ---------- | -------- |
| Inventory                    | ✓         |            | **4310** |
| Received Not Vouchered (RNV) |           | ✓          | **4320** |

**1.3 Step 3 - Match Voucher to Open Receipt (P4314)**

**Files created/updated:**

| **File**   | **Action**                                                                                                                                                             |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **F0411**  | Accounts Payable Ledger - PV document type created                                                                                                                     |
| **F0911**  | Account Ledger - PV document type created                                                                                                                              |
| **F43121** | PO Receiver file - Match Type 2 record written (indicates transaction completed in Purchasing); Match Type 1 record changes from open to paid for the amount vouchered |
| **F4311**  | PO Detail record created for any lines added at Voucher Match                                                                                                          |

**Journal entries created at Voucher Match:**

| **Entry**                    | **Debit** | **Credit** | **AAI**  |
| ---------------------------- | --------- | ---------- | -------- |
| Received Not Vouchered (RNV) | ✓         |            | **4320** |
| A/P Trade Account            |           | ✓          | **PC**   |

**1.4 Purchase Price Variances**

At times a supplier's invoice reflects a different dollar amount per item than the amount at which it was received. The variance is written to a Purchase Price Variance account using the applicable AAI, depending on the circumstances:

| **AAI**  | **Program**           | **When Invoked**                                                                                                                                                                                                   |
| -------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **4330** | Voucher Match (P4314) | Invoked when vouchering at a different amount than what was received.                                                                                                                                              |
| **4332** | Voucher Match (P4314) | Invoked when goods have been sold prior to voucher match and a cost variance exists. Triggered when the quantity on hand is less than the quantity being vouchered. See the AAI 4332 white paper for full details. |
| **4335** | Receipts (P4312)      | Invoked when receiving goods at a different cost than the Standard Cost (07) in F4105. Further variances at Voucher Match for standard cost items are booked to AAIs 4330/4332.                                    |

**Example 1 - Variance at Voucher Match (AAI 4330)**

A PO is issued for \$3.75 per item. The item is received at \$3.75, but the supplier invoice is \$4.00. The voucher amount is \$4.00.

| **Entry**               | **Debit** | **Credit** | **AAI** |
| ----------------------- | --------- | ---------- | ------- |
| RNV                     | \$3.75    |            | 4320    |
| Purchase Price Variance | \$0.25    |            | 4330    |
| A/P Trade Account       |           | \$4.00     | PC      |

**Example 2 - Variance Split Between Inventory and COGS (AAIs 4330 and 4332)**

A PO is issued for \$200 (20 items at \$10 each). An invoice for \$220 is received and vouchered. Half of the items (10) were sold to a customer prior to vouchering. Since quantity on hand (10) is less than quantity vouchered (20), AAI 4332 is invoked for the sold portion.

| **Entry**          | **Debit** | **Credit** | **AAI** |
| ------------------ | --------- | ---------- | ------- |
| RNV                | \$200.00  |            | 4320    |
| Inventory Variance | \$10.00   |            | 4330    |
| Cost of Goods Sold | \$10.00   |            | 4332    |
| A/P Trade Account  |           | \$220.00   | PC      |

**Example 3 - Standard Cost Variance at Receipt (AAI 4335)**

When using Standard Cost, dollar variances at receipt are not written to the Cardex. The variance is recorded to a variance account directed by AAI 4335.

| **Entry**              | **Debit** | **Credit** | **AAI** |
| ---------------------- | --------- | ---------- | ------- |
| Inventory              | \$100.00  |            | 4310    |
| Standard Cost Variance | \$5.00    |            | 4335    |
| RNV                    |           | \$105.00   | 4320    |

**Section 2: Non-Stock Purchasing - 2-Way Match**

**2.1 Step 1 - Purchase Order Entry (P4311)**

**Files created/updated:**

| **File**   | **Action**                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------- |
| **F4301**  | PO Header record created                                                                     |
| **F4311**  | PO Detail record created                                                                     |
| **F43199** | Purchasing Ledger record created (only if Order Activity Rules have "Y" in the Ledger field) |

**No journal entries are created at Purchase Order Entry.**

**2.2 Step 2 - Receive and Voucher PO (P4314)**

In a 2-way match, the receipt and voucher are processed simultaneously in a single step.

**Files created/updated:**

| **File**   | **Action**                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------------- |
| **F0411**  | Accounts Payable Ledger - PV document type created                                                            |
| **F0911**  | Account Ledger - PV document type created                                                                     |
| **F43121** | PO Receiver file - Match Type 2 record written (indicates transaction completed in Purchasing)                |
| **F4311**  | PO Detail record updated - record closed (Status Codes, Received and Open quantity and amount fields updated) |

**Journal entries created at Receive and Voucher:**

| **Entry**                      | **Debit** | **Credit** | **AAI / Source**                         |
| ------------------------------ | --------- | ---------- | ---------------------------------------- |
| Non-Stock or Inventory Account | ✓         |            | **4315** or account number entered on PO |
| A/P Trade Account              |           | ✓          | **PC**                                   |

**Section 3: Non-Stock Purchasing - 3-Way Match**

**3.1 Step 1 - Purchase Order Entry (P4311)**

**Files created/updated:**

| **File**   | **Action**                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------- |
| **F4301**  | PO Header record created                                                                     |
| **F4311**  | PO Detail record created                                                                     |
| **F43199** | Purchasing Ledger record created (only if Order Activity Rules have "Y" in the Ledger field) |

**No journal entries are created at Purchase Order Entry.**

**3.2 Step 2 - Enter Receipt by Purchase Order (P4312)**

**Files created/updated:**

| **File**   | **Action**                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------------- |
| **F4311**  | PO Detail record updated - record closed (Status Codes, Received and Open quantity and amount fields updated) |
| **F43121** | PO Receiver file - Match Type 1 record created                                                                |
| **F0911**  | Account Ledger - OV document type created                                                                     |

**Journal entries created at receipt:**

| **Entry**                    | **Debit** | **Credit** | **AAI**  |
| ---------------------------- | --------- | ---------- | -------- |
| Non-Stock Inventory Account  | ✓         |            | **4315** |
| Received Not Vouchered (RNV) |           | ✓          | **4320** |

**3.3 Step 3 - Match Voucher to Open Receipt (P4314)**

**Files created/updated:**

| **File**   | **Action**                                                                                     |
| ---------- | ---------------------------------------------------------------------------------------------- |
| **F0411**  | Accounts Payable Ledger - PV document type created                                             |
| **F0911**  | Account Ledger - PV document type created                                                      |
| **F43121** | PO Receiver file - Match Type 2 record written (indicates transaction completed in Purchasing) |

**Journal entries created at Voucher Match:**

| **Entry**                    | **Debit** | **Credit** | **AAI**  |
| ---------------------------- | --------- | ---------- | -------- |
| Received Not Vouchered (RNV) | ✓         |            | **4320** |
| A/P Trade Account            |           | ✓          | **PC**   |

**Section 4: AAI Quick Reference Summary**

| **AAI**  | **Account**                         | **Used In**                                                         |
| -------- | ----------------------------------- | ------------------------------------------------------------------- |
| **4310** | Inventory                           | Stock receipt - debit inventory                                     |
| **4315** | Non-Stock / Inventory Account       | Non-stock receipt - debit non-stock account                         |
| **4320** | Received Not Vouchered (RNV)        | Receipt - credit RNV; Voucher Match - debit RNV                     |
| **4330** | Purchase Price Variance / Inventory | Voucher Match - variance between receipt and voucher amount         |
| **4332** | Cost of Goods Sold                  | Voucher Match - variance for goods already sold prior to vouchering |
| **4335** | Standard Cost Variance              | Receipt - variance between PO cost and standard cost (07)           |
| **PC**   | A/P Trade Account                   | Voucher Match - credit A/P (entry made by GL Post program R09801)   |
