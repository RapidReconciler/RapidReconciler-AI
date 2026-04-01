**Reference Guide: Costs in EnterpriseOne**

**Inventory and Purchasing Costing - Storage, Usage, and Updates**

**Section 1: Cost Levels (CLEV)**

Inventory cost for an item can be tracked at one of three levels. Different items may be costed at different levels.

| **Level** | **Description**                                                                                                       |
| --------- | --------------------------------------------------------------------------------------------------------------------- |
| **1**     | **Costing by Item** - One cost for an item regardless of which Branch/Plant or Location it is in.                     |
| **2**     | **Costing by Branch/Plant** - Different costs in different Branch/Plants for the same item.                           |
| **3**     | **Costing by Branch/Plant and Location** - Different costs for each Location within a Branch/Plant for the same item. |

The Cost Level is selected when a new item is set up in **Item Master Information (P4101)** off menu G4111.

**1.1 Changing the Cost Level**

**Changing to a lower value:** Cannot be done through Item Master Information (P4101). Attempting to do so will produce error message **3755 - "Cost level update not allowed."** To change to a lower cost level, run the **Item Cost Level Conversion (R41815)** UBE.

**Note:** If the Purchase Price Level is set to "3" (Inventory Cost Level), all costs must be identical for the conversion to complete successfully.

**Changing to a higher value:** No issues. The system takes the existing cost and applies it at the new level. For example, changing from Level 2 (Item/Branch) to Level 3 (Item/Branch/Location) will simply apply the existing cost to all locations in the branch.

**Section 2: Cost Methods (LEDG)**

Cost Methods are defined in UDC table **40/CM**. Cost Methods 01 through 19 are reserved for EnterpriseOne software. Additional cost methods may be added to this table.

**2.1 Cost Methods with Built-In Functionality**

Three cost methods have included system functionality:

| **Cost Method** | **Description**                |
| --------------- | ------------------------------ |
| **01**          | Last In Cost                   |
| **02**          | Weighted Average Cost          |
| **08**          | Purchasing - Base Cost No Adds |

**2.2 Static Cost Methods**

All remaining cost methods (including any custom methods added to UDC 40/CM) are static - they have no included system functionality and must be maintained manually.

**Section 3: Where Are Costs Stored?**

Item costs are stored in the **Item Cost file (F4105)**. The number of F4105 records per item depends on the cost level:

| **Cost Level** | **F4105 Record Structure**                                                       |
| -------------- | -------------------------------------------------------------------------------- |
| **Level 1**    | One record per Cost Method per Item. Branch/Plant and Location fields are blank. |
| **Level 2**    | Multiple records per Item-Branch/Plant combination. Location field is blank.     |
| **Level 3**    | Multiple records per Item-Branch/Plant-Location combination.                     |

**Important:** Costs are always stored in the **primary unit of measure**. The F4105 file does not contain a unit of measure field.

**Section 4: Which Cost Does the System Use?**

Two indicator flags in the F4105 file tell the system which cost record to use:

| **Flag**                        | **Data Item** | **Description**                                                                                                                                                    |
| ------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Costing Method - Sales**      | CSIN          | When populated with **"I"**, identifies the cost method used to calculate the value of inventory. This cost defaults into Sales Orders and Inventory transactions. |
| **Costing Method - Purchasing** | CSPO          | When populated with **"P"**, identifies the cost method that defaults into Purchase Orders.                                                                        |

One F4105 record may serve as both the Sales/Inventory cost and the Purchasing cost.

**Section 5: Cost Revisions (P4105)**

The **Cost Revisions program (P4105)** off menu G4112 is used to add, change, or view costs, and to designate the Costing Method for Sales and Purchasing.

**5.1 Default Cost Methods for New Items**

- **Cost Level 1:** Both Costing Method - Sales and Costing Method - Purchasing default from the **Branch/Plant ALL** settings in Branch/Plant Constants (P41001).
- **Cost Levels 2 or 3:** Both defaults are sourced from the **Branch/Plant Constants (P41001)** for the specific Branch/Plant entered.

**5.2 Display Behavior**

Only the fields applicable to the item's cost level will be displayed:

