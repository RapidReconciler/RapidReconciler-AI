**RapidReconciler**

**Training Guide: Account Management**

**Topic: How to Add an Inventory Account**

**Section 1: Overview**

Inventory accounts cannot be added directly within the RapidReconciler application. All account additions must be made through the **DMAAI model table in JD Edwards**. RapidReconciler then picks up the new account during the next scheduled refresh cycle.

The default model table used for inventory accounts is **DMAAI table 4152** with document type **PI**.

**Note:** The default document type of PI may have been changed for your organization. Check with your RapidReconciler administrator to confirm the correct document type before proceeding.

**Section 2: Process for Adding an Inventory Account**

**2.1 Step-by-Step Procedure**

Follow these steps to add a new inventory account in RapidReconciler:

- **Log in to JD Edwards.**
- **Navigate to the DMAAI screen** (Account Revisions).
- **Inquire on table 4152**, filtering on your model document type (typically PI).
- **Create a new entry** using the following fields:

| **Field**          | **Description**                                                               |
| ------------------ | ----------------------------------------------------------------------------- |
| **Company Number** | The company number associated with the new account.                           |
| **GL Class Code**  | The GL class code for the inventory items to be associated with this account. |
| **Business Unit**  | The business unit component of the account number.                            |
| **Object Account** | The object account component of the account number.                           |
| **Subsidiary**     | The subsidiary component of the account number, if applicable.                |

**2.2 Additional Requirements**

In addition to creating the DMAAI entry, the following conditions must be met before the new account will appear in RapidReconciler:

- **Inventory transaction activity must exist** - There must be at least one inventory transaction for an item with the associated GL class code. The account will not appear in the filter list without transaction activity.
- **A RapidReconciler refresh cycle must be run** - The nightly import job must complete at least one full cycle after the DMAAI entry has been created and transaction activity exists.
- **Manual refresh if needed** - If the account still does not appear after the refresh cycle has completed, click the **refresh icon** in the top right corner of the account filters on the RapidReconciler reconciliation page to force the filter list to reload.
