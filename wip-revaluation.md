**JD Edwards EnterpriseOne**

**Reference Guide: WIP Revaluation for Standard Costing**

**Program: R30837**

|                 |                                                                          |
| --------------- | ------------------------------------------------------------------------ |
| **Document ID** | 1510992.1                                                                |
| **Type**        | Bulletin                                                                 |
| **Modified**    | September 11, 2013                                                       |
| **Applies To**  | JD Edwards EnterpriseOne Shop Floor Control - Version 8.9 and later      |
|                 | JD Edwards EnterpriseOne Product Data Management - Version 8.9 and later |
| **Platform**    | All platforms                                                            |

**Section 1: Overview**

The WIP Revaluation program (R30837) revalues the production costs for all open work orders in the Production Cost table (F3102) based on the latest item cost. The program displays differences between the original work-in-process values and the new WIP values, and can be configured to create journal entries in the Account Ledger table (F0911).

**1.1 Purpose**

For standard cost items, performing an automated WIP revaluation ensures that:

- Work-in-process inventory always reflects updates to component and labor costs.
- Variances caused by cost changes mid-work order lifecycle are eliminated.
- Manual journal entries for WIP revaluation are not required.

**1.2 Key Limitations**

- R30837 does **not** revalue on-hand inventory - it only revalues open work orders.
- R30837 **cannot** be performed for closed work orders. Closed work orders are identified by a value of **3** in the Variance Flag (PPFG) field in the Work Order Master table (F4801).
- Flex Accounting from R30837 is **not** supported - this is by design.
- R30837 will not look for a cost in F4105 or update labor when Frozen Work Center Rates change.
- R30837 does **not** eliminate variances that already exist in F3102, such as true actual variances due to over-issue of material or engineering variances caused by missing frozen costs at work order generation.

**1.3 Invocation - Standard Cost Only**

For standard costed items, R30837 **must** be called from the Frozen Standard Update (R30835) only. The standalone version of R30837 is designed for actual cost work orders only and should not be used for standard costing.

**Section 2: How It Works**

**2.1 Background**

When the cost of a standard cost item is changed via Simulate (R30812) and Freeze (R30835), the Frozen Cost Update changes the Production Cost (F30026) and revalues only on-hand inventory. The Production Cost Inquiry (F3102) for open work orders will still reflect the old costs, creating a discrepancy between:

- The **work order production costs** (based on the old cost), and
- The **item cost in F4105** (based on the new cost).

This results in incorrectly valued WIP on the balance sheet and may generate variances requiring manual journal entries.

**2.2 WIP Revaluation Calculation**

R30837 calculates the change in work-in-process value as follows:

**Change in WIP = New WIP − Old WIP**

Where:

**WIP = Actual − Completed**

**Example:**

|                               | **Actual** | **Completed** | **WIP**   |
| ----------------------------- | ---------- | ------------- | --------- |
| **Before Frozen Cost Update** | \$100      | \$50          | **\$50**  |
| **After Frozen Cost Update**  | \$200      | \$100         | **\$100** |
| **Change in WIP**             |            |               | **\$50**  |

The F3102 is updated with the new values and a journal entry is written to work-in-process to account for the \$50 change.

**Note:** If the change in WIP value equals zero (new WIP = old WIP), no journal entry is written, although the F3102 is still updated with the new costs.

**2.3 AAI Tables Used**

R30837 uses the following AAI tables for journal entries:

| **AAI**  | **Account**      | **Usage**                                                |
| -------- | ---------------- | -------------------------------------------------------- |
| **3120** | Work In Progress | Debit - WIP revaluation adjustment                       |
| **4136** | Expense or COGS  | Credit - WIP revaluation adjustment                      |
| **4134** | Inventory        | Used by Frozen Update (R30835) for inventory revaluation |

**Section 3: Prerequisites**

Before running WIP Revaluation, the following steps must be completed in order:

- **Run Manufacturing Accounting (R31802A)** - Clears all unaccounted units and updates the F3102 file with the latest transactions before any cost changes are implemented.
- **Run Simulated Roll Up (R30812)** - Calculates the new simulated costs for the item based on updated component costs and/or work center rates.
- **Run Frozen Update (R30835)** - Freezes the simulated costs as the new standard cost. WIP Revaluation (R30837) is called from R30835 by setting the processing option on the Process tab, option #5:
  - **Blank** = Do not invoke WIP Revaluation
  - **1** = Invoke WIP Revaluation for Work Orders
  - **2** = Invoke WIP Revaluation for Lean Manufacturing

**Section 4: Setup**

**4.1 AAI Configuration**

AAIs 3120 (Work in Progress) and 4136 (Expense or COGS) must be configured in Distribution/Manufacturing AAI Values (F4095) for the **IB (default) document type** before running WIP revaluation.

If the processing option to create journal entries is blank, manual journal entries must be written to reflect the correct changed WIP values in the applicable accounts.

**4.2 Frozen Standard Update (R30835) Configuration**

Before running WIP Revaluation from R30835:

- Confirm that all work orders at a closed status have **PPFG = 3** in F4801. R30837 uses the PPFG flag to identify open work orders eligible for revaluation.
- Enable the **Update Work Center Rates** processing option if work center rates have changed and the new rates should be used in the calculation of new production costs and WIP.
- R30835 will set the **CCFL (Cost Change Flag)** on all changed items. R30837 will clear this flag upon successful completion.

**Section 5: WIP Revaluation Program (R30837) - Behavior and Rules**

**5.1 Eligibility - When F3102 Will Be Updated**

R30837 will update the F3102 for a parent item / work order when:

