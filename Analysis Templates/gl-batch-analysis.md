# GL Batch Analysis Guide

## RapidReconciler — Unposted GL Batches Report Reference

---

## Section 1: Using Claude for Automated Analysis

Claude can perform the full Section 12 analysis procedure automatically and return a single updated `.xlsx` file with the analysis sheet added and all source rows highlighted.

### 1.1 What to Upload

Upload **two files**:

1. This guide (`.md`)
2. The Unposted GL Batches export (`.xlsx`)

Then use the following prompt:

> *"Analyze this file using the guide as a template, then produce an updated copy of the Excel file with the analysis written to a new sheet called 'GL Batch Analysis' and all source rows highlighted by priority."*

Claude will work through the Section 12 procedure against the Excel data, apply highlights to the source sheet, and add the analysis sheet in the format specified in Section 13. The returned file is a drop-in replacement for the original.

### 1.2 Follow-On Requests in the Same Session

Once the guide has been uploaded in a session, Claude retains it in context for the remainder of the conversation. Subsequent GL batch exports do not require the guide to be uploaded again. Use the shorter prompt:

> *"Analyze this file and return it with the analysis sheet and highlights."*

Start a new session when switching to a different guide version or when the conversation has been idle long enough that context may have been lost.

### 1.3 Output Specification

**File naming:** Name the output file `DMAAI Analysis.xlsx`.

**Sheet 1 — Unposted GL Batches (original sheet, highlights added)**

| Highlight | Color | Criteria |
|---|---|---|
| Red | `FFCCCC` | In Use OR age ≥ 8 days OR posting error |
| Orange | `FFE5CC` | Pending approval / Pending (needs approval) |
| Yellow | `FFFACD` | Approved / Approved (needs posting run only) |

**Sheet 2 — GL Batch Analysis (new sheet)**

Follows the structure defined in Section 13.4. Contains Report Summary, Status Summary, Findings by Priority, and Recommended Actions.

### 1.4 Notes and Limitations

- Claude analyzes the data as exported. If the report was generated with account filters applied, the total variance reflects only the filtered accounts — not the full GL Batches variance for the period.
- Batch age is calculated against the PeriodEnds date in the export. The analysis always uses PeriodEnds as the reference point, not the date the analysis is run.
- Claude cannot access JD Edwards to verify batch details, confirm user identities, or look up invoice amounts. Findings that require JD Edwards investigation are flagged as open items in the Recommended Actions section.
- For exports with more than 50 rows, include a note in the prompt identifying the period-end date to confirm the correct reference point for age calculations.
- Amounts in the exported file may display with floating-point precision artifacts. Claude rounds all amounts to two decimal places for reporting purposes.

---


## Overview

The Unposted GL Batches report in RapidReconciler lists every batch that contributes to the GL Batches variance for the selected period and account filters. Each row represents a single F0911 record — a GL detail entry that has not yet been fully posted to account balances (F0902).

The report is the primary diagnostic tool for the GL Batches variance source. Before any period-end closing activity can begin, this report must be worked to zero.

In JD Edwards EnterpriseOne, every transaction that affects the general ledger is grouped into a **batch** before it is posted to account balances. A batch must pass through two sequential gates before it updates the GL:

1. **Approval** — the batch is reviewed and authorized for posting
2. **Posting** — the GL detail table (F0911) is summarized into the account balance table (F0902)

Until both steps are complete, transactions exist in F0911 but are not reflected in F0902. RapidReconciler reports these unposted amounts as a variance under the GL Batches source.

**Key tables:**

| Table | Description |
|---|---|
| **F0011** | Batch Control Records — one record per batch; holds batch header, approval status, and posting status |
| **F0911** | Account Ledger — GL transaction detail; records exist here before and after posting |
| **F0902** | Account Balances — period-end balances; only updated when a batch is posted in final mode |

> **Who should use this guide:** JD Edwards cost accountants, inventory accountants, and AP/AR staff responsible for investigating and resolving unposted batch variances in RapidReconciler.

> **Important:** All corrections to batch status are made in JD Edwards. RapidReconciler displays batch posting variances for visibility but does not modify JD Edwards data.

---

## Section 2: Batch Processing Fundamentals

### 2.1 Batch Processing Flow

