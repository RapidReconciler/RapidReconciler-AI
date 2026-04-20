# RapidReconciler PO Receipts -- Key Concepts

## Understanding Received-Not-Vouchered (RNV), F43121, and Reconciliation Fundamentals

---

## Table of Contents

- [Overview](#overview)
- [Section 1: What Is PO Receipts / RNV?](#section-1-what-is-po-receipts--rnv)
- [Section 2: Process Flow](#section-2-process-flow)
- [Section 3: The F43121 Table](#section-3-the-f43121-table)
- [Section 4: Match Types](#section-4-match-types)
- [Section 5: Accounting Flow](#section-5-accounting-flow)
- [Section 6: What Affects the RNV Balance](#section-6-what-affects-the-rnv-balance)
- [Section 7: Reconciliation Challenges](#section-7-reconciliation-challenges)
- [Section 8: How RapidReconciler Helps](#section-8-how-rapidreconciler-helps)
- [Section 9: Related Documentation](#section-9-related-documentation)

---

## Overview

The PO Receipts module in RapidReconciler reconciles the Received-Not-Vouchered (RNV) balance sheet liability account against open purchase order receipt activity. The RNV account holds the value of goods and services received from suppliers until the corresponding supplier invoice is matched and vouchered through Accounts Payable.

At any point in time, the RNV account balance should equal the total value of receipts that have been processed but not yet matched to a supplier invoice. If the balance does not agree to open receipt activity, a reconciling variance exists.

**What the PO Receipts module reconciles:**

| Side | Source | Description |
|---|---|---|
| **Open Receipts Balance** | F43121 Match Type 1 records | Receipts that have not yet been vouchered |
| **GL Balance** | F0902 Account Balances | General ledger period-end balance for the RNV account |
| **Out of Balance** | Difference between the two | What must be explained and resolved |

---

## Section 1: What Is PO Receipts / RNV?

### 1.1 Definition

PO Receipts, also known as **Received-Not-Vouchered (RNV)**, is a balance sheet liability that accounts for goods and services received against a purchase order where the supplier invoice has not yet been processed.

The RNV account is controlled by **DMAAI 4320** in JD Edwards. It is credited when goods are received (the liability is recognized) and debited when the voucher is matched (the liability is cleared).

### 1.2 Important Distinction

| Term | Definition |
|---|---|
| **PO Receipts / RNV** | A receipt has been processed; the supplier invoice has not yet been matched. A liability exists. |
| **Open PO** | A purchase order or line where not all items have been received yet. No receipt exists. |

These are two separate concepts. An open PO creates no accounting entries and carries no RNV balance. PO Receipts refers specifically to the period between receipt and voucher match.

### 1.3 Why the RNV Account Matters

The RNV account is a temporary liability. It should be self-clearing over time as supplier invoices are received and vouchered. A large or growing RNV balance typically indicates one or more of the following:

- Supplier invoices are not being processed promptly
- Receipts are being processed incorrectly or out of sequence
- Voucher matches are being entered manually rather than through the standard process
- Aged open receipts are accumulating without investigation

---

## Section 2: Process Flow

### 2.1 Standard 3-Way Match

The standard PO Receipts process follows these steps:

| Step | Event | F43121 Record | GL Impact |
|---|---|---|---|
| **1** | Purchase order created | No record | None |
| **2** | Goods received (P4312) | Match Type **1** created | Inventory/Expense **debit**; RNV **credit** |
| **3** | Supplier invoice received | -- | -- |
| **4** | Voucher match processed (P4314) | Match Type **2** created | RNV **debit**; A/P Trade **credit** |
| **5** | Payment issued | -- | A/P Trade **debit**; Cash/Bank **credit** |

At Step 4, the RNV account is fully cleared and the liability transfers to Accounts Payable. The PO Receipts balance for this transaction returns to zero.

### 2.2 2-Way Match

In a 2-way match, the receipt and voucher are processed simultaneously. No separate receipt step occurs:

| Step | Event | F43121 Record | GL Impact |
|---|---|---|---|
| **1** | Purchase order created | No record | None |
| **2** | Receive and voucher simultaneously (P4314) | Match Type **1** and **2** created together | Non-stock account **debit**; A/P Trade **credit** |
| **3** | Payment issued | -- | A/P Trade **debit**; Cash/Bank **credit** |

> **Note:** In a 2-way match, the temporary liability AAIs 4320 and 4355 are not used. The RNV account is bypassed entirely.

### 2.3 Reversals

Reversals are a critical factor in understanding F43121 behavior. When a receipt or voucher match is reversed in JD Edwards, the original F43121 record is **overwritten** rather than a new record being created:

| Reversal Type | F43121 Behavior | Match Type Change |
|---|---|---|
| **Receipt reversal** | Original Match Type 1 record is overwritten | Match Type changes from **1 to 3** |
| **Voucher match reversal** | Original Match Type 2 record is overwritten | Match Type changes from **2 to 4** |

This overwrite behavior is the primary reason F43121 does not function as a true ledger and why As-Of reporting is not available for RNV.

---

## Section 3: The F43121 Table

### 3.1 Overview

Table **F43121** (PO Receiver) is the source of truth for purchase order receipts. It stores a record for every receipt and voucher match transaction on a purchase order line.

**Critical behavior:** F43121 does not behave as a standard ledger. During a receipt or voucher reversal, the original record is **overwritten** with new information rather than a new record being created. This means:

- There is no transaction history for reversed receipts -- only the final state of the record is preserved
- It is impossible to generate a true As-Of report from this table
- Reconciliation must be performed as a **current balance-to-balance comparison**, not a historical roll-forward

### 3.2 Key F43121 Fields

| Field | Description |
|---|---|
| **Match Type** | Identifies the record type (1 = receipt, 2 = voucher, 3 = receipt reversal, 4 = voucher reversal) |
| **PRLAND** | Identifies whether the record is a standard receipt or a landed cost, and if landed, whether it is eligible for voucher match |
| **PRLVLA** | Stores the Landed Cost Level -- a three-character code from UDC 40/CA |
| **Quantity fields** | Updated when reversals occur; reflect the net position after any reversals |
| **Amount fields** | Updated when reversals occur; reflect the net position after any reversals |

### 3.3 The PRLAND Field

The **PRLAND** field is the key indicator for landed cost records within F43121:

| PRLAND Value | Meaning | RNV Impact |
|---|---|---|
| **Blank** | Standard product/item receipt | Eligible for voucher match |
| **1** | Product/item line | Eligible for voucher match |
| **2** | Landed cost -- eligible for voucher match | Will have a Match Type 2 record when vouchered |
| **3** | Landed cost -- accrual only | **Never vouchered** -- creates a permanent open balance if not excluded or suspended |

> **Important:** PRLAND = 3 records will never have a corresponding Match Type 2 record. They contribute to the F43121 open balance indefinitely. In RapidReconciler, these orders should be suspended to prevent them from creating a permanent false variance in the RNV reconciliation. See [Reconciling RNV in RapidReconciler](../MDS/reconciling-rnv.md).

---

## Section 4: Match Types

Table F43121 contains a Match Type column that identifies what stage of the purchasing process each record represents:

| Match Type | Description | Effect on RNV |
|---|---|---|
| **1** | **Receipt** -- Created when goods are received (P4312). The initial record that opens the RNV balance. | **Opens** RNV -- credits the RNV account via AAI 4320 |
| **2** | **Voucher Match** -- Created when the supplier invoice is matched to the receipt (P4314/P0411). | **Closes** RNV -- debits the RNV account via AAI 4320 |
| **3** | **Receipt Reversal** -- The original Match Type 1 record is overwritten when a receipt is reversed. | **Closes** RNV for the reversed quantity and amount |
| **4** | **Voucher Match Reversal** -- The original Match Type 2 record is overwritten when a voucher match is reversed. | **Reopens** RNV for the reversed amount |

> **Key Point:** A fully reconciled purchase order line will have offsetting Match Type 1 and Match Type 2 records that net to zero. Any line with a Match Type 1 record and no corresponding Match Type 2 is an open receipt -- a legitimate component of the RNV balance. Lines that are unbalanced for reasons other than a missing voucher match are where reconciling variances originate.

**Landed cost match types:**

| Match Type | Description |
|---|---|
| **5** | Landed cost receipt -- created when a landed cost is applied at receipt (PRLAND = 2) |
| **6** | Landed cost voucher match -- created when a landed cost is matched to an invoice |

---

## Section 5: Accounting Flow

### 5.1 AAIs Used in PO Receipts Processing

| AAI | Account | Used At |
|---|---|---|
| **4310** | Inventory | Receipt -- debits inventory |
| **4320** | RNV (Received-Not-Vouchered) | Receipt -- credits RNV; Voucher match -- debits RNV |
| **4330** | Purchase Price Variance | Voucher match -- when invoice cost differs from receipt cost |
| **4332** | Cost of Sales Variance | Voucher match -- when goods are consumed before voucher match |
| **4335** | Standard Cost Variance | Receipt -- when receipt cost differs from standard cost |
| **4340** | Exchange Rate Variance | Voucher match -- for multi-currency orders |
| **4350** | Tax Expense | Receipt -- for S, U, C, and B tax explanation codes |
| **4355** | RNV Tax | Receipt -- temporary tax liability |
| **4385 / 4390** | Landed Cost / Landed Cost Liability | Receipt -- when landed costs are applied |
| **PC** | A/P Trade | Voucher match -- creates the accounts payable liability |
| **PT** | Tax-Related A/P | Voucher match -- for use tax (U) and PST withheld (B) |

For full AAI configuration guidance, see the [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md).

### 5.2 Standard 3-Way Match Journal Entries

**At Receipt (P4312):**

| Account | Debit | Credit | AAI |
|---|---|---|---|
| Inventory | x | | 4310 |
| RNV | | x | 4320 |

**At Voucher Match (P4314):**

| Account | Debit | Credit | AAI |
|---|---|---|---|
| RNV | x | | 4320 |
| A/P Trade \* | | x | PC |

*Created by the GL Post program (R09801).

**If a purchase price variance exists at voucher match:**

| Account | Debit | Credit | AAI |
|---|---|---|---|
| RNV | x | | 4320 |
| Purchase Price Variance | x or (x) | | 4330 |
| A/P Trade \* | | x | PC |

For the full tax treatment by tax explanation code (S, U, V, C, B), see the [Purchase Order Reference Guide](../MDS/purchase_order_reference.md).

---

## Section 6: What Affects the RNV Balance

Understanding what creates, clears, and distorts the RNV balance is essential for effective reconciliation.

### 6.1 What Opens the RNV Balance

| Event | Program | Match Type Created |
|---|---|---|
| Standard PO receipt | P4312 | 1 |
| Landed cost receipt (PRLAND = 2) | P4312 / P43214 | 5 |
| Voucher match reversal | P4314 / P0411 | 4 (reopens RNV) |

### 6.2 What Closes the RNV Balance

| Event | Program | Match Type Created |
|---|---|---|
| Voucher match | P4314 / P0411 | 2 |
| Receipt reversal | P4312 | 3 (closes RNV for reversed amount) |
| Landed cost voucher match | P4314 / P0411 | 6 |

### 6.3 What Creates False or Permanent RNV Balances

| Cause | Description | Resolution |
|---|---|---|
| **Manual GL entry to clear RNV** | A journal entry was posted directly to the RNV account instead of processing through voucher match | The F43121 record remains open. Suspend the order in RapidReconciler; verify the GL is correct. |
| **PRLAND = 3 landed cost** | Accrual-only landed cost will never be vouchered | Suspend in RapidReconciler to prevent a permanent false variance |
| **Out-of-sequence reversal** | A voucher match reversal that cannot be re-matched | Investigate with IT; may require a manual journal entry |
| **Receipts routing** | Goods in a routing step are not yet in final stock -- the receipt is open | Understand routing stage; goods will clear when moved to STK |
| **Purchase price variance remaining in RNV** | AAI 4330 or 4332 not configured to absorb the full variance | Review AAI configuration |

---

## Section 7: Reconciliation Challenges

### 7.1 System Challenges

**F43121 is not a true ledger.** Receipt and voucher reversals overwrite key data elements rather than creating new records. This means:

- There is no row-by-row transaction history for reversed receipts
- As-Of reporting is not available -- you cannot reconstruct the RNV balance at a prior date from F43121 alone
- Reconciliation must be performed as a **current balance-to-balance comparison**

**Implications for period-end close:** Because the open receipts listing reflects the current state of F43121 (not a point-in-time snapshot), the RNV reconciliation must be performed as close to the period end as possible, using the current open receipts balance compared to the current GL balance.

### 7.2 Process Challenges

| Challenge | Description |
|---|---|
| **Receipts routing complexity** | Goods in routing stages create open receipts that are not yet in final inventory. Understanding which stage goods are at is required to correctly assess whether an open receipt is legitimate. |
| **Tax configuration** | Multiple tax explanation codes (S, U, V, C, B) produce different journal entries. The presence of AAIs 4350 and 4355 in the RNV sub-ledger adds complexity to the reconciliation. See the [Purchase Order Reference Guide](../MDS/purchase_order_reference.md). |
| **Landed cost configuration** | PRLAND values determine whether landed costs are eligible for voucher match. PRLAND = 3 records create permanent open balances that must be managed through suspension in RapidReconciler. |
| **Out-of-sequence reversals** | Reversing a receipt or voucher match out of the normal sequence can create accounting entries that are difficult to trace and may require IT intervention to resolve. |
| **Aging open receipts** | Receipts that have been open for an extended period accumulate in the RNV balance. Without a dedicated reconciliation tool, these are difficult to identify and address systematically. |

### 7.3 Reconciliation Challenges

The absence of As-Of reporting from F43121 means the reconciliation methodology differs from inventory:

| Aspect | Inventory Reconciliation | RNV Reconciliation |
|---|---|---|
| **Method** | Roll-forward from item ledger vs. GL | Current balance-to-balance comparison |
| **Historical view** | Available via As-Of page | **Not available** -- F43121 overwrites on reversal |
| **Period comparison** | Can reconcile any prior period | Current balance only |
| **Key risk** | Timing differences between cardex and GL | Open receipts that should be cleared but are not |

---

## Section 8: How RapidReconciler Helps

RapidReconciler addresses the core challenges of RNV reconciliation through automated import, matching, and exception reporting.

| Challenge | RapidReconciler Solution |
|---|---|
| **Manual matching of F43121 to GL** | RapidReconciler imports F43121 and F0911 data and performs the comparison automatically, surfacing only unreconciled items |
| **Identifying which receipts are open** | The Unreconciled link on the home screen shows only purchase orders with open amounts and reconciliation issues |
| **Manual voucher clearances creating false variances** | The Suspension feature allows orders cleared via manual journal entry to be removed from variance calculations |
| **Drill-down to the root cause** | From the summary level, users can drill down to the order, line, and document level to identify exactly where the discrepancy exists |
| **Aging open receipts** | All open receipts are visible in a single view, making it straightforward to identify items that have been outstanding for extended periods |
| **PRLAND = 3 landed cost records** | These can be suspended in RapidReconciler to prevent them from creating a permanent false variance |

For the complete guide to using RapidReconciler for RNV reconciliation, see the [Reconciling RNV in RapidReconciler Guide](../MDS/reconciling-rnv.md).

---

## Section 9: Related Documentation

| Document | Relevance |
|---|---|
| [Reconciling RNV in RapidReconciler](../MDS/reconciling-rnv.md) | How to use the PO Receipts module -- summary, drill-down, suspension, and F43121 match type reference |
| [Purchase Order Reference Guide](../MDS/purchase_order_reference.md) | Tax treatment by code, landed cost setup and journal entries, receipts routing accounting |
| [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md) | Complete AAI configuration for all purchasing transactions including 4310, 4320, 4330, 4332, 4335, 4340, 4350, 4355, 4385, 4390 |
| [Stock Status and Trial Balance Reconciliation](../MDS/stock-status-trial-balance.md) | Root causes of GL balance discrepancies applicable to both inventory and RNV |
| [Getting Started with RapidReconciler](../MDS/getting-started-with-rapidreconciler.md) | Login, navigation, and application overview |