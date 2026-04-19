# JD Edwards Purchase Order Reference Guide

## Tax, Landed Costs, and Receipts Routing

---

## Overview

This reference guide covers three key areas of JD Edwards Purchase Order Management. Each section is self-contained and can be referenced independently.

| Section | Topic |
|---|---|
| **Section 1** | Tax in Procurement -- Setup, explanation codes, AAIs, and GL treatment by tax type |
| **Section 2** | Landed Costs -- Setup, application, journal entries, and F43121 records |
| **Section 3** | Receipts Routing -- Overview, routing operations, setup, and accounting |

---

## Section 1: Tax in Procurement

### 1.1 Tax Terms

| Term | Definition |
|---|---|
| **Sales Tax** | A tax paid to the supplier along with the cost of goods or services. The supplier collects and remits it to the taxing authority. |
| **Use Tax** | A self-assessed tax on goods or services paid directly to the taxing authority by the buyer. |
| **VAT (Value Added Tax)** | A tax paid to the supplier that is subsequently recoverable by the buyer from the taxing authority. |
| **GST (Goods and Services Tax)** | A Canadian Federal Government tax. GST is a recoverable VAT tax. |
| **PST (Provincial Sales Tax)** | A Canadian provincial tax applied to goods or services. PST can be payable to either the supplier (acts as sales tax) or directly to the taxing authority (acts as use tax). |

### 1.2 Tax Setup

Tax setup is performed on menu **G0021** and includes:

- Tax Authorities
- Tax Rate/Areas
- Tax Explanation Codes
- Tax Rules by Company

All taxing authorities should be set up as regular Address Book records.

### 1.3 Tax Rate/Area

| Field | Description |
|---|---|
| **Effective Date** | Blank defaults to the current date |
| **Expiration Date** | If tax rates are indefinite, extend as far as possible. Once established, the expiration date cannot be changed. |
| **Item Number** | A Tax Rate/Area can be applied to a group of items or a single item |
| **Maximum Unit Cost** | The maximum amount an item can be taxed |
| **Address** | Address Book number for each taxing authority. Up to five authorities per Tax Rate/Area. |
| **GL Offset** | The GL Class code used by tax AAIs (4350 and 4355). For procurement, the GL Offset comes from the Purchase Order Detail (F4311), not from the Tax Rate/Area. |
| **Compound Tax** | Controls GST/PST calculation. Checked = PST calculated on item cost plus GST (tax-on-tax). Unchecked = PST calculated on item cost only. |
| **VAT Expense** | Percentage of VAT not eligible for input credits. Checked = not recoverable (expense). Unchecked = recoverable (receivable, default). |

**Compound Tax Calculation Example (GST = 4%, PST = 6%):**

| | Compound Tax Checked | Compound Tax Unchecked |
|---|---|---|
| Item | $100.00 | $100.00 |
| GST | $4.00 | $4.00 |
| PST | $6.24 ($104 × 6%) | $6.00 ($100 × 6%) |
| **Total** | **$110.24** | **$110.00** |

### 1.4 Tax Explanation Codes (UDC 00/EX)

| Code | Description |
|---|---|
| **S** | Sales Tax -- seller-assessed |
| **U** | Use Tax -- self-assessed by buyer |
| **V** | VAT Tax -- seller-assessed and recoverable |
| **C** | GST/PST with PST paid to supplier |
| **B** | GST/PST with PST accrued and paid directly to taxing authority |
| **E** | Tax Exempt |

### 1.5 Tax Rules by Company

Access Tax Rules by Company for Procurement with **System = 2**.

| Field | Description |
|---|---|
| **Calculate Tax on Gross (Including Discount)** | Choose to calculate tax on gross including or excluding discount |
| **Calculate Discount on Gross (Including Tax)** | Check to calculate discount on item cost plus tax |

### 1.6 Default Tax Codes and Rates

Default tax information (Tax Explanation Code and Tax Rate/Area) is specified in **Supplier Master Information (P04012)**. These defaults populate the Purchase Order Entry screen and can be overridden at order entry.

> **Important:** If tax information is not entered during purchase order entry, taxes will not be accrued at PO Receipt. Tax codes can be entered at Voucher Match, and the resulting journal entries will resemble those for a 2-way match.