```
Transaction entered in JD Edwards
        ↓
Batch created in F0011
Batch status: Approved = blank, Posted = blank
        ↓
Manual or automatic approval
Batch status: Approved = A, Posted = blank
        ↓
Posting program runs (R09801)
        ↓
Post succeeds → F0902 updated
Batch status: Approved = A, Posted = D (Done)
        ↓
Post fails → Error written to F0011
Batch status: Approved = A, Posted = E (Error)
```

A batch that has not been approved (Approved = blank) will not post even if the posting program is run. A batch in error status (Posted = E) requires investigation and correction before it can be reposted.

### 2.2 Required Status Before Period-End Close

The GL Batches variance must equal **$0** before performing any period-end closing activities in RapidReconciler. Specifically:

- All inventory-related batches must have a posting status of **D** (Done)
- No batches in **E** (Error) or **In Use** status should remain outstanding
- The bell icon on the GL Batches row should not be present

> **Do not post closing journal entries or produce the Audit Report until the GL Batches variance is zero.** A non-zero GL Batches amount means the GL account balances in F0902 do not accurately reflect all posted transactions, and any closing entries based on those balances will be calculated on an incomplete picture.

---

## Section 3: Batch Type Reference

The batch type in F0011 identifies what kind of transactions the batch contains and determines which approval and posting rules apply.

| Batch Type | Description | Typical Source Programs |
|---|---|---|
| **G** | General Journal | Journal Entry (P0911) |
| **N** | Inventory Adjustments / Issues / Transfers | P4112, P4113, P4114, P4116 |
| **IB** | Inventory Balance Adjustments | Cost changes, Re-Roll operations |
| **V** | Accounts Payable Vouchers | Voucher Entry (P0411), Voucher Match (P4314) |
| **R** | Accounts Receivable | Invoice Entry (P03B11), Receipt Entry (P03B102) |
| **D** | Accounts Payable Payments | Payment Processing (R04570) |
| **O** | Purchase Order Receipts | PO Receipts (P4312) |
| **W** | Manufacturing / Work Orders | Manufacturing Accounting (R31802A) |
| **S** | Sales Update | Sales Update (R42800) |
| **ST** | Stock Transfer | Transfer Order processing |
| **NC** | Frozen Cost Update | Frozen Standard Cost Update (R30835) |

---

## Section 4: Approval Status Codes

The approval status is stored in F0011 and controls whether the batch is eligible to be posted.

| Code | Status | Description | Action Required |
|---|---|---|---|
| *(blank)* | **Pending** | Batch has been created but not yet approved. Will not post. | Approve manually via Batch Approval (P0011) or configure automatic approval — see Section 10. |
| **A** | **Approved** | Batch has been approved and is eligible for posting. | None — batch is ready to post. |
| **D** | **Approved (Auto)** | Batch was approved automatically based on company constants configuration. | None — batch is ready to post. |
| **H** | **Hold** | Batch has been placed on hold and will not be approved or posted until released. | Investigate why the hold was applied. Release via P0011 once the issue is resolved. |
| **R** | **Rejected** | Batch was submitted for approval but rejected by the approver. | Review rejection reason. Correct the batch and resubmit for approval. |
| **S** | **Submitted** | Batch has been submitted for approval and is awaiting review. | No action required until the approver acts. Follow up if approval is delayed. |

---

## Section 5: Posting Status Codes

The posting status is stored in F0011 and reflects the result of the most recent posting attempt.

| Code | Status | Description | Action Required |
|---|---|---|---|
| *(blank)* | **Unposted** | Batch has not yet been posted. May or may not be approved. | Approve if needed, then run the posting program (R09801). |
| **D** | **Posted** | Batch has been fully posted. F0902 account balances have been updated. | None. |
| **E** | **Error** | The posting program encountered an error and could not post the batch. F0902 has not been updated. | Investigate the error using P0011. See Section 9 for common errors and resolutions. |
| **P** | **In Process** | The posting program is currently running for this batch. | Wait for the posting run to complete. If the status remains P for an extended time, investigate whether the posting job has stalled. |
| **#** | **Held by System** | The system has placed the batch in a temporary hold during processing. | Usually resolves automatically. If the status persists, contact your system administrator. |

---

## Section 6: Report Structure and Field Reference

### 6.1 Report Structure

The Unposted GL Batches report is a flat row-per-account export. Unlike the Transaction Detail report, it does not have named sections — every row is a data row with the same column structure.

