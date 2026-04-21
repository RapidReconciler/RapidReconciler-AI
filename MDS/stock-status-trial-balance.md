---
---
# JD Edwards Inventory Reconciliation vs. RapidReconciler

## A Side-by-Side Comparison

---

Reconciling inventory to the general ledger in JD Edwards is a necessary but time-consuming process. The standard approach -- producing a Stock Status report and comparing it to the trial balance -- has five well-documented failure points. This document examines each one, contrasts the manual JD Edwards approach with RapidReconciler, and explains why a dedicated reconciliation tool produces more reliable results with significantly less effort.

---

## The Five Failure Points -- Side by Side

### 1. Timing

| | JD Edwards (Manual) | RapidReconciler |
|---|---|---|
| **How it works** | A Stock Status report is run at a specific moment. Any transaction that posts after the report runs but before the period closes creates a discrepancy -- the GL has the entry but the report does not. | Reconciliation is updated automatically with each nightly import cycle. There is no dependency on a perfectly timed manual report run. |
| **The risk** | In multi-timezone environments, transactions are recorded according to the JD Edwards server clock -- not the user's local time. A user in a western time zone entering a transaction after the report runs can silently create a reconciling item. | Nightly import captures all posted transactions. Timing discrepancies are surfaced immediately and clearly identified by document date and GL date. |
| **What you have to do** | Coordinate the exact timing of the report run with the JDE server clock, ensure all transactional activity has fully stopped, and investigate any discrepancies found at period end. | Review the reconciliation page. If the out-of-balance is zero, the period is reconciled. If not, the variance source is labeled. |

---

### 2. Backdating

| | JD Edwards (Manual) | RapidReconciler |
|---|---|---|
| **How it works** | A transaction is posted to a GL period that differs from the period in which the inventory quantity actually changed. The stock status reflects physical inventory; the GL reflects the backdated period. | Backdated transactions are captured in the reconciliation with both their transaction date and GL date visible, making the period mismatch immediately identifiable. |
| **The risk** | Backdating can occur via manual date entry or via processing option settings in Manufacturing Accounting and Sales Update -- sometimes intentionally, sometimes not. In either case, the stock status and trial balance will not agree. | The Transactions page surfaces period mismatches as a labeled variance type. The Sub Type field identifies "Periods" as the source, and the offset is shown in the adjacent period -- no manual tracing required. |
| **What you have to do** | Review each reconciling item individually, identify whether backdating caused it, trace the transaction to the originating document, and determine whether a correcting entry is needed. | Identify the period mismatch on the Transactions page, confirm whether it is intentional, and document or resolve accordingly. |

---

### 3. Report Definition

| | JD Edwards (Manual) | RapidReconciler |
|---|---|---|
| **How it works** | The Stock Status report depends on correct cost method logic, data selection criteria, and inclusion rules. These can drift over time as items, cost methods, and business units change. | RapidReconciler reads directly from JD Edwards data tables -- F4111, F0902, F0911 -- eliminating the risk of incorrect cost method logic or flawed data selection in a custom report. |
| **The risk** | Three common problems: specifying the wrong cost method (e.g., hardcoding "07" instead of using COCSIN = 'I'), including non-stock items that carry an inadvertent cost, or excluding stock items through incorrect data selection. Any of these cause totals that will never agree to the GL regardless of how clean the underlying data is. | No report definition to configure. The reconciliation is driven by the same source tables JD Edwards uses. If an item has a cardex record, it is included. |
| **What you have to do** | Audit the report definition at each period end. Review data selection criteria. Verify cost method logic. Periodically re-validate the report as items and cost methods change. | No action required. Review the Integrity Reports monthly to confirm all GL class codes are correctly mapped in the model table. |

---

### 4. DMAAI Misconfiguration

| | JD Edwards (Manual) | RapidReconciler |
|---|---|---|
| **How it works** | DMAAI tables define how inventory transactions map to GL accounts. An incorrect account number in any one table causes every transaction of that type to post to the wrong account -- silently, with no error message. | RapidReconciler's Integrity Reports compare DMAAI entries against the model table and flag mismatches by object account, business unit, and subsidiary. The Transaction Detail report identifies the specific AAI responsible for any account mismatch. |
| **The risk** | Unlike timing or backdating issues, DMAAI misconfiguration is entirely invisible until reconciliation. Transactions post successfully to the wrong account. The discrepancy only surfaces as an unexplained variance, and tracing it requires reviewing DMAAI tables, transaction document types, and GL class code assignments manually -- a process that can take hours. | Configuration issues are surfaced proactively by six Integrity Reports that run on every import cycle. A misconfigured AAI is identified before it compounds into a large period-end variance. |
| **What you have to do** | Manually review DMAAI table entries, cross-reference with transaction document types, identify the incorrect mapping, correct it in JD Edwards, and then determine which prior transactions were affected and whether correcting journal entries are needed. | Review Integrity Report 2 (DMAAI Entry Integrity) for flagged mismatches. Drill into the Transaction Detail report for any unreconciled transaction to see the exact AAI responsible. Correct in JD Edwards and document. |

