/* ============================================================
   task-manager-panel.js -- renders the Windows Task Manager
   Processes tab showing the RapidReconciler Java processes.

   USAGE
   -----
     <link rel="stylesheet" href="../Tools/task-manager-panel.css">
     <div data-tm-panel data-caption="What a healthy install looks like."></div>
     <script defer src="../Tools/task-manager-panel.js"></script>

   THE POINT OF THE PICTURE
   ------------------------
   After an install the agent and its data-services children take
   several minutes to come up, and until they do RapidReconciler
   signs in but shows nothing. A customer with no way to see
   progress reads that as a failed install and opens a ticket.
   Counting these processes is the progress bar.

   Parent agent + ONE child per RapidReconciler database. So the
   floor is two processes for a single-database install, and a
   four-database customer runs five. The parent/child model is
   documented in GSIRRTech/rr-agent-reference.html under
   "Processes & startup"; the heartbeat log in that same doc shows
   one RunningInstanceState entry per child, which is the same
   count from the other side.

   PROVENANCE -- measured, not remembered
   --------------------------------------
   Both command lines, the process display name, the column
   layout and the amber CPU/Memory tint come from a screenshot of
   a live customer install supplied by the owner 2026-09-09. The
   child's command line is TRUNCATED here exactly as Task Manager
   truncated it there; its tail was not visible and is not
   invented. The deployed bundle version in that path (files/371)
   is the one value here most likely to move -- it is a single
   edit in CHILD.cmd below, and greppable, which a screenshot
   never was.

   If this script does not run the panel is simply absent. The
   prose beside it in the consuming document carries the same
   instruction in words, so nothing is lost but the illustration.
   ============================================================ */
(function () {
  'use strict';

  var PROC_NAME = 'Java(TM) Platform SE binary';

  // Machine-wide totals in the column headers, straight from the source
  // screenshot. They are scene-setting: the caption says figures vary.
  var TOTALS = { cpu: '34%', mem: '55%' };

  var PARENT = {
    cpu: '0%',
    mem: '997.5 MB',
    cmd: '"C:\\Program Files\\Rapid Reconciler\\jre\\bin\\java.exe" '
       + '-jar "C:\\Program Files\\Rapid Reconciler\\rr-valc-agent.jar"',
    role: 'the agent'
  };

  var CHILD = {
    cpu: '0%',
    mem: '828.1 MB',
    // Truncated as Task Manager truncates it. Do not complete the tail.
    cmd: '"C:\\Program Files\\Rapid Reconciler\\jre\\bin\\java.exe" '
       + '-Xrs -Xmx2g -jar ./files/371 '
       + '--spring.profiles.active=production-https --sprin\u2026',
    role: 'one database'
  };

  var TABS = ['Processes', 'Performance', 'Users', 'Details', 'Services'];
  var TAB_ACTIVE = 'Processes';
  var MENU = ['File', 'Options', 'View'];

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function rowHTML(p) {
    return '<tr>'
      // No icon glyph. A bordered square standing in for the Java icon renders
      // as an unchecked checkbox, which invites a reader to tick it. Same
      // lesson the local-network panel's nav learned.
      + '<td><span class="tmp-proc">' + esc(PROC_NAME) + '</span></td>'
      + '<td class="tmp-num tmp-heat">' + esc(p.cpu) + '</td>'
      + '<td class="tmp-num tmp-heat">' + esc(p.mem) + '</td>'
      + '<td><span class="tmp-cmd">' + esc(p.cmd) + '</span>'
      + '<span class="tmp-role">' + esc(p.role) + '</span></td>'
      + '</tr>';
  }

  function panelHTML() {
    var label = 'Windows Task Manager, Processes tab, showing two "'
      + PROC_NAME + '" entries. One is the RapidReconciler agent, running '
      + 'rr-valc-agent.jar. The other is a data-services process for one '
      + 'RapidReconciler database, running the deployed bundle under '
      + 'files/371. A further entry appears for each additional database.';

    return '<div class="tmp" role="img" aria-label="' + esc(label) + '">'
      + '<div class="tmp-titlebar">'
      + '<span class="tmp-apptitle">Task Manager</span>'
      + '<span class="tmp-winbtns" aria-hidden="true">'
      + '<span>&minus;</span><span>&#9633;</span><span>&#10005;</span>'
      + '</span></div>'
      + '<div class="tmp-menu">'
      + MENU.map(function (m) { return '<span>' + esc(m) + '</span>'; }).join('')
      + '</div>'
      + '<div class="tmp-tabs">'
      + TABS.map(function (t) {
          return '<span class="tmp-tab' + (t === TAB_ACTIVE ? ' is-active' : '')
               + '">' + esc(t) + '</span>';
        }).join('')
      + '</div>'
      + '<div class="tmp-grid"><table class="tmp-table">'
      + '<thead><tr>'
      + '<th>Name</th>'
      + '<th class="tmp-num tmp-heat">'
      + '<span class="tmp-sortcaret" aria-hidden="true">&#94;</span> '
      + '<span class="tmp-total">' + esc(TOTALS.cpu) + '</span>'
      + '<span class="tmp-colname">CPU</span></th>'
      + '<th class="tmp-num tmp-heat">'
      + '<span class="tmp-total">' + esc(TOTALS.mem) + '</span>'
      + '<span class="tmp-colname">Memory</span></th>'
      + '<th>Command line</th>'
      + '</tr></thead>'
      + '<tbody>' + rowHTML(CHILD) + rowHTML(PARENT) + '</tbody>'
      + '</table></div></div>';
  }

  function captionHTML(lead) {
    return '<p class="tmp-caption">'
      + (lead ? '<strong>' + esc(lead) + '</strong> ' : '')
      + 'An illustration, not a screenshot. The <em>Command line</em> column '
      + 'is not shown by default &mdash; right-click the column headings to add '
      + 'it &mdash; and you do not need it to do the check, since counting the '
      + '<em>' + esc(PROC_NAME) + '</em> entries is enough. CPU and memory '
      + 'figures vary by machine and by how much data you hold; around a '
      + 'gigabyte per process is normal and is not a problem to report.'
      + '</p>';
  }

  function render() {
    var hosts = document.querySelectorAll('[data-tm-panel]');
    for (var i = 0; i < hosts.length; i++) {
      hosts[i].innerHTML = panelHTML()
        + captionHTML(hosts[i].getAttribute('data-caption'));
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render);
  } else {
    render();
  }
})();