Key structural rules:

- **One row per F0911 account line** — a single batch may appear across multiple rows if it contains entries to multiple accounts or multiple companies.
- **All rows are unposted** — the report only includes records where the GL posting code in F0911 is not **P** (Posted). Fully posted batches do not appear.
- **The report does not net by batch** — if a batch has entries to two accounts, both rows appear separately. The batch-level variance is the sum of all rows for that batch number.
- **Period filter applies** — the period shown in the filename and report header reflects the RapidReconciler period filter in effect when the report was generated. Rows from prior periods that remain unposted may also appear if they fall within that filter.

### 6.2 Column Definitions

| Column | Description |
|---|---|
| **CompanyNumber** | JD Edwards company number. Leading zeros are included (e.g., 00067). Used to group batches by entity and to identify which company constants govern approval requirements. |
| **BatchDate** | The date the batch was created in JD Edwards. Used to calculate batch age. Batches more than 2 days old at period end require escalated attention. |
| **PeriodEnds** | The period-end date for the RapidReconciler period filter in effect when the report was generated. All rows in a given export share the same PeriodEnds value. |
| **Username** | The JD Edwards user ID that created the batch. System schedulers appear as JDESCHED or similar. Use this field to identify the person or process responsible for the batch. |
| **LongAccount** | The full GL account number in Business Unit.Object.Subsidiary format (e.g., 67010.1421). Use this to identify the inventory account affected and to cross-reference against the chart of accounts. |
| **BatchNumber** | The JD Edwards batch number (F0011 key field). Multiple rows with the same batch number belong to the same batch — they must be resolved together. |
| **Type** | Batch type code. Identifies the source of the transaction. See Section 3 for the full batch type reference. Common types: **G** (General Journal), **IB** (Inventory Balance), **N** (Inventory), **O** (PO Receipt), **V** (Voucher). |
| **Amount** | The net GL amount for this account row. Positive = debit; negative = credit. For a given batch, amounts across all rows should net to zero for a balanced batch. |
| **Currency** | Currency code for the amount. USD is most common. Multi-currency batches require exchange rate verification before posting. |
| **Rate** | Exchange rate applied. 1.0 indicates domestic currency or no conversion required. Rates other than 1.0 indicate a foreign currency transaction. |
| **Approval_Status** | Current approval state of the batch in F0011. See Section 4 for all codes and actions. |
| **Posting_Status** | Current posting state of the batch in F0011. See Section 5 for all codes and actions. |

### 6.3 Derived Fields for Analysis

The following fields are not in the source report but should be calculated or noted during analysis:

| Derived Field | How to Calculate | Purpose |
|---|---|---|
| **Batch Age (Days)** | PeriodEnds date minus BatchDate | Identifies stale batches. Over 2 days requires attention. Over 7 days requires escalation. Over 14 days is critical. |
| **Batch Total** | Sum of Amount for all rows sharing the same BatchNumber | Confirms whether the batch is balanced (net = $0 for a standard inventory or purchasing batch). An unbalanced batch will fail to post. |
| **Total Variance** | Sum of all Amount values in the report | The total GL Batches variance for the period. Must reach $0 before period close. |

---

## Section 7: Status Code Combinations and What They Mean

Every row in the report carries both an Approval_Status and a Posting_Status. The combination determines the required action.

| Approval_Status | Posting_Status | Meaning | Priority | Action |
|---|---|---|---|---|
| **Pending approval** | **In Use** | The batch posting status needs to be manually reset in JD Edwards. Navigate to the Batch Header Revisions screen (P0011), locate the batch by number, and update the posting status to blank (unposted). The batch can then be approved and posted normally. | **Critical** | Open P0011, locate the batch, manually set the posting status to blank. Approve if needed, then run R09801. |
| **Pending approval** | **Pending** | Batch header exists but has not been approved. Will not post until approved. | **High** | Approve in P0011, then run R09801. |
| **Pending approval** | **Error** | Batch was approved, posted, encountered an error, and approval was reset. | **High** | Review the error in P0011. Resolve the underlying issue. Re-approve and repost. See Section 9. |
| **Approved** | **Approved** | Batch is approved and ready to post but R09801 has not yet run for it. | **Normal** | Run R09801 for the applicable company and batch type. |
| **Approved** | **Error** | Posting was attempted but failed. Batch is still approved. | **High** | Review the error in P0011. Resolve the issue. Repost with R09801. See Section 9. |
| **Approved** | **In Process** | Posting is currently running. | **Monitor** | Wait for completion. If the status does not change within a reasonable time, investigate whether the job has stalled. |

