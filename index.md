# GSI RapidReconciler Knowledge Base

Stop chasing reconciliation discrepancies across spreadsheets and manual processes.
RapidReconciler gives JD Edwards teams a faster, smarter way to reconcile inventory and general
ledger accounts - and this library is your complete guide to getting the most out of it.

Browse documentation covering everything from initial setup to advanced reconciliation workflows
for inventory, in-transit transfers, and PO receipts - plus worked examples of AI-powered
analysis that turn RapidReconciler exports into actionable insights in minutes.

---

## Collateral Pages

Here are some key collateral documents that provide an overview of RapidReconciler's benefits and features. These resources are intended to help you understand the value proposition of the application and how it can assist your JD Edwards reconciliation processes. Click on each document name to view the full content.

| Document                                                                                   | Description                                                                                      |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| [How RapidReconciler Helps](/RapidReconciler-AI/Collateral/how-rr-helps.html)              | Overview of the application's benefits and value proposition                                     |
| [RapidReconciler Fact Sheet](/RapidReconciler-AI/Collateral/rr-fact-sheet.html)            | One-page summary of key features and benefits                                                    |
| [Self-Guided Tour](/RapidReconciler-AI/Collateral/rr-self-guided-tour.html)                | Interactive walkthrough of the application interface and features                                |
| [Inventory Dashboard Sample](/RapidReconciler-AI/Collateral/inventory-dashboard.html)      | Executive summary of inventory reconciliation challenges and how RapidReconciler addresses them  |
| [In-Transit Dashboard Sample](/RapidReconciler-AI/Collateral/in-transit-dashboard.html)    | Executive summary of in-transit reconciliation challenges and how RapidReconciler addresses them |
| [PO Receipts Dashboard Sample](/RapidReconciler-AI/Collateral/po-receipts-dashboard.html)  | Executive summary of PO receipt reconciliation challenges and how RapidReconciler addresses them |

---

## RapidReconciler AI Touchpoints

The following examples demonstrate AI-powered analysis of JD Edwards data using RapidReconciler. Each example was sourced from RapidReconciler existing reports into Excel and analyzed using a functional template.
The result produces AI-generated insights: root causes, recommended actions, and prioritized next steps for resolution. Clicking on each report name will allow you to reviewing source data and to see how AI interpreted the issue:

| Document | Description |
|----------|-------------|
| [End of Day Analysis](AnalysisExamples/End-of-Day-Analysis.xlsx)                         | End of Day Preview Export                 |
| [DMAAI Integrity](AnalysisExamples/DMAAI-Analysis.xlsx)                                  | Inventory Integrity Report 2              |
| [Account Roll Forward](AnalysisExamples/Account-Roll-Forward-Analysis.xlsx)              | Inventory Validation Status Light Export  |
| [Unposted GL Batches](AnalysisExamples/Unposted-GL-Batch-Analysis.xlsx)                  | Batches Preview Export                    |
| [Cardex Item Analysis](AnalysisExamples/Cardex-Variance-Item-Analysis.xlsx)              | Expanding an Item on the As Of page       |
| [Transaction Details Analysis](AnalysisExamples/Transaction-Details-Analysis.xlsx)       | Expanding a line on the Transactions page |
| [GL Class Code Analysis](AnalysisExamples/GL-Class-Analysis.xlsx)                        | Inventory Integrity Report 5              |
| [Frozen Cost Integrity](AnalysisExamples/Frozen-Cost-Analysis.xlsx)                      | Inventory Integrity Report 6              |

---

## Technical Documentation

These technical documents provide detailed guidance on the installation, configuration, and maintenance of RapidReconciler. They cover everything from initial setup requirements to server migration and certificate management. Whether you're a system administrator responsible for maintaining the application or an IT professional involved in the deployment process, these resources will help ensure a smooth and successful implementation of RapidReconciler in your JD Edwards environment.

| Document | Description |
|----------|-------------|
| [Technical Requirements](/RapidReconciler-AI/HowToTech/tech-requirements.html)           | Installation and configuration requirements |
| [Certificate Management](/RapidReconciler-AI/HowToTech/tech-certificate-management.html) | SSL certificate scope, DNS 'A' record configuration, certificate renewal process, responsibilities by role, and troubleshooting common connectivity issues |
| [Installation Prep](/RapidReconciler-AI/HowToTech/installation-prep.html)                | Customer preparation process for RapidReconciler installation |
| [Installing the Database](/RapidReconciler-AI/HowToTech/tech-database-installation.html) | Step-by-step database installation including skill sets, architecture overview, SSISDB catalog setup, SSIS package deployment, initial data load, and security requirements |
| [Valc Onboarding](/RapidReconciler-AI/HowToTech/tech-valc-walkthrough.html)	           | A Companion doc used to familiarize RapidReconciler support technicians with VALC (version an license control)|
| [Client Management](/RapidReconciler-AI/HowToTech/tech-client-management.html)           | End-to-end VALC client setup including creating the client record, user accounts, module configuration, RR Agent installation, SQL Server connection validation, and company licensing |

