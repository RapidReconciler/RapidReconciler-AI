# JD Edwards Item Ledger (Cardex) Reference Guide

## Table F4111 -- Transaction History, Analysis, and Common Errors

---

## Overview

The JD Edwards item ledger -- table F4111, commonly referred to as "The Cardex" -- contains the complete transaction history for items in the inventory system. All transactions that impact an item's quantity on hand are recorded in this table, including receipts, transfers, sales shipments, material issues, completions, and more.

Understanding how to read, analyze, and validate the item ledger is essential for accurate inventory reconciliation. Errors made during cardex analysis are a common source of false variances -- issues that appear to be data integrity problems but are actually the result of incorrect analysis technique.

This guide covers:

- The structure and key fields of the F4111 table
- Common questions about item ledger behavior
- How to correctly analyze the cardex and avoid the three most common analyst errors
- A real-world example of a weighted average cost error identified through cardex analysis
- Best practices for maintaining item ledger integrity

---

## Section 1: F4111 Table Structure and Key Fields

### 1.1 What the Item Ledger Contains

The item ledger stores **transactional data only** -- it does not store running balances. To obtain the total on-hand quantity from this table, all qualifying transactions must be summarized. The actual on-hand balance for each item is stored in table **F41021** -- the Item Location table.

The balances displayed at the top of the item ledger screen are fetched from the following tables:

| Table | Contents |
|---|---|
| **F41021** | Item Location table -- quantity on hand |
| **F4105** | Item Cost table -- unit cost |

### 1.2 Posting Codes (ILIPCD)

The posting code in F4111 is stored in column **ILIPCD**. This field is not displayed by default on the item ledger grid but can be viewed using the JD Edwards **data browser** feature. There are four possible values:

| Posting Code | Description |
|---|---|
| **Blank** | The initial value assigned to all qualifying transactions. Also used for IB transactions created when an item is added to the system. |
| **Y** | Posted by the Item Ledger As-Of Record Generation program (R41542) to the Item ASOF file (F41112). |
| **S** | The value of inventory has not yet been impacted by the transaction. Examples include a ship confirmation transaction before running Sales Update, or an IM document type before Manufacturing Accounting has been run. |
| **X** | The transaction involved a movement of inventory only and had no effect on the general ledger. Examples include an IZ transaction created on a change of lot status. These transactions must be **excluded** when summarizing item ledger totals. |

> **Critical:** Transactions with a posting code of **"X"** must always be excluded from any cardex analysis. Including them will produce an incorrect total that does not match the on-hand balance.

### 1.3 Date Fields

There are two date fields in the item ledger to consider when determining when a transaction entered the system:

| Date Field | Description | Reliability |
|---|---|---|
| **Transaction Date** | The date typically associated with when the transaction occurred. Available on some entry screens and can be overridden by the user. Backdating and data entry errors are both common. | Less reliable |
| **Creation Date** | The date the transaction record was created in F4111. More reliable, with one exception: if Global Item Update is enabled and the second or third item number is changed, all item ledger records for that item will have their creation date updated to the date of the change. | More reliable |

> **Recommendation:** Use the creation date when attempting to determine when a transaction entered the system. However, there is no 100% reliable method for obtaining this information in all scenarios.

### 1.4 DMAAI Information

The item ledger table does **not** store information about which DMAAI entries were used to process a transaction. It is possible to make a reasonable assumption based on the available data points -- company number, document type, GL class code, and knowledge of JD Edwards transaction processing -- but this information cannot be retrieved directly from F4111.

> **Note:** The RapidReconciler Transaction Detail Report can provide DMAAI context by combining item ledger data with the applicable DMAAI configuration at the time of the transaction.

---

## Section 2: Should the Item Ledger Sum Equal the Item Balance Table?

**Yes** -- with the following conditions all being met:

- All transactions with a posting code of **"X"** have been removed from the calculation.
- The transaction quantity is expressed in the item's **current primary unit of measure**.
- The item ledger table has not been purged without leaving a **balance forward record** to maintain continuity.
- No item **conversion factors** have been removed from the system.
- Any changes to an item's **primary unit of measure** were performed using the recommended procedures.

If any of these conditions are not met, a discrepancy between the item ledger summary and the item balance table may exist that is not indicative of a true inventory integrity issue, but rather a data management consideration.

---

## Section 3: How to Correctly Analyze the Cardex

Analyzing the item ledger for integrity issues requires exporting the grid to Excel and summarizing the quantity and extended amount columns, then comparing those totals to the balances displayed at the top of the item ledger screen. Three common errors consistently cause false variances in this process.

### 3.1 Error 1 -- Including Memo Transactions

**The Issue**

Certain transactions in the item ledger do not count toward the on-hand totals and must be filtered out before performing the analysis. These are known as **memo transactions** and include:

- Location adds
- Lot releases
- Manufacturing scrap

Memo transactions are flagged with an **"X"** in the posting code field (ILIPCD). This field is not displayed by default on the item ledger grid.

**Corrective Action**

Before totaling the exported grid, identify and remove all rows where ILIPCD contains **"X"**. Including these transactions in the summary will result in an incorrect total that does not match the on-hand balance.

---

### 3.2 Error 2 -- Ignoring Alternate Units of Measure

**The Issue**

After exporting the item ledger grid, analysts must review the transaction unit of measure column to determine whether more than one UOM is referenced. The on-hand quantity total displayed at the top of the screen is always expressed in the **primary unit of measure**.

Any transaction recorded in a unit of measure other than the primary UOM must be **converted to the primary UOM** before totals are compared. Failing to do so produces an "apples to oranges" comparison and will make it appear that a variance exists when there may not be one.

**Corrective Action**

- After exporting the grid, scan the transaction UOM column and identify any rows not in the primary UOM.
- Apply the appropriate conversion factor to bring those quantities into the primary UOM.
- In later versions of JD Edwards, a grid column labelled **"Quantity in Primary"** may be available. If present, use this column for the analysis -- manual conversion will not be required.

---

### 3.3 Error 3 -- Incorrect Analysis Level for Average Cost Items

**The Issue**

Analyzing average cost items requires a different approach than standard cost items, and the correct method depends on the **item's cost level setting**.

- **Standard Cost Items** -- Analysis is performed at the lot level. Each combination of item, branch, location, and lot should summarize accurately to the balance shown at the top of the screen.
- **Average Cost Items** -- The analysis must be performed in accordance with the item's cost level setting.

**Cost Level Rules for Average Cost Items**

| Cost Level | Required Analysis Approach |
|---|---|
| **Cost Level 2** | The location and lot filter fields at the top of the item ledger screen must be populated with **"\*"** (wildcard). The analysis must include all locations and lots together -- individual location or lot filtering is not valid at this cost level. |
| **Cost Level 3** | A specific location and lot may be specified in the filter. Analysis can be performed at the individual location and lot level. |

> **Important:** If a Cost Level 2 item is analyzed by filtering to a specific location or lot, an apparent discrepancy may be identified that is actually offset by transactions in another location. This is not a true variance -- it is a result of analyzing the data at the wrong level.

---

### 3.4 Summary of the Three Common Errors

| Error | Root Cause | Corrective Action |
|---|---|---|
| **Memo Transactions Included** | Transactions flagged with "X" in ILIPCD are included in the summary total | Identify and remove all memo transactions before totaling the grid |
| **Alternate UOM Not Converted** | Transactions in non-primary units of measure are included without conversion | Convert all non-primary UOM transactions to primary UOM, or use the "Quantity in Primary" column if available |
| **Incorrect Cost Level for Average Cost Items** | Average cost items analyzed at the wrong level produce misleading variance results | For Cost Level 2 items, use a wildcard (\*) for location and lot filters; for Cost Level 3, individual filtering is valid |

---

