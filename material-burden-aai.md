**Reference Guide: Material Burden AAI (4337)**

**Section 1: Overview**

The Material Burden AAI (4337) is used in conjunction with inventory items that are valued at standard cost. It allows true additions to an item's cost - costs that should not be treated as a variance - to be rolled into the standard cost and frozen. This frozen cost is stored in table **F30026**.

If a variance exists in addition to the material burden, the Standard Cost Variance AAI (4335) is also invoked. The Material Burden AAI (4337) is called exclusively by the **receipts program (P4312)**. It is not invoked by the voucher match program (P4314).

Material burden provides a more accurate picture of the actual variance accrued against a standard cost item by separating true cost additions from standard cost variances.

**Section 2: Setup**

**2.1 Cost Program Requirements**

To use material burden, the following configuration must be in place:

- The **Sales/Inventory (CSMT) bucket** in the cost program (P4105) must be set to **7** (standard cost). A standard cost must exist to serve as the basis for the material burden calculation.
- The **Purchase Cost (PCSM) bucket** can be set to any valid value in UDC table **40/CM**.
- In UDC table **41/I**, the stocking type (STKT) must have a second description of **"P"** to indicate a purchased item. Material burden is intended for purchased items only.

**2.2 Cost Components, Rollup, and Freeze**

Cost component setup is accessed from menu **G3014** and involves the following programs:

| **Program** | **Purpose**                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **P30026**  | Cost Components - identifies the material cost (A1) and all burden components.                                                           |
| **P30820**  | Simulated Standard Rollup - calculates the total simulated cost by adding the A1 cost and the computed burden.                           |
| **P30835**  | Frozen Standard Update - takes the simulated cost and freezes it as the standard cost, replacing the 07 bucket in the cost file (F4105). |

**2.3 Material Burden Basis**

Material burden can be calculated using either of the following methods:

- **Factor and Rate** - The rate is defined in UDC table **30/CR** (accessed via F13 from P30026) and the factor is defined in UDC table **30/CF** (accessed via F21). The burden is calculated as: **Rate × Factor**.
- **Material Cost (A1) as Basis** - Enter **\*A1** in either the Rate (XSRC) or Factor (XSFC) field. The other field can contain a specific code or a percentage.

**Note:** If a percentage is added to UDC tables 30/CF or 30/CR, those rates will override any manual entry in the amount field.

Alternatively, a value can be placed directly in the **Net Added field (XSMC)**, which is then added to the material cost to produce the frozen cost.

**Example:**

| **Cost Type** | **Simulated Cost Net Added** | **Total** | **Factor Code or Amount** | **Rate Code or Amount** |
| ------------- | ---------------------------- | --------- | ------------------------- | ----------------------- |
| A1            | \$100                        | \$100     | -                         | -                       |
| X1            | \$25                         | \$125     | \*A1                      | .25                     |

If the A1 cost is \$100 and the percentage is 0.25, the material burden is **\$25** and the frozen standard cost is **\$125**, stored in F30026.

**Section 3: Calculation of Material Burden**

The standard cost produced by the rollup and freeze process is stored in table **F30026**.

Material burden is calculated as follows:

**Material Burden = F30026 Cost − A1 Cost**

Material burden will **always** result in a **credit** to the account configured in AAI 4337.

**Section 4: Functionality**

**4.1 How Material Burden Is Invoked**

Material burden is triggered by the receipts program **P4312** when a purchase order is received for an item that has cost components configured. There are no processing options in either purchase order entry (P4311) or the receipts program (P4312) related to material burden.

Any cost component that is not the A1 cost is considered material burden. The purchase order cost can be sourced from any valid cost bucket. Standard cost is generally not used as the purchasing cost when invoking material burden.

**4.2 Compatibility Notes**