- Cost Level 1 items: All Branch/Plant and Location fields are hidden.
- Cost Level 2 items: Location and Lot/Serial fields are hidden.

**Section 6: Cardex - IB Transactions**

IB transactions (inventory re-evaluation adjustments) are created in the Cardex (F4111) under the following conditions:

| **Scenario**                                                                    | **IB Transaction Created?**                                                                        |
| ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Changing the current Sales/Inventory Cost for an item                           | **Yes** - inventory value has changed. Journal entries use AAI 4134 (debit) and AAI 4136 (credit). |
| Changing the Sales/Inventory Cost Method in a way that results in a cost change | **Yes**                                                                                            |
| Changing the Sales/Inventory Cost Method with no resulting cost change          | **No**                                                                                             |
| Changing a cost for a method that is not the current Sales/Inventory Cost       | **No**                                                                                             |

**Section 7: Cost Methods Updated by Receipts (P4312) and Voucher Match (P0411/P4314)**

Certain programs within the Purchasing system update cost methods 01-08 automatically. A unit cost can be updated or created regardless of which method is currently assigned as the Purchasing Cost Method.

**7.1 Update Summary by Program**

| **Cost Method**                       | **Updated by P4312 (Receipts)**                             | **Updated by P0411/P4314 (Voucher Match)**  |
| ------------------------------------- | ----------------------------------------------------------- | ------------------------------------------- |
| **01 - Last In**                      | ✓                                                           | No                                          |
| **02 - Weighted Average**             | ✓                                                           | ✓ (if cost differs from receipt)            |
| **06 - Lot**                          | ✓ (only if 06 is the Sales/Inventory cost method)           | Only if UDC 43/VU has "Y" in Description 02 |
| **07 - Standard**                     | No (must be updated manually or via Manufacturing programs) | No                                          |
| **08 - Purchasing Base Cost No Adds** | ✓                                                           | ✓                                           |
| **03, 05, and custom methods**        | No                                                          | No - must be updated manually               |

**7.2 Cost Method Details**

**01 - Last In Cost**

- Updated by PO Receipt (P4312) - includes Unit Cost plus Tax.
- Can include Landed Cost if the **Include In Unit Cost** flag is set in Landed Cost Revisions (P41291). Landed cost must be applied at receipt; if applied via Stand Alone Landed Cost (P43214), the cost will only reflect the landed cost value.
- **Not updated by Voucher Match.**
- Freight Update (R4981) updates this cost for inbound shipments if processing option #4 (Process tab) = 1. R4981 must be run **after** the item is in stock - if run while in Receipt Routing, the cost will not include freight.

**02 - Weighted Average Cost**

Refer to the Weighted Average Cost Overview document for full details.

**06 - Lot Cost**

- Represents the cost of one unit for a specific Location/Lot combination.
- Updated by PO Receipt (P4312) only if cost method 06 is the **Sales/Inventory** cost method. If it is only the Purchasing cost method, it will not be updated.
- Includes Tax and can include Landed Cost if the Include In Unit Cost flag is set.
- Updated by Voucher Match only if UDC table **43/VU** has "Y" in the Description 02 field.

**07 - Standard Cost**

- **Not updated by any Distribution programs.**
- Can be updated by certain Manufacturing programs (see the Standard Cost Simulation document for details).

**08 - Purchasing - Base Cost No Adds**

- Excludes Landed Costs and Taxes.
- Updated by both PO Receipt (P4312) and Voucher Match (P0411/P4314).
- Same Landed Cost and Freight Update notes apply as for cost method 01.

**7.3 Example - Cost Updates by P4312 and Voucher Match**

**Setup:**

- Cost methods 06 (Lot) and 08 (Purchasing - Base Cost No Adds) are set at \$1.00.
- A Purchase Order is entered with tax.
- Landed cost of \$5.00 will be added at receipt.

**Purchase Order:**

| **Component** | **Amount** |
| ------------- | ---------- |
| Unit Cost     | \$1.00     |
| Tax           | \$0.07     |
| Total         | \$1.07     |

**After Receipt (adding \$5.00 landed cost) - Total PO = \$6.07:**