> **"In Use" posting status:** RapidReconciler displays "In Use" when the batch posting status in F0011 is in a state that prevents posting. The corrective action is to open the batch in the **Batch Header Revisions screen (P0011)** in JD Edwards and manually set the posting status back to blank (unposted). Once reset, the batch can be approved and posted through the normal process. It does not mean another user has the batch locked.

> **Bell icon:** A bell icon on the GL Batches row in RapidReconciler indicates one or more batches have been in an unposted or error state for more than 2 days. Escalate for immediate investigation.

---

## Section 8: Common Batch Patterns and Root Causes

### 8.1 "In Use" Posting Status — O-Type Batches from System Scheduler

**Symptoms:**
- Multiple O-type batches from JDESCHED (or another scheduler user) with Posting_Status = "In Use"
- All batches in the same company
- Spanning several weeks or multiple periods
- All pointing to the same inventory account

**What is happening:**

The batch posting status in F0011 is in a state that prevents posting — RapidReconciler labels this "In Use." This can occur when a posting job was interrupted mid-run, leaving the status in a non-blank, non-posted state. Because JDESCHED is a system scheduler, these situations accumulate silently — no user is monitoring the output. The result is a growing stack of batches that block the GL Batches variance from clearing.

**How to identify recurrence:**

If the oldest batch is significantly older than the newest (e.g., the oldest is 29 days old and the newest is 6 days old), the same failure has been occurring repeatedly. This indicates a systemic problem with the receipt posting job, not a one-time event.

**Resolution:**

> ⚠ **Before making any changes in JD Edwards:** Test all configuration changes in a non-production environment first. For any scenario where a GL journal entry may be required, review the Transactions page in RapidReconciler for the affected items to confirm exact amounts and accounts before posting.

1. Open the **Batch Header Revisions screen (P0011)** in JD Edwards.
2. Search for the batch by number.
3. Manually set the **posting status to blank** (unposted).
4. Approve the batch if it is not already approved.
5. Run R09801 to post.
6. Investigate the root cause of the scheduler failure with IT — configure alerting so future occurrences surface immediately rather than accumulating.

### 8.2 Pending Approval — IB Batch Spanning Multiple Accounts

**Symptoms:**
- Multiple rows with the same BatchNumber and Type = IB
- Each row shows a different LongAccount
- Both rows show Pending approval / Pending

**What is happening:**

An inventory balance adjustment (IB) affected multiple inventory accounts — for example, an item cost change that posted to accounts in two different business units. Both account rows are part of the same batch and must be reviewed and approved together.

**Resolution:**

1. Navigate to P0011 and locate the batch.
2. Review both account entries to confirm the amounts and accounts are correct.
3. Approve the batch. Both rows will clear simultaneously since they share a batch number.
4. Run R09801.

> **Note:** Do not approve the batch if the two account entries do not appear to offset each other or if the accounts are unexpected. Contact the user who created the batch (visible in the Username column) before approving.

### 8.3 Pending Approval — G-Type Manual Journal Entry

**Symptoms:**
- Batch type = G
- Approval_Status = Pending approval
- Username is a named user (not a scheduler)
- Batch age is several days

**What is happening:**

A user entered a manual journal entry (P0911) that has not been approved. G-type batches typically require manual approval due to segregation of duties controls. The batch will not post until an authorized approver reviews it.

**Resolution:**

1. Contact the user in the Username field to confirm the purpose of the journal entry.
2. Obtain supervisor sign-off if required by policy.
3. Approve in P0011.
4. Run R09801.

> **Escalation:** If the batch age exceeds 5 business days and the responsible user cannot be contacted, escalate to the finance manager. A manual journal entry sitting unposted across a period end can affect closing balances.

### 8.4 Pending Approval — V-Type AP Voucher

**Symptoms:**
- Batch type = V
- Approval_Status = Pending approval
- Amount is typically larger (supplier invoice level)

**What is happening:**

An AP voucher was entered and is awaiting approval before it can post. AP vouchers frequently require manual approval as part of payment controls.