- **Receipt Routing** - Material burden is fully functional with receipt routing.
- **Landed Costs** - Landed costs cannot be added at the time of receipt when using material burden. If landed costs are included in the receipt, all variance will be booked to the Standard Cost Variance AAI (4335). If both material burden and landed costs are required, use the standalone landed cost program **P43214** to apply landed costs separately. This allows both processes to function correctly.
- **Manufactured Items** - Material burden is intended for purchased items only (stocking type "P"). If a manufactured item (stocking type "M") is used with material burden, no A1 cost will be captured in the rollup and freeze programs, leaving only the material burden amount - which is not the intended behavior.

**Section 5: Journal Entry Scenarios**

There are three scenarios that produce different journal entries when using material burden, based on the relationship between the purchasing cost and the A1 cost.

**5.1 Scenario 1 - Purchasing Cost Equals A1 Cost**

| **Setup Values** |       |
| ---------------- | ----- |
| Purchase Cost    | \$100 |
| A1 Cost          | \$100 |
| F30026 Cost      | \$125 |

AAIs invoked: 4310, 4320, 4337

| **Account**            | **Debit** | **Credit** | **AAI** |
| ---------------------- | --------- | ---------- | ------- |
| Inventory              | \$125     |            | 4310    |
| Material Burden        |           | \$25       | 4337    |
| Received Not Vouchered |           | \$100      | 4320    |

Inventory is debited at the full frozen standard cost (\$125). Material burden is credited for the burden portion (\$125 − \$100 = \$25). RNV is credited for the purchase cost (\$100). No standard cost variance is generated.

**5.2 Scenario 2 - Purchasing Cost Greater Than A1 Cost**

| **Setup Values** |       |
| ---------------- | ----- |
| Purchase Cost    | \$105 |
| A1 Cost          | \$100 |
| F30026 Cost      | \$125 |

AAIs invoked: 4310, 4320, 4335, 4337

| **Account**            | **Debit** | **Credit** | **AAI** |
| ---------------------- | --------- | ---------- | ------- |
| Inventory              | \$125     |            | 4310    |
| Standard Cost Variance | \$5       |            | 4335    |
| Material Burden        |           | \$25       | 4337    |
| Received Not Vouchered |           | \$105      | 4320    |

Inventory is debited at the frozen standard cost (\$125). The \$5 excess of the purchase cost over the A1 cost is posted to the Standard Cost Variance account. Material burden captures the \$25 burden component. RNV is credited for the full purchase cost (\$105).

**5.3 Scenario 3 - Purchasing Cost Less Than A1 Cost**

| **Setup Values** |       |
| ---------------- | ----- |
| Purchase Cost    | \$95  |
| A1 Cost          | \$100 |
| F30026 Cost      | \$125 |

AAIs invoked: 4310, 4320, 4335, 4337

| **Account**            | **Debit** | **Credit** | **AAI** |
| ---------------------- | --------- | ---------- | ------- |
| Inventory              | \$125     |            | 4310    |
| Standard Cost Variance |           | \$5        | 4335    |
| Material Burden        |           | \$25       | 4337    |
| Received Not Vouchered |           | \$95       | 4320    |

Inventory is debited at the frozen standard cost (\$125). The \$5 favorable variance (A1 cost exceeds purchase cost) is credited to the Standard Cost Variance account. Material burden captures the \$25 burden component. RNV is credited for the actual purchase cost (\$95).

**Section 6: Helpful Hints Summary**

| **Topic**              | **Guidance**                                                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Landed Costs**       | Do not apply landed costs at the time of receipt when using material burden. Use standalone program P43214 instead.           |
| **Manufactured Items** | Material burden is for purchased items only (stocking type "P"). Do not use with manufactured items (stocking type "M").      |
| **Receipt Routing**    | Material burden is fully compatible with receipt routing.                                                                     |
| **UDC Rate Overrides** | Percentage rates in UDC tables 30/CF and 30/CR override manual entries in the amount field.                                   |
| **Net Added Field**    | A value entered in the Net Added field (XSMC) can be used instead of factor/rate calculations to determine the burden amount. |