**Processing option #7 on the Defaults tab of Purchase Order Entry (P4310):**

| Setting | Behavior |
|---|---|
| **1** | Defaults Tax Explanation Code and Tax Rate/Area from the Supplier Master of the Ship-To Address Book |
| **Blank** | Defaults Tax Explanation Code and Tax Rate/Area from the Supplier Master of the Supplier Address Book |

> **Note:** PO Receipts (P4312) and Voucher Match (P4314) have no processing options specific to taxes.

### 1.7 Tax AAIs

| AAI | Account | Description |
|---|---|---|
| **4310** | Inventory | Directs the procurement application to the Inventory GL account |
| **4320** | Received Not Vouchered (RNV) | Directs to the temporary liability GL account |
| **4350** | Tax Expense | Directs to the Tax Expense GL account |
| **4355** | RNV Tax (Temporary Tax Liability) | Directs to the temporary tax liability GL account |
| **PT** | Tax-Related A/P | Financial AAI for tax-related accounts payable entries |
| **PC** | AP Trade | Financial AAI for trade accounts payable entries |

> **Note:** In a 2-way match, the temporary liability AAIs 4320 and 4355 are not used.
> **Note:** All entries marked with \* in the journal entry tables below are made by the GL Post program (R09801).

### 1.8 GL Treatment by Tax Code

The accounting treatment varies based on three factors:
- Tax Explanation Code
- Inventory vs. Non-Inventory line (Inventory = line type with inventory interface "Y"; Non-Inventory = "N" or "A")
- Two-way match vs. three-way match

---

#### Tax Code "S" -- Simple Sales Tax

Tax is remitted to the supplier with the cost of goods.

**Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| 4310 -- Inventory | Item | |
| 4350 -- Tax Expense | Tax | |
| 4320 -- RNV | | Item |
| 4355 -- RNV Tax | | Tax |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| 4355 -- RNV Tax | Tax | |
| PC -- AP Trade \* | | Item + Tax |

**Non-Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item + Tax | |
| 4320 -- RNV | | Item |
| 4355 -- RNV Tax | | Tax |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| 4355 -- RNV Tax | Tax | |
| PC -- AP Trade \* | | Item + Tax |

**Non-Inventory -- 2-Way Match**

Receive and Voucher (P4314):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item + Tax | |
| PC -- AP Trade \* | | Item + Tax |

---

#### Tax Code "U" -- Use Tax

The buyer calculates, accrues, and remits the tax amount directly to the taxing authority.

**Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| 4310 -- Inventory | Item | |
| 4350 -- Tax Expense | Tax | |
| 4320 -- RNV | | Item |
| 4355 -- RNV Tax | | Tax |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| 4355 -- RNV Tax | Tax | |
| PC -- AP Trade \* | | Item |
| PT AAI \*@ | | Tax |

**Non-Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item + Tax | |
| 4320 -- RNV | | Item |
| 4355 -- RNV Tax | | Tax |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| 4355 -- RNV Tax | Tax | |
| PC -- AP Trade \* | | Item |
| PT AAI \*@ | | Tax |

**Non-Inventory -- 2-Way Match**

Receive and Voucher (P4314):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item + Tax | |
| PC -- AP Trade \* | | Item |
| PT AAI \*@ | | Tax |

> **@ PT AAI Logic for Use Tax:** The system first looks for AAI PT\_\_\_\_ (literal blank) to find the cost center and object account. It then looks for an account whose cost center, object, and subsidiary name match the Tax Rate/Area name. If a subsidiary account is not found, only the cost center and object are used. The GL Offset in the Tax Rate/Area is ignored.

---

#### Tax Code "V" -- Value Added Tax

The buyer pays tax to the supplier that is later recoverable from the taxing authority.

**Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| 4310 -- Inventory | Item | |
| 4320 -- RNV | | Item |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| VAT Recoverable \*@ | Tax | |
| PC -- AP Trade \* | | Item + Tax |

**Non-Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item | |
| 4320 -- RNV | | Item |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| VAT Recoverable \*@ | Tax | |
| PC -- AP Trade \* | | Item + Tax |

