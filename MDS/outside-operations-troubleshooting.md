**Troubleshooting Guide: Outside Operations**

**Why a Purchase Order Is Not Created During Work Order Processing**

|                 |             |
| --------------- | ----------- |
| **Document ID** | OMN-03-0003 |
| **Solution ID** | 200782906   |

**Section 1: Introduction**

If a Purchase Order is not generated for an Outside Operation, or the message **"No PO"** displays in the Outside Operation routing step, the cause is typically incorrect setup on the item, routing, constants, processing options, or the vendor.

**1.1 First Step Before Troubleshooting**

Before investigating further, attempt to manually enter a PO for the outside operation item directly from **P4310** (using the same version called by R31410). If an error occurs or the PO cannot be created, the problem likely lies with P4310 or the vendor setup. Refer to Section 5 for vendor and purchase order setup issues.

**Section 2: Item Setup Issues**

Check the following item-related setup issues:

| **#** | **Issue**                                 | **Description**                                                                                                                                                                                                                                                                                                                 |
| ----- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | Secondary UOM differs from primary UOM    | The \*OP item number has a secondary unit of measure different from the primary UOM.                                                                                                                                                                                                                                            |
| **2** | Missing UOM conversions                   | The \*OP item number does not have UOM conversions defined when UOM values are different.                                                                                                                                                                                                                                       |
| **3** | Parent second item number contains spaces | This is only a problem in releases prior to OneWorld XeU1. See SAR 4719215.                                                                                                                                                                                                                                                     |
| **4** | Parent item number exceeds 22 characters  | The item number field in F4101 is limited to 25 characters. R31410 looks for the \*OP portion of the outside operation item number to create the purchase order. A parent item number longer than 22 characters leaves insufficient space for the \*OP suffix and operation sequence. See Section 6 for full P4312/P3103 logic. |

**Section 3: System Setup Issues**

Check the following system-level configuration items:

| **#** | **Issue**                           | **Description**                                                                                                                                                                                                                                                                                              |
| ----- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **5** | Short item number set as primary ID | Do not define the short item number as the primary ID in the Branch/Plant Constants if using \*OP item numbers. See Section 7 for the full explanation.                                                                                                                                                      |
| **6** | Order Activity Rules mismatch       | The Order Activity Rules (P40204, accessed from G4241) for Order Type OP and Line Type X must match the document type, line type, and beginning status defined in: (1) Work Order Processing (R31410) Routing tab processing options, and (2) Enter Purchase Orders (P4310) Defaults tab processing options. |
| **7** | Special Handling Code not set to 1  | The Special Handling Code on the outside operation cost component (typically D1 in UDC 30/CA) must be set to **"1"**. This is required for the cost component used for outside operations - it does not have to be D1 specifically, but whatever cost component is used must have Special Handling Code = 1. |

**Section 4: Work Order and Routing Setup Issues**

Check the following work order and routing configuration items:

| **#** | **Issue**                         | **Description**                                                                                                    |
| ----- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **8** | Yield Percent is blank            | The Yield Percent field on the work order routing must be set to **100%**. A blank value will prevent PO creation. |
| **9** | Required routing fields are blank | The following fields on the outside operation routing step must be populated:                                      |

For item 9, verify each of the following:

| **Field**                   | **Requirement**                                                               |
| --------------------------- | ----------------------------------------------------------------------------- |
| **PO Type (RCTO)**          | Must be set to **"Y"**.                                                       |
| **Primary Supplier (VEND)** | Must contain a valid Address Book number.                                     |
| **Cost Type (COST)**        | Must be a valid cost type with Special Handling Code of **"1"** in UDC 30/CA. |

| **#**  | **Issue**                                                | **Description**                                                                                                                                                                           |
| ------ | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **10** | Work order header branch differs from cost center branch | The work order header branch plant is different from the cost center branch (Additional Details 1 tab on the work order header). Valid issue for release **B7332** only. See SAR 4079001. |

**Section 5: Purchase Order and Vendor Setup Issues**

Check the following purchasing and vendor configuration items. For additional reference, see related document **ODS-01-0086 - Defaults Into Purchase Orders**.

| **#**  | **Issue**                                         | **Description**                                                                                                                                                                                                      |
| ------ | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **11** | Item is on the vendor's restriction list          | The item is included in the vendor's list of item restrictions in Purchasing Instructions (P04012, accessed from G43A16).                                                                                            |
| **12** | Tax Rate/Area set with blank Tax Explanation Code | The vendor is configured with a Tax Rate/Area code (TXA2) but a blank Tax Explanation Code (EXR2).                                                                                                                   |
| **13** | PO request date precedes work order start date    | The PO request date is before the work order header start date. Valid issue for release **B7332** only. See SAR 4525293. Also refer to related document **OMN-99-0083 - How Outside Operations are Back-Scheduled**. |

**Section 6: P4312/P3103 (Status Window) Logic**

**6.1 How the System Determines Whether to Call P3103**

The key to understanding the P4312/P3103 behavior is that **the content of the item number does not matter** - only the **number of characters** does.

The logic works as follows:

- P4312 takes the **second item number (LITM)** of the parent item and counts the number of characters.
- It then **removes that number of characters** from the beginning of the \*OP item number.
- It checks whether the **next three characters** equal **"\*OP"**.
- If they do, the item is recognized as an outside operation and P3103 is called. If not, P3103 is not called.

**6.2 Example - Item Number Length Issue**

The maximum length for the second item number (LITM) is **25 characters**.

**Example:** Parent second item number = 1234567890ABCDEFGHIJKLM (23 characters).

R31410 will create the outside operation item number: 1234567890ABCDEFGHIJKLM\*O

When P4312 processes the receipt:

- The system counts 23 characters in the parent LITM.
- It removes the first 23 characters from the \*OP item number: 1234567890ABCDEFGHIJKLM.
- The remaining characters are \*O - the "P" is missing because the total item number length exceeded 25 characters.
- The comparison to "\*OP" fails.
- P3103 is **not called**, resulting in either no IM transaction or a blank IM cardex entry, and on-hand inventory is incorrectly created on the outside operation item number.

**Rule:** The parent second item number must be **22 characters or fewer** to ensure the full \*OP suffix and operation sequence number fit within the 25-character limit.

**Section 7: Using the Short Item Number as the Primary ID**

When R31410 generates the \*OP item number, it uses the **short item number** to construct it - not the second item number. However, when P4312 processes the receipt, it uses the **second item number** character count to identify the \*OP.

**Example:**

- Item: 220
- Short Item Number: 548691
- \*OP item generated by R31410: 548691\*OP10

When P4312 receives the PO:

- It takes the second item number **220**, counts **3 characters**.
- It removes the first 3 characters from the \*OP item number: removes 548.
- The next 3 characters are 691 - not \*OP.
- The item is **not recognized as an outside operation** and P3103 is **not called**.

**Exception:** Using short item numbers as the primary ID would only work correctly if the second item number and the short item number have the same number of characters.

**Recommendation:** Do not define the short item number as the primary ID in Branch/Plant Constants when using \*OP item numbers.

**Section 8: Security**

Insufficient security permissions to the **Item Branch/Plant program (P4102)** will prevent the system from creating a Purchase Order from the Work Order. Verify that the user account running R31410 has the appropriate permissions to P4102.
