**Reference Guide: Manufacturing AAIs**

**Transaction Types and Journal Entry Reference**

**Section 1: Overview**

Manufacturing AAIs control how the system generates journal entries for each transaction type in the manufacturing accounting cycle. Understanding which AAI tables are debited and credited - and the cost basis used - is essential for accurate general ledger postings and reconciliation.

**Important Note on GL Class Code Usage:**

- The **credit side of the IM (Material Issue)** transaction uses the **GL class codes of the individual components** to write journal entries reducing raw material or sub-assembly inventory.
- The **debit side of the IM** transaction and **all other manufacturing transaction types** use the **GL class code of the parent item** to generate journal entries.

**Section 2: Manufacturing Transaction AAIs**

**2.1 IM - Material Issue**

|            | **AAI**     | **Account**                           | **Basis**                                     |
| ---------- | ----------- | ------------------------------------- | --------------------------------------------- |
| **Debit**  | **3120**    | Work In Process (WIP)                 | Actual Issues × Frozen Standard Cost (F30026) |
| **Credit** | **3110** \* | Raw Material / Sub-Assembly Inventory | Actual Issues × Frozen Standard Cost (F30026) |

\*The credit side uses the GL class codes of each **component**, not the parent.

**2.2 IH - Labor, Outside Operations, and Cross-Charges**

|            | **AAI**  | **Account**           | **Basis**                               |
| ---------- | -------- | --------------------- | --------------------------------------- |
| **Debit**  | **3120** | Work In Process (WIP) | Actual Labor × Frozen Work Center Rates |
| **Credit** | **3401** | Payroll Accrual       | Actual Labor × Frozen Work Center Rates |

**2.3 IC - Completions**

|            | **AAI**  | **Account**                             | **Basis**                                  |
| ---------- | -------- | --------------------------------------- | ------------------------------------------ |
| **Debit**  | **3130** | Finished Goods / Sub-Assembly Inventory | Units Completed × Frozen Standard (F30026) |
| **Credit** | **3120** | Work In Process (WIP)                   | Units Completed × Frozen Standard (F30026) |

**2.4 IS - Parent Scrap**

|            | **AAI**          | **Account**           | **Basis** |
| ---------- | ---------------- | --------------------- | --------- |
| **Debit**  | **3130 (Scrap)** | Scrap Account         | -         |
| **Credit** | **3120**         | Work In Process (WIP) | -         |

**Section 3: Variance Accounting AAIs**

**3.1 IV - Variance Accounting**

Variance accounting clears the remaining WIP balance after all manufacturing transactions have been posted. The WIP balance is calculated as:

**WIP = (IM + IH) − IC = IV**

Depending on the resulting WIP balance, the IV transaction will either debit or credit the WIP account to clear the variance:

|                                   | **AAI**  | **Account**           |
| --------------------------------- | -------- | --------------------- |
| **Debit or Credit** (as required) | **3120** | Work In Process (WIP) |

**3.2 Variance Offset Accounts**

The offsetting entries for each type of variance are directed to the following AAI accounts:

| **AAI**  | **Variance Type**    |
| -------- | -------------------- |
| **3220** | Labor Variance       |
| **3240** | Material Variance    |
| **3260** | Planned Variance     |
| **3270** | Engineering Variance |
| **3280** | Other Variance       |

Each variance AAI will receive either a debit or credit entry depending on whether the variance is favorable or unfavorable, ensuring the WIP account is fully cleared after variance accounting is run.

**Section 4: Summary Reference Table**

| **Trans Type** | **Description**             | **Debit AAI**        | **Debit Account**                 | **Credit AAI**       | **Credit Account**         | **Cost Basis**                             |
| -------------- | --------------------------- | -------------------- | --------------------------------- | -------------------- | -------------------------- | ------------------------------------------ |
| **IM**         | Material Issue              | 3120                 | WIP                               | 3110\*               | Raw Mat / Sub-Assembly Inv | Actual Issues × Frozen Standard (F30026)   |
| **IH**         | Labor / Outside Op / X-Cost | 3120                 | WIP                               | 3401                 | Payroll Accrual            | Actual Labor × Frozen Work Center Rates    |
| **IC**         | Completions                 | 3130                 | Finished Goods / Sub-Assembly Inv | 3120                 | WIP                        | Units Completed × Frozen Standard (F30026) |
| **IS**         | Parent Scrap                | 3130 (Scrap)         | Scrap                             | 3120                 | WIP                        | -                                          |
| **IV**         | Variance Accounting         | 3120 or Variance AAI | WIP or Variance Account           | 3120 or Variance AAI | WIP or Variance Account    | (IM + IH) − IC                             |

\*IM credit side uses GL class codes of **components**; all other debit/credit entries use the GL class code of the **parent item**.
