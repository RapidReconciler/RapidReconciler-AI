# Installing the RapidReconciler-Prod Database
## Technical Overview and First Steps

---

## Skill Sets

RapidReconciler is a Microsoft SQL Server based product. Anyone designated to install RapidReconciler should have at least some basic knowledge in:

- Running scripts in SQL Server Management Studio
- SQL Server Database configuration
- SQL Server Agent Job configuration
- SQL Server Integration Services configuration and project deployments

---

## Architecture Overview

RapidReconciler consists of several hardware components. Setup is flexible and can vary based on the needs of the individual customer. The main components are:

- **Database server** running Microsoft SQL Server. Data is extracted using Integration Services (Read Only).
- **Application server** for the installation of the RapidReconciler agent and data services. See *Installing the RR Agent*.
- **User PC** for data access via web browser. The user must be behind the company firewall to view data.
- **Version control server** maintains licensing and control information for RapidReconciler configurations.

### Data Synchronized with the RR Agent

All data stored on GSI servers employs 256-bit encryption and is limited to:

- Public facing IP address of the application server
- Internal IP address of the application server
- IP address of the database server
- Credentials to access the RapidReconciler database
- RapidReconciler database(s) names and port numbers
- Usernames and passwords *(GSI cannot retrieve passwords, only reset them)*
- User access security settings (companies and tabs)
- 5-digit company number and name from JD Edwards *(used for licensing purposes only)*

### Notes

> - If a server is dedicated for RapidReconciler, both the database and agent can be on the same machine.
> - Port 443 outbound is used by RapidReconciler for JMS communications.
> - Work with the customer's I/T support to decide how RapidReconciler will be deployed.
> - Only 1 instance of the Agent can be run on the internal network. The agent can support multiple RapidReconciler databases, even if they are on different servers.

---

## Working with a New Client

When a new customer purchases RapidReconciler, the licensing is based on JD Edwards company numbers (normally 1 license per company). Obtain the following critical information from the sales rep:

- The number of companies purchased
- The exact JD Edwards company numbers (e.g. 00001, 00002, etc.)
- The name of the customer (e.g. Acme Manufacturing)
- The I/T contact email/phone number for the client — send the `RRV7 Technical Requirements.pdf` to them and have them return the requested information from page 3

Arrange a **2-hour web meeting** with the I/T contact in order to:

1. Ensure the server(s) meet the minimum requirements
2. Install the RapidReconciler database and create the `rruser` ID and `RapidReconciler_Prod` SQL Agent job
3. Configure and deploy the SSIS package
4. Perform the initial data load

---

## Application Server Requirements

> If the RR Agent is to be installed on the database server, this step can be skipped.

| Requirement | Details |
|---|---|
| Operating System | Windows Server 2008 or later |
| RAM | 8 GB minimum |
| Credentials | Local administrative credentials for configuration |
| Browser | Internet Explorer 10+ or latest Google Chrome |
| IP Address | Static external IP address |

### Access Requirements *(access by name preferred)*

| Host | IP Address | Ports |
|---|---|---|
| rapidreconciler.getgsi.com | 191.237.24.89 | 80 and 443 outbound |
| rr-valc-spa.cloudapp.net | 23.96.83.121 | 80 and 443 outbound |
| rr-spa.cloudapp.net | 52.170.255.174 | 443 and 8000 outbound |

### Connectivity Tests

- Navigate to `http://rr-spa.cloudapp.net:8000/check-ip` — the public facing IP is returned if port 8000 has been opened.
- Navigate to `rapidreconciler.getgsi.com` — the log in page should appear.

---

## Integration Services Requirements

> If integration services is installed and run on the database server, this step may be skipped.

### SSIS Server

- Windows Server 2008 or later
- 16 GB RAM minimum
- SQL Server Management Studio
- SQL Server Data Tools

### OLE DB Provider

| JDE Data Source | Requirement |
|---|---|
| AS400 / I-Series | I-Series Access (Client Access) — ensure OLE DB component is installed; check OLE DB drivers (not selected by default) |
| Oracle | Oracle 32-bit client (64-bit optional) — select 'Administrator' option, make applicable `tnsnames.ora` entries; if installing both versions, place in the same Oracle home |
| SQL Server | No additional configuration required |

---

## Database Server Requirements

### Minimum Requirements

| Requirement | Details |
|---|---|
| Operating System | Windows Server 2008 or later |
| Processor | Quad core |
| SQL Server | Standard Edition minimum, Version 2012 or later |
| RAM | 16 GB minimum |
| Authentication | Mixed mode |
| Other | Create Integration Services Catalog, SQL Server Management Studio |

### Disk Space

- **100 GB** per 1 million cardex (F4111) records per month
- Estimate covers 1 year of data; records may be purged after year-end close

**Example:** 2,000,000 cardex records/month requires **200 GB** disk space allocated.

### If Installing Integration Services on the Same Database Server

- SQL Server Data Tools *(free download from Microsoft)*
- OLE DB provider — see [Integration Services Requirements](#integration-services-requirements)

### If Installing the RR Agent on the Same Database Server

- Internet Explorer 10+ or latest Google Chrome
- Static external IP address
- Access requirements and connectivity tests — see [Application Server Requirements](#application-server-requirements)

---

## Installing the RapidReconciler Database

### Step 1 — Send the Zip File to the Client

[RRV7 - Build 178](https://github.com/RapidReconciler/rapidreconciler-sql/blob/main/Installation%20Files/RRV7%20-%20Build%20178.zip?raw=true)

Using `github.com/.../raw/main/` instead of `raw.githubusercontent.com` triggers a download prompt rather than displaying the file.
Have the I/T contact download and place the zip file on the database server and unzip the contents. The files will be needed for database and SSIS installation.

### Step 2 — Create the Database

1. Log on to the designated database server with the I/T contact
2. Open SQL Server Management Studio
3. Log in to SSMS with a login that has sys admin privileges
4. Run the database creation script

The script will:
- Create `mdf` and `ldf` files in the default locations specified by the server instance
- Set the initial DB size to **5 GB**
- Create the database with the default name **`RapidReconciler_Prod`**

### Step 3 — Add Database Objects

Run the object creation script in the same SQL Server instance and wait for the **"Successfully Completed"** message.

### Step 4 — Create the SQL User ID

Run the `rruser` login creation script. These are the credentials the application uses to read data from the SQL database.

### Step 5 — Create the SQL Agent Job

Run the SQL Agent job creation script. The job steps will need to be modified and a schedule added — this will be covered when deploying the SSIS package.

---

## Configuring the Integration Services Package

### Obtain Configuration Information

Gather the following JD Edwards-specific information (provided in the Technical Requirements documentation):

#### Variables

| Variable | Data Dictionary Value | Typical Default |
|---|---|---|
| Decimal places for extended cost | ECST | 2 |
| Decimal places for unit cost | UNCS | 4 |
| Decimal places for quantity on hand | PQOH | — |
| Decimal places for transaction quantities in cardex | TRQT | — |

#### JD Edwards Connection

- Name or IP address of the JDE data server or data warehouse
- Credentials for the JDE database *(use `rapidrec`/`rapidrec` if possible)*
- JDE server type: **I-Series**, **Oracle**, or **Microsoft SQL Server**
- Table qualifier name (e.g. `proddta`)

---

## Performing the Initial Data Load

*Refer to the initial data load documentation for next steps.*