## Section 4: Real-World Example -- Weighted Average Cost Calculation Error

This section documents a weighted average cost calculation error identified during a cardex analysis. Understanding this type of error helps analysts recognize similar patterns in their own data.

### 4.1 The Situation

During a routine review of item transaction history for a customer, the following observations were made when reviewing cardex data exported to Excel, covering the complete transaction history from mid-2020 to mid-2021:

- **Stock Status:** 700 EA on hand
- **Stated Value:** $390.74
- **Issue Identified:** The unit cost on receipt document **4058804 (OV transaction)** had increased, but the unit costs on subsequent IT (intercompany transfer) transactions did not reflect the updated cost -- they were still processed at the old unit cost.

### 4.2 Expected Behavior

In a weighted average cost scenario, a receipt processed at a cost different from the current running average should trigger an update to the weighted average unit cost. All subsequent transactions should then reflect the updated cost.

In this case, the transfers were processed at the **old cost**, indicating the weighted average was not recalculated at the time of the receipt.

### 4.3 Calculating the Impact

Taking the stock status quantities and calculating the implied unit cost produces a value of **$0.5582**, confirmed by checking the cost revisions screen in JD Edwards.

Summarizing the extended cost column in the cardex export produces a total of **$426.58**, not the stated value of $390.74. This represents a **dollar variance of $35.84** between the item ledger and the general ledger -- a direct reconciling item.

### 4.4 Potential Root Causes

| Theory | Description |
|---|---|
| **Cost Level Configuration** | Weighted average cost items under lot control should have their cost level set to **3**. If incorrectly set to **2**, the weighted average may not update correctly upon receipt. |
| **Third-Party Scanning Script** | Receipts at this facility were processed using a barcode gun. A similar issue was previously identified where the script used by the scanning device neglected to update the cost properly. The customer was using the same provider and had not updated the scanning software for an extended period, making this a likely contributing factor. |

### 4.5 How to Identify This Type of Error

Symptoms to watch for:

- A unit cost that does not appear to reflect recent receipts
- A discrepancy between the summarized extended cost in the cardex and the stated item value
- Subsequent transactions processed at a cost that predates a receipt with a different cost

**Recommended steps when these symptoms are observed:**

1. Perform a full cardex export and review the unit cost progression across all transactions.
2. Check the **cost level setting** for lot-controlled weighted average items -- it should be **3**.
3. Verify that any third-party scanning or receiving software is processing cost updates correctly.
4. Document the transaction details and engage your JD Edwards support team to investigate the root cause.
5. Once identified, the corrective action will typically involve a **cost restatement** and an **offsetting journal entry** to clear the dollar variance from the general ledger.

---

## Section 5: Best Practices for Item Ledger Integrity

| Topic | Best Practice |
|---|---|
| **Memo transactions** | Always exclude ILIPCD = "X" records from any cardex analysis |
| **Unit of measure** | Always verify the UOM column before totaling; convert non-primary UOM quantities before comparing |
| **Average cost analysis level** | Match the analysis level to the item's cost level setting -- wildcard for Cost Level 2, specific lot/location for Cost Level 3 |
| **Weighted average cost** | Do not allow on-hand quantities to go negative; verify cost level is set to 3 for lot-controlled items |
| **Third-party integrations** | Periodically verify that scanning and receiving software is correctly triggering cost updates in JD Edwards |
| **Purging** | Never purge the item ledger without leaving a balance forward record to maintain continuity |
| **UOM changes** | Follow the recommended procedure when changing the primary unit of measure -- see the [UOM Reference Guide](../MDS/uom-reference-guide.md) |
| **DMAAI tracing** | Use RapidReconciler Transaction Detail Report to identify which DMAIs were used for a transaction when standard JDE tools cannot provide this |
| **Period-end analysis** | Run cardex analysis before period-end close to identify and resolve integrity issues before they become reconciling items |

---

## Section 6: How RapidReconciler Helps

