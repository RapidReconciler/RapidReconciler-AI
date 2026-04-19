# RapidReconciler
## Document Library

Welcome to the GSI RapidReconciler documentation library. Use the links below to navigate to individual documents by topic area.

---

## Technical Documents

| Document | Description |
|----------|-------------|
| [Technical Requirements](MDS/tech-requirements) | Installation and configuration requirements |
| [Installing RapidReconciler-Prod](MDS/Installing_production_database.md) | Step-by-step database installation including skill sets, architecture overview, SSISDB catalog setup, SSIS package deployment, initial data load, and security requirements |
| [Installing a Client in VALC (GSI Use Only)](MDS/installing-valc) | End-to-end VALC client setup including creating the client record, user accounts, module configuration, RR Agent installation, SQL Server connection validation, and company licensing |
| [Server Migration Guide](MDS/server-migration) | Moving RapidReconciler to a new dedicated or separate server including prerequisites, database backup and restore, SSIS package migration, SQL Agent job setup, and VALC and Cloudflare updates |
| [Certificate Management](MDS/certificate_management.md) | SSL certificate scope, DNS 'A' record configuration, certificate renewal process, responsibilities by role, and troubleshooting common connectivity issues |

---

## Getting Started

| Document | Description |
|----------|-------------|
| [Why RapidReconciler?](MDS/stock-status-trial-balance) | Timing, backdating, report definition |
| [Getting Started with the Application](MDS/getting-started-with-rapidreconciler) | Logging in, navigating the interface, and system requirements |
| [Complex Password](MDS/complex-password) | Password policy requirements and reset process |
| [Administrator Responsibilities](MDS/admin-responsibilities) | Company management, user setup, general settings, and offset accounts |
| [Adding a New Company](MDS/adding-company.md) | How to request additional company licenses and edit company settings in RapidReconciler. |

---

## Inventory

| Document                                                                           | Description                                                                                                 |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [Inventory Key Concepts](MDS/inventory-key-concepts)                               | DMAAI tables, GL account assignment, period end logic, variance sources, cardex variance, GL class codes    |
| [Managing Inventory Accounts](MDS/add-account-rr) | DMAAI model table process and refresh requirements |
| [Inventory: Using the Application](MDS/inventory-using-application)                | Reconciliation page, transactions page, As-Of page, Roll Forward, integrity reports, reconciliation process |
| [Working with the Item Ledger](MDS/item-ledger-faq) | Balances, posting codes, dates, DMAAs, and integrity conditions |
| [Ultimate DMAAI Guide](MDS/distribution-aais)                                      | Setup, GL class codes, business unit, financial AAIs, error messages, full AAI listing                      |
| [Managing GL Class Codes](MDS/gl-class-code-changes)                               | Procedure, hierarchy of change locations, why adjustments are required                                      |
| [About Units of Measure](MDS/changing-primary-uom)                                 | Changing the primary unit of measure, impact on inventory transactions, and cardex analysis considerations  |
| [Product Costing Guide](MDS/weighted-average-cost)                                 | Cost methods, cost levels, F4105 storage, IB transactions, R41815 conversion, inventory valuation impact    |
| [Zero Balance Adjustments](MDS/zero-balance-adjustments) | Purpose, purchasing and inventory AAIs, journal entry examples |
| [Handling Cardex Variance](MDS/dollars-only-adjustment) | Standard vs. average cost environments, UDC 40/AV, P4114 procedure |
| [Understanding Outside Operations](MDS/outside-operations) | Item master, work center, routing, receipt, and WIP journal entries |
| [Sales Order Reference Guide](../MDS/sales_order_reference.md) | Sales order types, processing flow, AAIs, journal entries, and common issues |

---

## In Transit

| Document                                                                   | Description                                                                        |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [In Transit Key Concepts](MDS/in-transit-key-concepts)                     | ST/OT process, accounting setup, order pairs, exclusions                           |
| [In Transit: Using the Application](MDS/in-transit-using-application)      | Orders page, reconciliation page, transactions page, As-Of page, integrity reports |
| [Transfer Order Exclusion Guide](../MDS/transfer_order_exclusion_guide.md) | Exclusion types, setup, and troubleshooting                                        |
| [Transfer Order Reference Guide](../MDS/transfer_order_reference.md)       | Transfer order types, processing flow, AAIs, journal entries, and common issues    |

---

## PO Receipts

| Document | Description |
|----------|-------------|
| [PO Receipts Key Concepts](MDS/po-receipts-key-concepts) | RNV definition, process flow, Table F43121, match types, challenges |
| [PO Receipts: Using the Application](MDS/po-receipts-using-application) | Orders page, reconciliation page, line analysis, how to reconcile |
| [Reconciling RNV Accounts in RapidReconciler](MDS/reconciling-rnv) | Summary, drill-down, and suspension features in RR V7 |
| [Purchase Order Reference Guide](../MDS/purchase_order_reference.md) | Purchase order types, processing flow, AAIs, journal entries, and common issues |

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*