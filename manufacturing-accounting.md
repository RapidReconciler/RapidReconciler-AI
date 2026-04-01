**JD Edwards Manufacturing**

**Training Guide: Introduction to Manufacturing Accounting**

**Setup, Execution, and Best Practices**

**Section 1: The Importance of Manufacturing Accounting**

**1.1 Why It Matters**

Survival in an increasingly competitive global market requires a thorough understanding of a company's cost structure. Without it, organizations cannot identify where improvements can be made or accurately measure the profitability of individual products.

When properly implemented, JD Edwards Manufacturing Accounting provides the ability to:

- Measure expected cost versus actual cost by activity.
- Differentiate cost by individual product number rather than averaging across product lines.
- Identify areas requiring cost improvement and determine how to achieve them.
- Accurately measure the results of cost-reduction efforts.

**1.2 Common Implementation Challenges**

Despite its value, Manufacturing Accounting is frequently underimplemented. Common reasons include:

- The high degree of flexibility in JD Edwards can overwhelm cost accountants.
- Upper management may not recognize its importance and therefore does not allocate sufficient attention or resources.
- Organizations migrating from less sophisticated systems may not have personnel with the required skill set in place.

The module is complex and time-consuming to configure correctly, but the results justify the investment. After implementing general accounting functions, the efficiencies gained should free up staff who can then be directed toward Manufacturing Accounting.

**1.3 Applicability Across Industries**

JD Edwards Manufacturing Accounting is suitable for a wide variety of manufacturing environments, including:

- Make to stock
- Make to order (including configured products)
- Engineer to order
- Repetitive manufacturing
- Process manufacturing

Industries successfully using the module include aerospace and defense, food, pharmaceuticals, automotive, semiconductors, and consumer products, among others.

**Section 2: Manufacturing Cost Flows**

Manufacturing costs flow through the following balance sheet and income statement accounts:

| **Stage**                                                      | **Account Type**                                  |
| -------------------------------------------------------------- | ------------------------------------------------- |
| **Material Purchases / Direct Labor / Manufacturing Overhead** | Cost inputs                                       |
| **Raw Material Inventory**                                     | Balance sheet - raw materials on hand             |
| **Work in Progress (WIP)**                                     | Balance sheet - costs of items being manufactured |
| **Finished Goods**                                             | Balance sheet - completed items awaiting sale     |
| **Cost of Goods Sold (COGS)**                                  | Income statement - cost of items sold             |
| **Selling and Administrative**                                 | Income statement - period expenses                |

**Section 3: Detailed Transaction Example - Manufacturing a Work Order**

This section walks through each transaction type in the manufacturing accounting cycle using the example of a work order for four hammers.

**Note:** General ledger transactions are not generated until the Manufacturing Journal Entries Program (R31802) is run in final mode for the work order.

**3.1 Material Issues - Document Type IM**

When material is issued to a work order, the value of the material is transferred from the Raw Material Inventory account to the Work in Process account at **Standard Cost × Actual Quantity**.

| **AAI**  | **Account**            | **Entry** |
| -------- | ---------------------- | --------- |
| **3110** | Raw Material Inventory | Credit    |
| **3120** | Work In Process        | Debit     |

**Example:** Material value for four hammers = **\$100** (A1 cost type). Depending on the company's setup, cost types B1-B4, C1-C4, D1-D2, and extras may also be moved.

**3.2 Labor and Overhead - Document Type IH**

Labor and overhead accruals are transferred to WIP when Hours and Quantities are recorded (P311221) and the Hours and Quantities Update (R31422) is run. Dollars are transferred at **Actual Hours × Actual Rate**.

| **AAI**  | **Account**                     | **Entry** |
| -------- | ------------------------------- | --------- |
| **3401** | Labor/Overhead Accrual Accounts | Credit    |
| **3120** | Work In Process                 | Debit     |

**Example:**

- Labor rate: \$10/hour × 2.5 hours = **\$25** (B1 cost type)
- Overhead rate: \$20/hour × 2.5 hours = **\$50** (C1 cost type)

**3.3 Work Order Completions - Document Type IC**

Completions are reported using the Completions Program (P31114). The WIP account is credited and the Finished Goods account is debited at **Actual Quantity × Standard Cost**.

