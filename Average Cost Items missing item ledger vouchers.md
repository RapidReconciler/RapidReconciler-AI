# Average Cost Items missing item ledger vouchers

In JD Edwards, I am not seeing voucher entries in the item ledger for average cost items. What setup issues could I be having?

In JD Edwards (EnterpriseOne), **voucher (AP) entries not appearing in the Item Ledger (F4111)** for **Average Cost items** is almost always a **setup or process alignment issue** between Inventory, Purchasing, and AP. Below is a structured checklist of the most common causes, starting with the most likely.

**1\. Inventory Interface (A/P → Inventory) Is Disabled or Misconfigured**

Voucher lines only write to the Item Ledger when the **Inventory Interface** is active.

**What to check**

**Inventory Constants (P41001)**

- _G/L Interface_ = **Y**
- _A/P Interface_ = **Y**
- _Cost Update_ = **Y** (required for avg cost updates)
- _Interface Mode_ = usually **2 or 3**

If **A/P Interface = N**, vouchers will post to G/L but **not update F4111 or average cost**.

**2\. Item Cost Method Is Not Truly Average Cost**

The system only writes voucher cost adjustments to F4111 if the **primary cost method is average cost**.

**What to check**

**Item Cost Revisions (P4105)**

- Primary cost method = **02 (Average Cost)**
- Cost level is correct (Item / Item-Branch / Lot)

Also confirm:

- No other cost method (e.g., 07, 09) is overriding costing
- Item Branch (P41026) is not set to a different cost method

**3\. Receipt Routing or Match Type Prevents Cost Flow**

Voucher cost entries only flow to inventory if the **voucher is matched correctly**.

**Common problem scenarios**

- **3-way match (OP)** but receipt not completed
- Voucher created as **non-stock** or **no receipt**
- Voucher entered manually instead of via **Voucher Match (P4314)**

**What to check**

**PO Detail Line (P4310)**

- Line Type = **S** (stock)
- Match Type = **2 or 3** (Receipt Required)

**Receipt Routing (P43250)**

- Receipt actually completed to inventory (not just dock or inspection)

**4\. Line Type Is Not Inventory Affecting**

If the PO line type does not interface with inventory, no item ledger record will be created.

**What to check**

**Line Type Constants (P40205)**

- Inventory Interface = **Y**
- A/P Interface = **Y**
- G/L Interface = **Y**

Common issue: using **line type N or J** instead of **S**.

**5\. Cost Is Not Changing at Voucher Time**

For average cost items, JD Edwards only writes a voucher-related F4111 record if the **voucher cost differs from receipt cost**.

**What this means**

- If voucher unit cost = receipt unit cost → **no new F4111 entry**
- If voucher cost ≠ receipt cost → **F4111 record with doc type PV**

This is normal behavior and often misunderstood.

👉 Check if:

- Price variance actually exists
- Quantity vouchered = quantity received

**6\. Expense Distribution Is Bypassing Inventory**

If the voucher is expensed directly, inventory will not be updated.

**What to check**

**AAIs**

- 4310 / 4320 → Inventory
- 4330 → Received Not Vouchered
- 4350 → AP Trade

If AAIs point to an **expense account instead of inventory**, the item ledger will not update.

**7\. Post Program Not Updating Inventory**

If vouchers are entered but **not posted correctly**, item ledger records will not appear.

**What to check**

- Voucher is **Posted**
- AP Post (R09801) completed without errors
- No errors in **Work Center**

**8\. Branch/Plant or Item Ledger Security Filtering**

Sometimes entries exist but are not visible.

**What to check**

- Branch/Plant security
- Item Ledger (P4111) processing options
- Data selection filters (doc type PV, IM, OV)

**9\. Average Cost Freeze or Future Cost Dates**

Average cost updates are suppressed if:

- Cost is frozen
- Effective dates are future-dated

**What to check**

**Item Cost Revisions**

- No freeze flag
- Cost effective date ≤ voucher G/L date

**Quick Diagnostic Test (Highly Recommended)**

- Receive a PO for an avg cost item at **\$10**
- Voucher it at **\$12**
- Post the voucher
- Review **F4111**:
  - You should see a **PV document** adjusting inventory value
  - Average cost should increase

If this does not occur → focus on **Inventory Constants + Line Type + Match Type**.

If you want, tell me:

- E1 version (e.g., 9.2)
- Match type (2-way vs 3-way)
- Line type used
- Whether vouchers are entered via P4314 or P0411

…and I can pinpoint the exact setup causing it.

Top of Form

Bottom of Form