**Resolution:**

1. Confirm the voucher is valid — locate the supplier invoice and verify the amount matches.
2. Confirm the GL account in the LongAccount column is correct for the purchase.
3. Approve in P0011.
4. Run R09801.

> **Important:** Do not approve an AP voucher without verifying the underlying invoice. An incorrectly entered voucher that posts to an inventory account will appear as a GL-only variance in RapidReconciler's Transactions page.

### 8.5 Approved and Ready to Post — N-Type Inventory Batches

**Symptoms:**
- Batch type = N
- Approval_Status = Approved
- Posting_Status = Approved
- Batch dates are recent (same day or prior day)
- Multiple batches from the same user on the same account

**What is happening:**

Inventory transactions (P4112, P4113, P4114, P4116) have been entered and approved — either manually or automatically — but the GL posting program (R09801) has not yet run for these batches. This is normal for end-of-day or same-day transactions. No approval action is required; the batches just need to be posted.

**Resolution:**

Run R09801 for the applicable company. All approved N-type batches for that company will be posted in the run. No batch-by-batch action is needed.

> **If N-type batches from a prior day or earlier are still unposted:** Investigate whether the scheduled R09801 job ran successfully for that period. A missing or failed posting run may explain why multiple days of transactions are backed up.

---

## Section 9: Resolving Common Posting Errors

When a batch has a posting status of **E** (Error), navigate to the Batch Review program (P0011) and review the error message in the batch header. The most common errors and their resolutions are below.

### 9.1 Invalid Object Account

| Field | Detail |
|---|---|
| **Error** | Object account is invalid or is not set up as a posting account |
| **How to identify** | Error message in P0011 references an invalid account number; the account does not exist in the Chart of Accounts (F0901) or has a posting code of "N" (non-posting) |
| **Cause** | An AAI, manual journal entry, or program processing option references an account that does not exist or is marked as a header account |
| **Resolution** | (1) Verify the account exists in the Chart of Accounts (P0901 off menu G09411). (2) If the account does not exist, add it or correct the AAI pointing to it. (3) If the account exists but is non-posting, change the posting code to "Y" or redirect the AAI to a valid posting account. (4) Correct the account directly in F0911 if required (IT involvement). |

### 9.2 Invalid Business Unit

| Field | Detail |
|---|---|
| **Error** | Business unit does not exist in the Business Unit Master (F0006) |
| **How to identify** | Error message references an unrecognized business unit; the business unit is not visible in the Organization Structure (P0006) |
| **Cause** | An AAI, manual entry, or program references a business unit that has not been set up, was deleted, or has a typo |
| **Resolution** | (1) Verify the business unit exists in F0006 (P0006 off menu G09411). (2) If missing, add the business unit or correct the AAI. (3) If the business unit was recently deleted or renamed, update any AAIs or processing options referencing it. |

### 9.3 Amounts Out of Balance

| Field | Detail |
|---|---|
| **Error** | Debits do not equal credits in the batch |
| **How to identify** | Error message states the batch is out of balance; running the batch proof report shows a non-zero net amount |
| **Cause** | A transaction was partially entered, a line was deleted after entry, a rounding difference was introduced, or a system interruption occurred during transaction creation |
| **Resolution** | (1) Run the batch proof report to identify which document is out of balance. (2) Locate the document in F0911 and review all lines. (3) Add the missing offsetting entry or remove the orphaned line. (4) For system-generated batches, investigate the source program — do not rebalance by adding manual lines without understanding the root cause. |

### 9.4 Invalid GL Date — Closed Period

| Field | Detail |
|---|---|
| **Error** | Batch is attempting to post to a closed or non-existent fiscal period |
| **How to identify** | Error message references an invalid GL date or closed period; the GL date on the batch falls outside the open period range in Company Constants |
| **Cause** | The batch was created with a GL date in a period that has since been closed, or the GL date was entered incorrectly |
| **Resolution** | (1) Check the open period in Company Constants (P0010) for the applicable company. (2) If the period should still be open, re-open it temporarily, post the batch, then re-close. (3) If the transaction should post in the current period, change the GL date on the batch via P0011 or directly in F0911. Consult the finance team before re-opening closed periods. |

### 9.5 Account in a Locked Company

