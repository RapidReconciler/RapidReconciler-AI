# GSI RapidReconciler Knowledge Base

# Welcome to the GSI RapidReconciler Knowledge Base

Stop chasing reconciliation discrepancies across spreadsheets and manual processes. 
RapidReconciler gives JD Edwards teams a faster, smarter way to reconcile inventory and general 
ledger accounts — and this library is your complete guide to getting the most out of it.

Browse documentation covering everything from initial setup to advanced reconciliation workflows 
for inventory, in-transit transfers, and PO receipts — plus worked examples of AI-powered 
analysis that turn RapidReconciler exports into actionable insights in minutes.

---

## Collateral Pages (Beta)

Here are some key collateral documents that provide an overview of RapidReconciler's benefits and features. These resources are intended to help you understand the value proposition of the application and how it can assist your JD Edwards reconciliation processes. Click on each document name to view the full content.

| Document                                                                                     | Description                                                  |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [How RapidReconciler Helps Web Site](/RapidReconciler-AI/Collateral/how-rr-helps.html)       | Overview of the application's benefits and value proposition |
| [RapidReconciler Fact Sheet](/RapidReconciler-AI/Collateral/rr-fact-sheet.html) | One-page summary of key features and benefits                |

---

## AI Analysis Examples

The following examples demonstrate AI-powered analysis of JD Edwards data using RapidReconciler. Each example was sourced from RapidReconciler existing reports into Excel, uploaded to Claude, and analyzed using a functional template.
The result produces AI-generated insights: root causes, recommended actions, and prioritized next steps for resolution. Clicking on each report name will allow you to reviewing source data and to see how AI arrived at its conclusions. These examples are intended to illustrate the potential of AI-assisted analysis in RapidReconciler and inspire new ways to leverage the application for faster, more effective reconciliations.

| Report | RR Source | Description |
| --- | --- | --- |
| [End of Day Analysis](Analysis%20Examples/End-of-Day-Analysis.xlsx) | End of Day Preview Export | End of day reconciliation analysis. Identifies outstanding GL variances, flags unprocessed transactions, and provides prioritized action items for resolution before period close. |
| [DMAAI Integrity](Analysis%20Examples/DMAAI-Analysis.xlsx) | Inventory Integrity Report 2 | DMAAI entry integrity analysis. Reviews automatic accounting instruction (AAI) configurations across companies, identifying account mismatches and entries flagged for net-zero review. |
| [Account Roll Forward](Analysis%20Examples/Account-Roll-Forward-Analysis.xlsx) | Inventory Validation Status Light Export | Period-over-period account roll forward analysis reconciling beginning GL balances, period activity, and ending balances against the perpetual inventory ledger. Highlights accounts with GL variances, cardex discrepancies, and unposted batches across multiple periods. |
| [Unposted GL Batches](Analysis%20Examples/Unposted-GL-Batch-Analysis.xlsx) | Batches Preview Export | Analysis of unposted general ledger batches. Identifies batches across multiple companies and batch types that are pending approval or stuck in an "In Use" state, with prioritized resolution steps to clear the backlog before period close. |
| [Cardex Item Analysis](Analysis%20Examples/Cardex-Variance-Item-Analysis.xlsx) | Expanding an Item on the As Of page and exporting | Item-level cardex roll forward analysis for a single item across a specific branch and location. Traces quantity and amount variances between the item ledger and on-hand balances back to their root cause transaction, using standard cost method. |
| [Transaction Details Analysis](Analysis%20Examples/Transaction-Details-Analysis.xlsx) | Expanding a line on the Transactions page and exporting | Deep-dive transaction analysis for a specific document, reconciling F4111 item ledger entries against GL account F0911 postings. Includes DMAAI inventory account mapping validation and identifies misconfigured model table entries contributing to posting discrepancies. |
| [GL Class Code Analysis](Analysis%20Examples/GL-Class-Analysis.xlsx) | Inventory Integrity Report 5 | GL class code integrity analysis comparing item branch records (F4102) against item location records (F41021). Identifies blank location GL class codes and branch-to-location mismatches that cause inventory transactions to post to incorrect accounts, with prioritized remediation steps. |
| [Frozen Cost Integrity](Analysis%20Examples/Frozen-Cost-Analysis.xlsx) | Inventory Integrity Report 6 | Frozen cost integrity analysis comparing the frozen standard unit cost in F4105 (cost method 07) against the sum of cost components in F30026. Identifies zero-cost inventory, missing cost builds, and cost mismatches that cause manufacturing transactions to post at incorrect values, with GL understatement calculated per item. |

---

## Technical Documents

These technical documents provide detailed guidance on the installation, configuration, and maintenance of RapidReconciler. They cover everything from initial setup requirements to server migration and certificate management. Whether you're a system administrator responsible for maintaining the application or an IT professional involved in the deployment process, these resources will help ensure a smooth and successful implementation of RapidReconciler in your JD Edwards environment.

| Document | Description |
|----------|-------------|
| [Technical Requirements](MDS/tech-requirements.md) | Installation and configuration requirements |
| [Installing the Database](MDS/Installing_production_database.md) | Step-by-step database installation including skill sets, architecture overview, SSISDB catalog setup, SSIS package deployment, initial data load, and security requirements |
| [Installing a Client in VALC](MDS/installing-valc.md) | End-to-end VALC client setup including creating the client record, user accounts, module configuration, RR Agent installation, SQL Server connection validation, and company licensing |
| [Server Migration Guide](MDS/server-migration.md) | Moving RapidReconciler to a new dedicated or separate server including prerequisites, database backup and restore, SSIS package migration, SQL Agent job setup, and VALC and Cloudflare updates |
| [Certificate Management](MDS/certificate_management.md) | SSL certificate scope, DNS 'A' record configuration, certificate renewal process, responsibilities by role, and troubleshooting common connectivity issues |