- The F4801 Variance Flag (PPFG) is **not equal to 3** (work order is open).
- A change has been made to a Work Center Rate and R30835 is run to freeze the cost, update work centers, and call WIP Revaluation.

**5.2 Eligibility - When F3102 Will NOT Be Updated**

R30837 will not update the F3102 for a parent item / work order when:

- The F4801 Variance Flag (PPFG) **equals 3** (work order is closed).
- The F4105 Cost Change Flag (CCFL) is **blank** - this field is cleared by R30837 after a successful run.
- No Work Center Rates related to parent items / work orders in the R30835 data selection have been changed.

**5.3 Data Selection**

R30837 uses the cache built from the R30835 data selection. It uses the **F3111 Part List** as the source to revalue component lines in the F3102 Variance Inquiry (Current, Planned, and Actual Material Amounts).

**Important:** R30837 does not reference the F3002 BOM file for Current Amounts in F3102. If the part list has been changed via P3111 or P31113, re-simulating, freezing, and calling R30837 - regardless of whether component costs have changed - can cause Engineering Variances when Planned variances would have been expected.

Data selection in R30837 has been intentionally omitted because the program should only be called from R30835 for standard cost items.

**5.4 Journal Entry Logic**

R30837 rewrites all columns in F3102 with new costs, including:

- **Actual column** (IM and IH transactions)
- **Completed column** (IC transactions)

An **IB journal entry** is written for the change in WIP (F3102 Actual − Completed) only when there is a positive or negative change in WIP value. Work orders where the WIP change equals zero will have their F3102 updated but will not appear in the report output and will not generate a journal entry.

**Note:** The GL Work in Process account will balance to F3102 in total only. If F3102 is used heavily for detailed reporting purposes, rewriting this file via R30837 may not be the appropriate option.

**Section 6: How to Run a Sample WIP Revaluation Test**

The following procedure is recommended for testing prior to implementation to gain a full understanding of the process and expected outputs:

- Add a new parent item and some component items for the test.
- Run Simulate (R30812) and Freeze (R30835) - do not call R30837 at this stage.
- Create three work orders for the new parent item:
  - **Work Order 1** - Attach parts list and routing only.
  - **Work Order 2** - Take through material issues and run Manufacturing Accounting (R31802A).
  - **Work Order 3** - Take through material issues, complete half the work order quantity, and run Manufacturing Accounting (R31802A).
- Review all work orders using Production Cost Inquiry (P31022) and note the Standard, Current, Planned, Actual, and Completed values.
- Change the cost of the component items (08 cost type).
- Run Simulated Roll Up (R30812) from cost method 08 to cost method 07 for the parent item, exploding the BOM.
- Run Frozen Update (R30835), exploding the BOM, with the WIP Revaluation processing option enabled to call R30837.
- Review all work orders (P31022) for changes to Standard, Current, Planned, Actual, and Completed values.
- Review the IB journal entries for correct values reflecting the changes to work-in-process.

**Section 7: Full Example**

**7.1 Before Running R30837**

**Initial frozen costs:**

| **Cost Type** | **Cost** |
| ------------- | -------- |
| A1            | \$10.00  |
| B1            | \$1.00   |
| C3            | \$0.01   |
| C4            | \$0.01   |

**Work Center Rates (Simulated = Frozen):**

| **Rate Type**      | **Amount** |
| ------------------ | ---------- |
| Direct Labor       | \$1.00     |
| Labor Variable O/H | \$0.01     |
| Labor Fixed O/H    | \$0.01     |

A work order for 100 units was entered, material was issued for 100 units at \$10 each, 100 hours of Hours and Quantities were recorded, and 50 units were completed. After running R31802A, **Total WIP (Actual − Completed) = \$551.00**.

**7.2 Cost Change**

The component cost is changed to **\$20** and work center rates are updated to **\$2.00 and \$0.02**.

New frozen costs:

| **Cost Type** | **New Cost** |
| ------------- | ------------ |
| A1            | \$20.00      |
| B1            | \$2.00       |
| C3            | \$0.02       |
| C4            | \$0.02       |

**7.3 After Running R30837**

After running Simulated Roll Up (R30812), Frozen Update (R30835) with work center rate freeze enabled, and WIP Revaluation (R30837), **Total WIP (Actual − Completed) = \$1,102.00**.

All production costs in F3102 are revalued according to the changed work center rates and component costs. An IB journal entry is written for the change in WIP value of **\$551.00** (\$1,102.00 − \$551.00).

**Section 8: Key Reminders**

- For standard costing, always call R30837 from the Frozen Update (R30835) - never run it standalone.
- R30837 rewrites all columns in F3102, including Actual (IM and IH) and Completed (IC). An IB journal entry is written for the change in WIP value. The GL WIP account will balance to F3102 in total only.
- Before running WIP Revaluation from R30835, confirm that all closed work orders have **PPFG = 3** in F4801.
- Before running R30835, always run Manufacturing Accounting (R31802A) to clear all unaccounted units.
- R30835 sets the CCFL flag on changed items. R30837 clears this flag upon successful completion.

**Section 9: Known Issues**

| **Bug**      | **Description**                                                                                                                                                                          | **Workaround**                                                   |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **17285174** | R30837 WIP Revaluation and Standard Cost Zero - the program should update F3102 to the latest standard cost whenever R30835/R30837 is run, even when the new standard cost is zero.      | Under review.                                                    |
| **16785420** | B1 Current Amount in F3102 is cleared when a quantity or date is changed on the work order and R30835 is run calling R30837. Expected behavior: B1 Current Amount should not be cleared. | Rerun R31410 immediately after making changes to the work order. |