| Field | Detail |
|---|---|
| **Error** | The company associated with the batch is locked for posting |
| **How to identify** | Error message references a locked company; Company Constants (P0010) shows the company is in a lock state |
| **Cause** | The company was locked for period-end processing, year-end close, or audit |
| **Resolution** | (1) Confirm with the finance team whether the lock is intentional. (2) If the lock should be released, unlock the company in Company Constants (P0010). (3) Do not unlock a company without authorization — the lock may be in place for audit or legal reasons. |

---

## Section 10: Setting Up Automatic Batch Approval

By default, JD Edwards requires batches to be manually approved before they can be posted. Automatic batch approval eliminates this step for routine transaction types. It is configured at the company and batch type level in **Company Constants (P0010)**.

### 10.1 When to Use Automatic Approval

Automatic approval is appropriate when:

- The source program has sufficient built-in validation (e.g., standard inventory receipts, voucher matching)
- Posting volume is high enough that manual approval creates a bottleneck
- Transactions are system-generated rather than manually entered

Manual approval should be retained for:

- General journal entries entered by users
- Adjusting entries and period-end accruals
- Any batch type where segregation of duties is required by policy or audit

### 10.2 Configuration in Company Constants (P0010)

1. Navigate to **Company Constants** via fast path **P0010**.
2. Select the company to configure and click **Revise**.
3. Locate the **Batch Control** section of the form.
4. For each batch type, set the **Batch Approval Required** field:

| Setting | Effect |
|---|---|
| **Y** | Manual approval required. Batches remain in Pending status until approved via P0011. |
| **N** | Automatic approval. Batches are set to Approved status (code **D**) immediately upon creation. |

5. Save the Company Constants record.

> **Note:** Changes take effect for new batches only. Existing pending batches are not affected retroactively. Each company must be configured independently.

### 10.3 Typical Settings by Batch Type

| Batch Type | Typical Setting | Rationale |
|---|---|---|
| **G** — General Journal | Manual (**Y**) | Journal entries carry higher risk; second-level review is standard practice |
| **N** — Inventory | Automatic (**N**) | System-generated; low manual intervention risk; high volume |
| **IB** — Inventory Balance | Manual (**Y**) or Automatic (**N**) | Depends on whether manual IB entries are in use |
| **O** — PO Receipts | Automatic (**N**) | System-generated at receipt; high volume makes manual approval impractical |
| **V** — Vouchers | Manual (**Y**) | AP vouchers typically require approval for payment controls |
| **W** — Manufacturing | Automatic (**N**) | System-generated by R31802A; manual approval creates End of Day backlogs |
| **S** — Sales Update | Automatic (**N**) | System-generated by R42800; manual approval delays period-end close |
| **D** — Payments | Manual (**Y**) | Payment batches require segregation of duties in most control environments |

### 10.4 Important Considerations

- **Audit trail:** Automatically approved batches carry a system code (D) rather than a named approver. If audit requirements mandate a named approver for specific transaction types, automatic approval cannot be used for those types.
- **Error batches:** Automatic approval does not prevent posting errors. A batch that fails to post still requires manual investigation.
- **Segregation of duties:** For batch types subject to SOD requirements, automatic approval removes the explicit approval step. Review with your internal audit or controls team before enabling on sensitive batch types (G, D, V).

---

## Section 11: Reposting Damaged Account Balances

If an account balance in F0902 becomes corrupted or misaligned with F0911 after all batches have been confirmed as posted, it can be regenerated using the **Account Balance Repost** program **R099102**.

### 11.1 When to Use R099102

- F0902 balance differs from the F0911 sum for the same account and period after all batches are confirmed posted
- The GL Batches variance in RapidReconciler persists as zero but the Valuation section still shows an out-of-balance amount
- A year-end close or period close left F0902 in an inconsistent state

### 11.2 How to Run R099102

1. Identify the affected company, fiscal year, and account numbers.
2. Navigate to R099102 via the General Accounting reports menu or fast path.
3. Set data selection to the specific company, fiscal year, and account range.
4. Run in **proof mode** first to review which accounts will be affected.
5. Run in **final mode** to regenerate the F0902 balances from F0911.
6. Confirm account balances in the trial balance match F0911 totals after the run.

> **Caution:** R099102 replaces F0902 balances entirely for the selected accounts and periods. Run with precise data selection to avoid unintended impact on accounts outside the problem area. Involve your JD Edwards administrator and finance team before running in final mode.

