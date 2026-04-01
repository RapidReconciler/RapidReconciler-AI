**Rapid Reconciler PO Receipts**

**Training Manual: Key Concepts**

**Section 1: Definition**

PO Receipts, also known as "Received-Not-Vouchered" (RNV), is a balance sheet liability that accounts for goods and services received against a purchase order.

**Important Distinction:** PO Receipts should not be confused with an "Open PO," which refers to a purchase order or line where not all items have been received. These are two separate concepts.

**Section 2: Process Flow**

The PO Receipts process follows these steps:

- A receipt transaction is performed against an established purchase order. This transaction creates an "open receipt" pending a supplier invoice.
- Once the supplier invoice is received, it is matched to the receipt document(s) in JD Edwards via the voucher match process. This can be either a 2-way or 3-way match.
- The voucher transaction clears the open receipt and posts the applicable entries to the general ledger.

**Section 3: Table F43121**

Table F43121 is the table of record for purchase order receipts. It is important to understand that this table does not behave as a standard ledger, where each transaction associated with a receipt would have a unique record.

During a receipt or voucher reversal, the original receipt record is **overwritten** with new information. This behavior makes it impossible to generate an "As-Of" report from this table.

**Section 4: Match Types**

Table F43121 contains a "Match Type" column. There are four match types, defined as follows:

| **Match Type** | **Description**                                                                                                                                                                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**          | A Match Type 1 record is created for each receipt document generated. This is the first step in the process. An "Open Receipts" report may be produced by selecting Match Type 1 records from the table.                                                                      |
| **2**          | Match Type 2 records are vouchers generated for Match Type 1 receipts. In an ideal scenario, the voucher will be for the same quantity and amount as the original receipt, with exceptions for pricing variances. This is typically the end of the process.                   |
| **3**          | Match Type 3 records are Match Type 1 receipts that have been reversed. The Match Type column changes from 1 to 3, and additional columns for quantities and amounts are updated accordingly. Reversals are the primary reason this table does not function as a true ledger. |
| **4**          | Match Type 4 records are the same as Match Type 3, except they represent voucher reversals rather than receipt reversals.                                                                                                                                                     |

**Section 5: Accounting Flow**

The following illustrates the accounting flow for a standard 3-way match process:

- **Purchase Order Created** - A purchase order is established in JD Edwards.
- **Receipt Entered** - Goods or services are received against the PO. A Match Type 1 record is created in table F43121. The RNV (Received-Not-Vouchered) account is credited and the inventory or expense account is debited.
- **Supplier Invoice Received** - The supplier invoice is matched to the receipt in JD Edwards via the voucher match process.
- **Voucher Created** - A Match Type 2 record is created. The RNV account is debited and Accounts Payable is credited, clearing the open receipt.
- **Payment Processed** - Accounts Payable is debited and cash or the bank account is credited, completing the process.

**Section 6: Challenges**

The following challenges are associated with the PO Receipts reconciliation process:

- **System** - The receipts table (F43121) is not a true ledger. Receipt and voucher reversals overwrite key data elements, making As-Of reporting impossible. This places additional importance on current-balance reconciliation methods.
- **Process** - Receipts routing, taxes, and landed cost configuration can add levels of complexity to the process. Reversals performed out of sequence may cause accounting discrepancies that are difficult to trace.
- **Reconciliation** - Because As-Of reporting is not available, reconciliation must be performed as a balance-to-balance comparison between the current open receipts report and the general ledger balance. This requires that the open receipts listing be carefully validated before any journal entries are made.
