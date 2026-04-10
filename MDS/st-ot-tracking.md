**JD Edwards In Transit**

**Training Guide: ST/OT Transfer Orders**

**Topic: Inventory Tracking Without Receipts Routing**

**Section 1: Overview of ST/OT Transfer Orders**

ST/OT transfer orders in JD Edwards are used to move materials between branch plants (A to B) within the same company. The process uses a clearing account to hold the value of goods while they are in transit.

This In Transit balance sheet account differs from a standard perpetual inventory account in an important way: while goods are in transit, the quantities on hand are removed from the perpetual counts and exist only as a balance in the clearing account. Once items are received at the destination branch, the clearing account is relieved and perpetual inventory is restored.

**Section 2: Traditional Approach - Receipts Routing**

Receipts routing is a JD Edwards feature that can be used to track inventory that is physically in transit from one branch to another. After the shipping branch confirms the sales order shipment, the goods become available for receipt at the receiving branch and can be tracked through a receipt routing operation.

The two key routing stages are:

- **TRAN (In Transit)** - The goods are in transit and have not yet been physically received into stock.
- **STK (Stock)** - The goods have been physically received and entered into inventory at the destination branch.

While receipts routing provides visibility into in-transit inventory, it requires a dedicated setup and configuration within JD Edwards to function correctly.

**Section 3: RapidReconciler Alternative - In Transit As-Of Tracking**

RapidReconciler provides a built-in alternative to receipts routing by generating an inventory "As-Of" view dynamically as transfer orders are shipped and received. This functionality is accessible directly through the RapidReconciler user interface on the In Transit As-Of page.

**3.1 Key Features**

- **Period Selector** - The period selector in the top right corner of the As-Of page allows the user to select any fiscal period within the available timeline. This produces an immediate listing of all items that were in transit as of that period end date.
- **Transaction Detail** - Clicking the **+** sign at the left of any row expands the view to show all individual detail transactions that make up the current in-transit balance for that item. These details can be exported to Excel for further analysis.

**3.2 Benefit Over Receipts Routing**

Using RapidReconciler for in-transit inventory tracking eliminates the need to configure and maintain the JD Edwards receipts routing setup, while still providing full visibility into what is in transit at any point in time.

**Section 4: Coming Next - Exclusion Adjust**

Within the In Transit As-Of transaction details, an item labeled **"Exclusion Adjust"** may appear. This represents an adjustment related to the order exclusion process in RapidReconciler.

A full explanation of what Exclusion Adjust means and how it impacts the In Transit As-Of data will be covered in the next installment of this series.
