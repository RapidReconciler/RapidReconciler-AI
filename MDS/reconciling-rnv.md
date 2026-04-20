# Reconciling Received-Not-Vouchered (RNV) Accounts in RapidReconciler

## PO Receipts Module Reference Guide

---

## Table of Contents

- [Overview](#overview)
- [Section 1: Understanding the RNV Account](#section-1-understanding-the-rnv-account)
  - [1.1 What Is the RNV Account?](#11-what-is-the-rnv-account)
  - [1.2 Why RNV Reconciliation Is Challenging](#12-why-rnv-reconciliation-is-challenging)
  - [1.3 The F43121 Table](#13-the-f43121-table)
  - [1.4 F43121 Match Types](#14-f43121-match-types)
  - [1.5 The PRLAND Field](#15-the-prland-field)
- [Section 2: The Reconciliation Summary](#section-2-the-reconciliation-summary)
- [Section 3: Investigating Unreconciled Amounts](#section-3-investigating-unreconciled-amounts)
- [Section 4: Drill-Down Analysis](#section-4-drill-down-analysis)
- [Section 5: Common Causes of RNV Variances](#section-5-common-causes-of-rnv-variances)
- [Section 6: Key Benefits](#section-6-key-benefits)
- [Section 7: Related Documentation](#section-7-related-documentation)

---

## Overview

RapidReconciler provides the ability to reconcile Received-Not-Vouchered (RNV) accounts within the same application used for inventory and goods in-transit reconciliation. Receipt table data is imported into RapidReconciler and balanced directly against general ledger details, eliminating the need for separate tools or manual processes.

---

## Section 1: Understanding the RNV Account

### 1.1 What Is the RNV Account?

The Received-Not-Vouchered (RNV) account -- controlled by DMAAI **4320** -- is a temporary liability account that holds the value of goods received from a supplier until the corresponding supplier invoice is matched and vouchered. It acts as the bridge between the purchasing and accounts payable processes.

**The standard flow:**

| Step | Transaction | Account Debited | Account Credited | AAI |
|---|---|---|---|---|
| **1** | PO Receipt | Inventory | **RNV** | 4310 / 4320 |
| **2** | Voucher Match | **RNV** | A/P Trade | 4320 / PC |

At any point in time, the RNV account balance should equal the value of goods that have been received but not yet matched to a supplier invoice. If the balance does not agree to open receipt activity, a reconciling variance exists.

### 1.2 Why RNV Reconciliation Is Challenging

Without a dedicated tool, reconciling the RNV account requires manually matching F43121 (PO Receiver) records to general ledger entries -- a time-consuming process that becomes increasingly complex as transaction volume grows. Common challenges include:

- **Volume** -- High-volume purchasing environments can have thousands of open receipts at any point in time.
- **Aging receipts** -- Old receipts that were never vouchered or incorrectly closed accumulate over time and are difficult to identify manually.
- **Manual vouchers** -- Receipts cleared through manual journal entries rather than the standard voucher match process leave the F43121 record open, creating a false variance.
- **Cost variances** -- Price variances at voucher match (AAIs 4330, 4332, 4335) can leave residual balances in the RNV account that are difficult to trace.
- **Currency differences** -- In multi-currency environments, exchange rate variances at voucher match (AAI 4340) can create additional reconciling items.

### 1.3 The F43121 Table

The F43121 (PO Receiver) table is the source of truth for RNV reconciliation. It stores a complete record of every receipt and voucher match transaction on a purchase order line. RapidReconciler imports F43121 data and compares it directly to the corresponding GL entries to identify where the two do not agree.

### 1.4 F43121 Match Types

Each record in F43121 carries a **Match Type** field that identifies what stage of the purchasing process the record represents. Understanding match types is essential for interpreting the RNV reconciliation.

| Match Type | Description | Effect on RNV |
|---|---|---|
| **1** | **Receipt** -- Created when goods are received against a purchase order (P4312). The initial record that opens the RNV balance. | **Opens** RNV -- credits the RNV account via AAI 4320 |
| **2** | **Voucher Match** -- Created when the supplier invoice is matched to the receipt (P4314/P0411). Written when the Match Type 1 record transitions from open to paid. | **Closes** RNV -- debits the RNV account via AAI 4320 |
| **3** | **Reversal of Receipt** -- Created when a receipt is reversed. Offsets the original Match Type 1 record. | **Closes** RNV for the reversed quantity |
| **4** | **Reversal of Voucher Match** -- Created when a voucher match is reversed. Reopens the RNV balance for the reversed amount. | **Reopens** RNV for the reversed amount |
| **5** | **Landed Cost Receipt** -- Created when a landed cost is applied at the time of receipt (P4312). | Opens RNV for the landed cost amount (AAI 4390) |
| **6** | **Landed Cost Voucher Match** -- Created when a landed cost is matched to an invoice. | Closes RNV for the landed cost amount |

> **Key Point:** At any point in time, a fully reconciled purchase order line should have offsetting Match Type 1 and Match Type 2 records that net to zero. Any line where Match Type 1 exists without a corresponding Match Type 2 represents an open receipt -- a legitimate component of the RNV balance. Lines that appear unbalanced for reasons other than a missing voucher match are where reconciling variances originate.

### 1.5 The PRLAND Field

The **PRLAND** field in F43121 identifies whether a record is a standard receipt or a landed cost, and whether the landed cost is eligible for voucher match:

| PRLAND Value | Meaning |
|---|---|
| **Blank** | Standard product/item receipt line |
| **1** | Product/item line |
| **2** | Landed cost -- eligible for voucher match |
| **3** | Landed cost -- accrual only, not eligible for voucher match |

> **Note:** When PRLAND = 3, the landed cost is accrued at receipt but will never be vouchered. These records contribute to the F43121 open balance but will not have a corresponding Match Type 2 record. They must be identified and excluded or suspended in RapidReconciler to avoid creating a permanent false variance in the RNV reconciliation.

---

## Section 2: The Reconciliation Summary

### 2.1 Home Screen Overview

The open receipts balance is summarized on the home screen and compared to the general ledger balance. The system automatically calculates the following:

| Field | Description |
|---|---|
| **Open Receipts Balance** | The total value of receipts that have not yet been matched to a supplier voucher |
| **GL Balance** | The corresponding general ledger balance for the RNV account |
| **Out of Balance Amount** | The difference between the open receipts balance and the GL balance |
| **Unreconciled Amount** | The difference between receipt detail documents (receipts and vouchers) and the corresponding amounts booked to the general ledger details |

### 2.2 Understanding the Two Variances

The **Out of Balance Amount** and the **Unreconciled Amount** measure different things and both require attention:

- The **Out of Balance Amount** compares the total F43121 open receipts balance to the total GL balance. If these do not agree, there is a high-level mismatch between the purchasing subledger and the general ledger.
- The **Unreconciled Amount** identifies specific documents where the receipt or voucher amounts do not agree to the GL at the document level. This is where the root cause investigation begins.

---

## Section 3: Investigating Unreconciled Amounts

### 3.1 Displaying Unreconciled Purchase Orders

Clicking the **Unreconciled** link on the home screen displays a filtered list of purchase orders with open amounts and reconciliation issues. This focused view eliminates the need to review all purchase orders and directs attention only to those requiring action.

### 3.2 Suspending Orders Cleared by Manual Voucher

If an open receipt was cleared using a manual voucher entry (rather than the standard voucher match process), the F43121 record remains open even though the GL has been cleared. In RapidReconciler, the order can be **suspended** to remove it from the variance calculations, keeping the reconciliation clean and focused on genuine outstanding issues.

> **Best Practice:** Document the reason for each suspension for audit purposes. Suspended orders should be reviewed periodically to confirm they remain appropriately suspended and have not had new activity applied against them.

### 3.3 Aging Analysis

Reviewing RNV balances by age is an important part of the reconciliation process. Receipts that have been open for an extended period may indicate:

- Supplier invoices that were never received or processed
- Purchase orders that were incorrectly closed without a voucher match
- Disputed invoices being held outside the normal process
- System errors that prevented the voucher match from completing

Addressing aging RNV items regularly prevents the balance from accumulating to a point where it becomes difficult to manage.

---

## Section 4: Drill-Down Analysis

### 4.1 Line-Level Detail

From the unreconciled purchase order list, users can drill down to the line level to identify exactly where the discrepancy exists within a given order. This narrows the investigation from the order level to the specific item line causing the variance.

### 4.2 Document-Level Detail

Each line can be further analyzed to identify the specific document -- receipt or voucher -- that caused the issue. This level of detail makes it straightforward to:

- Determine the root cause of the discrepancy
- Identify the corrective action required
- Resolve the issue directly in JD Edwards or via a suspension in RapidReconciler as applicable

### 4.3 Corrective Actions

Once the root cause is identified through drill-down, the appropriate corrective action can be taken:

| Root Cause | Corrective Action |
|---|---|
| Open receipt with no corresponding voucher | Process the voucher match in JD Edwards (P4314) |
| Receipt cleared by manual journal entry | Suspend the order in RapidReconciler |
| Cost variance remaining in RNV | Review AAI 4330/4332/4335 configuration; post a manual journal entry if needed |
| Duplicate receipt or voucher | Reverse the incorrect transaction in JD Edwards |
| Purchase order incorrectly closed | Reopen and reprocess through standard voucher match |

---

## Section 5: Common Causes of RNV Variances

| Cause | Description | Resolution |
|---|---|---|
| **Unmatched receipt** | Goods received but supplier invoice not yet processed | Process voucher match when invoice is received |
| **Manual GL entry used to clear RNV** | A journal entry was posted directly to the RNV account instead of processing through voucher match | Suspend the order in RapidReconciler; verify the GL is correct |
| **Price variance at voucher match** | Invoice amount differs from receipt amount; AAI 4330 or 4332 not configured to clear RNV | Review AAI configuration; post manual journal entry if needed |
| **Standard cost variance** | Receiving at a different cost than the standard (AAI 4335) | Verify DMAAI 4335 configuration for the applicable order type |
| **Exchange rate variance** | Multi-currency orders where the rate changed between receipt and voucher match | Review AAI 4340; post manual entry to clear residual |
| **Landed cost not vouchered** | Landed cost applied at receipt with PRLAND = 2 but voucher match not completed | Process voucher match for the landed cost; or set PRLAND = 3 if accrual only |
| **Aging open receipts** | Old receipts never vouchered accumulating in the balance | Investigate each aged item; process voucher match, reversal, or manual entry as appropriate |

---

## Section 6: Key Benefits

Using RapidReconciler for RNV reconciliation provides the following advantages:

- **Consolidated platform** -- RNV reconciliation is performed in the same application as inventory and goods in-transit reconciliation, reducing the need for multiple tools
- **Automated balancing** -- Receipt table data is automatically imported and compared to general ledger details, eliminating manual matching
- **Focused exception reporting** -- The unreconciled link surfaces only the orders with issues, saving time during the reconciliation process
- **Flexible handling** -- Orders cleared by manual voucher can be suspended to prevent them from distorting the variance calculations
- **Full drill-down capability** -- From the summary level down to the individual document, all detail is accessible within the application
- **Aging visibility** -- Open receipts can be reviewed by age to identify and address items that have been outstanding for extended periods

---

## Section 7: Related Documentation

- [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md)
- [Accounting in Purchasing](../MDS/accounting-in-purchasing.md)
- [Purchase Order Reference Guide](../MDS/purchase_order_reference.md)
- [Stock Status and Trial Balance Reconciliation](../MDS/stock-status-trial-balance.md)

---

*For more information about RNV reconciliation in RapidReconciler, contact GSI support at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com) with "RNV for RapidReconciler" in the subject line.*