**Non-Inventory -- 2-Way Match**

Receive and Voucher (P4314):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item | |
| VAT Recoverable \*@ | Tax | |
| PC -- AP Trade \* | | Item + Tax |

> **@ VAT Recoverable AAI Logic:** The system looks up the GL Offset from the Tax Rate/Area and searches for an AAI of PT followed by the GL Offset (e.g., PTTXTX).

---

#### Tax Code "C" -- GST/PST with PST Paid to Supplier

Used in Canada. PST behaves like "S" (seller-assessed); GST behaves like "V" (recoverable VAT).

**Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| 4310 -- Inventory | Item | |
| 4350 -- Tax Expense | PST Tax | |
| 4320 -- RNV | | Item |
| 4355 -- RNV Tax | | PST Tax |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| 4355 -- RNV Tax | PST Tax | |
| VAT Recoverable \*@ | GST Tax | |
| PC -- AP Trade \* | | Item + PST + GST |

**Non-Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item + PST | |
| 4320 -- RNV | | Item |
| 4355 -- RNV Tax | | PST Tax |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| 4355 -- RNV Tax | PST Tax | |
| VAT Recoverable \*@ | GST Tax | |
| PC -- AP Trade \* | | Item + PST + GST |

**Non-Inventory -- 2-Way Match**

Receive and Voucher (P4314):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item + PST | |
| VAT Recoverable \*@ | GST Tax | |
| PC -- AP Trade \* | | Item + PST + GST |

> **@ VAT Recoverable AAI Logic:** The system uses the GL Offset from the first line of the Tax Rate/Area table and looks for an AAI of PT followed by the GL Offset (e.g., PTTXTX).

---

#### Tax Code "B" -- GST/PST with PST Withheld

Used in Canada. GST is paid to the supplier; PST is withheld and paid directly to the Provincial tax authority. PST behaves like "U" (self-assessed use tax).

**Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| 4310 -- Inventory | Item | |
| 4350 -- Tax Expense | PST Tax | |
| 4320 -- RNV | | Item |
| 4355 -- RNV Tax | | PST Tax |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| 4355 -- RNV Tax | PST Tax | |
| VAT Recoverable \*@ | GST Tax | |
| Tax Payable \*# | | PST Tax |
| PC -- AP Trade \* | | Item + GST |

**Non-Inventory -- 3-Way Match**

PO Receipt (P4312):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item + PST Tax | |
| 4320 -- RNV | | Item |
| 4355 -- RNV Tax | | PST Tax |

Voucher Match (P4314):

| Entry | Debit | Credit |
|---|---|---|
| 4320 -- RNV | Item | |
| 4355 -- RNV Tax | PST Tax | |
| VAT Recoverable \*@ | GST Tax | |
| Tax Payable \*# | | PST Tax |
| PC -- AP Trade \* | | Item + GST |

**Non-Inventory -- 2-Way Match**

Receive and Voucher (P4314):

| Entry | Debit | Credit |
|---|---|---|
| Account entered on PO | Item + PST Tax | |
| VAT Recoverable \*@ | GST Tax | |
| Tax Payable \*# | | PST Tax |
| PC -- AP Trade \* | | Item + GST |

> **@ VAT Recoverable AAI Logic:** The system uses the GL Offset from the first line of the Tax Rate/Area table and uses the financial AAI of PT followed by the GL Offset (e.g., PTTXTX).

> **\# Tax Payable AAI Logic for PST:** The system first looks for AAI PT\_\_\_\_ (literal blank) to find the cost center and object account. It then looks for an account whose cost center, object, and subsidiary name match the Tax Rate/Area name. If a subsidiary account is not found, only the cost center and object are used. The GL Offset in the Tax Rate/Area is ignored.

---

## Section 2: Landed Costs

### 2.1 Overview

Landed costs are additional fees automatically added to an item's cost to account for expected charges associated with delivery or handling. Common examples include:

- Harbor Fees
- Brokerage Fees
- Commissions
- Import Duties

**Key Rules:**
- Landed costs are costs that **exceed** the purchase price of an item
- Landed costs are applied to an **individual item line** -- they cannot be applied to the total cost of a purchase order
- Landed costs are **not taxable**