---

## Section 12: Step-by-Step Analysis Procedure

Use this procedure for every Unposted GL Batches export:

**Step 1 — Note the Report Header**

Record the period-end date and generation timestamp from the report title row. This establishes the reference point for all age calculations.

**Step 2 — Calculate the Total Variance**

Sum the Amount column across all rows. This is the total GL Batches variance that must reach $0 before period close. Confirm it matches the GL Batches variance shown on the RapidReconciler Reconciliation page for the same period and filters.

**Step 3 — Group by Batch Number**

Identify all rows that share the same BatchNumber. These must be resolved together — a batch cannot be partially approved or partially posted. For each batch group:
- Sum the amounts to check whether the batch is balanced (should net to $0 for most batch types)
- Note the oldest row date for that batch (the BatchDate value)

**Step 4 — Triage by Status Combination**

Classify each batch using the status combination table in Section 7:

| Status Combination | First Action |
|---|---|
| Pending approval / In Use | Open P0011, reset posting status to blank |
| Pending approval / Pending | Approve in P0011 |
| Any / Error | Review error in P0011 — see Section 9 |
| Approved / Approved | Run R09801 |

**Step 5 — Assess Batch Age**

For each batch, calculate days between BatchDate and PeriodEnds:

| Age | Action Level |
|---|---|
| 0–2 days | Normal — monitor |
| 3–7 days | Investigate — confirm there is a clear resolution path |
| 8–14 days | Escalate — identify owner and set a resolution deadline |
| 15+ days | Critical — immediate action required; likely a recurring systemic issue |

**Step 6 — Identify Patterns Across Batches**

Look for patterns that suggest systemic problems rather than one-off incidents:
- Same batch type, same company, same user, multiple batches all with "In Use" → recurring posting job interruption; consider configuring alerting with IT
- Same user, multiple G-type batches across several days → approver bottleneck; consider configuring auto-approval per Section 10
- All batches dated the same day → single missed R09801 posting run

**Step 7 — Determine Actions by Priority**

Assign each batch a priority and action:

| Priority | Criteria | Action |
|---|---|---|
| **1 — Immediate** | In Use OR batch age > 7 days OR posting error | Reset status / resolve error same day |
| **2 — High** | Pending approval, batch age 3–7 days | Contact approver; complete within 1 business day |
| **3 — Normal** | Approved but unposted, batch age 0–2 days | Include in next R09801 run |

**Step 8 — Document Findings**

Record the analysis on the GL Batch Analysis sheet (see Section 13 for formatting rules). Note the root cause, responsible party, and recommended action for each batch group.

**Step 9 — Follow Up**

After corrections are made, verify that the GL Batches variance in RapidReconciler returns to $0 at the next refresh. If any residual balance remains, re-run the export and repeat this procedure. If F0902 is still misaligned after all batches are posted, run R099102 — see Section 11.

---

## Section 13: Excel Output Formatting Rules

The following rules govern the format of the Excel output produced when analyzing an Unposted GL Batches export.

### 13.1 File Naming

Output file name: `DMAAI Analysis.xlsx`

### 13.2 Sheet Structure

The workbook must contain exactly two sheets:

| Sheet | Contents |
|---|---|
| **Unposted GL Batches** | The original source data, unchanged except for row highlights |
| **GL Batch Analysis** | The analysis sheet — see Section 13.4 for structure |

Do not delete, rename, or reorder the source sheet. Do not add columns, rows, or formulas to the source sheet. The only permitted modification to the source sheet is cell background color (highlights).

### 13.3 Row Highlighting — Source Sheet

Every data row in the source sheet must be highlighted based on its priority classification:

| Color | Hex | Criteria |
|---|---|---|
| **Red** | `FFCCCC` | Posting_Status = "In Use" (requires manual status reset in P0011) **OR** batch age ≥ 8 days **OR** Posting_Status = "Error" |
| **Orange** | `FFE5CC` | Approval_Status = "Pending approval" AND Posting_Status = "Pending" (batch header exists, needs approval) |
| **Yellow** | `FFFACD` | Approval_Status = "Approved" AND Posting_Status = "Approved" (approved, needs posting run only) |
| **Green** | `D9EAD3` | Reserved for future use — batches confirmed as resolved but not yet cleared from the export |

