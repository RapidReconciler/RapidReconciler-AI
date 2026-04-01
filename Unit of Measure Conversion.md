**Reference Guide: Unit of Measure Conversion**

**Overview, Setup, and Configuration**

**Section 1: Overview**

Unit of Measure (UOM) conversion in JD Edwards serves two purposes:

- **Standard UOM Conversions** - Apply to all items system-wide, such as 12 inches = 1 foot.
- **Item-Specific UOM Conversions** - Apply to a specific item or item/branch plant combination.

The **Unit of Measure Conversions by Branch** setting in System Constants controls whether item-specific conversions are maintained at the item level or the item/branch level.

**1.1 Storage Tables**

| **Table**  | **Contents**                                 |
| ---------- | -------------------------------------------- |
| **F41003** | Standard Unit of Measure Conversions         |
| **F41002** | Item-specific or item/branch UOM Conversions |

**Section 2: Hierarchy to Determine UOM for an Item**

The system searches for a valid conversion in the following order:

- Searches the **Item/Branch UOM Conversion table (F41002)** for the item or item/branch combination.
- If not found, searches the **Standard UOM Conversion table (F41003)**.
- If no conversion is found in either table, the system displays an **error message**.

**Section 3: Setting Up Units of Measure**

**3.1 UDC Table Setup**

Before any UOM conversions can be configured, all units of measure must be set up in UDC table **00/UM**.

**3.2 Standard Units of Measure Conversions**

Standard UOM conversions are set up using **P41003**, accessed from menu **G4141**. Data is stored in table F41003.

Once configured, these conversions do not need to be entered individually for each item in the Item UOM Conversion table (F41002). They apply universally to all items.

**Section 4: Default Units of Measure for an Item**

Each item has a set of Default Units of Measure, each serving a specific purpose. These are accessed from **Item Master (G4111)** by pressing **F8** to navigate to the Default Units of Measure screen.

| **UOM Type**               | **Description**                                                                                                                                                                                                                                                                                           |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary** (Stocking UOM) | The primary unit of measure must be the **smallest unit of measure** for the item to avoid conversion rounding problems. Many programs are hard-coded to convert to the primary UOM and then back to the transaction UOM. Clients whose primary UOM is not the smallest may encounter unexpected results. |
| **Secondary**              | An additional valid UOM for use in Inventory, Sales, or Purchasing programs. Not specifically used by any program other than for validation. Some clients use this UOM to create advanced pricing formulas.                                                                                               |
| **Purchasing**             | The UOM used when purchasing an item. Defaults into the purchasing UOM field. If processing option 8 behind Purchase Order Entry is set to blank, this UOM defaults into the transaction UOM.                                                                                                             |
| **Pricing**                | The UOM generally used when selling an item. Defaults into the pricing UOM field. If processing option 8 is set to 1, the pricing UOM defaults into the transaction UOM on sales orders.                                                                                                                  |
| **Shipping**               | Typically used when shipping an item. Historically referenced in the Bill of Lading program; now serves as another valid item UOM value.                                                                                                                                                                  |
| **Production**             | Used in Manufacturing.                                                                                                                                                                                                                                                                                    |
| **Component**              | Used in Manufacturing.                                                                                                                                                                                                                                                                                    |
| **Weight/Volume**          | The primary UOM for weight and volume ratios. Used when setting up Landed Cost and Shipping tables. Landed costs can be applied based on overall weight or volume. Also provides the default for displaying weight/volume information on sales and purchase orders and is used for freight calculations.  |

**Section 5: Unit of Measure Conversions by Branch**

The **Unit of Measure Conversions by Branch** field (BUMC) in System Constants controls whether UOM conversions are maintained at the item level or the item/branch level. System Constants is accessed by pressing **F10** from the Branch/Plant Constants screen. This is a universal system-wide setting.

| **Setting** | **Behavior**                                                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Y**       | UOM conversion is set up for an **item and branch/plant** combination. The branch field will appear on the Item UOM video. |
| **N**       | UOM conversion is set up for an **item across all branch/plants**.                                                         |

**Important:** If this field is changed after conversions have been set up, the UOM conversions will need to be re-entered for all applicable items.

**Section 6: Sales and Purchase Price Retrieval UOM**

The sales and purchase price retrieval UOM is also configured in System Constants. This setting controls which UOM is used to retrieve the price on sales and purchasing orders. Options include the primary, transaction, or pricing unit of measure. This is a universal system-wide setting.

**Section 7: Item UOM Conversion Setup**

**7.1 Navigation**

To access the Item UOM Conversion table, press **F8** from the Default Unit of Measure screen within the Item Master program.

**7.2 Entering Conversion Information**

- Enter the unit of measure to convert **from** on the left side of the screen.
- Enter the number of units required to equal the **to** unit of measure.
- The system automatically creates the reciprocal conversion on the right side of the screen.
- An unlimited number of conversions can be entered for each item.
- Each unit of measure entered should be converted back to the **primary unit of measure**.
- Each conversion set up makes that unit of measure valid within entry and inquiry screens.

**Note:** The Structured Only field is used in the Warehouse Management system only.

**Section 8: Examples - Sales and Purchase Orders**

**8.1 Purchase Order Transaction UOM**

Processing option 8 behind **Purchase Order Entry (P4311)** controls which UOM defaults into the transaction UOM:

| **Processing Option 8** | **Behavior**                                 | **Example**                                    |
| ----------------------- | -------------------------------------------- | ---------------------------------------------- |
| **Blank**               | Purchasing UOM defaults into transaction UOM | Transaction UOM = **Case**; order for 10 cases |
| **1**                   | Primary UOM defaults into transaction UOM    | Transaction UOM = **Can**; order for 10 cans   |

The extended cost is determined by the transaction unit of measure in both scenarios.

**8.2 Sales Order Transaction UOM**

Processing option 8 behind **Sales Order Entry (P4211)** controls which UOM defaults into the transaction UOM:

| **Processing Option 8** | **Behavior**                              | **Example**                                    |
| ----------------------- | ----------------------------------------- | ---------------------------------------------- |
| **Blank**               | Primary UOM defaults into transaction UOM | Transaction UOM = **Can**; order for 10 cans   |
| **1**                   | Pricing UOM defaults into transaction UOM | Transaction UOM = **Case**; order for 10 cases |

The extended cost is determined by the transaction unit of measure in both scenarios.

**Section 9: Weight and Volume UOM Setup**

**9.1 UDC Table Configuration**

To enable weight and volume usage in transactions, navigate to the **Unit of Measure UDC table (00/UM)** and open the fold for each applicable UOM. In the **Special Handling Code** field, enter:

| **Value** | **Meaning**                                         |
| --------- | --------------------------------------------------- |
| **V**     | Volume - specifies this UOM can be used for volume. |
| **W**     | Weight - specifies this UOM can be used for weight. |

**9.2 Customer Billing Instructions**

Navigate to **page 2 of the Customer Billing Instructions** and specify the **Display Weight/Volume Unit of Measure** to be used for that customer.

**9.3 Usage of Weight and Volume UOM**

Once configured, weight and volume UOM data appears in the following locations:

- **Landed Cost Revisions** - A rate can be charged based on weight or volume. The system multiplies that rate by the unit weight or volume and the item cost to calculate the landed cost.
- **Sales Order Detail (behind the detail)** - Extended weight and volume display in the details behind the detail line.
- **Purchase Order Detail (behind the detail)** - Extended weight and volume display in the details behind the detail line.