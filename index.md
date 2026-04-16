# RapidReconciler
## Document Library

Welcome to the GSI RapidReconciler documentation library. Use the links below to navigate to individual documents by topic area.

---

## Technical Guide

| Document | Description |
|----------|-------------|
| [Technical Requirements](MDS/tech-requirements) | Installation and configuration requirements |
| [Installing RapidReconciler-Prod)](MDS/Installing_production_database.md) | Step-by-step VALC setup and RR Agent installation |
| [Installing a Client in VALC (GSI Use Only)](MDS/installing-valc) | Step-by-step database, user and job installation |
| [Server Migration Guide](MDS/server-migration) | Moving RapidReconciler to a new dedicated or separate server |


---

## Getting Started

| Document | Description |
|----------|-------------|
| [Adding a New Company](MDS/adding-company.md) | How to request additional company licenses and edit company settings in RapidReconciler. |
| [Getting Started with the Application](MDS/getting-started-with-rapidreconciler) | Logging in, navigating the interface, and system requirements |
| [Administrator Responsibilities](MDS/admin-responsibilities) | Company management, user setup, general settings, and offset accounts |
| [Complex Password](MDS/complex-password) | Password policy requirements and reset process |

---

## Inventory

| Document | Description |
|----------|-------------|
| [Inventory Key Concepts](MDS/inventory-key-concepts) | DMAAI tables, GL account assignment, period end logic, variance sources, cardex variance, GL class codes |
| [How to Add an Inventory Account in RR](MDS/add-account-rr) | DMAAI model table process and refresh requirements |
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