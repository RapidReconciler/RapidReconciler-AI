**Reference Guide: How to Set Up a Branch/Plant in JD Edwards**

**Step-by-Step Configuration Guide**

**Section 1: Overview**

Setting up a new Branch/Plant in JD Edwards OneWorld requires completing four steps in the following order:

- Add the Address Book Number
- Set up the Business Unit
- Set up Branch/Plant Constants
- Update the Default Branch/Plant on the Address Book Number

Each step must be completed before proceeding to the next.

**Section 2: Step 1 - Add the Address Book Number**

**2.1 Navigation**

Go to menu **G01** and open **Address Book Revisions (P01012)**.

**2.2 Procedure**

- Click **Add** and enter the following values:

| **Field**          | **Value**                                         |
| ------------------ | ------------------------------------------------- |
| **Address Number** | 730                                               |
| **Alpha Name**     | New Address Book                                  |
| **Search Type**    | F                                                 |
| **Business Unit**  | 1 _(temporary value - will be updated in Step 4)_ |

- Click on the **Mailing** tab and fill in the street address and mailing name.
- Click on the **Additional** tab and set the following values:

| **Field**       | **Value** |
| --------------- | --------- |
| **Payables**    | Y         |
| **Receivables** | Checked   |
| **Employee**    | Blank     |

- All other fields can be left at their default values.
- The system will automatically display the **Supplier Master** and **Customer Master** screens. Click **OK** on both screens to accept the default values for the initial Branch/Plant setup.

**Note:** A Search Type warning message may appear. Click **OK** to dismiss it and continue.

**Section 3: Step 2 - Set Up the Business Unit**

**3.1 Create the Business Unit Record**

**Navigation:** Go to menu **G09411** and open **Business Units By Company (P0006)**.

- Inquire on the applicable Company (e.g., 100, 200, etc.).
- Highlight an existing row and click **Copy**.
- Enter the following information and click **OK**:

| **Field**                              | **Value**               |
| -------------------------------------- | ----------------------- |
| **Business Unit**                      | BP10                    |
| **Description**                        | New Distribution Center |
| **Address Number** _(More Detail tab)_ | 730                     |

**3.2 Copy Accounts to the New Business Unit**

**Navigation:** Still on menu **G09411**, open **Accounts By Business Unit (P0901)**. Take the **Accounts By Business Unit** row exit.

- Inquire on an existing Branch/Plant that has a similar financial and accounting setup to the new Branch/Plant being created.
- Click the **Copy Accounts** form exit.
- Enter the new Branch/Plant code in the **"To Business Unit"** field.
- Click **OK**.

**Note:** If Interactive Mode is selected, a message will appear indicating that the process may take a significant amount of time. Once the accounts have been added, a confirmation window will display the number of accounts added. Click **OK** to continue.

**Section 4: Step 3 - Set Up Branch/Plant Constants**

**Navigation:** Go to menu **G4141** and open **Branch Plant Constants (P41001)**.

- Inquire on any existing Branch/Plant in the QBE line.
- Highlight the row and click **Copy**.
- Enter the following information:

| **Field**          | **Value** |
| ------------------ | --------- |
| **Branch/Plant**   | BP10      |
| **Address Number** | 730       |

- Review and update all remaining fields to reflect the specific business requirements for the new Branch/Plant.

**Section 5: Step 4 - Update the Default Branch/Plant on the Address Book Number**

**Navigation:** Go to menu **G01** and open **Address Book Revisions (P01012)**.

- Inquire on Address Book Number **730**.

**Note:** Be sure to clear the default Search Type field before querying to ensure the record is retrieved correctly.

- Click **Select** to open the record.
- Change the **Business Unit** field from the temporary value of **"1"** to the new Branch/Plant code **"BP10"**.
- Save the record.

The Branch/Plant setup is now complete. The Address Book record, Business Unit, chart of accounts, and Branch/Plant Constants are all linked and configured for use.
