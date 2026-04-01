**RapidReconciler**

**Technical Guide: Server Migration**

**Process Steps for Dedicated and Separate Server Configurations**

**Section 1: Overview**

This guide covers the steps required to migrate the RapidReconciler environment to a new server. There are two migration scenarios depending on the server architecture:

- **Dedicated Server** - The application (Agent) and database are hosted on the same server.
- **Separate Servers** - The Agent and database are hosted on different servers.

Both scenarios require a final VALC and Cloudflare update to complete the migration.

**Section 2: Dedicated Server Migration**

**2.1 Software Prerequisites**

Ensure the following are in place on the new server before beginning:

- SQL Server Standard Edition (minimum)
- Administrator access to complete all required tasks
- Integration Services installed
- RapidReconciler folder added to SSISDB
- RRUSER account added (via script)
- SQL Server Data Tools installed
- Applicable JDE database drivers (AS/400 or Oracle)

**2.2 Migration Process**

Follow these steps in order:

**Step 1 - Database Backup and Restore**

- Back up the current production RapidReconciler database on the old server.
- Restore the RapidReconciler database on the new server.
- Add the RRUSER SQL Authentication login on the new server using the script from the old server.

**Step 2 - SSIS Package Migration**

- Locate the SSIS package file (.dtsx) on the old server and copy it to the new server.
- Update and deploy the SSIS package to SQL Server using the following procedure:
  - Open **SQL Server Data Tools** using the Integration Services template.
  - Create a new project named **"RapidReconciler"**.
  - Add the copied .dtsx package to the project.
  - Update the source and destination connection strings.
  - Test all connections to confirm they are valid.
  - Deploy the package to the **SQL Server SSISDB RapidReconciler folder**.

**Step 3 - SQL Agent Job**

- Create the RapidReconciler job in SQL Agent using the script from the old server.
- Configure the job settings accordingly.

**Step 4 - Obtain IP Addresses for VALC**

- Navigate to the RapidReconciler log file on the new server.
- Note the following IP addresses for use in the VALC update (Section 4):
  - Internal IP address
  - External (public-facing) IP address

**Section 3: Separate Servers Migration**

**3.1 Application Server**

**Software Prerequisites**

- SQL Server Management Studio
- SQL Server Data Tools
- RapidReconciler Agent
- Applicable JDE database drivers (AS/400 or Oracle)

**Application Server Process**

**Step 1 - SSIS Package**

- Locate the SSIS package file (.dtsx) on the old server and copy it to the application server.

**Step 2 - Install the RR Agent**

**Note:** VALC status must be changed to **"Created"** before installing the agent.

- Navigate to <https://rapidreconciler.getgsi.com>.
- Enter the **GSIADMIN** credentials.
- Download and install the RapidReconciler Agent.

**Step 3 - Obtain IP Addresses**

- Navigate to the RapidReconciler log file.
- Note the Internal and External IP addresses (required for VALC update).

**Step 4 - Deploy SSIS Package**

- Open **SQL Server Data Tools** using the Integration Services template.
- Create a new project named **"RapidReconciler"**.
- Add the copied .dtsx package to the project.
- Update the source and destination connection strings.
- Test all connections to confirm they are valid.
- Deploy the package to the **SQL Server SSISDB RapidReconciler folder** on the database server.

**3.2 Database Server**

**Software Prerequisites**

- SQL Server Standard Edition (minimum)
- Administrator access to complete all required tasks
- Integration Services installed
- RapidReconciler folder added to SSISDB
- Applicable JDE database drivers (AS/400 or Oracle)

**Database Server Process**

- Back up the current production RapidReconciler database on the old server.
- Restore the RapidReconciler database on the new database server.
- Add the RRUSER SQL Authentication login using the script from the old server.
- Create the RapidReconciler SQL Agent job using the script from the old server.

**Section 4: Update VALC and Cloudflare**

This section applies to both migration scenarios and must be completed after the server work is finished.

**4.1 Update VALC**

- Navigate to the **Client Details** page in VALC and update both the **Internal IP** and **External IP** addresses for the client.
- Navigate to the **Databases** page in VALC and update the **Internal IP** address.

**4.2 Update Cloudflare**

Contact **Daren** to update the IP address in Cloudflare. Provide the following information:

- **Domain URL** - from the Client Details page in VALC.
- **Internal IP** - from the Client Details page in VALC.

**Important:** Data will not appear in the RapidReconciler UI until the Cloudflare update is in place.

**4.3 Install the RR Agent (if not already completed)**

**Note:** VALC status must be changed to **"Created"** before installing the agent.

- Navigate to <https://rapidreconciler.getgsi.com>.
- Enter the **GSIADMIN** credentials.
- Download and install the RapidReconciler Agent.

**4.4 Test Results**

- Log in to the RapidReconciler UI using the GSIADMIN credentials.
- Confirm that the applicable data appears correctly in the interface.