| **AAI**  | **Account**     | **Entry** |
| -------- | --------------- | --------- |
| **3120** | Work In Process | Credit    |
| **3130** | Finished Goods  | Debit     |

**Example standards used:**

- Material standard: \$90 (A1)
- Labor standard: \$20 (B1)
- Overhead standard: \$40 (C1)

**Note:** Current versions of JD Edwards do not transfer cost type detail from Finished Goods to Cost of Goods Sold at this stage.

**3.4 Variance Accounting - Document Type IV**

Variance accounting can be run for a work order only once - after all material and labor transactions have been posted. WIP is credited and variance accounts are debited.

| **AAI**  | **Variance Type**    |
| -------- | -------------------- |
| **3220** | Labor Variance       |
| **3240** | Material Variance    |
| **3260** | Planned Variance     |
| **3270** | Engineering Variance |
| **3280** | Other Variance       |

**How variances are determined:**

| **Variance Type**             | **How It Is Generated**                                                                                                                                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Engineering Variance**      | Determined when Work Order Processing (R31410) is run. The system compares Standard Cost to Current Cost. Current Cost reflects BOM or routing changes not yet included in the standard.                                                   |
| **Planned Variance**          | Generated when a different raw material is used than specified in the current BOM, or if the item is assembled at a different work center with different rates.                                                                            |
| **Material Variance**         | Generated when the material or labor actually used differs from what was planned.                                                                                                                                                          |
| **Labor Efficiency Variance** | Calculated when a labor efficiency other than 100% is used.                                                                                                                                                                                |
| **Other Variance**            | Used to clear WIP accounts for a work order. For example: if 4 sets of material were issued for 4 hammers but only 3 were completed and the unused material was not returned, the remaining value is transferred to this variance account. |

**Example:**

- Engineering design change increased material cost by \$2.50/hammer = **\$10 engineering variance** (AAI 3220).
- Additional 0.125 hours/hammer for assembly = **\$5 labor variance** and **\$10 overhead variance** (AAI 3220).

**Section 4: Two Main Recommendations**

**4.1 Decide Up Front What Information Management Requires**

The vast array of functionality available in Manufacturing Accounting - from complex routings and scrap percentages to detailed AAI configurations - can make implementation overwhelming. Keep the configuration manageable. If the administrative burden of maintaining the setup becomes too great, inaccurate shop floor data will follow, making management reports unreliable.

**4.2 Document All Assumptions and Design Decisions**

Document how standards were developed, what assumptions were made, and why specific configuration choices were made. Organizations that fail to document this information often find that two years later no one can explain how overhead rates were determined. A simpler initial implementation can always be expanded once the shop floor has adjusted to the new system.

**Section 5: Setup Tips**

**5.1 Branch/Plant Constants - GL Explanation Field**

Set the General Ledger Explanation field in Branch/Plant Constants to **"2"** (Primary Part Number). The default value of "1" inserts the part description into the journal entry. Part descriptions often become less accurate over time, with a single description used for multiple parts. Using the Primary Part Number clearly identifies the item generating each journal entry, making variance research and report generation significantly easier.

**5.2 Manufacturing Constants**

**Work Center Efficiency**

Enabling this feature creates separate journal entries for labor efficiency - a useful tool for measuring productivity. For organizations new to Manufacturing Accounting, it is recommended to delay including Work Center Efficiency in overhead for 12 to 18 months until sufficient real-world data is available to calculate efficiency accurately.

**Fixed and Variable Overhead**

JD Edwards calculates both fixed and variable overhead identically - as a rate or a percentage of labor. If both are needed, consider configuring only Variable Overhead in Manufacturing Constants and using the Cost Component add-on functionality for Fixed Overhead, which provides more granular control.

**Accounting Cost Quantity (ACQ)**

This field determines setup cost by dividing the setup time by the normal production quantity. It represents an average lot size. The value must be set correctly - work orders with quantities larger than this value will generate favorable setup variances; smaller quantities will generate unfavorable variances.

**Caution:** If ACQ is left at the default value of "1" and setup costs are significant, the per-unit cost will be dramatically overstated. For example, a \$5,000 setup cost with ACQ = 1 results in \$5,000 per unit rather than \$0.50 per unit for a 10,000-unit production run.