### 2.2 Setup

#### Required UDC Tables

| UDC Table | Purpose |
|---|---|
| **41/P5** | All Landed Cost Rules must exist here before they can be used |
| **40/CA** | Defines the Landed Cost Level used to calculate additional fees |
| **41/9** | All GL class codes used for landed costs must be included here |

#### Assignment Methods

Landed costs may be assigned by a **specific Item and Branch/Plant combination** or by a **Cost Rule** -- a named group of landed costs reusable across items and suppliers.

A Cost Rule can be assigned to:
- An inventory item (Item Branch/Plant Category Codes -- P41026)
- A supplier (Supplier Master, Purchasing1 tab -- P04012)
- A purchase order header (Additional Information form exit in P4310)
- A purchase order detail line (Additional Information in P4310)
- A processing option in Purchase Order Entry (P4310)

#### Calculation Methods

| Method | Description | Example |
|---|---|---|
| **Percentage of unit price** | Entered as a whole number (e.g., 5% entered as 5.00). Calculated as % × quantity × unit cost. | 5% of a PO line with 10 units at $10.00 = $5.00 |
| **Fixed dollar amount** | A flat fee applied per unit | -- |
| **Rate × weight or volume** | Rate entered as a whole number per unit of weight or volume | $4.50/lb for a 10 lb item with quantity 1 = $45.00 |

#### Landed Cost Level and Basis

All landed costs must be assigned a **Landed Cost Level** from UDC 40/CA. The **Based on Level** field controls what the landed cost is calculated against -- the purchase order line only, or the purchase order line plus a previously applied landed cost level (cumulative).

#### GL Class Code

The GL Class determines how landed costs are routed to the GL via AAIs 4385 and 4390. Different GL classes direct landed costs to different accounts.

**Examples:**
- LC21 → Harbor Fees
- LC24 → Brokerage Fees

> **Note:** If the GL class is left blank in Landed Cost Revisions, the system retrieves the GL class from the Item Location record.

#### Landed Cost Configuration Options

| Field | Description |
|---|---|
| **Effective Dates** | Limits the landed cost to a specific date range |
| **Supplier** | The landed cost can be paid to a different supplier than the one on the PO |
| **Voucher (Y/N)** | Y = eligible for voucher match (PRLAND = 2); N = accrual only (PRLAND = 3) |
| **Include in Cost (Y/N)** | Y = updates Average Cost and Last-In buckets (UDC 40/AV applies); N = does not update any inventory cost bucket |

> **Note:** The purchasing bucket (08) and standard cost bucket (07) are never updated by landed cost.

### 2.3 Cost Rule Hierarchy

When more than one landed cost assignment exists, the system applies the following priority (highest to lowest):

1. Cost Rule -- Item Branch/Plant combination (P41291)
2. Purchase Order Header -- Additional Information
3. Processing option behind Purchase Order Entry P4310
4. Purchasing Instructions from the Ship To address
5. Landed Cost category code in the Item Branch/Plant Category Codes (P41026)

### 2.4 Applying Landed Costs

Landed costs are applied and calculated using **Landed Cost Revisions (P41291)**, invoked at three points:

| Point | Program |
|---|---|
| **At Receipt** | Purchase Order Receipts (P4312) |
| **At Voucher Match** | Voucher Match to Open Receipt (P4314), called from P0411 |
| **Stand-Alone** | Stand Alone Landed Cost (P43214) -- used between receipt and voucher match |

**Processing option #6 on the Process tab of P4312:**

| Setting | Behavior |
|---|---|
| **1** | Form W43291A displays after the receipt. Enter option 1 to include the landed cost. Click OK to create journal entries and F43121 records; Cancel to exit without applying. |
| **2** | Blind Landed Cost -- applied and calculated automatically without displaying the form |
| **Blank** | No landed cost applied |

> **Note:** If a purchase order receipt is reversed, any landed costs applied -- including journal entries, F43121 records, and cardex records -- will also be reversed.

> **Note:** Landed costs cannot be reversed through the Stand Alone program (P43214: ZJDE0003). Reversal is possible only if the purchase order itself is reversed using Open Receipts by Supplier (P43214: ZJDE0001).