Analyzing the item ledger manually in JD Edwards is time-consuming, technically demanding, and prone to the errors described in this guide. RapidReconciler by GSI is purpose-built to eliminate these challenges by automating the reconciliation process and surfacing item ledger issues in a clear, actionable interface.

### 6.1 Continuous Reconciliation vs. Point-in-Time Analysis

The manual cardex analysis process produces a snapshot at a single point in time. If a transaction posts after the analysis is run, the work must be repeated. RapidReconciler updates automatically with each nightly import cycle, providing a **continuous, up-to-date view** of inventory value against the general ledger without requiring manual intervention.

### 6.2 Posting Code Filtering -- Handled Automatically

One of the most common analyst errors -- including memo transactions (ILIPCD = "X") in the summary -- is handled automatically by RapidReconciler. The application excludes non-posting transactions from all reconciliation calculations, eliminating the risk of false variances caused by this error.

### 6.3 Unit of Measure Handling

RapidReconciler reads quantity data directly from the JD Edwards tables and applies the correct unit of measure conversions automatically. Analysts do not need to manually identify non-primary UOM transactions or apply conversion factors before comparing totals -- the application handles this consistently for every item and every transaction.

### 6.4 Cost Level Awareness for Average Cost Items

RapidReconciler respects the cost level configuration for each item, ensuring that average cost items are analyzed at the correct level (Cost Level 2 or Cost Level 3) without requiring the analyst to manually set wildcard filters or manage analysis boundaries. This eliminates the third common analyst error entirely.

### 6.5 Weighted Average Cost Variance Detection

The type of weighted average cost error described in Section 4 -- where a receipt fails to trigger a cost update and subsequent transactions are processed at the old cost -- can persist undetected for months in a manual reconciliation environment. RapidReconciler surfaces dollar variances between the item ledger and the general ledger automatically, allowing these issues to be identified and investigated as they occur rather than at period end.

### 6.6 DMAAI Traceability

As noted in Section 1.4, JD Edwards does not store DMAAI information in the item ledger. The **RapidReconciler Transaction Detail Report** bridges this gap by combining item ledger data with the applicable DMAAI configuration at the time of each transaction. This allows analysts to quickly determine which GL accounts were impacted by a transaction and whether the correct DMAAI entries were used -- without manually cross-referencing multiple JD Edwards screens.

### 6.7 Drill-Down from Variance to Transaction

When a reconciling item is identified, RapidReconciler allows users to drill down directly from the variance to the underlying JD Edwards transactions. This eliminates the need to navigate between multiple JD Edwards applications -- Item Ledger, Account Ledger, Cost Revisions, and DMAAI -- to trace the source of a discrepancy. The full transaction context is available in a single view.

### 6.8 Summary of RapidReconciler Benefits for Cardex Analysis

| Manual JDE Approach | RapidReconciler |
|---|---|
| Point-in-time snapshot; must be repeated each period | Continuous reconciliation updated each import cycle |
| Memo transactions (ILIPCD = "X") must be manually excluded | Excluded automatically |
| Non-primary UOM transactions must be manually converted | Handled automatically |
| Average cost level must be manually configured per analysis | Respected automatically per item cost level setting |
| Weighted average cost errors may go undetected for months | Surfaced automatically as dollar variances |
| DMAAI information not available in F4111 | Transaction Detail Report combines item ledger with DMAAI context |
| Tracing variances requires navigating multiple JDE applications | Single drill-down from variance to underlying transaction |

> For more information on RapidReconciler, contact [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com).

---

## Section 7: Related Documentation

- [DMAAI Reference Guide](../MDS/dmaai-reference-guide.md)
- [Product Costing Reference Guide](../MDS/product-costing-reference.md)
- [GL Class Code Management and Change Procedures](../MDS/gl-class-code-changes.md)
- [UOM Reference Guide](../MDS/uom-reference-guide.md)
- [Stock Status and Trial Balance Reconciliation](../MDS/stock-status-trial-balance.md)