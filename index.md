# RapidReconciler
## Document Library

Welcome to the GSI RapidReconciler documentation library. Use the links below to navigate to individual documents by topic area.

---

## Technical Documents

| Document | Section | Description |
|---|---|---|
| [Technical Requirements](MDS/tech-requirements) | [RR Database Server](MDS/tech-requirements#rr-database-server) | Minimum server requirements, SQL Server specifications, storage estimates, and network information |
| | [Integration Services](MDS/tech-requirements#integration-services) | Alternate server requirements, SSMS, Visual Studio, and OLE DB provider configuration for AS/400, Oracle, and SQL Server |
| | [RR Application Server](MDS/tech-requirements#rr-application-server) | Server requirements, internal and external network access, and port configuration |
| | [End User PC](MDS/tech-requirements#end-user-pc) | Operating system, browser, and network requirements for end users |
| | [JD Edwards Information](MDS/tech-requirements#jd-edwards-information) | Data dictionary variables and JDE connection details required for installation |
| | [Table Listing](MDS/tech-requirements#table-listing) | All JD Edwards tables accessed by RapidReconciler in read-only mode |
| | [Appendix A -- Integration Services Catalog](MDS/tech-requirements#appendix-a--creating-the-integration-services-catalog) | Steps to create the SSISDB catalog and RapidReconciler project folder |
| | [Appendix B -- Proof of Concept](MDS/tech-requirements#appendix-b--proof-of-concept-requirements) | Steps and table extract statements for providing data to GSI for a proof of concept |
| [Installing RapidReconciler-Prod](MDS/Installing_production_database.md) | [Skill Sets](MDS/Installing_production_database.md#skill-sets) | Required technical knowledge for installation |
| | [Architecture Overview](MDS/Installing_production_database.md#architecture-overview) | Hardware components, data synchronized with the RR Agent, and network notes |
| | [Working with a New Client](MDS/Installing_production_database.md#working-with-a-new-client) | Information to gather from the sales rep and web meeting agenda |
| | [Separate Application Server Requirements](MDS/Installing_production_database.md#separate-application-server-requirements-if-needed) | Server, access, and OLE DB provider requirements for separate server configurations |
| | [Database Server Requirements](MDS/Installing_production_database.md#database-server-requirements) | Minimum SQL Server requirements for the database server |
| | [Creating the Integration Services Catalog](MDS/Installing_production_database.md#creating-the-integration-services-catalog) | Steps to create the SSISDB catalog and RapidReconciler folder |
| | [Installing the RapidReconciler Database](MDS/Installing_production_database.md#installing-the-rapidreconciler-database) | Steps to create the database, objects, SQL user, and SQL Agent job |
| | [Configuring and Deploying the Integration Services Package](MDS/Installing_production_database.md#configuring-and-deploying-the-integration-services-package) | Steps to create the Visual Studio solution, configure connections and variables, and deploy the SSIS package |
| | [Performing the Initial Data Load](MDS/Installing_production_database.md#performing-the-initial-data-load) | Steps to enable and configure the SQL Agent job schedule |
| | [Security Requirements](MDS/Installing_production_database.md#security-requirements) | SQL login permissions, Agent service account, and SSIS catalog permissions |
| [Installing a Client in VALC (GSI Use Only)](MDS/installing-valc) | [Part 1: Initial VALC Setup](MDS/installing-valc#part-1-initial-valc-setup) | Creating the client record, initial user account, module configuration, additional fields, and certificate management |
| | [Part 2: Installing the RapidReconciler Agent](MDS/installing-valc#part-2-installing-the-rapidreconciler-agent) | Downloading and installing the agent, validating the SQL Server connection, and verifying connectivity in VALC |
| | [Part 3: Completing the Setup in VALC](MDS/installing-valc#part-3-completing-the-setup-in-valc) | Verifying database status and licensing company numbers |
| | [Summary Checklist](MDS/installing-valc#summary-checklist) | End-to-end installation checklist |
| [Server Migration Guide](MDS/server-migration) | [Section 1: Overview](MDS/server-migration#section-1-overview) | Migration scenarios and pre-migration planning |
| | [Section 2: Dedicated Server Migration](MDS/server-migration#section-2-dedicated-server-migration) | Prerequisites, database backup and restore, SSIS package migration, SQL Agent job, RR Agent installation, and obtaining IP addresses |
| | [Section 3: Separate Servers Migration](MDS/server-migration#section-3-separate-servers-migration) | Application server and database server prerequisites and migration steps |
| | [Section 4: Update VALC and Cloudflare](MDS/server-migration#section-4-update-valc-and-cloudflare) | Updating VALC IP addresses, Cloudflare DNS update, enabling the SQL Agent job schedule, and testing |
| | [Section 5: Post-Migration Checklist](MDS/server-migration#section-5-post-migration-checklist) | End-to-end migration checklist |
| [Certificate Management](MDS/certificate_management.md) | [Components](MDS/certificate_management.md#components) | Overview of the wildcard SSL certificate, DNS 'A' record, domain URL, and RR Agent |
| | [DNS Configuration](MDS/certificate_management.md#dns-configuration) | How 'A' records work, when they are required, and the process to request one |
| | [SSL Certificate Management](MDS/certificate_management.md#ssl-certificate-management) | Certificate scope, renewal process, backend update, agent deployment via VALC, and verification |
| | [Responsibilities Summary](MDS/certificate_management.md#responsibilities-summary) | Task ownership by role across GSI, GSI I/T, and the UI developer |
| | [Troubleshooting](MDS/certificate_management.md#troubleshooting) | Common connectivity and certificate issues with causes and actions |

---

## Getting Started

| Document | Description |
|----------|-------------|
| [Getting Started with the Application](MDS/getting-started-with-rapidreconciler) | Logging in, navigating the interface, and system requirements |
| [Administrator Responsibilities](MDS/admin-responsibilities) | Company management, user setup, general settings, and offset accounts |
| [Complex Password](MDS/complex-password) | Password policy requirements and reset process |
| [Adding a New Company](MDS/adding-company.md) | How to request additional company licenses and edit company settings in RapidReconciler. |
| [Managing Inventory Accounts](MDS/add-account-rr) | DMAAI model table process and refresh requirements |

---

## Inventory

| Document | Description |
|----------|-------------|
| [Inventory Key Concepts](MDS/inventory-key-concepts) | DMAAI tables, GL account assignment, period end logic, variance sources, cardex variance, GL class codes |
| [Inventory: Using the Application](MDS/inventory-using-application) | Reconciliation page, transactions page, As-Of page, Roll Forward, integrity reports, reconciliation process |
| [Reconciliation: Top 6 Issues — Part 2](MDS/top-6-issues-pt2) | GL class code changes and reconciliation impact |
| [Reconciliation: Top 6 Issues — Part 3](MDS/top-6-issues-pt3) | Product costing and R30543 cost component integrity |
| [RapidReconciler: Transaction Detail Report Update](MDS/transaction-detail-report) | Enhanced drill-down for intercompany, transfer, and direct ship orders |
| [Stock Status vs. Trial Balance — Part 1](MDS/stock-status-trial-balance) | Timing, backdating, report definition |
| [Stock Status vs. Trial Balance — Part 2](MDS/stock-status-trial-balance-pt2) | DMAAI setup and GL class code change impacts |

---

## In Transit

| Document | Description |
|----------|-------------|
| [In Transit Key Concepts](MDS/in-transit-key-concepts) | ST/OT process, accounting setup, order pairs, exclusions |
| [In Transit: Using the Application](MDS/in-transit-using-application) | Orders page, reconciliation page, transactions page, As-Of page, integrity reports |
| [ST/OT Transfer Order Accounting — Part 3](MDS/transfer-order-accounting-pt3) | OT receipt with DMAAI 4335, cost change before shipment |
| [ST/OT Transfer Order Accounting — Part 4](MDS/transfer-order-accounting-pt4) | Standard cost variance in receiving branch, DMAAI 4335 configuration |
| [ST/OT: Inventory Tracking Without Receipts Routing](MDS/st-ot-tracking) | RapidReconciler As-Of alternative to receipts routing |
| [ST/OT: Exclusions in RapidReconciler](MDS/st-ot-exclusions) | Unbalanced transfers, exclusion process, journal entries |
| [ST/OT: Exclusion Variance Added to Orders Page](MDS/st-ot-exclusion-variance) | ExclVarQty and ExclVarAmt columns, unexclude and re-exclude process |

---

## PO Receipts

| Document | Description |
|----------|-------------|
| [PO Receipts Key Concepts](MDS/po-receipts-key-concepts) | RNV definition, process flow, Table F43121, match types, challenges |
| [PO Receipts: Using the Application](MDS/po-receipts-using-application) | Orders page, reconciliation page, line analysis, how to reconcile |
| [Reconciling RNV Accounts in RapidReconciler](MDS/reconciling-rnv) | Summary, drill-down, and suspension features in RR V7 |

---

## Reference Library

| Document | Description |
|----------|-------------|
| [Introduction to Manufacturing Accounting](MDS/manufacturing-accounting) | Cost flows, transaction types, setup tips, execution best practices |
| [Manufacturing AAIs Reference](MDS/manufacturing-aais) | IM, IH, IC, IS, and IV transaction types with AAI debit/credit tables |
| [R30837 WIP Revaluation for Standard Costing](MDS/wip-revaluation) | How WIP reval works, prerequisites, setup, journal entries, full example |
| [Outside Operations: Setup and Accounting](MDS/outside-operations) | Item master, work center, routing, receipt, and WIP journal entries |
| [Outside Operations: Troubleshooting](MDS/outside-operations-troubleshooting) | Why POs are not created — item, system, routing, vendor, and security issues |
| [Global Item Update: A "Gotcha"](MDS/global-item-update) | Creation date override on item ledger records |
| [FAQ: Sales Update (P42800)](MDS/sales-update-faq) | File updates, processing order, AAIs, batch types, proof vs. final, errors |
| [Tax in Sales](MDS/tax-in-sales) | Tax explanation codes, Rate/Area setup, AAIs, S/V/C/E examples |
| [Sales Order Intercompany Processing](MDS/intercompany-processing) | SI/SK/OK orders, R4210IC, journal entries, cost alignment |
| [Accounting in Purchasing: Overview](MDS/accounting-in-purchasing) | File updates and journal entries for stock 3-way, non-stock 2-way and 3-way match |
| [Taxes in Procurement](MDS/taxes-procurement) | Tax setup, explanation codes, AAIs, and GL treatment for S, U, V, C, B codes |
| [Landed Costs in EnterpriseOne](MDS/landed-costs) | Setup, cost rules, journal entries, F43121 records, performance notes |
| [The 4332 AAI: Purpose and Impact](MDS/aai-4332) | Cost variance at voucher match, journal entry examples, configuration |
| [Material Burden AAI (4337)](MDS/material-burden-aai) | Purpose, setup, calculation, and journal entry scenarios |
| [AAIs for Distribution](MDS/distribution-aais) | Setup, GL class codes, business unit, financial AAIs, error messages, full AAI listing |
| [Flexible Accounting for Distribution](MDS/flexible-accounting) | Background, requirements, enabling, establishing flexible accounts |
| [How to Set Up a Branch/Plant](MDS/branch-plant-setup) | Address book, business unit, constants, and default branch update |
| [GL Class Codes: Changing a GL Class Code](MDS/gl-class-code-changes) | Procedure, hierarchy of change locations, why adjustments are required |
| [Changing Item Primary Unit of Measure](MDS/changing-primary-uom) | Risks, procedure, and considerations for history, BOM, GL, warehousing, EDI |
| [Unit of Measure Conversion](MDS/uom-conversion) | Hierarchy, standard vs. item conversions, weight and volume setup |
| [Weighted Average Cost](MDS/weighted-average-cost) | Setup, UDC 40/AV, online vs. batch, landed cost and receipt routing impacts |
| [Costs in EnterpriseOne](MDS/costs-enterpriseone) | Cost levels, cost methods, F4105 storage, IB transactions, R41815 conversion |
| [Zero Balance Adjustments](MDS/zero-balance-adjustments) | Purpose, purchasing and inventory AAIs, journal entry examples |
| [Cardex Analysis: Weighted Average Cost Error](MDS/cardex-weighted-average-error) | Identifying and investigating weighted average cost calculation errors |
| [Cardex Analysis: 3 Common Analyst Errors](MDS/cardex-analyst-errors) | Memo transactions, alternate UOM, average cost item analysis levels |
| [Performing a Dollars-Only Inventory Adjustment](MDS/dollars-only-adjustment) | Standard vs. average cost environments, UDC 40/AV, P4114 procedure |
| [Item Ledger: Top 5 Questions Answered](MDS/item-ledger-faq) | Balances, posting codes, dates, DMAAs, and integrity conditions |
| [Direct Ship Orders](MDS/direct-ship-orders) | Setup, line type, AAIs, partial shipments, multi-currency, ECS |

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*