---

## Getting Started with RapidReconciler

These documents provide an introduction to RapidReconciler, including its benefits, how it compares to traditional reconciliation methods in JD Edwards, and the basics of using the application. Whether you're new to RapidReconciler or looking for a refresher on its core features, these resources will help you get up to speed quickly and start leveraging the application for more efficient reconciliations.

| Document | Description |
|----------|-------------|
| [How RapidReconciler Helps Document](/MDS/how-rr-helps.md) | Printable version of the application's benefits and value proposition |
| [JDE vs. RapidReconciler Comparison](MDS/stock-status-trial-balance.md) | Timing, backdating, report definition |
| [Application Basics](MDS/getting-started-with-rapidreconciler.md) | Logging in, navigating the interface, and system requirements |
| [Complex Password Option](MDS/complex-password.md) | Password policy requirements and reset process |
| [Administrator Responsibilities](MDS/admin-responsibilities.md) | Company management, user setup, general settings, and offset accounts |
| [Obtaining a New Company License](MDS/adding-company.md) | How to request additional company licenses and edit company settings in RapidReconciler. |

---

## Inventory

This section covers all aspects of inventory reconciliation using RapidReconciler, including key concepts, application usage, and specific topics like the item ledger, DMAAIs, GL class codes, units of measure, product costing, zero balance adjustments, cardex variance, and outside operations. Whether you're looking to understand the fundamentals of inventory reconciliation or seeking guidance on specific issues and scenarios, these documents provide comprehensive information to help you effectively manage your inventory accounts in JD Edwards with RapidReconciler.

| Document | Description |
|----------|-------------|
| [Inventory Key Concepts](MDS/inventory-key-concepts.md) | DMAAI tables, GL account assignment, period end logic, variance sources, cardex variance, GL class codes |
| [Managing Inventory Accounts](MDS/add-account-rr.md) | DMAAI model table process and refresh requirements |
| [Inventory: Using the Application](MDS/inventory-using-application.md) | Reconciliation page, transactions page, As-Of page, Roll Forward, integrity reports, reconciliation process |
| [Working with the Item Ledger](MDS/item-ledger-faq.md) | Balances, posting codes, dates, DMAAs, and integrity conditions |
| [Ultimate DMAAI Guide](MDS/distribution-aais.md) | Setup, GL class codes, business unit, financial AAIs, error messages, full AAI listing |
| [Managing GL Class Codes](MDS/gl-class-code-changes.md) | Procedure, hierarchy of change locations, why adjustments are required |
| [About Units of Measure](MDS/uom_reference_guide.md) | Changing the primary unit of measure, impact on inventory transactions, and cardex analysis considerations |
| [Product Costing Guide](MDS/product-costing.md) | Cost methods, cost levels, F4105 storage, IB transactions, R41815 conversion, inventory valuation impact |
| [Zero Balance Adjustments](MDS/zero-balance-adjustments.md) | Purpose, purchasing and inventory AAIs, journal entry examples |
| [Handling Cardex Variance](MDS/cardex_variance.md) | Standard vs. average cost environments, UDC 40/AV, P4114 procedure |
| [Understanding Outside Operations](MDS/outside-operations.md) | Item master, work center, routing, receipt, and WIP journal entries |

## In Transit

This section focuses on the reconciliation of in-transit inventory using RapidReconciler. It covers key concepts related to the in-transit process, how to use the application, and a wealth of JD Edwards best practice knowledge.

| Document                                                                   | Description                                                                        |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [In Transit Key Concepts](MDS/in-transit-key-concepts.md)                     | ST/OT process, accounting setup, order pairs, exclusions                           |
| [In Transit: Using the Application](MDS/in-transit-using-application.md)      | Orders page, reconciliation page, transactions page, As-Of page, integrity reports |
| [Transfer Order Exclusion Guide](MDS/transfer_order_exclusion_guide.md) | Exclusion types, setup, and troubleshooting                                        |
| [Transfer Order Reference Guide](MDS/transfer_order_reference.md)       | Transfer order types, processing flow, AAIs, journal entries, and common issues    |

---

## PO Receipts

This section provides comprehensive information on reconciling purchase order receipts, aka RNV or RNI,  using RapidReconciler. It includes key concepts related to the PO receipt process, how to use the application for PO receipt reconciliation, and a reference guide covering various aspects of purchase orders in JD Edwards.

| Document | Description |
|----------|-------------|
| [PO Receipts Key Concepts](MDS/po-receipts-key-concepts.md) | RNV definition, process flow, Table F43121, match types, challenges |
| [PO Receipts: Using the Application](MDS/po-receipts-using-application.md) | Orders page, reconciliation page, line analysis, how to reconcile |
| [Reconciling RNV Accounts in RapidReconciler](MDS/reconciling-rnv.md) | Summary, drill-down, and suspension features in RR V7 |
| [Purchase Order Reference Guide](MDS/purchase_order_reference.md) | Purchase order types, processing flow, AAIs, journal entries, and common issues |

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*