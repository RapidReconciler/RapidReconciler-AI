# RapidReconciler & JD Edwards
## Training Manual Library

Welcome to the GSI RapidReconciler and JD Edwards training documentation. Use the links below to navigate to individual training manuals by topic area.

---

## RapidReconciler — GSI Technical Guide

| Document | Description |
|----------|-------------|
| [Installing a Client in VALC](installing-valc) | Step-by-step VALC setup and RR Agent installation |
| [Server Migration Guide](server-migration) | Moving RapidReconciler to a new dedicated or separate server |

---

## RapidReconciler — Getting Started

| Document | Description |
|----------|-------------|
| [Adding a New Company](adding_company.md) | How to request additional company licenses and edit company settings in RapidReconciler. |
| [Getting Started with the Application](getting-started-with-rapidreconciler) | Logging in, navigating the interface, and system requirements |
| [Administrator Responsibilities](admin-responsibilities) | Company management, user setup, general settings, and offset accounts |

---

## RapidReconciler — Inventory

| Document | Description |
|----------|-------------|
| [Inventory Key Concepts: Preparing Item Data](inventory-key-concepts) | DMAAI tables, GL account assignment, period end logic, variance sources, cardex variance, GL class codes |
| [How to Add an Inventory Account in RR](add-account-rr) | DMAAI model table process and refresh requirements |
| [Inventory: Using the Application](inventory-using-application) | Reconciliation page, transactions page, As-Of page, Roll Forward, integrity reports, reconciliation process |
| [Inventory Reconciliation: Top 6 Issues — Part 2](top-6-issues-pt2) | GL class code changes and reconciliation impact |
| [Inventory Reconciliation: Top 6 Issues — Part 3](top-6-issues-pt3) | Product costing and R30543 cost component integrity |
| [RapidReconciler: Transaction Detail Report Update](transaction-detail-report) | Enhanced drill-down for intercompany, transfer, and direct ship orders |

---

## RapidReconciler — In Transit

| Document | Description |
|----------|-------------|
| [In Transit Key Concepts](in-transit-key-concepts) | ST/OT process, accounting setup, order pairs, exclusions |
| [In Transit: Using the Application](in-transit-using-application) | Orders page, reconciliation page, transactions page, As-Of page, integrity reports |
| [ST/OT Transfer Order Accounting — Part 3](transfer-order-accounting-pt3) | OT receipt with DMAAI 4335, cost change before shipment |
| [ST/OT Transfer Order Accounting — Part 4](transfer-order-accounting-pt4) | Standard cost variance in receiving branch, DMAAI 4335 configuration |
| [ST/OT: Inventory Tracking Without Receipts Routing](st-ot-tracking) | RapidReconciler As-Of alternative to receipts routing |
| [ST/OT: Exclusions in RapidReconciler](st-ot-exclusions) | Unbalanced transfers, exclusion process, journal entries |
| [ST/OT: Exclusion Variance Added to Orders List](st-ot-exclusion-variance) | ExclVarQty and ExclVarAmt columns, unexclude and re-exclude process |

---

## RapidReconciler — PO Receipts 

| Document | Description |
|----------|-------------|
| [PO Receipts Key Concepts](po-receipts-key-concepts) | RNV definition, process flow, Table F43121, match types, challenges |
| [PO Receipts: Using the Application](po-receipts-using-application) | Orders page, reconciliation page, line analysis, how to reconcile |
| [Direct Ship Orders](direct-ship-orders) | Setup, line type, AAIs, partial shipments, multi-currency, ECS |
| [Reconciling RNV Accounts in RapidReconciler](reconciling-rnv) | Summary, drill-down, and suspension features in RR V7 |

---

## JD Edwards — Insights

| Document | Description |
|----------|-------------|
| [Introduction to Manufacturing Accounting](manufacturing-accounting) | Cost flows, transaction types, setup tips, execution best practices |
| [Manufacturing AAIs Reference](manufacturing-aais) | IM, IH, IC, IS, and IV transaction types with AAI debit/credit tables |
| [R30837 WIP Revaluation for Standard Costing](wip-revaluation) | How WIP reval works, prerequisites, setup, journal entries, full example |
| [Outside Operations: Setup and Accounting](outside-operations) | Item master, work center, routing, receipt, and WIP journal entries |
| [Outside Operations: Troubleshooting](outside-operations-troubleshooting) | Why POs are not created — item, system, routing, vendor, and security issues |
| [Global Item Update: A "Gotcha"](global-item-update) | Creation date override on item ledger records |
| [FAQ: Sales Update (P42800)](sales-update-faq) | File updates, processing order, AAIs, batch types, proof vs. final, errors |
| [Tax in Sales](tax-in-sales) | Tax explanation codes, Rate/Area setup, AAIs, S/V/C/E examples |
| [Sales Order Intercompany Processing](intercompany-processing) | SI/SK/OK orders, R4210IC, journal entries, cost alignment |
| [Accounting in Purchasing: Overview](accounting-in-purchasing) | File updates and journal entries for stock 3-way, non-stock 2-way and 3-way match |
| [Taxes in Procurement](taxes-procurement) | Tax setup, explanation codes, AAIs, and GL treatment for S, U, V, C, B codes |
| [Landed Costs in EnterpriseOne](landed-costs) | Setup, cost rules, journal entries, F43121 records, performance notes |
| [The 4332 AAI: Purpose and Impact](aai-4332) | Cost variance at voucher match, journal entry examples, configuration |
| [Material Burden AAI (4337)](material-burden-aai) | Purpose, setup, calculation, and journal entry scenarios |
| [AAIs for Distribution](distribution-aais) | Setup, GL class codes, business unit, financial AAIs, error messages, full AAI listing |
| [Flexible Accounting for Distribution](flexible-accounting) | Background, requirements, enabling, establishing flexible accounts |
| [How to Set Up a Branch/Plant](branch-plant-setup) | Address book, business unit, constants, and default branch update |
| [GL Class Codes: Changing a GL Class Code](gl-class-code-changes) | Procedure, hierarchy of change locations, why adjustments are required |
| [Changing Item Primary Unit of Measure](changing-primary-uom) | Risks, procedure, and considerations for history, BOM, GL, warehousing, EDI |
| [Unit of Measure Conversion](uom-conversion) | Hierarchy, standard vs. item conversions, weight and volume setup |
| [Weighted Average Cost](weighted-average-cost) | Setup, UDC 40/AV, online vs. batch, landed cost and receipt routing impacts |
| [Costs in EnterpriseOne](costs-enterpriseone) | Cost levels, cost methods, F4105 storage, IB transactions, R41815 conversion |
| [Zero Balance Adjustments](zero-balance-adjustments) | Purpose, purchasing and inventory AAIs, journal entry examples |
| [Cardex Analysis: Weighted Average Cost Error](cardex-weighted-average-error) | Identifying and investigating weighted average cost calculation errors |
| [Cardex Analysis: 3 Common Analyst Errors](cardex-analyst-errors) | Memo transactions, alternate UOM, average cost item analysis levels |
| [Performing a Dollars-Only Inventory Adjustment](dollars-only-adjustment) | Standard vs. average cost environments, UDC 40/AV, P4114 procedure |
| [Item Ledger: Top 5 Questions Answered](item-ledger-faq) | Balances, posting codes, dates, DMAAs, and integrity conditions |
| [3 Reasons Stock Status May Not Match Trial Balance](stock-status-trial-balance) | Timing, backdating, report definition |
| [Stock Status vs. Trial Balance — Part 2](stock-status-trial-balance-pt2) | DMAAI setup and GL class code change impacts |


---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*
