**JD Edwards Inventory Reconciliation**

**Training Guide: Cardex Analysis**

**Topic: Weighted Average Cost Calculation Error**

**Section 1: Overview**

This guide documents a weighted average cost calculation error identified during a cardex analysis for a customer. The issue surfaced during a routine review of item transaction history and resulted in a dollar variance between the item ledger and the general ledger. Understanding how to identify this type of error is valuable for any organization running weighted average costing in JD Edwards.

**Section 2: Identifying the Issue**

**2.1 Transaction Data Review**

The following observations were made when reviewing the JD Edwards cardex data exported to Excel, representing the complete transaction history for the item from mid-2020 to mid-2021:

- **Stock Status:** 700 EA on hand
- **Stated Value:** \$390.74
- **Issue Identified:** The unit cost on receipt document **4058804 (OV transaction)** had increased, but the unit costs on the subsequent IT (intercompany transfer) transactions did not reflect the updated cost - they were still processed at the old unit cost.

**2.2 Expected Behavior**

In a weighted average cost scenario, a receipt processed at a cost different from the current running average should trigger an update to the weighted average unit cost. All subsequent transactions should then reflect the updated cost.

In this case, the transfers were processed at the **old cost**, indicating the weighted average was not recalculated at the time of the receipt.

**Section 3: Calculating the Impact**

**3.1 Unit Cost Discrepancy**

Taking the stock status quantities and calculating the implied unit cost produces a value of **\$0.5582**, which was confirmed by checking the cost revisions screen in JD Edwards.

**3.2 Dollar Variance**

Summarizing the extended cost column in the cardex export produces a total of **\$426.58**, not the stated value of **\$390.74**. This represents a **dollar variance of \$35.84** between the item ledger and the general ledger - a direct reconciling item.

**Section 4: Potential Root Causes**

The root cause of the weighted average cost not being updated upon receipt is still under investigation. The following theories are being evaluated:

- **Cost Level Configuration** - In JD Edwards, weighted average cost items under lot control should have their cost level set to **3**. If the cost level is incorrectly set to **2**, the weighted average may not update correctly upon receipt.
- **Barcode Scanning Script Issue** - Receipts at this facility are processed using a barcode gun. A similar situation was previously identified where the script used by the scanning device to process receipts neglected to update the cost properly. This customer uses the same provider and has not updated the scanning software for an extended period of time, making this a likely contributing factor.

**Section 5: Key Takeaway**

Weighted average cost errors of this nature can be difficult to detect without a detailed review of the item's full transaction history in the cardex. The combination of a cost that fails to update on receipt and subsequent transactions processed at the old cost can result in material dollar variances that are not immediately obvious during standard reconciliation.

**Recommendation:** If similar symptoms are observed - such as a unit cost that does not appear to reflect recent receipts, or a discrepancy between the summarized extended cost in the cardex and the stated item value - perform a full cardex export and review the unit cost progression across all transactions. Check the cost level setting for lot-controlled weighted average items, and verify that any third-party scanning or receiving software is processing cost updates correctly.

If you observe a similar issue in your data, document the transaction details and engage your JD Edwards support team to investigate the root cause. Once identified, the corrective action will typically involve a cost restatement and an offsetting journal entry to clear the dollar variance from the general ledger.
