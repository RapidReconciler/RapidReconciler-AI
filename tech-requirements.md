 
TABLE OF CONTENTS

RR Database Server	2
Integration Services	3
RR Application Server	3
End User PC	3
JD Edwards information	4
Table Listing	5
APPENDIX A – Creating the Integration Services catalog	6
Create the catalog	6
Creating the project folder	6
APPENDIX B – Proof of Concept requirements	7

RR DATABASE SERVER
In most cases existing servers running Microsoft SQL Server will meet minimum requirements. If a new server needs to be built use the guidelines below:
1)	Windows Sever 2019 or later
2)	Quad core processor
3)	Microsoft SQL Server:
- 	a.	Version 2019 or later
- 	b.	16GB RAM minimum
- 	c.	Standard Edition minimum
- 	d.	Mixed mode authentication
- 	e.	Set the default locations for the database and log files
- 	i.	20 GB for initial data file size
- 	ii.	10 GB for initial log file size
- 	f.	SQL Administrative access to the server instance
- 	g.	SQL based log in and role created during installation for user connectivity
- 	h.	SQL Server 2019 and later – Create Integration Services Catalog. See Appendix.
4)	Recommended weekly backup of RapidReconciler database.
5)	Estimated disk space:
	a.	100GB per 1M cardex (F4111) records per month
	b.	Estimate covers 1 year of data. Records may be purged after year end close.
	c.	Example: 2,000,000 cardex records per month requires 200GB disk space allocated
6)	Note the IP address of the database server:								
7)	If using a named instance, note the listening port number						

INTEGRATION SERVICES
Integration services is typically installed and run on the database server. However, in certain cases, it may be preferable to run on an alternate server. The OLEDB provider must be installed on the server running the services:
1)	Alternate server:
	a.	Windows Server 2012 or later
	b.	16GB RAM minimum
2)	SQL Server management tools:
	a.	SQL Server Management Studio
	b.	Visual Studio Community 2019 or later
3)	OLE DB provider (as applicable):
	a.	Data is on an AS400: I-Series Access (Client Access).
		i.	Ensure the OLE DB component is installed on the hard drive.
		ii.	Check OLE DB drivers as it is not selected by default
	b.	Data is on Oracle: Oracle 32 client:
		i.	Select the ‘Administrator’ option.
		ii.	Make applicable tnsnames.ora entries.
		iii.	Both versions in same Oracle home.
	c.	Data is on SQL Server: No additional configuration is required.

RR APPLICATION SERVER
1)	It is highly recommended to use a dedicated server.
2)	Windows Sever 2019 or later.
3)	16GB RAM Minimum.
4)	Local administrative credentials for configuration.
5)	Microsoft Edge or Google Chrome.
6)	Static IP address.
7)	Internal access via database port(s) assigned during installation
	a.	Port range: 32145-49152.
	b.	url: rrprod-[companyname].getgsi.com (Please provide internal IP of app server)
8)	External access (443) by name preferred:
	a.	rapidreconciler.getgsi.com - 191.237.24.89
	b.	rr-valc-spa.cloudapp.net - 23.96.83.121 ( rr-valc-spa.cloudapp.net/check-ip returns external IP).
	c.	rr-spa.cloudapp.net - 52.170.255.174 

END USER PC
1)	Windows XP or later, MAC OSX 10.9 or later
2)	8GB RAM minimum
3)	Screen resolution 1280 x 800 minimum recommended
4)	Browsers: Microsoft Edge, Chrome, Firefox, Safari
5)	Internet access to https:\\rapidreconciler.getgsi.com
6)	Access to application server

JD EDWARDS INFORMATION
The information below is needed for product configuration. Record your values in the space provided.
1)	Variables:
	a.	Decimal places used for extended cost (Data dictionary value ECST). This is normally 2.    		
	b.	Decimal places used for unit cost (Data dictionary value UNCS). This is normally 4.		
	c.	Decimal places used for quantity on hand (Data dictionary values PQOH).			
	d.	Decimal places used for transaction quantities in cardex (Data Dictionary TRQT). 		
2)	JD Edwards connection:
	a.	Name or I/P address of the JDE data server or data warehouse.				
	b.	Credentials for the JDE database. (Use rapidrec/rapidrec if possible).				
	c.	JDE Server is I-Series, Oracle, or Microsoft SQL Server?
	d.	The table qualifier name to be used (e.g. proddta) 						
 
TABLE LISTING
The tables in the list below are accessed by RapidReconciler in “Read Only” mode.

Table	Description
F0006	Business Unit Master
F0008	Date Patterns
F0010	Company Master
F0011	Batch Headers
F0013	Currency Codes
F0015	Exchange Rates
F0101	Address Book (Vendor Names Only)
F0901	Account Master
F0902	Account Balances
F0911	Account Ledger
F1113	Currency Restatement
F30026	Cost Components
F3106	Work Order Cross Ref
F4095	D/M Accounting Instructions
F4096	Flex Accounting Rules
F41001	Inventory Constants
F41002	UOM Conversions
F41003	Standard Conversions
F4101	Item Master
F4102	Item Branch
F41021	Item Location
F4105	Cost Ledger
F4108	Lot Master
F4111	Item Ledger
F4211	Sales Order Details
F42119	Sales Order History
F4311	Purchase Order Details
F43121	Purchase Receipts
F4801	Work Order Headers
 