---

## Getting Started with the Application

These documents provide an introduction to RapidReconciler, including its benefits, how it compares to traditional reconciliation methods in JD Edwards, and the basics of using the application. Whether you're new to RapidReconciler or looking for a refresher on its core features, these resources will help you get up to speed quickly and start leveraging the application for more efficient reconciliations.

| Document | Description |
|----------|-------------|
| [Application Basics](MDS/getting-started-with-rapidreconciler.md)                        | Logging in, navigating the interface, and system requirements |
| [Complex Password Option](MDS/complex-password.md)                                       | Password policy requirements and reset process |
| [Walkthrough](HowToHTML/administrator-walkthrough.html)         | Company management, user setup, general settings, and offset accounts |

---

## Inventory Module

This section covers all aspects of inventory reconciliation using RapidReconciler, including key concepts, application usage, and specific topics like the item ledger, DMAAIs, GL class codes, units of measure, product costing, zero balance adjustments, cardex variance, and outside operations. Whether you're looking to understand the fundamentals of inventory reconciliation or seeking guidance on specific issues and scenarios, these documents provide comprehensive information to help you effectively manage your inventory accounts in JD Edwards with RapidReconciler.

| Document | Description |
|----------|-------------|
| [Reference Guide](MDS/inventory-reference-guide.md)          | DMAAI tables, GL account assignment, period end logic, variance sources, cardex variance, GL class codes |
| [Managing Accounts](MDS/inventory-add-account-rr.md)         | DMAAI model table process and refresh requirements |
| [Reconciling Inventory](MDS/inventory-reconciliation.md)     | Reconciliation page, transactions page, As-Of page, Roll Forward, integrity reports, reconciliation process |
| [Handling Cardex Variance](MDS/inventory-cardex-variance.md) | Standard vs. average cost environments, UDC 40/AV, P4114 procedure |

---

## In Transit Module

This section focuses on the reconciliation of in-transit inventory using RapidReconciler. It covers key concepts related to the in-transit process, how to use the application, and a wealth of JD Edwards best practice knowledge.

| Document | Description |
|----------|-------------|
| [Reference Guide](MDS/transfer-order-reference.md)                      | Transfer order types, processing flow, AAIs, journal entries, and common issues    |
| [Reconciliation Walkthrough](HowToHTML/in-transit-rec-walkthrough.html) | Step-by-step reconciliation
| [Exclusions Guide](MDS/transfer-order-exclusion-guide.md)               | Exclusion types, setup, and troubleshooting                                        |

---

## PO Receipts Module

This section provides comprehensive information on reconciling purchase order receipts, aka RNV or RNI, using RapidReconciler. It includes key concepts related to the PO receipt process, how to use the application for PO receipt reconciliation, and a reference guide covering various aspects of purchase orders in JD Edwards.

| Document | Description |
|----------|-------------|
| [Reference Guide](MDS/purchase_order_reference.md)                     | Purchase order types, processing flow, AAIs, journal entries, and common issues |
| [Reconciliation Walkthrough](HowToHTML/po-receipts-walkthrough.html)   | Step-by-step reconciliation |
| [Suspension and Exclusions](po-receipts-suspension-exclusion)          | Suspension and exclusion features in RR V7, including setup, use cases, and troubleshooting |

---

## Reference Materials

This section includes reference materials that provide in-depth information on various aspects of RapidReconciler and its use in JD Edwards reconciliation processes. These documents serve as a valuable resource for users seeking detailed explanations, best practices, and troubleshooting guidance related to the application. Whether you're looking for specific information on a particular feature or need comprehensive guidance on a broader topic, these reference materials will help you navigate and utilize RapidReconciler effectively.

| Document | Description |
|----------|-------------|
| [Working with the Item Ledger](MDS/inventory-item-ledger.md) | Balances, posting codes, dates, DMAAs, and integrity conditions |
| [Managing GL Class Codes](MDS/inventory-gl-class-codes.md)   | Procedure, hierarchy of change locations, why adjustments are required |
| [Product Costing Guide](MDS/inventory-costing.md)            | Cost methods, cost levels, F4105 storage, IB transactions, R41815 conversion, inventory valuation impact |
| [Ultimate DMAAI Guide](MDS/distribution-aais.md)                                         | Setup, GL class codes, business unit, financial AAIs, error messages, full AAI listing |
| [About Units of Measure](MDS/inventory-uom.md)               | Changing the primary unit of measure, impact on inventory transactions, and cardex analysis considerations |
| [Zero Balance Adjustments](MDS/inventory-zero-balance.md)    | Purpose, purchasing and inventory AAIs, journal entry examples |
| [Outside Operations](MDS/inventory-outside-ops.md)           | Item master, work center, routing, receipt, and WIP journal entries |

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*
