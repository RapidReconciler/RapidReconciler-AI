# ST/OT Transfer Order Reference Guide

## Accounting, In-Transit Tracking, and DMAAI Configuration

---

## Table of Contents

- [Overview](#overview)
- [Section 1: ST/OT Order Structure](#section-1-stot-order-structure)
  - [1.4 JD Edwards Setup Requirements](#14-jd-edwards-setup-requirements-for-stot-orders)
- [Section 2: Transfer at Cost -- No Branch Cost Variance](#section-2-transfer-at-cost----no-branch-cost-variance)
- [Section 3: Transfer at Cost -- Branch Cost Variance (Different Standard Costs)](#section-3-transfer-at-cost----branch-cost-variance-different-standard-costs)
- [Section 4: Transfer at Cost Plus (With Markup)](#section-4-transfer-at-cost-plus-with-markup)
- [Section 5: Complete Scenario Matrix](#section-5-complete-scenario-matrix)
- [Section 6: In-Transit Inventory Tracking](#section-6-in-transit-inventory-tracking)
- [Section 7: Period-End Reconciliation Considerations](#section-7-period-end-reconciliation-considerations)
- [Section 8: DMAAI Quick Reference for Transfer Orders](#section-8-dmaai-quick-reference-for-transfer-orders)
- [Section 9: Related Documentation](#section-9-related-documentation)

---

## Overview

ST/OT transfer orders in JD Edwards are used to move materials between branch plants within the same company. The process uses a clearing account to hold the value of goods while they are in transit between locations.

This clearing account -- commonly referred to as the **In Transit** or **Goods In Transit** account -- differs from a standard perpetual inventory account in an important way: while goods are in transit, the quantities on hand are removed from the perpetual counts and exist only as a balance in the clearing account. Once items are received at the destination branch, the clearing account is relieved and perpetual inventory is restored.

This guide covers:

- The ST/OT order structure and how it works
- DMAAI configuration for transfer at cost and transfer at cost plus
- How standard cost variances affect the accounting
- How to configure DMAAI 4335 for different scenarios
- RapidReconciler in-transit tracking as an alternative to receipts routing
- A complete reference of all scenarios from simple to complex

---

## Section 1: ST/OT Order Structure

### 1.1 Order Types

| Order Type | Description | Direction |
|---|---|---|
| **ST** | Sales order -- the shipping branch sells the goods | Branch A (shipping) |
| **OT** | Purchase order -- the receiving branch buys the goods | Branch B (receiving) |

The ST and OT orders are linked. The cost on the ST becomes the price on the OT. When transferred **at cost**, the ST cost and OT cost are equal. When transferred **at cost plus** (with markup), the ST price is higher than the ST cost, and the OT receives the goods at the ST price.

### 1.2 Key DMAAI Tables

| DMAAI | Account | Used At |
|---|---|---|
| **4220** | In Transit (Cost) or COGS | ST ship -- cost transfer |
| **4230** | Revenue | ST ship -- cost plus transfer |
| **4240** | Inventory | ST ship -- reduces inventory at shipping branch |
| **4245** | A/R or In Transit (Cost Plus) | ST ship -- cost plus transfer |
| **4310** | Inventory | OT receipt -- increases inventory at receiving branch |
| **4320** | RNV / Goods In Transit | OT receipt -- clears the In Transit account |
| **4335** | Purchased Part Variance (PPV) | OT receipt -- absorbs cost variances |

### 1.3 Recommended DMAAI Configuration

| DMAAI | Account | Transfer at Cost | Transfer at Cost Plus |
|---|---|---|---|
| **4220** | COGS / In Transit | **In Transit** (clearing account) | COGS |
| **4230** | Revenue | In Transit (clearing) | **Revenue** |
| **4240** | Inventory | Inventory | Inventory |
| **4245** | A/R / In Transit | In Transit (clearing) | **In Transit** |
| **4310** | Inventory | Inventory | Inventory |
| **4320** | RNV / In Transit | In Transit | In Transit |
| **4335** | PPV | Expense or In Transit* | Expense |

*See Section 3 for the critical distinction on DMAAI 4335 configuration.

> **Important:** The RapidReconciler In Transit balance at shipment uses the **price** if the In Transit account is configured in DMAAI 4245, or the **cost** if the In Transit account is configured in DMAAI 4220. At receipt, the balance uses the **cost on the PO**.

### 1.4 JD Edwards Setup Requirements for ST/OT Orders

Before processing ST/OT transfer orders, confirm the following are configured correctly in JD Edwards:

| Requirement | Description |
|---|---|
| **Order Activity Rules** | Must be configured for both ST and OT order types at each applicable status code |
| **Line Type** | The line type used on ST/OT orders must have the correct inventory interface setting |
| **Branch/Plant constants** | Both the shipping and receiving Branch/Plants must be configured and active |
| **AAIs** | DMAIIs 4220/4230/4240/4245/4310/4320/4335 must be set up for the applicable order types and GL class codes |
| **Item setup** | The item must be set up in both the shipping and receiving Branch/Plants with consistent GL class codes |
| **Standard cost** | If using standard cost, costs should be frozen in both Branch/Plants before transfer orders are entered |
| **Inter-branch markup** | If transferring at cost plus, Branch Sales Markup (P3403) must be configured before orders are entered |

---

---

## Section 2: Transfer at Cost -- No Branch Cost Variance

This is the simplest scenario: both branches have the same standard cost, and no cost changes occur between order entry and receipt.

### 2.1 Scenario 1 -- No Variance (Cost on OT Matches ST)

**Setup:**
- Item 123, 10 units
- Standard cost: Branch A = **$1.00** | Branch B = **$1.00**
- ST cost: $10.00 | OT cost: $10.00

#### Ship Confirmation (ST)

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch A) | 4240 | | $10.00 |
| In Transit | 4220 | $10.00 | |

#### OT Receipt (Branch B)

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch B) | 4310 | $10.00 | |
| In Transit | 4320 | | $10.00 |

**Result:** In Transit clears perfectly. No variance. DMAAI 4335 not needed. ✓

---

### 2.2 Scenario 2 -- Cost Change After Order Entry (Same Cost Updated in Both Branches)

**Setup:**
- Item 123, 10 units
- Standard cost updated from $1.00 to $1.10 in **both** branches after order entry
- ST cost at shipment: $11.00 | OT cost on PO: $10.00 (not updated)

#### Ship Confirmation (ST)

Ship confirmation automatically updates to the new standard cost:

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch A) | 4240 | | $11.00 |
| In Transit | 4220 | $11.00 | |

#### OT Receipt (Branch B)

The OT PO still expects $10.00:

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch B) | 4310 | $11.00 | |
| In Transit | 4320 | | $10.00 |
| **In Transit (4335)** | **4335** | | **$1.00** |

**Result:** If DMAAI 4335 points to the **In Transit account**, the $1.00 variance clears and In Transit is fully resolved. ✓

> **Configuration required:** Set DMAAI 4335 to the **Goods In Transit account** for OT order types to absorb timing variances caused by cost changes between order entry and shipment.

---

## Section 3: Transfer at Cost -- Branch Cost Variance (Different Standard Costs)

This scenario occurs when the standard cost has **not** been updated in the receiving branch. This is a true cost variance between branches, not a timing issue.

### 3.1 Scenario 3 -- Branch A and Branch B Have Different Standard Costs

**Setup:**
- Item 123, 10 units
- Standard cost: Branch A = **$1.00** | Branch B = **$0.90** (not updated)
- ST cost: $10.00 | OT cost: $10.00

#### Ship Confirmation (ST)

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch A) | 4240 | | $10.00 |
| In Transit | 4220 | $10.00 | |

#### OT Receipt (Branch B)

Branch B's standard cost is $0.90, so Inventory is debited at $9.00:

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch B) | 4310 | $9.00 | |
| In Transit | 4320 | | $10.00 |
| **PPV Expense (4335)** | **4335** | **$1.00** | |

**Result:** In Transit clears fully. The $1.00 cost difference is correctly expensed to PPV. ✓

> **Configuration required:** Set DMAAI 4335 to the **PPV Expense account** when the receiving branch has a different standard cost than the shipping branch.

---

### 3.2 The DMAAI 4335 Conflict -- No Perfect Setup

This is the core challenge of ST/OT transfer order accounting. **DMAAI 4335 can only be configured one way** in JD Edwards, but different scenarios require different accounting treatment:

| Scenario | Variance Type | DMAAI 4335 Should Point To |
|---|---|---|
| **Scenario 2** -- Cost changed after order entry; both branches updated | Timing variance between order cost and shipment cost | **In Transit account** -- to clear the remaining balance |
| **Scenario 3** -- Standard cost not updated in receiving branch | True standard cost variance between branches | **PPV Expense account** -- to correctly expense the variance |

> **Best Practice:** Analyze the transfer order scenarios that occur most frequently in your organization and configure DMAAI 4335 to handle those scenarios correctly. Document the configuration decision and the rationale. Any exceptions -- where a different scenario occurs -- must be managed through manual journal entries or procedural controls.

---

## Section 4: Transfer at Cost Plus (With Markup)

When goods are transferred at a markup, the ST order carries both a cost and a price. The price becomes the OT cost. This changes how the In Transit account is used.

### 4.1 Scenario 4 -- Transfer at Cost Plus, No Branch Variance

**Setup:**
- Item 123, 10 units
- Standard cost: Branch A = **$1.00** | Branch B = **$1.00**
- ST cost: $10.00 | ST price: **$12.00**
- OT cost: $12.00 (matches ST price)

#### Ship Confirmation (ST)

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch A) | 4240 | | $10.00 |
| In Transit | 4245 | $12.00 | |
| Revenue | 4230 | | $12.00 |
| COGS | 4220 | $10.00 | |

#### OT Receipt (Branch B)

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch B) | 4310 | $10.00 | |
| In Transit | 4320 | | $12.00 |
| **PPV Expense (4335)** | **4335** | **$2.00** | |

**Result:** In Transit clears. The $2.00 markup is expensed to PPV. ✓

---

### 4.2 Scenario 5 -- Transfer at Cost Plus, Price on ST Does Not Match OT Cost

**Setup:**
- Item 123, 10 units
- Standard cost: Branch A = **$1.00** | Branch B = **$1.00**
- ST cost: $10.00 | ST price: $12.00
- OT cost: **$11.00** (does not match ST price)

#### Ship Confirmation (ST)

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch A) | 4240 | | $10.00 |
| In Transit | 4245 | $12.00 | |
| Revenue | 4230 | | $12.00 |
| COGS | 4220 | $10.00 | |

#### OT Receipt (Branch B)

| Account | AAI | Debit | Credit |
|---|---|---|---|
| Inventory (Branch B) | 4310 | $10.00 | |
| In Transit | 4320 | | $11.00 |
| **PPV Expense (4335)** | **4335** | **$1.00** | |

**Result:** In Transit does **not** clear. A balance of **$1.00** remains ($12.00 In Transit debit - $11.00 credit - $1.00 PPV debit = $0 does not resolve the $12.00 In Transit balance). This scenario requires investigation and a manual journal entry to clear the In Transit account. ✗

---

## Section 5: Complete Scenario Matrix

The following matrix summarizes all scenarios from the T-account analysis, organized by transfer type and whether a branch cost variance exists.

### 5.1 Transfer at Cost

| Scenario | Branch A Std | Branch B Std | ST Cost | OT Cost | PPV | In Transit Clears? | DMAAI 4335 Config |
|---|---|---|---|---|---|---|---|
| **1** No variance | $1.00 | $1.00 | $10.00 | $10.00 | None | ✓ Yes | Not needed |
| **2** Cost change (both updated) | $1.10 | $1.10 | $11.00 | $10.00 | $1.00 credit | ✓ Yes | **In Transit** |
| **3** Branch variance | $1.00 | $0.90 | $10.00 | $10.00 | $1.00 debit | ✓ Yes | **PPV Expense** |
| **4** Branch variance + cost change | $1.10 | $0.90 | $11.00 | $10.00 | $1.00 debit | ✗ **No** | Neither resolves |

### 5.2 Transfer at Cost Plus

| Scenario | Branch A Std | Branch B Std | ST Price | OT Cost | PPV | In Transit Clears? | DMAAI 4335 Config |
|---|---|---|---|---|---|---|---|
| **5** No variance | $1.00 | $1.00 | $12.00 | $12.00 | $2.00 debit | ✓ Yes | **PPV Expense** |
| **6** OT cost does not match ST price | $1.00 | $1.00 | $12.00 | $11.00 | $1.00 debit | ✗ **No** | Neither resolves |
| **7** Branch variance, cost plus | $1.00 | $0.90 | $12.00 | $12.00 | $3.00 debit | ✓ Yes | **PPV Expense** |
| **8** Branch variance, cost mismatch | $1.00 | $0.90 | $12.00 | $11.00 | $2.00 debit | ✗ **No** | Neither resolves |

> **Key finding from the matrix:** The only scenarios where In Transit **does not clear** are those where the OT cost does not match the ST price (cost plus) or where multiple variances exist simultaneously. These require manual journal entries to resolve.

---

## Section 6: In-Transit Inventory Tracking

### 6.1 Traditional Approach -- Receipts Routing

Receipts routing is a JD Edwards feature that tracks inventory physically in transit from one branch to another. After the shipping branch confirms the sales order shipment, goods become available for receipt at the receiving branch through receipt routing operations.

**The two key routing stages:**

| Stage | Description |
|---|---|
| **TRAN (In Transit)** | Goods are in transit and have not yet been physically received into stock |
| **STK (Stock)** | Goods have been physically received and entered into inventory at the destination branch |

While receipts routing provides visibility into in-transit inventory, it requires dedicated setup and configuration within JD Edwards to function correctly and adds complexity to the receiving process.

### 6.2 RapidReconciler Alternative -- In Transit As-Of Tracking

RapidReconciler provides a built-in alternative to receipts routing by generating an inventory "As-Of" view dynamically as transfer orders are shipped and received. This functionality is accessible directly through the RapidReconciler user interface on the **In Transit As-Of page**.

**Key features:**

| Feature | Description |
|---|---|
| **Period Selector** | Select any fiscal period to see all items that were in transit as of that period end date |
| **Transaction Detail** | Click the **+** sign at the left of any row to expand the view and see all individual detail transactions making up the current in-transit balance |
| **Export** | Detail transactions can be exported to Excel for further analysis |

**Benefit over receipts routing:** Using RapidReconciler for in-transit tracking eliminates the need to configure and maintain the JD Edwards receipts routing setup, while still providing full visibility into what is in transit at any point in time.

### 6.3 In Transit Balance Calculation in RapidReconciler

RapidReconciler calculates the In Transit balance as follows:

- At **shipment**, the balance uses the **price** if the In Transit account is configured in DMAAI 4245, or the **cost** if configured in DMAAI 4220.
- At **receipt**, the balance uses the **cost on the purchase order (OT)**.

This means the In Transit balance in RapidReconciler reflects the same amounts as the GL -- any variance between ship and receive will be visible as a reconciling item.

### 6.4 Exclusion Adjust

Within the In Transit As-Of transaction details, an item labeled **"Exclusion Adjust"** may appear. This represents an adjustment related to the order exclusion process in RapidReconciler and is covered in detail in the exclusions documentation.

---

## Section 7: Period-End Reconciliation Considerations

### 7.1 When the In Transit Account Does Not Clear

If the In Transit GL account carries a balance at period end, investigate using the following approach:

1. **Identify open transfer orders** -- Use the RapidReconciler In Transit Orders page or JD Edwards open order inquiry to identify all ST orders that have shipped but not yet been fully received.
2. **Verify the OT cost matches the ST price** -- For cost plus transfers, confirm the OT purchase order cost matches the ST sales order price. A mismatch is the most common cause of an unresolved In Transit balance.
3. **Check for DMAAI 4335 mismatches** -- Confirm that DMAAI 4335 is configured correctly for the scenario that occurred.
4. **Identify standard cost changes** -- Determine whether any standard cost updates occurred between order entry and shipment or between shipment and receipt.
5. **Manual journal entry** -- If the variance cannot be resolved through the above steps, a manual journal entry to clear the In Transit account may be required. Document the reason for the manual entry.

### 7.2 Preventing In Transit Variances

| Action | Prevention |
|---|---|
| Keep standard costs synchronized across branch plants | Eliminates Scenario 3/4 branch variance issues |
| Update OT purchase order costs when ST prices change | Prevents cost mismatch on cost plus transfers |
| Run cost updates in both branches simultaneously | Prevents Scenario 4 (cost change only in one branch) |
| Configure DMAAI 4335 for the most common scenario | Reduces unresolved In Transit balances |
| Use RapidReconciler In Transit As-Of report at period end | Identifies open items before they become reconciling issues |

### 7.3 Manual Journal Entry for Unresolved In Transit Balances

When the In Transit account does not clear and the variance cannot be resolved through normal JD Edwards processing, a manual journal entry is required. The appropriate offsetting account depends on the cause:

| Cause | Debit | Credit | Notes |
|---|---|---|---|
| OT cost does not match ST price (cost plus) | In Transit | COGS or Variance account | The price/cost mismatch created an unresolved balance |
| Branch cost variance with multiple variances | In Transit or PPV | In Transit or PPV | Net the two sides to determine the required entry |
| Goods lost or damaged in transit | Expense / Write-Off | In Transit | Removes the value from In Transit and expenses the loss |
| Cost change after shipment, before receipt | In Transit | Inventory Variance | Adjusts for the timing difference in the cost update |

> **Best Practice:** Document all manual journal entries with the ST and OT order numbers, the reason the variance occurred, and the period in which it was posted. Use RapidReconciler's In Transit reconciliation to confirm the balance clears after the entry is posted.

---

| DMAAI | Account | Transfer at Cost | Transfer at Cost Plus | Notes |
|---|---|---|---|---|
| **4220** | In Transit / COGS | **In Transit** (clearing) | COGS | At cost: debits In Transit at shipment |
| **4230** | Revenue | Clearing | **Revenue** | Cost plus only: records intercompany revenue |
| **4240** | Inventory | Inventory | Inventory | Credits inventory at shipping branch |
| **4245** | In Transit / A/R | **In Transit** (clearing) | **In Transit** | Cost plus: debits In Transit at price |
| **4310** | Inventory | Inventory | Inventory | Debits inventory at receiving branch |
| **4320** | RNV / In Transit | **In Transit** | **In Transit** | Credits In Transit at OT cost at receipt |
| **4335** | PPV | **In Transit** (Scenario 2) or **Expense** (Scenario 3) | **Expense** | Only one setting possible -- choose based on most common scenario |

---

## Section 9: Related Documentation

- [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md)
- [Accounting in Purchasing](../MDS/accounting-in-purchasing.md)
- [Sales Order Reference Guide](../MDS/sales_order_reference.md)
- [Stock Status and Trial Balance Reconciliation](../MDS/stock-status-trial-balance.md)
- [Item Ledger and Cardex Analysis Guide](../MDS/item-ledger-cardex-guide.md)