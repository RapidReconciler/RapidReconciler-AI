**RapidReconciler**

**Training Manual: Installing a Client in VALC**

**Section 1: Before You Begin**

**1.1 Prerequisites**

Before starting a new client setup in VALC, gather the following information from the sales contract or directly from the customer contact:

- The number of companies purchased (per the license agreement).
- The full name of the customer (e.g., Acme Manufacturing).
- The IT contact's email address and phone number for the client.
- The client's version of JD Edwards (optional - for reference only).

**Section 2: Logging In to VALC**

**2.1 What Is VALC?**

VALC (Version and Licensing Control) is a GSI-developed website hosted on Microsoft Azure where RapidReconciler and Genius customers are managed. New customers must be added in VALC before the installation process can begin. The preliminary setup can be performed prior to installing the database.

**Important:** Adding a customer in VALC is performed by GSI only.

**Login URL:** <https://rr-valc-spa.cloudapp.net>

Use the login credentials that have been provided to you.

**2.2 Navigating VALC**

The main navigation in VALC contains five pages. The first three are RapidReconciler options; the remaining two are for Genius. The Clients page for RapidReconciler is the default page upon login.

**RapidReconciler Pages:**

| **Page**          | **Description**                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| **Clients**       | Where clients are added and maintained. This is the primary setup page.                                      |
| **SQL Scripts**   | Used to deploy updates to the RapidReconciler database. Access is restricted to RR developers only.          |
| **Message Users** | Messages entered here appear in the application each time a user logs in. Messages include expiration dates. |

**Top Right Buttons:**

| **Button**           | **Description**                                                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Create Client**    | Initiates the process of creating a new client record.                                                                           |
| **Status Drop-Down** | Switches the view between active and inactive clients. A client is deactivated when they opt out of their maintenance agreement. |

**Section 3: Step 1 - Create Client Record**

**3.1 Procedure**

Click the **Create Client** button to begin.

**Note:** Once a client record has been created, it cannot be deleted via the application. If a client becomes inactive, use the client details option to mark them as inactive. Active and inactive clients are toggled using the filter to the left of the Create Client button.

Complete the following fields in the Create Client form:

| **Field**                     | **Instructions**                                                                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Client Name**               | Enter the client's full name (e.g., Acme Manufacturing).                                                                                               |
| **Agent I/P Address**         | Leave blank. This will populate automatically during the Agent Installation process.                                                                   |
| **License Start Date**        | Enter today's date.                                                                                                                                    |
| **License End Date**          | Enter the last day of the current calendar year. This must be updated manually each year. Users will be locked out of the application after this date. |
| **Version**                   | Select the latest version from the drop-down. This represents the version of the Agent.                                                                |
| **JDE Version**               | Enter the client's JDE version. This is informational only.                                                                                            |
| **HTTPS**                     | Select **True** from the drop-down. RapidReconciler has been updated to work with HTTPS only.                                                          |
| **Maximum Companies Allowed** | Enter the number of licenses procured per the sales contract.                                                                                          |
| **Agent Protocol**            | Select **SSL** from the drop-down. Offline functionality has not been implemented.                                                                     |

Click **Confirm** when complete.

**3.2 Post-Creation Status**

After confirming the client parameters, a new record will appear in the grid with the following initial values:

| **Field**                    | **Initial Value** | **Notes**                                                                                                      |
| ---------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------- |
| **Status**                   | Disconnected      | Will change to "Connected" once communication with the RR Agent is established.                                |
| **Agent Version**            | Blank             | Will populate once the agent connects.                                                                         |
| **System Status / Messages** | Blank             | Will populate once the database setup on SQL Server is complete and the import job has been run at least once. |
| **Manage Clients icon**      | -                 | Provides access to client details, database settings, company licensing, and user accounts.                    |
| **Manage Deploys icon**      | -                 | Used to deploy updated services to the client.                                                                 |

**Section 4: Step 2 - Create Initial User Record**

**4.1 Overview**

An account associated with the client must be created before the agent can be installed. This account will be used as the credentials during the RR Agent installation.

**4.2 Procedure**

- Click the **Manage Clients** icon for the newly created client.
- Click the **User Accounts** tab.
- Click **New User**.
- Complete the New User pop-up window with the following information:

| **Field**        | **Value**                                                           |
| ---------------- | ------------------------------------------------------------------- |
| **Full Name**    | GSI Admin                                                           |
| **Client Email** | <gsiadmin@clientdomain.com> (e.g., <rradmin@acmemanufacturing.com>) |
| **Password**     | 12345678                                                            |
| **Active**       | Yes                                                                 |

- Click **Confirm**.

A new row for the created user will appear on the User Accounts tab. These credentials will be used to install the RR Agent in the following steps.

**Section 5: Step 3 - Set Initial Modules**

**5.1 Procedure**

Click the **Manage Client** icon and review the following:

| **Field / Setting**   | **Notes**                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Setup Step**        | Will display "Created." This will cycle through steps as the full installation progresses.                                                           |
| **Agent External IP** | Populates automatically during the agent installation process.                                                                                       |
| **Agent Internal IP** | Populates automatically during the agent installation process.                                                                                       |
| **Authorized Tabs**   | Check **Inventory** and **Admin** to start. It is recommended to get the client running on these modules before enabling In Transit and PO Receipts. |

**Section 6: Installing the RapidReconciler Agent**

**6.1 Prerequisites**

You must be logged in on the customer's application server to perform this task. Coordinate a web meeting with the client's IT contact to complete this step.

**Important:** The Setup Step in the client details in VALC must be set to "Created" in order to trigger the agent download prompt.

**6.2 Download and Install the RR Agent**

Follow these steps from the customer's application server:

- Open a web browser and navigate to <https://rapidreconciler.getgsi.com>.
- Log in using the initial RR user credentials created in VALC (Step 2).
- Upon first login, the agent download screen will be displayed.
- Download the applicable version of the agent. In the vast majority of cases, this will be the **64-bit version**.
- Execute the downloaded file and follow the installation prompts.
- Once installed, the web page will complete the installation automatically. The **"Installation Complete"** message will appear once finished. This process may take several minutes.

**6.3 Validating Data**

After the installation has finished, return to the web browser to complete the setup. Within a couple of minutes, the "Validating Data" step will appear, followed by the SQL Server connection properties screen.

**6.4 Validate SQL Server Connection Properties**

When prompted, enter the following SQL Server connection details:

| **Field**     | **Value**                                                                |
| ------------- | ------------------------------------------------------------------------ |
| **Address**   | Enter the internal IP address of the RapidReconciler database server.    |
| **Port**      | Enter the port for the instance. This is normally **1433**.              |
| **User Name** | Enter **rruser** (the default set up during the database creation step). |
| **Password**  | Enter **rruser** (the default set up during the database creation step). |

**6.5 Installation Complete**

Once the database information has been entered, the browser will display a "Deploying" message followed by the **"Installation Complete"** screen. Return to your local machine to verify connectivity in VALC.

**Section 7: Completing VALC Setup**

**7.1 Check Database Settings**

Return to VALC and confirm that all database statuses are showing as **online**.

**7.2 Company Licensing**

Once connectivity has been established and the initial data load is complete, the client's company numbers will be available to license.

- Click the **Manage Client** icon for the applicable client.
- Click the **Companies** tab.
- Check the applicable company numbers in accordance with the purchase agreement.

**Note:** If more than one RapidReconciler database has been configured for the client, company licensing must be completed for each database individually.