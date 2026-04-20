---
layout: null
---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RapidReconciler — Reconciliation for JD Edwards</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --navy: #0d1f3c;
    --navy-light: #162d56;
    --blue: #1a56db;
    --blue-mid: #1e40af;
    --sky: #dbeafe;
    --sky-pale: #eff6ff;
    --gold: #f59e0b;
    --gold-light: #fef3c7;
    --slate: #475569;
    --slate-light: #94a3b8;
    --white: #ffffff;
    --off-white: #f8fafc;
    --border: #e2e8f0;
    --text: #1e293b;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
    background: var(--white);
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }

  /* ── HERO ─────────────────────────────────────── */
  .hero {
    background: var(--navy);
    color: var(--white);
    padding: 80px 48px 90px;
    position: relative;
    overflow: hidden;
  }

  .hero::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 520px; height: 520px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(26,86,219,0.35) 0%, transparent 70%);
    pointer-events: none;
  }

  .hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 20%;
    width: 360px; height: 360px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(245,158,11,0.12) 0%, transparent 70%);
    pointer-events: none;
  }

  .hero-inner {
    max-width: 860px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }

  .eyebrow {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 20px;
  }

  h1 {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(38px, 5vw, 62px);
    line-height: 1.1;
    color: var(--white);
    margin-bottom: 24px;
  }

  h1 em {
    font-style: italic;
    color: #93c5fd;
  }

  .hero-sub {
    font-size: 18px;
    font-weight: 300;
    color: #cbd5e1;
    max-width: 620px;
    margin-bottom: 44px;
    line-height: 1.7;
  }

  .hero-stats {
    display: flex;
    gap: 48px;
    flex-wrap: wrap;
  }

  .stat {
    border-left: 2px solid var(--gold);
    padding-left: 16px;
  }

  .stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 32px;
    color: var(--white);
    line-height: 1;
    margin-bottom: 4px;
  }

  .stat-label {
    font-size: 13px;
    color: var(--slate-light);
    font-weight: 400;
  }

  /* ── PROBLEM STRIP ────────────────────────────── */
  .problem-strip {
    background: var(--gold-light);
    border-top: 3px solid var(--gold);
    padding: 36px 48px;
  }

  .problem-strip-inner {
    max-width: 860px;
    margin: 0 auto;
  }

  .problem-strip h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    color: var(--navy);
    margin-bottom: 16px;
  }

  .problem-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    list-style: none;
  }

  .problem-list li {
    font-size: 14px;
    color: var(--slate);
    padding-left: 20px;
    position: relative;
    line-height: 1.5;
  }

  .problem-list li::before {
    content: '✕';
    position: absolute;
    left: 0;
    color: #dc2626;
    font-size: 12px;
    top: 1px;
    font-weight: 600;
  }

  /* ── SECTIONS ─────────────────────────────────── */
  section {
    padding: 72px 48px;
  }

  section:nth-child(even) {
    background: var(--off-white);
  }

  .section-inner {
    max-width: 900px;
    margin: 0 auto;
  }

  .section-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--blue);
    background: var(--sky);
    padding: 4px 10px;
    border-radius: 3px;
    margin-bottom: 14px;
  }

  h2 {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(26px, 3.5vw, 38px);
    line-height: 1.2;
    color: var(--navy);
    margin-bottom: 14px;
  }

  .section-lead {
    font-size: 16px;
    color: var(--slate);
    max-width: 680px;
    margin-bottom: 44px;
    line-height: 1.7;
  }

  /* ── FEATURE CARDS ────────────────────────────── */
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
  }

  .card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 28px 26px;
    position: relative;
    transition: box-shadow 0.2s, transform 0.2s;
  }

  .card:hover {
    box-shadow: 0 8px 32px rgba(13,31,60,0.1);
    transform: translateY(-2px);
  }

  .card-icon {
    width: 40px; height: 40px;
    background: var(--sky);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    font-size: 18px;
  }

  .card h4 {
    font-size: 15px;
    font-weight: 600;
    color: var(--navy);
    margin-bottom: 8px;
    line-height: 1.3;
  }

  .card p {
    font-size: 13.5px;
    color: var(--slate);
    line-height: 1.6;
  }

  /* ── MODULE SECTIONS ──────────────────────────── */
  .module-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
  }

  .module-icon {
    width: 52px; height: 52px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
  }

  .module-icon.inv { background: #dbeafe; }
  .module-icon.transit { background: #d1fae5; }
  .module-icon.po { background: #fce7f3; }

  .module-header-text h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 24px;
    color: var(--navy);
    margin-bottom: 4px;
  }

  .module-header-text p {
    font-size: 14px;
    color: var(--slate);
  }

  .feature-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
  }

  .feature-table thead tr {
    background: var(--navy);
    color: var(--white);
  }

  .feature-table thead th {
    padding: 12px 16px;
    text-align: left;
    font-weight: 500;
    font-size: 12px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .feature-table thead th:first-child { border-radius: 6px 0 0 0; }
  .feature-table thead th:last-child { border-radius: 0 6px 0 0; }

  .feature-table tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
  }

  .feature-table tbody tr:hover { background: var(--sky-pale); }

  .feature-table td {
    padding: 14px 16px;
    vertical-align: top;
    line-height: 1.55;
    color: var(--slate);
  }

  .feature-table td:first-child {
    font-weight: 600;
    color: var(--navy);
    white-space: nowrap;
    width: 220px;
  }

  .check {
    display: inline-block;
    color: #16a34a;
    font-weight: 700;
    margin-right: 6px;
  }

  /* ── CHALLENGE CALLOUT ────────────────────────── */
  .challenge-box {
    background: var(--navy);
    color: var(--white);
    border-radius: 12px;
    padding: 32px 36px;
    margin-bottom: 36px;
  }

  .challenge-box h4 {
    font-family: 'DM Serif Display', serif;
    font-size: 18px;
    color: #93c5fd;
    margin-bottom: 12px;
  }

  .challenge-box p {
    font-size: 14px;
    color: #cbd5e1;
    line-height: 1.65;
  }

  /* ── COMPARISON TABLE ─────────────────────────── */
  .comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 44px;
  }

  .compare-col {
    border-radius: 10px;
    overflow: hidden;
  }

  .compare-head {
    padding: 14px 20px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.04em;
  }

  .compare-head.before {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
  }

  .compare-head.after {
    background: #f0fdf4;
    color: #16a34a;
    border: 1px solid #bbf7d0;
  }

  .compare-body {
    padding: 0;
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 10px 10px;
  }

  .compare-item {
    padding: 12px 20px;
    font-size: 13.5px;
    color: var(--slate);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: flex-start;
    gap: 10px;
    line-height: 1.5;
  }

  .compare-item:last-child { border-bottom: none; }

  .compare-item .icon { flex-shrink: 0; margin-top: 1px; }

  /* ── QUOTE ────────────────────────────────────── */
  .quote-band {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%);
    padding: 64px 48px;
    text-align: center;
  }

  .quote-band blockquote {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(20px, 2.8vw, 30px);
    font-style: italic;
    color: var(--white);
    max-width: 780px;
    margin: 0 auto 20px;
    line-height: 1.45;
  }

  .quote-attribution {
    font-size: 13px;
    color: var(--slate-light);
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  /* ── CTA ──────────────────────────────────────── */
  .cta-section {
    background: var(--sky-pale);
    padding: 72px 48px;
    text-align: center;
    border-top: 1px solid var(--border);
  }

  .cta-section h2 {
    margin-bottom: 16px;
  }

  .cta-section p {
    font-size: 16px;
    color: var(--slate);
    max-width: 540px;
    margin: 0 auto 36px;
  }

  .btn {
    display: inline-block;
    background: var(--blue);
    color: var(--white);
    padding: 14px 32px;
    border-radius: 6px;
    font-size: 15px;
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 0.01em;
    transition: background 0.2s, transform 0.15s;
  }

  .btn:hover {
    background: var(--blue-mid);
    transform: translateY(-1px);
  }

  .btn-secondary {
    display: inline-block;
    background: transparent;
    color: var(--blue);
    padding: 14px 32px;
    border-radius: 6px;
    border: 1.5px solid var(--blue);
    font-size: 15px;
    font-weight: 600;
    text-decoration: none;
    margin-left: 12px;
    transition: background 0.2s, color 0.2s;
  }

  .btn-secondary:hover {
    background: var(--blue);
    color: var(--white);
  }

  /* ── FOOTER ───────────────────────────────────── */
  footer {
    background: var(--navy);
    color: var(--slate-light);
    padding: 28px 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    flex-wrap: wrap;
    gap: 12px;
  }

  footer a { color: #93c5fd; text-decoration: none; }
  footer a:hover { text-decoration: underline; }

  /* ── DIVIDER ──────────────────────────────────── */
  .divider {
    height: 1px;
    background: var(--border);
    margin: 40px 0;
  }

  @media (max-width: 640px) {
    .hero, section, .problem-strip, .quote-band, .cta-section { padding: 48px 24px; }
    .hero-stats { gap: 24px; }
    .comparison { grid-template-columns: 1fr; }
    footer { flex-direction: column; text-align: center; }
    .feature-table td:first-child { white-space: normal; width: auto; }
  }
</style>
</head>
<body>

<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <p class="eyebrow">GSI — RapidReconciler</p>
    <h1>Inventory Reconciliation<br>that <em>actually works</em><br>for JD Edwards.</h1>
    <p class="hero-sub">Stop spending days every period chasing variances across spreadsheets, JD Edwards reports, and manual data extracts. RapidReconciler automates the comparison, surfaces what matters, and tells you exactly what to fix.</p>
    <div class="hero-stats">
      <div class="stat">
        <div class="stat-num">3</div>
        <div class="stat-label">Modules: Inventory,<br>In Transit &amp; PO Receipts</div>
      </div>
      <div class="stat">
        <div class="stat-num">Nightly</div>
        <div class="stat-label">Automated data import<br>from JD Edwards</div>
      </div>
      <div class="stat">
        <div class="stat-num">100%</div>
        <div class="stat-label">Read-only access to<br>JD Edwards data</div>
      </div>
    </div>
  </div>
</section>

<!-- PROBLEM STRIP -->
<div class="problem-strip">
  <div class="problem-strip-inner">
    <h3>Sound familiar?</h3>
    <ul class="problem-list">
      <li>Stock Status doesn't tie to the trial balance — again</li>
      <li>Three hours of spreadsheet work to find one misconfigured AAI</li>
      <li>Aged RNV receipts no one can explain</li>
      <li>In Transit clearing account that never fully clears</li>
      <li>GL class code change caused a split inventory balance</li>
      <li>Period-end close is a discovery exercise, not a confirmation</li>
      <li>End of Day orders sitting unprocessed for days</li>
      <li>Variances that carry forward month after month</li>
    </ul>
  </div>
</div>

<!-- WHY IT'S HARD -->
<section>
  <div class="section-inner">
    <span class="section-tag">The Challenge</span>
    <h2>JD Edwards reconciliation is harder than it should be</h2>
    <p class="section-lead">The standard approach — running a Stock Status report and comparing it to the trial balance — has five well-documented failure points. Each one produces a mismatch that must be traced manually, and most recur every period if the root cause isn't found and fixed.</p>

    <div class="cards">
      <div class="card">
        <div class="card-icon">⏱</div>
        <h4>Timing</h4>
        <p>Transactions entered after the Stock Status report but before period close appear in the GL but not in the report. In multi-timezone environments, the JD Edwards server clock compounds the problem.</p>
      </div>
      <div class="card">
        <div class="card-icon">📅</div>
        <h4>Backdating</h4>
        <p>Transactions booked to a prior GL period after the Stock Status is run create discrepancies that appear in neither report correctly. Processing option settings in Manufacturing Accounting and Sales Update can cause this silently.</p>
      </div>
      <div class="card">
        <div class="card-icon">📋</div>
        <h4>Report Definition</h4>
        <p>Incorrect cost method logic, non-stock items, or flawed data selection in the Stock Status report produce totals that will never agree to the GL — regardless of how clean the underlying data is.</p>
      </div>
      <div class="card">
        <div class="card-icon">🗺</div>
        <h4>DMAAI Misconfiguration</h4>
        <p>A single incorrectly mapped AAI causes every transaction of that type to post to the wrong GL account — silently, with no error message, creating a growing systematic variance that's difficult to trace manually.</p>
      </div>
      <div class="card">
        <div class="card-icon">🏷</div>
        <h4>GL Class Code Changes</h4>
        <p>JD Edwards allows GL class code changes without checking for quantity on hand or cascading through the hierarchy. The wrong procedure leaves inventory value stranded in the original account indefinitely.</p>
      </div>
    </div>
  </div>
</section>

<!-- BEFORE / AFTER -->
<section>
  <div class="section-inner">
    <span class="section-tag">Before &amp; After</span>
    <h2>From discovery exercise to confirmed close</h2>
    <p class="section-lead">RapidReconciler transforms the period-end close from an investigation into a confirmation of an already-understood position.</p>

    <div class="comparison">
      <div class="compare-col">
        <div class="compare-head before">✕ &nbsp;Without RapidReconciler</div>
        <div class="compare-body">
          <div class="compare-item"><span class="icon">🔴</span>Run Stock Status and trial balance, manually compare in Excel</div>
          <div class="compare-item"><span class="icon">🔴</span>Extract F4111, exclude memo transactions, summarize and compare to F41021 by hand — for every item</div>
          <div class="compare-item"><span class="icon">🔴</span>No visibility into which DMAAI caused an account mismatch without tracing each transaction individually</div>
          <div class="compare-item"><span class="icon">🔴</span>GL class code mismatches detected only when a reconciling variance appears — often months later</div>
          <div class="compare-item"><span class="icon">🔴</span>RNV reconciliation requires matching F43121 records to GL entries manually across hundreds of PO lines</div>
          <div class="compare-item"><span class="icon">🔴</span>In Transit clearing account balanced by manually comparing shipment and receipt records per order</div>
          <div class="compare-item"><span class="icon">🔴</span>Unresolved variances carried forward indefinitely because the root cause was never identified</div>
        </div>
      </div>
      <div class="compare-col">
        <div class="compare-head after">✓ &nbsp;With RapidReconciler</div>
        <div class="compare-body">
          <div class="compare-item"><span class="icon">🟢</span>F4111 vs. F0902 comparison performed automatically on every nightly import — no manual reporting required</div>
          <div class="compare-item"><span class="icon">🟢</span>Cardex Integrity pop-up shows exactly which items have variances and whether it's a quantity or dollar issue</div>
          <div class="compare-item"><span class="icon">🟢</span>Transaction Detail drill-down identifies the specific DMAAI entry causing any account mismatch</div>
          <div class="compare-item"><span class="icon">🟢</span>Integrity Reports 2, 3, and 5 proactively flag DMAAI mismatches and GL class code inconsistencies monthly</div>
          <div class="compare-item"><span class="icon">🟢</span>PO Receipts module automatically matches F43121 to GL, shows only unreconciled orders, and enables document-level investigation</div>
          <div class="compare-item"><span class="icon">🟢</span>In Transit module calculates the open position per order pair, surfaces cost mismatches, and manages exclusions with full audit trail</div>
          <div class="compare-item"><span class="icon">🟢</span>Every variance source is labeled, quantified, and linked to the correct corrective action</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- INVENTORY MODULE -->
<section>
  <div class="section-inner">
    <span class="section-tag">Module 1</span>

    <div class="module-header">
      <div class="module-icon inv">📦</div>
      <div class="module-header-text">
        <h3>Inventory Reconciliation</h3>
        <p>Perpetual item ledger (F4111) vs. General Ledger (F0902 / F0911)</p>
      </div>
    </div>

    <div class="challenge-box">
      <h4>The challenge</h4>
      <p>The perpetual inventory balance and the GL balance should always agree — but timing differences, DMAAI mismatches, cardex integrity issues, unposted batches, and GL class code changes each create variances that the standard Stock Status report cannot identify, isolate, or explain. Without a systematic way to break down the total variance into its sources, every period-end close starts with an unexplained number.</p>
    </div>

    <table class="feature-table">
      <thead>
        <tr>
          <th>Feature</th>
          <th>What it does</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Valuation Section</td>
          <td><span class="check">✓</span>Automatically compares summarized F4111 perpetual balance to F0902 GL balance for every period — no manual report run required. If the out-of-balance is zero, inventory is reconciled.</td>
        </tr>
        <tr>
          <td>Variance Calculation</td>
          <td><span class="check">✓</span>Breaks the total out-of-balance into six labeled sources — Carry Forward, GL Batches, End of Day, Transactions, Cardex, and Manual Journal Entries — each with the correct resolution path.</td>
        </tr>
        <tr>
          <td>Cardex Integrity Pop-Up</td>
          <td><span class="check">✓</span>Compares summarized F4111 to F41021 for every item automatically, excluding memo transactions and applying UOM conversions. Shows exactly which items have variances and whether the issue is quantity (requires IT) or dollars (requires a dollars-only IA adjustment).</td>
        </tr>
        <tr>
          <td>Transaction Detail Drill-Down</td>
          <td><span class="check">✓</span>For any unreconciled transaction, shows the F4111 cardex, F0911 GL entries, how RapidReconciler matched them, and — critically — the complete DMAAI entries for every GL class code in the transaction. Identifies the exact AAI causing an account mismatch.</td>
        </tr>
        <tr>
          <td>As-Of Page</td>
          <td><span class="check">✓</span>Continuously maintained period-end inventory position by item, branch, location, and lot — with QtyVar and AmtVar columns that surface cardex integrity issues at the item level. Replaces the timing-dependent Stock Status report entirely.</td>
        </tr>
        <tr>
          <td>Integrity Reports 2–6</td>
          <td><span class="check">✓</span>Monthly proactive checks for DMAAI mismatches, excluded GL class codes, UOM conversion gaps, GL class code inconsistencies between item branch and location records, and frozen cost discrepancies — catching configuration issues before they produce reconciling variances.</td>
        </tr>
        <tr>
          <td>Re-Roll Options</td>
          <td><span class="check">✓</span>Three tools to synchronize RapidReconciler with JD Edwards after a correction — Re-Roll Item, Zero Beginning Balance, and Remove CX Var — with period recalculation and full audit transparency. No undo; used with precision after JD Edwards is confirmed correct.</td>
        </tr>
        <tr>
          <td>Audit Report</td>
          <td><span class="check">✓</span>Complete period-end reconciliation document — account summaries, unposted batches, open orders, manual entries, variances, and perpetual detail — exportable in Excel or PDF for internal review and audit support.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<!-- IN TRANSIT MODULE -->
<section>
  <div class="section-inner">
    <span class="section-tag">Module 2</span>

    <div class="module-header">
      <div class="module-icon transit">🚚</div>
      <div class="module-header-text">
        <h3>In Transit Reconciliation</h3>
        <p>ST/OT transfer order activity vs. General Ledger clearing account</p>
      </div>
    </div>

    <div class="challenge-box">
      <h4>The challenge</h4>
      <p>When goods move between branch plants via ST/OT transfer orders, their value sits in an In Transit clearing account until receipt. Standard cost changes between order entry and shipment, cost differences between branches, and quantity mismatches between ship and receive all create balances that don't clear. Once both the ST and OT orders reach status 999, no further JD Edwards processing is possible — and the balance remains indefinitely without a systematic way to identify and manage it.</p>
    </div>

    <table class="feature-table">
      <thead>
        <tr>
          <th>Feature</th>
          <th>What it does</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Orders Page</td>
          <td><span class="check">✓</span>Automatically calculates the in-transit position (Shipments − Receipts) for every order pair. Orders that reconcile exactly are removed automatically — no manual filtering required. Displays the current in-transit position regardless of period selected.</td>
        </tr>
        <tr>
          <td>Exclusion Process</td>
          <td><span class="check">✓</span>When both ST and OT orders are closed (status 999) but a residual balance remains, the Exclusion feature isolates those amounts and displays the exact journal entry value needed to clear the In Transit GL account.</td>
        </tr>
        <tr>
          <td>ExclVarQty / ExclVarAmt</td>
          <td><span class="check">✓</span>Monitors previously excluded orders for new activity. If a receipt is processed against an excluded open PO, these columns surface the discrepancy immediately — preventing new transactions from being silently omitted from the reconciliation.</td>
        </tr>
        <tr>
          <td>Variance Calculation</td>
          <td><span class="check">✓</span>Breaks the GL out-of-balance into Carry Forward, GL Batches, End of Day, Transactions, Exclusions, and Manual Journal Entries — each with the appropriate resolution path identified.</td>
        </tr>
        <tr>
          <td>As-Of Page</td>
          <td><span class="check">✓</span>Reconstructs the in-transit position as of any historical period end, calculated backwards from the current position. Full transaction-level detail with drill-down and export for period-end documentation and audit support.</td>
        </tr>
        <tr>
          <td>Integrity Report 4 — Transfer Cost Variances</td>
          <td><span class="check">✓</span>Lists orders where the ST sales cost or price does not match the OT purchase order cost — the most common cause of In Transit balances that do not clear after receipt. Surfaces these proactively before they accumulate into large unresolved balances.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<!-- PO RECEIPTS MODULE -->
<section>
  <div class="section-inner">
    <span class="section-tag">Module 3</span>

    <div class="module-header">
      <div class="module-icon po">📄</div>
      <div class="module-header-text">
        <h3>PO Receipts (RNV) Reconciliation</h3>
        <p>Open purchase order receipts (F43121) vs. General Ledger RNV account</p>
      </div>
    </div>

    <div class="challenge-box">
      <h4>The challenge</h4>
      <p>The F43121 table — the source of truth for purchase order receipts — is not a true ledger. Receipt and voucher reversals overwrite existing records rather than creating new ones, making As-Of reporting impossible. Reconciliation must always be performed as a current balance-to-balance comparison. Without automation, this means manually matching Match Type 1 and 2 records across hundreds or thousands of PO lines, every period, with no historical roll-forward to rely on.</p>
    </div>

    <table class="feature-table">
      <thead>
        <tr>
          <th>Feature</th>
          <th>What it does</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Orders Page</td>
          <td><span class="check">✓</span>Imports F43121 and F0911 automatically and displays only purchase orders with open amounts or variances between the receipts table and the GL. Fully reconciled orders are removed automatically.</td>
        </tr>
        <tr>
          <td>Calculation Section</td>
          <td><span class="check">✓</span>Separates the out-of-balance into Open Receipts, Unreconciled, and Batches components. Provides a Suggested Entry amount excluding outstanding variances — making it straightforward to decide whether to close around unresolved items or resolve them first.</td>
        </tr>
        <tr>
          <td>PO Receipts Aging</td>
          <td><span class="check">✓</span>Visual breakdown of open receipts by period — immediately identifying whether the RNV balance reflects recent legitimate activity or aged receipts that have not been vouchered, without running a separate aging report.</td>
        </tr>
        <tr>
          <td>Suspension Feature</td>
          <td><span class="check">✓</span>Removes orders cleared by manual voucher entry, accrual-only landed costs (PRLAND = 3), or data cutoff artifacts from the variance calculation — isolating genuine unresolved items from known exceptions without changing JD Edwards data.</td>
        </tr>
        <tr>
          <td>Line Analysis Page</td>
          <td><span class="check">✓</span>Side-by-side F43121 vs. GL comparison at the document level for any PO line. Supports document-level exclusion with audit notes and a Recalc function that updates variance calculations within minutes.</td>
        </tr>
        <tr>
          <td>Document Button</td>
          <td><span class="check">✓</span>Displays all transactions for a PO line with a Variance column identifying precisely which documents have discrepancies between F43121 and F0911 — eliminating the need to cross-reference two separate data extracts manually.</td>
        </tr>
        <tr>
          <td>Unreconciled Link</td>
          <td><span class="check">✓</span>One-click navigation from the Reconciliation page to a pre-filtered Orders view showing only orders requiring action — removing the need to manually filter the full order listing each period.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<!-- QUOTE -->
<div class="quote-band">
  <blockquote>"The period-end close should be a confirmation of what you already know — not a discovery of what went wrong."</blockquote>
  <p class="quote-attribution">GSI — RapidReconciler Design Philosophy</p>
</div>

<!-- WHAT RR DOESN'T DO -->
<section>
  <div class="section-inner">
    <span class="section-tag">Important to Know</span>
    <h2>What RapidReconciler is — and isn't</h2>
    <p class="section-lead">RapidReconciler is a reconciliation and diagnostic tool. Understanding its boundaries helps set accurate expectations and ensures the right workflows are in place.</p>

    <div class="cards">
      <div class="card">
        <div class="card-icon">🔒</div>
        <h4>Read-only access to JD Edwards</h4>
        <p>RapidReconciler reads JD Edwards data in read-only mode. It never modifies JD Edwards tables. All corrections — adjustments, journal entries, AAI changes — are made directly in JD Edwards.</p>
      </div>
      <div class="card">
        <div class="card-icon">🌙</div>
        <h4>Nightly data refresh</h4>
        <p>Data is imported from JD Edwards on a nightly cycle. Transactions entered in JD Edwards after the most recent import will not appear in RapidReconciler until the following night's refresh.</p>
      </div>
      <div class="card">
        <div class="card-icon">📐</div>
        <h4>Identifies, not corrects</h4>
        <p>RapidReconciler identifies what is out of balance, where the discrepancy originates, and what the correct corrective action is. The resolution itself always happens in JD Edwards.</p>
      </div>
      <div class="card">
        <div class="card-icon">📅</div>
        <h4>History from initiation date</h4>
        <p>RapidReconciler calculates its cardex position from the point the program was first initiated, or from the last data reset. Transaction history predating that point is not visible without a Re-Roll.</p>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<div class="cta-section">
  <span class="section-tag">Get Started</span>
  <h2>Ready to close the books with confidence?</h2>
  <p>Contact GSI to learn more about RapidReconciler, request a proof of concept with your own JD Edwards data, or talk to an implementation specialist.</p>
  <a href="mailto:rrsupport@getgsi.com" class="btn">Contact GSI Support</a>
  <a href="https://rapidreconciler.getgsi.com" class="btn-secondary">Log In to RapidReconciler</a>
</div>

<!-- FOOTER -->
<footer>
  <span>© GSI — RapidReconciler. All rights reserved.</span>
  <span>
    <a href="mailto:rrsupport@getgsi.com">rrsupport@getgsi.com</a>
    &nbsp;·&nbsp;
    <a href="https://rapidreconciler.getgsi.com">rapidreconciler.getgsi.com</a>
  </span>
</footer>

</body>
</html>