### 2.5 Landed Cost Journal Entries

**Setup for examples:** Landed Cost Rule = 10% of cost; Include in Cost = Y; Purchase Order = $100.

**Positive On-Hand Quantity:**

| Account | Debit | Credit | AAI |
|---|---|---|---|
| Inventory | $100 | | 4310 |
| RNV | | $100 | 4320 |
| Cost/Expense (landed cost) | $10 | | 4385 |
| Cost/Liability (landed cost) | | $10 | 4390 |

**Negative On-Hand Quantity:**

If the on-hand quantity is negative, the landed cost expense is split between AAI 4385 and AAI 4332. The cardex record and AAI 4385 are created only for the portion applicable to the quantity on hand.

**Example:** On-hand = -50; PO quantity = 100; PO cost = $100.

| Account | Debit | Credit | AAI |
|---|---|---|---|
| Inventory | $100 | | 4310 |
| RNV | | $100 | 4320 |
| Cost of Sales | $5 | | 4332 |
| Cost/Expense (landed cost) | $5 | | 4385 |
| Cost/Liability (landed cost) | | $10 | 4390 |

> **Note:** Landed costs will not update the cardex (F4111) if the standard cost (07) rule is used for inventory.

### 2.6 Landed Cost F43121 Records

The **PRLAND** field in the F43121 table is the key indicator for landed cost records:

| PRLAND Value | Meaning |
|---|---|
| **Blank** | Not related to landed cost |
| **1** | Product/item line |
| **2** | Landed cost eligible for voucher match |
| **3** | Landed cost for accrual only -- not eligible for voucher match |

The **PRLVLA** field stores the Landed Cost Level -- a three-character value from UDC 40/CA identifying the specific landed cost applied.

### 2.7 Multi-Currency Landed Costs

Landed costs support multi-currency processing. A purchase order can be in one currency while landed costs are in different currencies. When multi-currency is enabled:

- The currency field within the landed cost record becomes active
- The currency defaults from the Supplier Master and **cannot be overridden**
- Exchange rate variances for landed costs are tracked using **AAI 4340**

---

## Section 3: Receipts Routing

### 3.1 Overview

Receipts Routing in JD Edwards allows organizations to track inventory through a series of inspection and handling steps between the time goods are received from a supplier and when they are placed into usable stock. Rather than immediately crediting inventory upon receipt, goods can be held in intermediate routing operations until quality checks and other processing requirements are satisfied.

Receipts routing is commonly used for:

- Incoming quality inspection
- Quarantine periods for regulated goods
- In-transit tracking for intercompany transfer orders (ST/OT)
- Staged receipt processing where goods must pass through multiple handling steps

### 3.2 How Receipts Routing Works

When a purchase order is received, instead of immediately posting to inventory, the goods are placed into a **routing operation**. Each routing operation represents a physical stage in the receiving process. The goods progress through the routing steps until they reach the final operation, at which point they are moved into usable stock.

**Standard routing stages:**

| Stage | Description |
|---|---|
| **INSPE (Inspection)** | Goods are held for quality inspection before being released to stock |
| **TRAN (In Transit)** | Goods are in transit and have not yet been physically received into stock -- commonly used for ST/OT transfer orders |
| **STK (Stock)** | Goods have been physically received and entered into usable inventory |

At each routing stage, JD Edwards tracks the quantity and value in the routing operation. The goods are not available for use until they reach the stock stage.

### 3.3 Setup Requirements

**UDC Table 43/RC -- Routing Operations**

All routing operations must be defined in UDC table **43/RC** before they can be used. Each operation code represents a stage in the routing process.

**Order Activity Rules (P40204)**

Order Activity Rules must be configured for the applicable order type and line type to support routing operations. The rules define which status codes are valid for each stage of the routing process.

**Receipt Routing Definition (P43091)**

The routing definition program (P43091) is used to define the sequence of routing operations for a given item or item group. The definition specifies:

- The order in which routing operations are performed
- Whether goods at a routing stage are available for use
- Whether the goods are included in on-hand quantity at each stage

**Processing Options**