---

### 5. GL Class Code Changes

| | JD Edwards (Manual) | RapidReconciler |
|---|---|---|
| **How it works** | Changing a GL class code on an item with quantity on hand does not automatically generate a journal entry to reclassify the inventory value. Subsequent transactions post to the new account while the original value remains stranded in the old account. | GL class code mismatches are surfaced immediately. Variances caused by an incorrect class code change appear in the reconciliation on the next import cycle. Integrity Report 5 identifies mismatches between Item Branch and Item Location records. |
| **The risk** | JD Edwards allows GL class code changes at any level without checking whether inventory is on hand. If the correct procedure (adjust out, change code, adjust back in) is not followed, the result is a permanent reconciling item that grows with every subsequent transaction. | The impact is visible before it compounds. Integrity Report 3 identifies GL class codes missing from the model table. Integrity Report 5 identifies inconsistencies between item branch and location records. The As-Of page surfaces items carrying balances in multiple accounts. |
| **What you have to do** | Follow the adjust-out, change-code, adjust-in procedure for any item with quantity on hand. Update the GL class code at all levels (item master, item branch, item location, open order lines). Verify no residual balance remains in the original account. | Review Integrity Reports 3 and 5 after any GL class code change. If a variance is present, the corrective procedure can be applied in JD Edwards and confirmed on the next import cycle. |

---

## Summary

| Failure Point | Manual JDE Approach | RapidReconciler |
|---|---|---|
| **Timing** | Requires perfect coordination of report timing with JDE server clock | Continuous nightly reconciliation -- no report timing dependency |
| **Backdating** | Identified only after manual investigation of period-end discrepancies | Visible immediately with document date, GL date, and period label |
| **Report Definition** | Fragile -- depends on correct cost method, data selection, and inclusion logic | Not applicable -- reads directly from F4111, F0902, F0911 |
| **DMAAI Misconfiguration** | Invisible until reconciliation; requires hours of manual tracing | Surfaced proactively by Integrity Reports; drill-down identifies the exact AAI |
| **GL Class Code Changes** | Silent risk -- no warning when changing with quantity on hand | Immediate visibility; Integrity Reports 3 and 5 flag mismatches |

---

## Why the Manual Approach Breaks Down at Scale

Each of the five issues above is manageable in a small, simple JD Edwards environment. The manual approach breaks down as complexity increases:

**Volume** -- As transaction volume grows, the number of potential reconciling items grows with it. Manual investigation that takes an hour for 10 items takes a day for 100.

**Multiple companies** -- Each company requires its own Stock Status and trial balance comparison. DMAAI configuration must be maintained independently per company. Errors in one company are invisible to reconcilers working on another.

**Multiple cost methods** -- Environments using a mix of standard cost, weighted average, and actual cost require careful report definition management. A single incorrect cost method specification affects every item using that method.

**Frequent cost changes** -- Standard cost updates can create WIP revaluation variances. Without a tool to surface these, they accumulate as unexplained balances until the next reconciliation cycle.

**Staff turnover** -- The manual process depends heavily on institutional knowledge of the report configuration, DMAAI setup, and organizational backdating practices. When the person who knows how the reports are configured leaves, that knowledge leaves with them.

RapidReconciler addresses all of these by applying a consistent, automated reconciliation methodology that does not depend on report configuration, server timing, or organizational knowledge of DMAAI setup.

---

## How RapidReconciler Works

RapidReconciler reads JD Edwards data in **read-only mode** on a nightly import cycle and maintains a continuously updated reconciliation across three modules:

- **Inventory** -- F4111 perpetual item ledger vs. F0902 / F0911 GL balances
- **In Transit** -- ST/OT transfer order activity vs. In Transit clearing account
- **PO Receipts** -- F43121 receipt table vs. Received-Not-Vouchered GL account

For each module, variances are broken into labeled sources so the correct corrective action is immediately apparent. All corrections are made in JD Edwards -- RapidReconciler identifies the problem and tracks the resolution.

---

> *The period-end close should be a confirmation of what you already know -- not a discovery of what went wrong.*

---

*For more information, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com) or visit [rapidreconciler.getgsi.com](https://rapidreconciler.getgsi.com)*

---

## Related Documentation

- [DMAAI Reference Guide](../MDS/distribution-aais.md)
- [GL Class Code Management and Change Procedures](../MDS/gl-class-code-changes.md)
- [Inventory: Using the Application](../MDS/inventory-using-application.md)