APPENDIX A – CREATING THE INTEGRATION SERVICES CATALOG
CREATE THE CATALOG
To create an Integration Services catalog connect to a SQL Server instance in SSMS (SQL Server Management Studio) and right click on the Integration Services node under the connected server in the Object Explorer and click on Create Catalog as shown below:
By default the catalog name appears as SSISDB and cannot be changed. You need to provide a strong password for the SSISDB Integration Services catalog you are creating which is used for the database master key. For encryption, it needs to have a database master key and for that only you need to provide a password here. It's recommended to back up the database master key after the Integration Services catalog creation.
Once an Integration Services Catalog gets created you can verify it in SSMS as shown below. An Integration Services Catalog stores application data in a SQL Server database and hence a database has been created with the same name as the Integration Services Catalog. If you browse through the database you will notice there are several tables which store the data, several views built on top of these tables and several stored procedure to access and manage this data.
The Integration Services catalog uses CLR based stored procedures and by default CLR is not enabled for a SQL Server instance, so you need to enable it before creating an Integration Services catalog. Be sure the ‘Enable CLR Integration’ box is checked.

CREATING THE PROJECT FOLDER
To create a folder, right click on the Integration Services Catalog name under Integration Services node in SSMS as shown above and click on the Create Folder menu item. This will launch the Create Folder dialog box; specify the name ‘RapidReconciler’ for the folder and a folder description if desired. The RapidReconciler SSIS package may now be deployed to the server and scheduled.
 
APPENDIX B – PROOF OF CONCEPT REQUIREMENTS
The steps for providing the data to GSI are as follows:
1)	Create an empty database in Microsoft SQL Server 2012 minimum.
2)	Using the ETL tool of your choice, run each of the select statements below.
3)	The destination tables must have the same naming conventions as the original JDE tables.
4)	Once complete, please make a compressed backup of the database.
5)	Please email rrsupport@getgsi.com for data transfer instructions.
6)	Our sales team will contact you to schedule the results presentation.

Table	Description	Select Statement
F0006	Business Unit Master	Select * From F0006
F0008	Fiscal Date Patterns	Select * From F0008
F0010	Company Master	Select * From F0010
F0011	Batch Headers	Select * From F0011 Where ICDICJ >= 122001
F0013	Currency Codes	Select * From F0013
F0901	Account Master	Select * From F0901
F0902	Account Balances	Select GBAID, GBCO, GBFY, GBLT
, SUM (GBAPYC)GBAPYC ,SUM (GBAN01)GBAN01  
, SUM (GBAN02)GBAN02,	SUM (GBAN03)GBAN03, SUM (GBAN04)GBAN04 
, SUM (GBAN05)GBAN05,	SUM (GBAN06)GBAN06, SUM (GBAN07)GBAN07 
, SUM (GBAN08)GBAN08,	SUM (GBAN09)GBAN09, SUM (GBAN10)GBAN10 
, SUM (GBAN11)GBAN11,	SUM (GBAN12)GBAN12, SUM (GBAN13)GBAN13 
, SUM (GBAN14)GBAN14 
From F0902 Where GBFY between 11 and 40 And GBLT = 'AA'   
Group By GBAID,  GBCO, GBFY, GBLT
F0911	Account Ledger	Select * From F0911   Where GLLT = 'AA'  And GLDGJ >= 122001
F3106	Work Order Cross Ref	Select * From F3106 Where SDDICJ >= 122001
F30026	Cost Components	Select * From F30026 Where IELEDG = ‘07’
F4095	D/M Accounting Instructions	Select * From F4095
F4096	Flex Accounting Instructions	Select * From F4096
F41001	Inventory Constants	Select * From F41001
F41002	Unit of Measure Conversions	Select * From F41002
F41003	Unit of Measure Conversions	Select * From F41003
F4101	Item Master	Select * From F4101
F41021	Item Balances	Select * From F41021
F4111	Item Ledger	Select * From F4111   Where ILCRDJ      >= 121350
F4105	Cost Ledger	Select * From F4105   Where COCSIN = ‘I’
F4211	Sales Order Details	Select * From F4211   Where SDUPMJ   >= 121350
F42119	Sales History	Select * From F42119 Where SDUPMJ   >= 121350
F4311	Purchase Order Details	Select * From F4311   Where PDTRDJ     >= 121350
F4801	Work Order Headers	Select * From F4801   Where WAUPMJ  >= 122001
F4102	Item Branch Plant	Select * From F4102
F0015	Currency Exchange Rates	Select * from F0015 Where CXEFT >= 122001
F1113	Restatement Rates	Select * from F1113 Where C1EFT >= 122001
F43121	Purchase Order Receipts	Select * from F43121
F0101	Address Book	Select ABAN8, ABALPH from F0101
For accurate results, please extract tables F41021 and F4111 as close together when activity is at a minimum.