Processing option #3 on the Process tab of Purchase Order Receipts (P4312) controls whether routing is activated at receipt. When set, goods received against purchase orders with routing assigned will be placed into the first routing operation rather than directly into stock.

### 3.4 Routing Operation Status

Goods at each routing stage carry a status that determines their availability:

| Status | Description |
|---|---|
| **In Routing** | Goods are at a routing operation and not yet in usable stock |
| **Available** | Goods have passed all routing operations and are in usable stock |
| **Rejected** | Goods failed inspection and are flagged for return or disposition |

### 3.5 Moving Goods Through Routing Operations

The **Movement and Disposition program (P43250)** is used to move goods from one routing operation to the next. At each movement:

- The quantity is transferred from the current routing operation to the next
- Journal entries are created based on the configured routing AAIs (4365/4370)
- The F43121 record is updated to reflect the current routing stage

When goods are moved to the final stock operation, inventory is fully credited and the goods become available for use.

### 3.6 Receipts Routing Journal Entries

Receipts routing uses two additional AAIs for journal entries at routing operations:

| AAI | Account | Usage |
|---|---|---|
| **4365** | Prior to Receipt/Completion Liability | Liability account for goods at a routing operation |
| **4370** | Routing Operation | Asset account tracking goods through routing stages |
| **4375** | Expense | Debits expense account for items dispositioned off during receipt routing |

**At initial receipt into routing:**

| Entry | Debit | Credit | AAI |
|---|---|---|---|
| Routing Operation | x | | 4370 |
| RNV / In Transit | | x | 4320 |

**At movement to stock:**

| Entry | Debit | Credit | AAI |
|---|---|---|---|
| Inventory | x | | 4310 |
| Routing Operation | | x | 4370 |

**At disposition (rejection/write-off):**

| Entry | Debit | Credit | AAI |
|---|---|---|---|
| Expense | x | | 4375 |
| Routing Operation | | x | 4370 |

### 3.7 Receipts Routing and Landed Costs

Landed costs are fully compatible with receipts routing. However, there is one important restriction: **landed costs cannot be applied at the time of receipt when material burden is also in use**. If both are required, use the standalone landed cost program (P43214) to apply landed costs separately after receipt.

### 3.8 Receipts Routing for ST/OT Transfer Orders

Receipts routing is frequently used to track inventory in transit between branch plants on ST/OT transfer orders. The TRAN routing operation holds goods between the time the ST order is ship confirmed and the time the OT is received at the destination branch.

**Key considerations for ST/OT routing:**

- The TRAN routing stage keeps goods visible as in-transit inventory without crediting the receiving branch's on-hand balance
- Goods at the TRAN stage are excluded from the receiving branch's perpetual inventory but remain tracked in the routing operation
- RapidReconciler provides an alternative to receipts routing for in-transit tracking -- see the [Transfer Order Reference Guide](../MDS/transfer_order_reference.md) for details

### 3.9 Receipts Routing Best Practices

| Practice | Recommendation |
|---|---|
| **Define operations clearly** | Keep routing operations simple and purposeful -- complex routing with many stages increases administrative burden |
| **Train receiving staff** | Ensure receiving staff understand how to move goods through routing operations correctly -- goods left in a routing stage create reconciliation issues |
| **Monitor routing inventory** | Regularly review goods at routing stages to identify items that have been stuck in a routing operation longer than expected |
| **Configure AAIs carefully** | Ensure AAIs 4365 and 4370 point to appropriate accounts -- goods at routing stages must be distinguishable from fully received inventory in the GL |
| **Consider the RapidReconciler alternative** | For ST/OT in-transit tracking specifically, RapidReconciler's As-Of tracking provides the same visibility without requiring receipts routing configuration |

---

## Section 4: Related Documentation

- [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md)
- [Accounting in Purchasing](../MDS/accounting-in-purchasing.md)
- [Sales Order Reference Guide](../MDS/sales_order_reference.md)
- [Transfer Order Reference Guide](../MDS/transfer_order_reference.md)
- [Product Costing Reference Guide](../MDS/product-costing-reference.md)
- [Zero Balance Adjustments](../MDS/zero-balance-adjustments.md)
