# RapidReconciler & JD Edwards
## Training Manual Library

Welcome to the GSI RapidReconciler and JD Edwards training documentation. Use the links below to navigate to individual training manuals by topic area.

---

## RapidReconciler — Getting Started

| Document | Description |
|----------|-------------|
| [Getting Started with the Application](03-getting-started.md) | Logging in, navigating the interface, and system requirements |
| [Administrator Responsibilities](04-admin-responsibilities.md) | Company management, user setup, general settings, and offset accounts |
| [Installing a Client in VALC](09-installing-valc.md) | Step-by-step VALC setup and RR Agent installation |
| [Server Migration Guide](52-server-migration.md) | Moving RapidReconciler to a new dedicated or separate server |

---

## RapidReconciler — Inventory Module

| Document | Description |
|----------|-------------|
| [Inventory Key Concepts: Preparing Item Data](01-inventory-key-concepts.md) | DMAAI tables, GL account assignment, period end logic, variance sources, cardex variance, GL class codes |
| [Inventory: Using the Application](05-inventory-using-application.md) | Reconciliation page, transactions page, As-Of page, Roll Forward, integrity reports, reconciliation process |

---

## RapidReconciler — In Transit Module

| Document | Description |
|----------|-------------|
| [In Transit Key Concepts](06-in-transit-key-concepts.md) | ST/OT process, accounting setup, order pairs, exclusions |
| [In Transit: Using the Application](07-in-transit-using-application.md) | Orders page, reconciliation page, transactions page, As-Of page, integrity reports |

---

## RapidReconciler — PO Receipts Module

| Document | Description |
|----------|-------------|
| [PO Receipts Key Concepts](08-po-receipts-key-concepts.md) | RNV definition, process flow, Table F43121, match types, challenges |
| [PO Receipts: Using the Application](02-po-receipts-using-application.md) | Orders page, reconciliation page, line analysis, how to reconcile |

---

## JD Edwards — Inventory

| Document | Description |
|----------|-------------|
| [GL Class Codes: Changing a GL Class Code](20-gl-class-code-changes.md) | Procedure, hierarchy of change locations, why adjustments are required |
| [Changing Item Primary Unit of Measure](10-changing-primary-uom.md) | Risks, procedure, and considerations for history, BOM, GL, warehousing, EDI |
| [Unit of Measure Conversion](47-uom-conversion.md) | Hierarchy, standard vs. item conversions, weight and volume setup |
| [Weighted Average Cost](48-weighted-average-cost.md) | Setup, UDC 40/AV, online vs. batch, landed cost and receipt routing impacts |
| [Costs in EnterpriseOne](51-costs-enterpriseone.md) | Cost levels, cost methods, F4105 storage, IB transactions, R41815 conversion |
| [Zero Balance Adjustments](49-zero-balance-adjustments.md) | Purpose, purchasing and inventory AAIs, journal entry examples |
| [Cardex Analysis: Weighted Average Cost Error](18-cardex-weighted-average-error.md) | Identifying and investigating weighted average cost calculation errors |
| [Cardex Analysis: 3 Common Analyst Errors](19-cardex-analyst-errors.md) | Memo transactions, alternate UOM, average cost item analysis levels |
| [Performing a Dollars-Only Inventory Adjustment](27-dollars-only-adjustment.md) | Standard vs. average cost environments, UDC 40/AV, P4114 procedure |

---

## JD Edwards — Purchasing

| Document | Description |
|----------|-------------|
| [Accounting in Purchasing: Overview](50-accounting-in-purchasing.md) | File updates and journal entries for stock 3-way, non-stock 2-way and 3-way match |
| [Taxes in Procurement](46-taxes-procurement.md) | Tax setup, explanation codes, AAIs, and GL treatment for S, U, V, C, B codes |
| [Landed Costs in EnterpriseOne](40-landed-costs.md) | Setup, cost rules, journal entries, F43121 records, performance notes |
| [The 4332 AAI: Purpose and Impact](30-aai-4332.md) | Cost variance at voucher match, journal entry examples, configuration |
| [Material Burden AAI (4337)](31-material-burden-aai.md) | Purpose, setup, calculation, and journal entry scenarios |
| [Direct Ship Orders](35-direct-ship-orders.md) | Setup, line type, AAIs, partial shipments, multi-currency, ECS |
| [How to Add an Inventory Account in RR](32-add-account-rr.md) | DMAAI model table process and refresh requirements |