**Time Basis Code (TBC)**

The Time Basis Code is stored in the second description of UDC table **30/TB** and is used to divide labor and machine time for cost calculations. The default value of "4" represents hours per 10,000 units. This should be changed to reflect the actual quantities produced in your facility. Setting up separate TBCs for common batch sizes avoids repeated manual conversions.

**5.3 Item Master / Item Branch - GL Class Code**

The GL class code used for journal entry creation is sourced from the **Item Branch Location table (F41021)** - not from the Item Branch table (F4102), as is commonly assumed. JD Edwards allows different values in these two tables without generating a warning. Create an exception report to identify mismatches between the two before running a cost rollup, as undetected differences will produce unexpected journal entry results.

**5.4 Bill of Material and Routing**

- **Bill Type** - JD Edwards only performs cost rollups on the **"M" type** (production manufacturing) BOM. Other types (e.g., Engineering, Cost Simulation) cannot be used for costing without data replication in a separate environment.
- **Effectivity Dates** - Only components and operations effective as of the date entered in the rollup program's processing options will be included in the cost rollup. Keep effectivity dates current, especially during periods of major product changes.
- **BOM Percent Scrap and Routing Operation Scrap** - These fields plan for expected component scrap. BOM scrap is entered by component as a percentage; Routing operation scrap is entered as a yield percentage per operation, accumulated from the bottom up. Both increase the A2 Material Scrap Cost component.
- **Shrink Factor** - Allows planning for production yield. If 100 usable units are needed and 40% scrap is expected, the system automatically increases the work order quantity to ensure sufficient output. The Shrink Factor has no effect on the rolled cost.

**Section 6: Execution Tips**

**6.1 Work Order Processing**

When Work Order Processing (R31410) is run, the following costs are captured and will not update for open work orders if changed afterward:

- Frozen standards
- Current costs
- Planned costs

**6.2 Recommended Work Order Statuses**

Include the following statuses in Work Order Activity Rules:

| **Status** | **Description**                                              |
| ---------- | ------------------------------------------------------------ |
| **90**     | Complete - all manufacturing is complete.                    |
| **95**     | Manufacturing Complete - manufacturing accounting may begin. |

**6.3 Work Order Completion Review - Two Required Checks**

Before moving a work order from Status 90 to Status 95 and running Manufacturing Accounting, perform both of the following checks:

**Check 1 - Material**

Using the Inventory Issues program (P31113) on the Daily Work Order Preparation Menu (G3111), review work orders closed during the most recent business cycle. Verify that the **Quantity Ordered** and **Quantity Issued** fields contain the same values.

- If the values differ, a variance exists. Research and correct it before proceeding.
- Valid variances (e.g., component scrap) should be documented in the Remarks field (WorldSoftware) or as an attachment (OneWorld).

**Example:** A BOM calling for 3 units of part 1234Y per assembly, on a work order for 5 assemblies, should show Quantity Ordered = 15. Any other value in Quantity Issued requires investigation.

**Check 2 - Hours**

Using the Order Hour Status Program (P31121), review work orders closed during the most recent business cycle. Compare **Actual Hours** to **Standard Hours** for Machine, Labor, and Setup.

- If the values differ, a variance exists. Research and correct it before proceeding.
- Document valid variances on the work order before running Manufacturing Accounting (R31802 and R31804).

**6.4 Actual Labor - UDC Table 31/ER**

If actual labor is charged to work orders by individual, UDC table **31/ER** must be maintained for each employee charging actual hours. This table is referenced by the Work with Work Order Time Entry Program (P311221) to retrieve the employee's labor rate.

If payroll does not maintain this table systematically, a separate process must be established to keep it synchronized with payroll records - particularly as hourly pay increases take effect.

**6.5 Reconciliation with Payroll**

Hours charged to the manufacturing system through Time and Attendance should be reconciled with Payroll regularly to ensure that actual labor costs are being captured accurately.

**Example:** If actual labor hours and dollars from Time and Attendance for one month total \$20,000 but only \$19,500 were reported against work orders, the \$500 difference must be investigated and accounted for to maintain accurate product costs.