**Rules:**
- Apply the highlight to all columns in the row, not just the status columns.
- When multiple rows share the same BatchNumber, all rows receive the same highlight color.
- If a batch qualifies for both Red and Orange (e.g., pending approval and age > 8 days), Red takes precedence.
- The header row (row 2) and title row (row 1) are never highlighted.

### 13.4 Analysis Sheet Structure

The GL Batch Analysis sheet must contain the following sections in order, each separated by a blank row:

| Section | Content |
|---|---|
| **Report Summary** | Period-end date, generation timestamp, total record count, total variance amount, companies present, batch types present |
| **Status Summary** | One row per status combination showing row count, batch count, and total amount. Use the same highlight colors as the source sheet. |
| **Findings by Priority** | One sub-section per priority level (Priority 1, Priority 2, Priority 3). Each sub-section lists the individual batches with batch number, detail (company, type, date, user, age), and amount. Followed by a note box explaining the root cause pattern and recommended resolution. |
| **Recommended Actions** | Numbered action steps in execution order. Each step includes the specific action, the batches or systems it applies to, and the responsible owner. |

### 13.5 Analysis Sheet Formatting

| Element | Specification |
|---|---|
| **Font** | Arial throughout |
| **Section headers** | Dark blue fill (`1F3864`), white bold text, 11pt |
| **Sub-section headers** | Medium blue fill (`2E75B6`), white bold text, 10pt |
| **Column headers** | Light blue fill (`D6E4F0`), dark blue bold text, 10pt |
| **Data rows** | Alternating white and light gray (`F2F2F2`) fill; 10pt Arial |
| **Priority 1 rows** | Red fill (`FFCCCC`), dark red bold text (`C00000`) |
| **Priority 2 rows** | Orange fill (`FFE5CC`), dark brown text (`7B3F00`) |
| **Priority 3 rows** | Yellow fill (`FFFACD`), dark gold text (`5C4A00`) |
| **Note boxes** | Light gold fill (`FFF3CD`), dark gold italic text (`7B4C00`); full-width merged cell; wrap text enabled |
| **Column widths** | Fixed widths sized for readability — not auto-stretched to full sheet width. |
| **Row heights** | Calculated from content length and column width — not a flat default. |
| **Wrap text** | Enabled on all cells on the GL Batch Analysis sheet. |
| **Resolution tables** | Two-column layout: condition spans cols A–B, action spans cols C–E. Do not merge the full row width. |
| **Colour palette** | Priority 1 fill `FFE0E0` / text `8B0000`; Priority 2 fill `FFF0DC` / text `6B3A00`; Priority 3 fill `FEFBD8` / text `4A3B00`. Lighter fills and non-bold text for readability. |
| **Source sheet** | AutoFilter on row 2; freeze panes at row 3. Row highlights match analysis priority colours. |
| **Colour key** | Include a colour key section at the top of the analysis sheet. |

### 13.6 Amounts

All dollar amounts must be formatted with a dollar sign, comma thousands separator, and two decimal places (e.g., `$13,354.12`). Negative amounts use a leading minus sign (e.g., `$-5,583.45`). Do not use parentheses for negative amounts.

### 13.7 Batch Age Calculation

Batch age is calculated as the number of calendar days between the BatchDate and the PeriodEnds date. Write this as an integer followed by "days before period end" in the detail column of the findings section (e.g., "27 days before period end").

### 13.8 What Not to Include

- Do not include raw JD Edwards status codes (e.g., "D", "E", "P") in the analysis sheet. Use the descriptive labels from Section 7.
- Do not include the Currency or Rate columns in the analysis sheet unless a non-1.0 exchange rate requires explanation.
- Do not calculate or display batch totals as formulas. Write the sum as a static value.
- Do not add conditional formatting, data validation, or pivot tables to either sheet.

---

## Section 14: Related Documentation

- [Inventory: Using the Application](../MDS/inventory-using-application.md)
- [Transaction Detail Analysis Guide](../MDS/transaction-detail-analysis-guide.md)
- [DMAAI Reference Guide](../MDS/distribution-aais.md)
- [Manufacturing Work Order Reference Guide](../MDS/manufacturing-reference.md)

---

*For support, contact GSI at [rrsupport@getgsi.com](mailto:rrsupport@getgsi.com)*
