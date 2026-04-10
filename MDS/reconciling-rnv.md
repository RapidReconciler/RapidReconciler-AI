**RapidReconciler**

**Training Guide: PO Receipts Module**

**Topic: Reconciling Received-Not-Vouchered (RNV) Accounts**

**Section 1: Overview**

RapidReconciler Version 7 by GSI provides the ability to reconcile Received-Not-Vouchered (RNV) accounts within the same application used for inventory and goods in-transit reconciliation. Receipt table data is imported into RapidReconciler and balanced directly against general ledger details, eliminating the need for separate tools or manual processes.

**Section 2: The Reconciliation Summary**

**2.1 Home Screen Overview**

The open receipts balance is summarized on the home screen and compared to the general ledger balance. The system automatically calculates the following:

| **Field**                 | **Description**                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Open Receipts Balance** | The total value of receipts that have not yet been matched to a supplier voucher.                                                           |
| **GL Balance**            | The corresponding general ledger balance for the RNV account.                                                                               |
| **Out of Balance Amount** | The difference between the open receipts balance and the GL balance.                                                                        |
| **Unreconciled Amount**   | The difference between receipt detail documents (receipts and vouchers) and the corresponding amounts booked to the general ledger details. |

**Section 3: Investigating Unreconciled Amounts**

**3.1 Displaying Unreconciled Purchase Orders**

Clicking the **Unreconciled** link on the home screen displays a filtered list of purchase orders that have open amounts and reconciliation issues. This focused view eliminates the need to review all purchase orders and directs attention only to those requiring action.

**3.2 Suspending Orders Cleared by Manual Voucher**

If an open receipt was cleared using a manual voucher entry (rather than the standard voucher match process), the order can be **suspended** within RapidReconciler. Suspending an order removes it from the variance calculations, keeping the reconciliation clean and focused on genuine outstanding issues.

**Section 4: Drill-Down Analysis**

**4.1 Line-Level Detail**

From the unreconciled purchase order list, users can drill down quickly to the line level to identify exactly where the discrepancy exists within a given order.

**4.2 Document-Level Detail**

Each line can be further analyzed to identify the specific document - receipt or voucher - that caused the issue. This level of detail makes it straightforward to:

- Determine the root cause of the discrepancy.
- Identify the corrective action required.
- Resolve the issue directly in JD Edwards or via a suspension in RapidReconciler as applicable.

**Section 5: Key Benefits**

Using RapidReconciler for RNV reconciliation provides the following advantages:

- **Consolidated platform** - RNV reconciliation is performed in the same application as inventory and goods in-transit reconciliation, reducing the need for multiple tools.
- **Automated balancing** - Receipt table data is automatically imported and compared to general ledger details, eliminating manual matching.
- **Focused exception reporting** - The unreconciled link surfaces only the orders with issues, saving time during the reconciliation process.
- **Flexible handling** - Orders cleared by manual voucher can be suspended to prevent them from distorting the variance calculations.
- **Full drill-down capability** - From the summary level down to the individual document, all detail is accessible within the application.

**Section 6: Contact Information**

For more information about RNV reconciliation in RapidReconciler, or if you are a current RapidReconciler customer with questions, contact GSI support at **<rrsupport@getgsi.com>** with "RNV for RapidReconciler" in the subject line.