---

## JD Edwards — Sales

| Document | Description |
|----------|-------------|
| [FAQ: Sales Update (P42800)](44-sales-update-faq.md) | File updates, processing order, AAIs, batch types, proof vs. final, errors |
| [Tax in Sales](45-tax-in-sales.md) | Tax explanation codes, Rate/Area setup, AAIs, S/V/C/E examples |
| [Sales Order Intercompany Processing](39-intercompany-processing.md) | SI/SK/OK orders, R4210IC, journal entries, cost alignment |

---

## JD Edwards — Manufacturing

| Document | Description |
|----------|-------------|
| [Introduction to Manufacturing Accounting](34-manufacturing-accounting.md) | Cost flows, transaction types, setup tips, execution best practices |
| [Manufacturing AAIs Reference](41-manufacturing-aais.md) | IM, IH, IC, IS, and IV transaction types with AAI debit/credit tables |
| [R30837 WIP Revaluation for Standard Costing](33-wip-revaluation.md) | How WIP reval works, prerequisites, setup, journal entries, full example |
| [Outside Operations: Setup and Accounting](42-outside-operations.md) | Item master, work center, routing, receipt, and WIP journal entries |
| [Outside Operations: Troubleshooting](43-outside-operations-troubleshooting.md) | Why POs are not created — item, system, routing, vendor, and security issues |

---

## JD Edwards — Distribution Setup

| Document | Description |
|----------|-------------|
| [AAIs for Distribution](36-distribution-aais.md) | Setup, GL class codes, business unit, financial AAIs, error messages, full AAI listing |
| [Flexible Accounting for Distribution](37-flexible-accounting.md) | Background, requirements, enabling, establishing flexible accounts |
| [How to Set Up a Branch/Plant](38-branch-plant-setup.md) | Address book, business unit, constants, and default branch update |
| [ST/OT Transfer Order Accounting — Part 3](16-transfer-order-accounting-pt3.md) | OT receipt with DMAAI 4335, cost change before shipment |
| [ST/OT Transfer Order Accounting — Part 4](25-transfer-order-accounting-pt4.md) | Standard cost variance in receiving branch, DMAAI 4335 configuration |
| [ST/OT: Inventory Tracking Without Receipts Routing](17-st-ot-tracking.md) | RapidReconciler As-Of alternative to receipts routing |
| [ST/OT: Exclusions in RapidReconciler](15-st-ot-exclusions.md) | Unbalanced transfers, exclusion process, journal entries |
| [ST/OT: Exclusion Variance Added to Orders List](14-st-ot-exclusion-variance.md) | ExclVarQty and ExclVarAmt columns, unexclude and re-exclude process |

---

## JD Edwards — General Reference

| Document | Description |
|----------|-------------|
| [Automatic Accounting Instructions: The 4332 AAI](30-aai-4332.md) | Purpose, pre- and post-4332 journal entry comparison |
| [Item Ledger: Top 5 Questions Answered](22-item-ledger-faq.md) | Balances, posting codes, dates, DMAAs, and integrity conditions |
| [3 Reasons Stock Status May Not Match Trial Balance](23-stock-status-trial-balance.md) | Timing, backdating, report definition |
| [Stock Status vs. Trial Balance — Part 2](26-stock-status-trial-balance-pt2.md) | DMAAI setup and GL class code change impacts |
| [Global Item Update: A "Gotcha"](29-global-item-update.md) | Creation date override on item ledger records |

---

## GSI Insider Articles — JD Edwards Insights

| Document | Description |
|----------|-------------|
| [Inventory Reconciliation: Top 6 Issues — Part 2](11-top-6-issues-pt2.md) | GL class code changes and reconciliation impact |
| [Inventory Reconciliation: Top 6 Issues — Part 3](12-top-6-issues-pt3.md) | Product costing and R30543 cost component integrity |
| [RapidReconciler: Transaction Detail Report Update](13-transaction-detail-report.md) | Enhanced drill-down for intercompany, transfer, and direct ship orders |
| [Reconciling RNV Accounts in RapidReconciler](21-reconciling-rnv.md) | Summary, drill-down, and suspension features in RR V7 |
| [GSI Introduces Online Training Modules](24-online-training.md) | Trainual platform overview and available modules |
| [Cardex Analysis: Weighted Average Cost Error](18-cardex-weighted-average-error.md) | Root cause investigation and dollar variance identification |

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*