| **Cost Method** | **Status**      | **Comment**                                                                   |
| --------------- | --------------- | ----------------------------------------------------------------------------- |
| 07              | Unchanged       | Not updated by Distribution programs.                                         |
| 03              | Unchanged       | Static - manual update only.                                                  |
| 01              | Created/Updated | Reflects unit cost + tax + landed cost.                                       |
| 02              | Updated         | Weighted average of unit cost + tax + landed cost.                            |
| 06              | Updated         | Reflects \$1.00 (would reflect new cost if unit cost had changed at receipt). |
| 08              | Updated         | Reflects \$1.00 - excludes tax and landed cost.                               |

**After Voucher Match (unit cost changed from \$1.00 to \$10.00) - Total PO = \$15.70:**

| **Cost Method** | **Status** | **Comment**                                                       |
| --------------- | ---------- | ----------------------------------------------------------------- |
| 01              | Unchanged  | Not updated by Voucher Match.                                     |
| 03              | Unchanged  | Static.                                                           |
| 06              | Updated    | Reflects new unit cost of \$10.00 (excludes tax and landed cost). |
| 07              | Unchanged  | Not updated by Distribution programs.                             |
| 08              | Updated    | Reflects new unit cost of \$10.00 (excludes tax and landed cost). |
| 02              | Updated    | Averages unit cost + landed cost + tax based on new cost.         |

**Section 8: Item Cost Level Conversion (R41815)**

**8.1 Purpose**

To change an item's Cost Level to a lower value, run the **Item Cost Level Conversion (R41815)** UBE. This program does **not** write journal entries.

**8.2 Processing Options**

| **Option**           | **Description**                                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 - Cost Level**   | Enter the target Cost Level to convert to.                                                                                                                  |
| **2 - Branch/Plant** | When converting to Level 1, specify which Branch/Plant's costs to use. When converting from Level 3, costs default from the Primary Location automatically. |
| **3 - Mode**         | Enter "1" for Final mode (files will be updated). Leave blank for proof mode (no file updates).                                                             |
| **4 - Report**       | Enter "1" to print exceptions only. Leave blank to print all items.                                                                                         |

**8.3 Conversion Rules**

**Level 2 → Level 1:** At Level 2, costs are set per Branch/Plant. Specify the source Branch/Plant in processing option 2.

**Level 3 → Level 2:** At Level 3, costs are set per Location. The program automatically uses the cost from the **Primary Location**.

**Note:** If the Purchase Price Method is set to "3" (Inventory Cost Level), all costs must be identical for the conversion to succeed.

**8.4 Error Conditions**

The program will error with **"Cost and/or Method difference"** if it attempts to merge different Sales/Inventory costs into one record. This is because changing the Sales/Inventory cost revalues inventory, and R41815 does not write journal entries to account for that change.

**Resolution:** Use Cost Revisions (P4105) to make all Sales/Inventory costs equal before running R41815.

**Multi-currency note:** Cost Level 1 cannot be used in a multi-currency environment. Items may exist in multiple Branch/Plants belonging to different companies with different currencies. R41815 will error if run in a multi-currency environment when converting to Level 1.

**8.5 Conversion Example**

**Scenario:** Sales/Inventory cost method is CM 04. Converting from Level 2 to Level 1.

| **Branch A - CM 04** | **Branch B - CM 04** | **Branch A - CM 03** | **Branch B - CM 03** | **Processing Option 2** | **Result**                              |
| -------------------- | -------------------- | -------------------- | -------------------- | ----------------------- | --------------------------------------- |
| \$10                 | \$15                 | \$10                 | \$13                 | Either A or B           | **Program errors** (CM 04 costs differ) |
| \$10                 | \$10                 | \$15                 | \$13                 | A                       | CM 04 = \$10; CM 03 = \$15              |
| \$10                 | \$10                 | \$15                 | \$13                 | B                       | CM 04 = \$10; CM 03 = \$13              |

When Sales/Inventory costs are identical but other costs differ, the program runs to completion. The Branch/Plant specified in processing option 2 determines which value is used for the non-Sales/Inventory cost methods.