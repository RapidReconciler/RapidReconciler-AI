/* ============================================================
   local-network-panel.js -- renders the Edge "Local network"
   settings page as markup, replacing a screenshot that had gone
   stale three different ways (see local-network-panel.css for the
   full account).

   USAGE
   -----
     <link rel="stylesheet" href="../Tools/local-network-panel.css">
     <div data-lnp-panel data-host="rapidreconciler-prod.getgsi.com"
          data-caption="What to look for."></div>
     <script defer src="../Tools/local-network-panel.js"></script>

   data-host    the address to show in the Allowed list. Required;
                without it the panel renders nothing rather than
                showing a placeholder a customer might type in.
   data-caption optional lead-in sentence for the caption. The
                "this is drawn, not photographed" half is always
                appended, because a reader who takes it for a
                screenshot will report a bug when their own Edge
                lays it out differently.

   WHY THE LABELS LIVE HERE AND NOT IN THREE HTML FILES
   ----------------------------------------------------
   Three documents show this panel. Microsoft reworded one of
   these labels inside four months and nothing caught it, so the
   labels get exactly one home. Correcting a rename is one edit
   here.

   EVERY STRING BELOW IS MEASURED, NOT REMEMBERED -- from a
   screenshot of Edge 152 supplied 2026-09-09, cross-checked
   against Edge 152.0.4191.66 and Chrome 152.0.7977.83
   Locales\en-US.pak the same day. Note the page is titled "Local
   network", not "Local network access", and "Not allowed" is
   listed ABOVE "Allowed".

   If this script does not run, the panel is simply absent. That
   is deliberate: the numbered steps beside it in every consuming
   document carry the same information in words, so nothing is
   lost but the illustration.
   ============================================================ */
(function () {
  'use strict';

  // Edge's own Settings nav, in order, as it appears beside this page.
  var NAV = [
    'Profiles',
    'Passwords and autofill',
    'Privacy, search, and services',
    'Copilot and AI',
    'Appearance',
    'Default browser',
    'Start, home, and new tab page',
    null,
    'Languages',
    'Downloads',
    'Accessibility',
    'System and performance',
    'Reset settings',
    null,
    'Extensions',
    'About Microsoft Edge'
  ];
  var NAV_ACTIVE = 'Privacy, search, and services';

  var CRUMB = [
    'Privacy, search, and services',
    'Site permissions',
    'All permissions',
    'Local network'
  ];

  var TEXT = {
    settings:      'Settings',
    search:        'Search settings',
    defaultLabel:  'Default behavior',
    defaultMain:   'Ask before accessing (recommended)',
    defaultNote:   'Will block if turned off',
    customLabel:   'Customized behaviors',
    customNote:    'Sites listed below follow a custom setting instead of the default',
    blocked:       'Not allowed to access other devices on your local network',
    allowed:       'Allowed to access other devices on your local network',
    empty:         'No sites added',
    addSite:       'Add site'
  };

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function navHTML() {
    var out = '<div class="lnp-nav"><div class="lnp-nav-title">'
            + esc(TEXT.settings) + '</div>';
    NAV.forEach(function (item) {
      if (item === null) { out += '<div class="lnp-nav-gap"></div>'; return; }
      // No icon glyphs. A first pass drew each nav row with a small bordered
      // square standing in for Edge's icon; rendered, they read as a column of
      // unchecked checkboxes, which invites a reader to go ticking them. The
      // nav is scene-setting, so it gets none.
      out += '<div class="lnp-nav-item'
           + (item === NAV_ACTIVE ? ' is-active' : '') + '">'
           + esc(item) + '</div>';
    });
    return out + '</div>';
  }

  function crumbHTML() {
    var parts = CRUMB.map(function (c, i) {
      var cls = i === CRUMB.length - 1 ? ' class="lnp-here"' : '';
      return '<span' + cls + '>' + esc(c) + '</span>';
    });
    return '<div class="lnp-crumb"><span class="lnp-back" aria-hidden="true">&lsaquo;</span>'
         + parts.join('<span class="lnp-sep">/</span>') + '</div>';
  }

  function blockHTML(title, isTarget, rowsHTML) {
    return '<div class="lnp-block' + (isTarget ? ' is-target' : '') + '">'
         + '<div class="lnp-block-head"><div class="lnp-block-title">'
         + esc(title) + '</div>'
         + '<span class="lnp-add">' + esc(TEXT.addSite) + '</span></div>'
         + rowsHTML + '</div>';
  }

  function panelHTML(host) {
    var blockedRows = '<div class="lnp-block-note">' + esc(TEXT.empty) + '</div>';
    var allowedRows = '<div class="lnp-row is-target">'
                    + '<span class="lnp-host">' + esc(host) + '</span>'
                    + '<span class="lnp-dots" aria-hidden="true">&#8943;</span>'
                    + '</div>';

    // Spoken description, so a screen reader gets the finding rather than a
    // recital of Edge's navigation.
    var label = 'The Edge Local network settings page. Default behavior is set '
      + 'to "' + TEXT.defaultMain + '". Under Customized behaviors, the "'
      + TEXT.blocked + '" list is empty, and the "' + TEXT.allowed
      + '" list contains ' + host + '.';

    return '<div class="lnp" role="img" aria-label="' + esc(label) + '">'
      + navHTML()
      + '<div class="lnp-main">'
      + '<div class="lnp-search"><span class="lnp-mag" aria-hidden="true"></span>'
      + esc(TEXT.search) + '</div>'
      + crumbHTML()
      + '<p class="lnp-label">' + esc(TEXT.defaultLabel) + '</p>'
      + '<div class="lnp-card"><div class="lnp-card-text">'
      + '<div class="lnp-card-main">' + esc(TEXT.defaultMain) + '</div>'
      + '<div class="lnp-card-note">' + esc(TEXT.defaultNote) + '</div>'
      + '</div><span class="lnp-toggle" aria-hidden="true"></span></div>'
      + '<p class="lnp-label">' + esc(TEXT.customLabel) + '</p>'
      + '<p class="lnp-sublabel">' + esc(TEXT.customNote) + '</p>'
      + blockHTML(TEXT.blocked, false, blockedRows)
      + blockHTML(TEXT.allowed, true, allowedRows)
      + '</div></div>';
  }

  function captionHTML(lead, host) {
    return '<p class="lnp-caption">'
      + (lead ? '<strong>' + esc(lead) + '</strong> ' : '')
      + 'An illustration, not a screenshot &mdash; the labels are taken from '
      + 'Edge 152, but your version may lay them out differently. '
      + esc(host) + ' must appear in the <em>' + esc(TEXT.allowed)
      + '</em> block, the lower of the two. Chrome&rsquo;s page carries the same '
      + 'title and the same two blocks; only the route to reach it differs.'
      + '</p>';
  }

  function render() {
    var hosts = document.querySelectorAll('[data-lnp-panel]');
    for (var i = 0; i < hosts.length; i++) {
      var el = hosts[i];
      var host = el.getAttribute('data-host');
      if (!host) { continue; }   // no address to show: draw nothing
      el.innerHTML = panelHTML(host)
                   + captionHTML(el.getAttribute('data-caption'), host);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render);
  } else {
    render();
  }
})();
