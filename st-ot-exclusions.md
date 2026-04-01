**JD Edwards In Transit**

**Training Guide: ST/OT Transfer Orders**

**Topic: Exclusions in RapidReconciler**

**Section 1: Overview of ST/OT Transfer Orders and the In Transit Account**

ST/OT transfer orders in JD Edwards are used to move materials between branch plants (A to B) within the same company. The process uses a clearing account to hold the value of goods while they are in transit.

This In Transit balance sheet account differs from a standard perpetual inventory account in an important way: while goods are in transit, the quantities on hand are removed from the perpetual counts and exist only as a balance in the clearing account. Once the items are received at the destination branch, the clearing account is relieved and the perpetual balance is restored.

**Section 2: The Problem - Unbalanced Transfer Orders**

**2.1 What Is an Unbalanced Transfer?**

An unbalanced transfer order occurs when the quantity or amount received does not match what was shipped, yet both the sales order (ST) and the purchase order (OT) have been fully closed.

Since In Transit is calculated as **Quantity Shipped minus Quantity Received**, any unbalanced transfer will remain open in perpetuity in JD Edwards. There is no standard process within JD Edwards to balance these transactions once both orders are closed.

**2.2 Impact on Reconciliation**

Unbalanced transfer orders create a direct challenge when reconciling the In Transit GL account. The remaining balance has no corresponding open order activity to clear it, and no further processing can be performed in JD Edwards to resolve it.

**Example Scenario:**

For two items on a transfer order, the receipt quantity exactly offsets the shipped quantity - however, the receipt amount is greater than the amount shipped. Both the ST and OT orders carry a status of **999**, meaning no additional processing can be performed in JD Edwards on either order.

**Section 3: The Solution - Order Exclusion in RapidReconciler**

**3.1 What Is the Exclusion Process?**

RapidReconciler includes an Order Exclusion feature specifically designed to handle unbalanced transfer orders that cannot be resolved through standard JD Edwards processing.

Flagging an order pair using the Exclusion feature accomplishes the following:

- The excluded amounts are **summarized in the Variance Calculation section** of the In Transit Reconciliation page, isolating the unbalanced amount as a distinct variance source.
- This summarized amount allows the user to identify the exact value of the offsetting journal entry needed to bring the In Transit GL account back into balance.
- Individual exclusions are also listed in the **In Transit As-Of transaction details**, providing a complete audit trail of all excluded order activity.

**3.2 How to Perform an Exclusion**

- Navigate to the **In Transit Orders page** in RapidReconciler.
- Identify the order pair with an unbalanced quantity or amount where both the ST and OT orders are at status 999.
- Flag the order pair using the **Exclusion** process.
- Review the updated Variance Calculation section - the excluded amount will now appear as an Exclusions variance line item.
- Use the summarized exclusion amount to prepare and post the appropriate offsetting journal entry in JD Edwards.

**Section 4: Key Benefits of the Exclusion Process**

The Order Exclusion feature in RapidReconciler provides the following capabilities that are not available through standard JD Edwards functionality:

- **Identification** - Surfaces unbalanced transfer orders that would otherwise remain undetected within the In Transit account balance.
- **Tracking** - Maintains a visible record of all excluded orders, including the quantities and amounts involved.
- **Correction** - Enables the preparation of accurate offsetting journal entries to clear the unbalanced amounts from the In Transit GL account.
- **Audit Trail** - Individual exclusion details are listed in the In Transit As-Of transaction details, supporting period-end documentation and audit requirements.

**Section 5: Key Takeaway**

Unbalanced transfer orders are a common occurrence in JD Edwards environments where high-volume or complex transfer activity takes place. Because JD Edwards provides no native mechanism to resolve these situations once both orders are closed, the RapidReconciler Exclusion process fills a critical gap in the reconciliation workflow.

**Best Practice:** As part of the monthly In Transit reconciliation, review the Orders page for any order pairs at status 999 with remaining open quantities or amounts. Use the Exclusion process to isolate these items, prepare the appropriate journal entry, and maintain a clean and accurate In Transit GL account balance.
