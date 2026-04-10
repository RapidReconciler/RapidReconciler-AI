# RapidReconciler Distribution AAI Reference

---

## AAI Table Usage by Document Type

### Manufacturing (31xx)

| Doc Type | Description | 3110 | 3130 | 3220 | 3240 | 3260 | 3270 | 3280 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| IC | Inventory Completion | | X | | | | | |
| IM | Material Issue | X | | | | | | |
| IV | Variance | | | X | X | X | X | X |

### Inventory Management (41xx)

| Doc Type | Description | 4122 | 4124 | 4126 | 4128 | 4134 | 4136 | 4141 | 4152 | 4154 | 4172 | 4174 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| IA | Inventory Adjustments | X | X | X | X | | | | | | | |
| IB | Item Cost Change | | | | | X | X | X | X | | | |
| IC | Inventory Completion | X | X | X | X | | | | | | | |
| II | Inventory Issue | X | X | X | X | | | | | | | |
| IK | Inventory Reclassifications | X | X | X | X | | | | | | | |
| IT | Inventory Transfers | X | X | X | X | | | | | X | | |
| PI | Physical Inventory Adjustment | | | | | X | X | | | | X | X |
| WD | Future Cost Update | | | | | X | X | | | | | X | X |

### Sales Order Processing (42xx)

| Doc Type | Description | 4220 | 4230 | 4240 | 4241 | 4245 | 4270 | 4280 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| CE | Credit Memo | X | X | X | X | X | X | X |
| CI | Interco Credit | X | X | X | | | | |
| CO | Return | X | X | X | X | X | X | X |
| CR | Customer Return | X | X | X | | X | X | |
| SA | Sample | X | X | X | | | | |
| SE | Export Sale | X | X | X | X | X | X | X |
| SI | Interco Sale | X | X | X | | | | |
| SO | Standard Order | X | X | X | X | X | X | X |
| ST | Whse Transfer Order | X | X | X | | X | | |

### Purchasing / Receiving / Voucher Match (43xx)

| Doc Type | Description | 4310 | 4320 | 4330 | 4332 | 4335 | 4337 | 4400 | 4405 | 4920 | 4921 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| OP | Purchase Order | X | X | X | X | X | X | X | X | X | X |
| OT | Transfer Order | X | X | | | X | X | X | X | X | |

---

## AAI Table Legend

### Manufacturing Accounting

| AAI | Description | Calculation |
|---|---|---|
| 3110 | Material Usage Backflushed against Work Orders | Actual Qty × Std Cost |
| 3130 | Finished Goods Produced on Work Orders | Actual Qty Completed × Std Cost |

### Variance Accounting

| AAI | Description | Calculation |
|---|---|---|
| 3220 | Labor Efficiency Variance to Standard | Actual Labor − Planned Labor × Std Rates |
| 3240 | Material Usage Variance to Standard | Actual Material − Planned Material × Std Cost |
| 3260 | Planning Variance | Current Cost vs. WO planned amounts (e.g. blend changes) |
| 3270 | Engineering Variance | Current BOM & Routing extended at Std Cost vs. Frozen Standard |
| 3280 | Other Variance | Qty Ordered @ Standard vs. Qty Completed @ Standard |

### Inventory Management

| AAI | Description | Calculation |
|---|---|---|
| 4122 | Dr/Cr to Inventory for Misc Issues/Transfers/Adjustments | Actual Qty × Standard Cost |
| 4124 | Dr/Cr to Expense for Misc Issues/Transfers/Adjustments | Actual Qty × Standard Cost |
| 4126 | Dr/Cr to Inventory to clear remaining value when Qty on Hand is Zero | Remaining Value |
| 4128 | Dr/Cr to Expense to clear remaining value when Qty on Hand is Zero | Remaining Value |
| 4134 | Dr/Cr to Inventory generated when standard cost is changed | Qty on Hand × (Old Std Cost − New Std Cost) |
| 4136 | Dr/Cr to Expense generated when standard cost is changed | Qty on Hand × (Old Std Cost − New Std Cost) |
| 4141 | Dr/Cr to Expense when Inv is transferred to B/P with different Std Cost | Qty Transferred × (Outbound Std Cost − Inbound Std Cost) |
| 4152 | Dr/Cr to Inventory for Physical Inventory Adjustment | Inv Adj Qty × Standard Cost |
| 4154 | Dr/Cr to Expense for Physical Inventory Adjustment | Inv Adj Qty × Standard Cost |
| 4172 | Dr/Cr to Inventory generated when standard cost is changed | Qty on Hand × (Old Std Cost − New Std Cost) |
| 4174 | Dr/Cr to Expense generated when standard cost is changed | Qty on Hand × (Old Std Cost − New Std Cost) |

### Sales Order Processing

| AAI | Description | Calculation |
|---|---|---|
| 4220 | Cost of Goods Sold | Qty Shipped × Standard Cost |
| 4230 | Revenue | Qty Shipped × Price |
| 4240 | Inventory | Qty Shipped × Standard Cost |
| 4241 | Inventory in Transit | Qty Shipped × Standard Cost |
| 4245 | Trade A/R | Qty Shipped × Price |
| 4270 | Price Adjustments | Qty Shipped × Price Adjustment |
| 4280 | Rebates | — |

### Purchasing / Receiving / Voucher Match

| AAI | Description | Calculation |
|---|---|---|
| 4310 | Inventory | Qty Received × Standard Cost |
| 4320 | Received Not Vouchered | Qty Received × PO Price |
| 4330 | Purchase Price Variance @ Voucher Match | Invoice Price vs. PO Price +/− Extra Charges |
| 4332 | Purchase Price Variance @ PO Receipt | Qty Received × (Std Cost (A1 cost type) − PO Price) |
| 4335 | Purchase Price Variance @ PO Receipt | Qty Received × (Std Cost − PO Price) |
| 4337 | Material Burden | Qty Received × (Std Cost (all other cost types) − PO Price) |
| 4400 | Dr/Cr to Inventory to clear remaining value when Receipt is reversed @ different Std Cost | Remaining Value |
| 4405 | Dr/Cr to Expense to clear remaining value when Receipt is reversed @ different Std Cost | Remaining Value |
| 4920 | Freight Payable | Qty Received × Freight Rate |
| 4921 | Freight Expense | Qty Received × Freight Rate |
