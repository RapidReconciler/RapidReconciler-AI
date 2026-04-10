**JD Edwards Inventory**

**Training Guide: Item Master Maintenance**

**Topic: A "Gotcha" on Using Global Item Update**

**Section 1: Overview**

Global Item Update in JD Edwards is a feature that transfers changes made to the second item number (LITM) or third item number in the item master table F4101 to all other inventory tables that contain the same information.

The processing options for program P4101 provide the following three options for triggering these updates:

| **Setting** | **Behavior**                                 |
| ----------- | -------------------------------------------- |
| **Blank**   | Do not transfer the changes to other tables. |
| **1**       | Transfer changes to all applicable tables.   |
| **2**       | Transfer changes to selected tables only.    |

When option 2 is selected, the specific tables to be updated are defined in UDC table **40/IC**, which by default lists **57 tables** to be updated. The item ledger (F4111) is one of the tables included in this list - logically, since it contains the second and third item numbers and must be kept in sync with the item master.

**Section 2: The "Gotcha" - Creation Date Override**

**2.1 What Happens**

When Global Item Update is run following a change to the second or third item number, the program updates the matching records across all designated tables. The unintended consequence is that the **Creation Date field (ILCRDJ)** is also updated to the date the change was made - for **every record** in the item ledger for that item.

The program responsible for this update is **R41803**.

**2.2 Why This Is a Problem**

The creation date in the item ledger serves as the most reliable indicator of when a transaction was originally entered into the system. Unlike the transaction date, which can be manually overridden by users, the creation date is system-generated and generally cannot be altered through normal processing.

However, once Global Item Update is run, all item ledger records for the affected item will show the date of the item number change as their creation date - regardless of when the original transactions actually occurred. This makes it extremely difficult or impossible to determine when specific transactions were entered into the system.

**Important:** There is no "date updated" field or other reliable date field in the item ledger that can be used as an alternative once the creation date has been overwritten. The original transaction entry dates are effectively lost.

**Section 3: Impact on Transaction History**

The loss of accurate creation dates has the following practical impacts:

- **Transaction dating** - Determining when a specific inventory transaction was entered into the system becomes unreliable for all historical records on the affected item.
- **RapidReconciler date logic** - RapidReconciler uses the creation date as part of its period assignment logic for item ledger records. If creation dates are overwritten, historical period assignments may be affected.
- **Audit and compliance** - In environments where transaction timestamps are required for audit or regulatory purposes, overwritten creation dates may create gaps in the audit trail.
- **Reconstruction of history** - Once the change is made and Global Item Update is run, it may not be possible to reconstruct an accurate transaction history for the affected items.

**Section 4: Key Takeaway and Recommendation**

**Critical Warning:** Understand the full impact of Global Item Update before making any changes to a second or third item number in the item master. Once the change is made and the update program is run, the creation dates on all item ledger records for that item will be overwritten and the original transaction history cannot be reliably reconstructed.

The following precautions are recommended:

- **Evaluate necessity** - Before changing a second or third item number, confirm that the change is truly necessary and that the business benefit outweighs the loss of transaction date history.
- **Document before changing** - If the change must be made, export and archive the full item ledger history for the affected item before running Global Item Update, preserving a record of the original creation dates.
- **Consider the scope** - In environments with large transaction volumes, even a single item number change can overwrite thousands of item ledger records. Assess the full scope of impact before proceeding.
- **Notify stakeholders** - Inform reconciliation teams, cost accountants, and auditors before making the change, as it may affect period-end reporting and reconciliation accuracy.
