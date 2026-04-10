**JD Edwards**

**Reference Guide: Changing Item Primary Unit of Measure**

**Section 1: Overview**

Changing the primary unit of measure (UOM) after operating in a live inventory environment is **not recommended by JD Edwards**. A fundamental principle of the inventory system is that the primary UOM should be established and maintained as the smallest unit of measure. Setting up items otherwise may generate unpredictable results.

**1.1 Recommended Alternative**

Before proceeding with a primary UOM change, consider the following alternative:

Create a set of new items cross-referenced as replacement items for the existing ones, using recognizable but slightly different product numbers. These replacement items would be configured with the new primary UOM. Inventory counts and all active sales and purchase orders would then need to be cleared from the old items and re-established under the replacement items.

If this alternative is not viable and the existing items must be changed, the procedures and considerations outlined in this document should be carefully evaluated and implemented as appropriate.

**Section 2: Procedure**

The following steps must be completed in the order listed to avoid complications. Deviating from this sequence may result in data integrity issues.

- **Complete or cancel all open orders** - Close all open sales orders, purchase orders, and work orders for the item. Supply/Demand Inquiry (P4021) may be a useful tool for verifying that this has been completed.
- **Zero out all inventory locations** - Issue out the inventory from all locations so that the on-hand quantity is zero. Verify using Summary Availability Inquiry (P41202).
- **Change the Primary Unit of Measure in the Item Master** - Update the primary UOM field in the Item Master record.
- **Update Default Units of Measure (P41012)** - Change other UOM fields as required. The Primary UOM field will reflect the change made in the previous step.
- **Verify the Unit of Measure Conversion table** - Confirm that the conversion table is still valid or make corrections as needed using program P41002.
- **Verify costs and selling prices** - Ensure that costs (P4105) and selling prices (P4106) are correct for the new primary UOM.
- **Adjust on-hand quantity back into inventory** - Enter the actual on-hand quantity, expressed in the new primary UOM, back into the applicable inventory locations.
- **Re-enter any previously cancelled orders** - Recreate any active orders that were cancelled in Step 1.

**Section 3: Other Considerations**

**3.1 History and Ledger Files**

Several history and ledger files store the primary unit of measure for an item, including:

- **F43199** - Purchasing ledger
- **F42199** - Sales ledger
- **F42119** - Sales history

Records written to these files prior to the UOM change will retain the original primary UOM. Any reports that reference the primary UOM from these files may present incorrect information following the change.

In the Sales system, two additional history files store cumulative item quantities by period in the primary UOM:

- **F4115** - Item sales by branch and fiscal year
- **F4229** - Item sales by customer, order type, line type, branch, and fiscal year

Changing the primary UOM for an item will corrupt existing cumulative data in these files.

**Example:** If F4115 contains a record for item "widget" in branch 10 for the year 2001 with a primary UOM of "dozen," and the first period bucket (SQ01) contains a quantity of 10 (representing 10 dozen widgets sold in January) - changing the primary UOM to "each" and then selling 2 more widgets in January would update the bucket to 12. This value is incorrect, as it represents 10 dozen and 2 each mixed in the same field.

JD Edwards does not provide programs to make retroactive changes to history or ledger files. Available options for correction include:

- Correcting records using a data file utility (prone to error).
- Using an RPG program or World Writer to replace the data.
- Correcting only the most recent history records and modifying reporting to exclude data older than a defined cutoff date.

Management should carefully evaluate the trade-offs involved in working with history data that contains invalid quantities, units of measure, or amounts.

**3.2 Bill of Material**

If the item being changed is a kit, a manufactured item, or a component of a kit or manufactured item, and a bill of material exists for the item in table F3002, the BOM must be updated to reflect the new unit of measure as necessary.

**3.3 General Ledger**

If units are updated to the general ledger, the F0911 and F0902 files must be considered. This is only relevant if a single transaction unit of measure is used for the item, as conversions are not applied upon updating the GL.

**Example:** If widgets are only transacted by the dozen and 100 dozen units are currently applied against a particular account number - changing the primary UOM to "each" and posting 2 additional units against the same account would result in a cumulative unit total of 102, which is incorrect (100 dozen and 2 each).

**3.4 Advanced Warehousing**

If the Advanced Warehousing module is in use, changing the primary UOM for an item should not cause issues, provided:

- There are no open purchase orders or sales orders for the item.
- There is no on-hand quantity for the item.

It is also advisable to:

- Verify that there are no F4602 records for the item.
- Confirm that any existing F4611 and F46130 records have been purged for the item, as these files store the primary UOM.

**3.5 EDI**

If the EDI module is in use, verify that all 47-series files for incoming and outgoing data do not contain an incorrect primary unit of measure for the item in question.

**3.6 Processing Options**

Several programs allow a transaction UOM to be specified in processing options, including:

- Sales Order Entry (P4211)
- Purchase Order Entry (P4311)
- Sales Transfers (P4242)
- Direct Ship Orders (P4243)

Following a primary UOM change, review the processing options for each of these programs to verify that the transaction UOM remains valid.

**Section 4: Summary**

Changing an item's primary unit of measure in a live production environment carries significant risk to data integrity. The following precautions are strongly recommended:

- **Test first** - The conversion should be performed in a test environment and reviewed thoroughly before any changes are made in the production environment.
- **Start with one item** - Observe the effects of converting a single item before applying the procedure to multiple items.
- **Consult management** - It is advisable to discuss the project with the client manager before undertaking the conversion.

**Important:** It is beyond the capabilities of Global Support Services to assist in this conversion. Proceed with caution and ensure all stakeholders are aware of the risks involved.
