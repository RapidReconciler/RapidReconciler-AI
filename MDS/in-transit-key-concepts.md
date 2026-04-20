# RapidReconciler In Transit -- Key Concepts

## Understanding ST/OT Transfer Orders, Accounting Setup, and Reconciliation Fundamentals

---

## Table of Contents

- [Overview](#overview)
- [Section 1: What Is "In Transit"?](#section-1-what-is-in-transit)
- [Section 2: In Transit Accounting Setup](#section-2-in-transit-accounting-setup)
- [Section 3: How RapidReconciler Calculates In Transit](#section-3-how-rapidreconciler-calculates-in-transit)
- [Section 4: Glossary of Terms](#section-4-glossary-of-terms)
- [Section 5: Common Issues and How to Resolve Them](#section-5-common-issues-and-how-to-resolve-them)
- [Section 6: Related Documentation](#section-6-related-documentation)

---

## Overview

The RapidReconciler In Transit module reconciles the goods in transit clearing account against open ST/OT transfer order activity. When goods are shipped from one branch plant to another, the value of those goods is held in a clearing account until they are received at the destination branch. If the shipment and receipt do not match exactly in both quantity and amount, a balance remains in the clearing account that must be identified, investigated, and resolved.

This guide covers the foundational concepts needed to work effectively in the In Transit module:

- How ST/OT transfer orders work and what triggers an in-transit balance
- How DMAAs must be configured for transfers at cost and at cost plus
- How RapidReconciler calculates the in-transit position
- Key terms used throughout the module
- Common issues and resolution paths

> **Before using the In Transit module**, ensure you are familiar with the order types your organization uses for transfers and whether goods are transferred at cost or with a markup. This determines which DMAAI configuration applies and how variances are handled.

---

## Section 1: What Is "In Transit"?

### 1.1 Definition

In Transit reconciliation in RapidReconciler refers to the movement of inventory via the ST/OT (Stock Transfer / Order Transfer) process. The following conditions typically apply:

- Inventory is moved from branch plant **"A"** to branch plant **"B"**
- There is sufficient distance between the branches to warrant physical transportation
- Both branch plants are typically in the same company -- if branch plants are in different companies, consider using an intercompany sale instead
- The time between shipment and receipt is within a few weeks

### 1.2 The ST/OT Order Pair

Every transfer in JD Edwards involves two linked orders:

| Order | Type | Role | Branch |
|---|---|---|---|
| **ST** | Sales order | Shipping branch sells the goods | Branch A (shipping) |
| **OT** | Purchase order | Receiving branch buys the goods | Branch B (receiving) |

The ST and OT orders are linked. The cost on the ST becomes the price on the OT. When the ST order is ship confirmed, inventory leaves Branch A and the In Transit clearing account is debited. When the OT order is received at Branch B, the clearing account is credited and inventory is restored.

### 1.3 Key Rules

| Rule | Explanation |
|---|---|
| **Same order type, same costing method** | Do not mix costing methods on the same order type -- this causes accounting issues |
| **Matching item and line numbers** | The item number and line number on the ST sales order must match the OT purchase order |
| **No A/R interface** | The Sales Update program (P42800) for transfer orders must have the A/R interface turned off to avoid generating receivables |
| **No invoices** | There are typically no invoices generated for ST transfer orders |
| **Dollars only in RapidReconciler** | The In Transit account is tracked in dollars only in the GL. RapidReconciler calculates both quantity and amount in transit. |

### 1.4 When to Use Intercompany Instead of ST/OT

If the shipping and receiving branch plants are in **different companies**, an intercompany sale (SI/SK/OK) is generally more appropriate than an ST/OT transfer. Intercompany processing generates proper A/R and A/P entries between the companies, whereas ST/OT is designed for intra-company movements.

For intercompany processing details, see the [Sales Order Reference Guide](../MDS/sales_order_reference.md).

---

## Section 2: In Transit Accounting Setup

### 2.1 Transfer at Cost (No Markup)

When goods are transferred at cost with no markup, the price and cost on the ST order are the same value. The DMAAI configuration uses a wash account for the 4230/4245 AAIs to ensure no revenue or A/R impact occurs, regardless of the price entered on the order.

**Shipping Entries (ST Ship Confirmation):**

| AAI | Account | Debit | Credit | Notes |
|---|---|---|---|---|
| **4245** | Clearing (wash) | Price | | A/R interface is off -- 4245 is used instead of RC |
| **4230** | Clearing (wash) | | Price | Revenue account set to same wash account as 4245 |
| **4240** | Inventory | | Cost | Reduces inventory at Branch A |
| **4220** | In Transit | Cost | | Debits the clearing account at Branch A's cost |

**Receiving Entries (OT Receipt):**

| AAI | Account | Debit | Credit | Notes |
|---|---|---|---|---|
| **4310** | Inventory | Cost | | Increases inventory at Branch B's standard cost |
| **4320** | In Transit | | Cost | Credits the clearing account at OT order cost |

**How the wash accounts work:** Setting DMAAs 4245 and 4230 to the same clearing account means the price on the ST order has no net GL impact. Whether the price is $0 or $1,000,000, the debit and credit to the wash account cancel each other. Only the COST field drives the actual In Transit and Inventory entries.

**Variances at receipt:** Any difference between the amount debited to In Transit at shipment and the amount credited at receipt flows through DMAAI 4335. The correct 4335 configuration depends on whether the variance is a timing variance or a true branch cost difference. See the [Transfer Order Reference Guide](../MDS/transfer_order_reference.md) for full scenario analysis.

### 2.2 Transfer With Markup

When goods are transferred with a markup, the ST order carries both a cost and a higher price. The price becomes the cost on the OT order. In this configuration, the 4230 and 4245 AAIs point to real revenue and In Transit accounts -- price management on the ST order is critical.

**Shipping Entries (ST Ship Confirmation):**

| AAI | Account | Debit | Credit | Notes |
|---|---|---|---|---|
| **4245** | In Transit | Price | | Debits In Transit at the transfer price |
| **4230** | Interbranch Revenue | | Price | Records intercompany revenue at the transfer price |
| **4240** | Inventory | | Cost | Reduces inventory at Branch A's cost |
| **4220** | Cost of Goods Sold | Cost | | Records COGS at Branch A's cost |

**Receiving Entries (OT Receipt):**

| AAI | Account | Debit | Credit | Notes |
|---|---|---|---|---|
| **4310** | Inventory | Cost | | Increases inventory at Branch B's standard cost |
| **4320** | In Transit | | Cost | Credits In Transit at the OT order cost (= ST price) |

> **Key difference from transfer at cost:** The In Transit account is debited at the **price** (via 4245) rather than at the cost (via 4220). RapidReconciler uses the price if the In Transit account is in DMAAI 4245, or the cost if it is in DMAAI 4220, to calculate the in-transit balance at shipment.

For T-account examples of all transfer scenarios, see the [Transfer Order Reference Guide](../MDS/transfer_order_reference.md).

### 2.3 DMAAI Configuration Summary

| DMAAI | Transfer at Cost | Transfer at Cost Plus |
|---|---|---|
| **4220** | **In Transit** (clearing) | COGS |
| **4230** | Clearing (wash) | **Interbranch Revenue** |
| **4240** | Inventory | Inventory |
| **4245** | Clearing (wash) | **In Transit** |
| **4310** | Inventory | Inventory |
| **4320** | In Transit | In Transit |
| **4335** | In Transit or PPV Expense* | PPV Expense |

*The correct 4335 configuration depends on whether variances are timing-based or branch cost differences. See the [Transfer Order Reference Guide](../MDS/transfer_order_reference.md).

---

## Section 3: How RapidReconciler Calculates In Transit

### 3.1 In Transit Formulas

RapidReconciler calculates the in-transit position using the following formulas:

| Measure | Formula |
|---|---|
| **In Transit Quantity** | Quantity Shipped − Quantity Received |
| **In Transit Amount** | Amount Shipped − Amount Received |

These calculations are performed at the **order pair** level -- summarized by ST order, OT order, and item number. Lot and line number detail is collapsed into the order pair.

### 3.2 What Drives the In Transit Amount

| Event | Amount Used | DMAAI Source |
|---|---|---|
| **Shipment** | Price (if In Transit is in 4245) or Cost (if In Transit is in 4220) | From the ST sales order |
| **Receipt** | Cost on the OT purchase order | From the OT purchase order |

This means the In Transit balance in RapidReconciler mirrors the GL -- any difference between what was debited at shipment and credited at receipt is visible as a reconciling item.

### 3.3 The Variance Calculation Section

The In Transit Variance Calculation section breaks down the full GL out-of-balance amount into its sources:

| Variance Source | Description | Resolution |
|---|---|---|
| **Carry Forward** | Balance carried from the prior period | Resolve in prior period or include in current manual entry |
| **GL Batches** | Unposted GL batches affecting the In Transit account | Work with finance to post outstanding batches |
| **End of Day** | Sales Update not yet run for shipped orders | Confirm Sales Update P42800 transfer version ran successfully |
| **Transactions** | Mismatch between item ledger and GL for a specific document | Offsetting journal entry in JD Edwards + note in RapidReconciler |
| **Exclusions** | Order pairs excluded because both ST and OT are at status 999 with remaining balances | Offsetting journal entry for the excluded amount |
| **Manual Journal Entries** | Manual entries posted to the In Transit GL account | Informational -- confirms manual entries are reflected in the reconciliation |

### 3.4 The As-Of Page

The In Transit As-Of page provides a period-end view of all items that were in transit as of the selected fiscal period end date. Key features:

- **Period Selector** -- Select any fiscal period to see the in-transit position as of that period end
- **Transaction Detail** -- Click the **+** sign on any row to see all individual transactions making up the balance
- **Export** -- Transaction details can be exported to Excel for further analysis
- **Exclusion Adjust** -- An "Exclusion Adjust" entry appears when an order pair has been excluded. This is a RapidReconciler adjustment, not a JD Edwards transaction. It ensures the As-Of balance is accurately stated.

---

## Section 4: Glossary of Terms

### 4.1 Orders Page

The Orders page lists all order pairs that have either an open quantity or open amount. Key behaviors:

- Displays the **current** in-transit balance regardless of the period selected. Changing the period does not change what is shown on this page.
- A new order pair appears once a new shipment occurs on a transfer order.
- A receipt that matches the shipment in both units and amount will automatically remove the order pair from the page.
- Any remaining balances that cannot be cleared through JD Edwards processing must be removed using the Exclusion process.

### 4.2 Order Pair

In JD Edwards, a transfer order is broken down into line numbers. An item can appear on more than one line due to delivery date or lot number variations. In RapidReconciler, in-transit entries are based on an **order pair** concept.

An **Order Pair** is a summarized item number at the ST sales order, OT purchase order, and item number level. Lines and lots are collapsed in this summarization. All order pairs are listed on the Orders page.

**Order pair columns:**

| Column | Description |
|---|---|
| **From / To** | Shipping and receiving branch plants |
| **Item** | Item number |
| **Ship Qty** | Total quantity shipped on the ST order |
| **Rec Qty** | Total quantity received on the OT order |
| **TranQty** | In-transit quantity (Ship Qty − Rec Qty) |
| **Ship Amt** | Total amount shipped |
| **Rec Amt** | Total amount received |
| **TranAmt** | In-transit amount (Ship Amt − Rec Amt) |
| **Ship Sts** | Current status of the ST sales order |
| **Rec Sts** | Current status of the OT purchase order |

**Example:**

| From | To | Item | Ship Qty | Rec Qty | TranQty | Ship Amt | Rec Amt | TranAmt | Ship Sts | Rec Sts |
|---|---|---|---|---|---|---|---|---|---|---|
| A | B | 12345 | 100 | 94 | 6 | $100 | $94 | $6 | 999 | 999 |

In this example, both orders are fully closed (status 999) but 6 units valued at $6 remain unreconciled. No further JD Edwards transactions are possible -- the Exclusion process must be used.

### 4.3 Exclusions

When an order pair has a minimum status code of **999 on both the ST and OT**, no additional transactions can be performed in JD Edwards. Any remaining balance must be cleared using the **Exclusion** process in RapidReconciler.

Excluding an order pair removes its balance from the In Transit calculation. The excluded amount appears as a distinct **Exclusions** line in the Variance Calculation section:

| Variance Calculation | Amount |
|---|---|
| Carry Forward | ($750.10) |
| GL Batches | $0.00 |
| End of Day | $0.00 |
| Transactions | $0.00 |
| **Exclusions** | **($23.31)** |
| Manual Journal Entries | $0.00 |
| **Unreconciled Variance** | **($773.41)** |

The corrective action for an excluded order pair is an **offsetting journal entry in JD Edwards**. The Exclusions amount in the Variance Calculation section identifies the exact amount required.

For the complete exclusion procedure including the Exclusion Variance columns (ExclVarQty, ExclVarAmt), see the [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md).

---

## Section 5: Common Issues and How to Resolve Them

| Issue | Cause | Resolution |
|---|---|---|
| **In Transit account does not clear after receipt** | OT cost does not match ST price (cost plus); or standard cost changed between order entry and shipment | Review the scenario against the DMAAI 4335 configuration. See [Transfer Order Reference Guide](../MDS/transfer_order_reference.md). |
| **Order pair appears on the Orders page but status is not 999** | Goods have been shipped but not yet received | Normal -- monitor until receipt is processed |
| **Order pair at status 999 with a remaining balance** | Quantity or amount discrepancy between ship and receive that cannot be corrected in JD Edwards | Apply the Exclusion process; post an offsetting journal entry. See [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md). |
| **Exclusion Variance (ExclVarQty or ExclVarAmt) is non-zero** | New transactions occurred on a previously excluded open purchase order | Unexclude and re-exclude the order pair to recalculate the exclusion amount |
| **End of Day variance in In Transit** | Sales Update P42800 (transfer order version) did not run or did not complete successfully | Confirm the Sales Update job completed; investigate any errors |
| **Same order appearing multiple times** | Multiple lines or lots on the same order -- collapsed into the order pair but visible in drill-down | Normal behavior; review at the order pair level |
| **In Transit amount differs from what is expected** | DMAAI 4245 vs. 4220 configuration affects whether price or cost is used for the in-transit balance | Confirm which AAI holds the In Transit account for the applicable order type |
| **Carry Forward balance that does not resolve** | A prior period exclusion or manual journal entry was not correctly applied | Return to the prior period and investigate; ensure the journal entry offsets the correct account |

---

## Section 6: Related Documentation

| Document | Relevance |
|---|---|
| [Transfer Order Reference Guide](../MDS/transfer_order_reference.md) | Full accounting detail for all transfer at cost and cost plus scenarios, DMAAI 4335 configuration, and period-end reconciliation |
| [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md) | Step-by-step exclusion process, Exclusion Variance columns, unexclude/re-exclude procedure, and journal entry guidance |
| [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md) | Complete AAI reference for all distribution and manufacturing transactions |
| [Sales Order Reference Guide](../MDS/sales_order_reference.md) | Sales Update (R42800) and intercompany processing |
| [Stock Status and Trial Balance Reconciliation](../MDS/stock-status-trial-balance.md) | Root causes of GL vs. perpetual discrepancies |
| [Getting Started with RapidReconciler](../MDS/getting-started-with-rapidreconciler.md) | Login, navigation, and application overview |