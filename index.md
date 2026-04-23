# RapidReconciler Document Library

Welcome to the GSI RapidReconciler documentation library. Use the links below to navigate to individual documents by topic area.

---

## AI Analysis Examples

The following examples demonstrate AI-powered analysis of RapidReconciler reports. Each report was exported from RapidReconciler into Excel, uploaded to Claude, and analyzed using the applicable template.
Each workbook contains multiple sheets with the original report data on the left, AI-generated insights, and recommended action items. The analysis focuses on identifying variances, root causes, and prioritized next steps for resolution.

| Report | Description |
|--------|-------------|
| [End of Day Analysis](Analysis%20Examples/End-of-Day-Analysis.xlsx) | End of day reconciliation analysis. Identifies outstanding GL variances, flags unprocessed transactions, and provides prioritized action items for resolution before period close. |
| [DMAAI Integrity](Analysis%20Examples/DMAAI-Analysis.xlsx) | DMAAI entry integrity analysis. Reviews automatic accounting instruction (AAI) configurations across companies, identifying account mismatches and entries flagged for net-zero review. |
| [Account Roll Forward](Analysis%20Examples/Account-Roll-Forward-Analysis.xlsx) | Period-over-period account roll forward analysis reconciling beginning GL balances, period activity, and ending balances against the perpetual inventory ledger. Highlights accounts with GL variances, cardex discrepancies, and unposted batches across multiple periods. |
| [Unposted GL Batches](Analysis%20Examples/Unposted-GL-Batch-Analysis.xlsx) | Analysis of unposted general ledger batches. Identifies batches across multiple companies and batch types that are pending approval or stuck in an "In Use" state, with prioritized resolution steps to clear the backlog before period close. |
| [Cardex Item Analysis](Analysis%20Examples/Cardex-Variance-Item-Analysis.xlsx) | Item-level cardex roll forward analysis for a single item across a specific branch and location. Traces quantity and amount variances between the item ledger and on-hand balances back to their root cause transaction, using standard cost method. |
| [Transaction Details Analysis](Analysis%20Examples/Transaction-Details-Analysis.xlsx) | Deep-dive transaction analysis for a specific document, reconciling F4111 item ledger entries against GL account F0911 postings. Includes DMAAI inventory account mapping validation and identifies misconfigured model table entries contributing to posting discrepancies. |

---


## Collateral Documents

| Document                                                                                     | Description                                                  |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [How RapidReconciler Helps Web Site](/RapidReconciler-AI/Collateral/how-rr-helps.html)       | Overview of the application's benefits and value proposition |
| [RapidReconciler Fact Sheet](/RapidReconciler-AI/Collateral/rr-fact-sheet.html) | One-page summary of key features and benefits                |

---

## Technical Documents

| Document | Description |
|----------|-------------|
| [Technical Requirements](MDS/tech-requirements.md) | Installation and configuration requirements |
| [Installing the Database](MDS/Installing_production_database.md) | Step-by-step database installation including skill sets, architecture overview, SSISDB catalog setup, SSIS package deployment, initial data load, and security requirements |
| [Installing a Client in VALC](MDS/installing-valc.md) | End-to-end VALC client setup including creating the client record, user accounts, module configuration, RR Agent installation, SQL Server connection validation, and company licensing |
| [Server Migration Guide](MDS/server-migration.md) | Moving RapidReconciler to a new dedicated or separate server including prerequisites, database backup and restore, SSIS package migration, SQL Agent job setup, and VALC and Cloudflare updates |
| [Certificate Management](MDS/certificate_management.md) | SSL certificate scope, DNS 'A' record configuration, certificate renewal process, responsibilities by role, and troubleshooting common connectivity issues |

---

## Getting Started

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

| Document                                                                   | Description                                                                        |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [In Transit Key Concepts](MDS/in-transit-key-concepts.md)                     | ST/OT process, accounting setup, order pairs, exclusions                           |
| [In Transit: Using the Application](MDS/in-transit-using-application.md)      | Orders page, reconciliation page, transactions page, As-Of page, integrity reports |
| [Transfer Order Exclusion Guide](MDS/transfer_order_exclusion_guide.md) | Exclusion types, setup, and troubleshooting                                        |
| [Transfer Order Reference Guide](MDS/transfer_order_reference.md)       | Transfer order types, processing flow, AAIs, journal entries, and common issues    |

---

## PO Receipts

| Document | Description |
|----------|-------------|
| [PO Receipts Key Concepts](MDS/po-receipts-key-concepts.md) | RNV definition, process flow, Table F43121, match types, challenges |
| [PO Receipts: Using the Application](MDS/po-receipts-using-application.md) | Orders page, reconciliation page, line analysis, how to reconcile |
| [Reconciling RNV Accounts in RapidReconciler](MDS/reconciling-rnv.md) | Summary, drill-down, and suspension features in RR V7 |
| [Purchase Order Reference Guide](MDS/purchase_order_reference.md) | Purchase order types, processing flow, AAIs, journal entries, and common issues |

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*