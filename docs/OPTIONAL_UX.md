# Calibre Clarity: optional presentation pack

This optional pack styles book details with a consistent white background,
clearer typography and small field icons. It is independent of the icon theme.
It does not change books, metadata or conversion settings. It is not a plugin
or an executable installer. No scripts need to be run.

## Contents

- `book_details.css`, with its SVG artwork embedded.
- English and French instructions.
- MIT license for CSS and CC BY 4.0 for artwork by Loic Gridaine.

Layout recommendations below are optional and applied manually in calibre.
Copying the CSS does not apply those settings or change your selected icon theme.

## Install

1. Extract `calibre-clarity-ux.zip`.
2. In calibre, open **Preferences > Advanced > Miscellaneous > Open calibre configuration directory**.
3. Keep that folder open and quit calibre completely.
4. Open `resources/templates` inside this configuration folder. Create the
   `resources` and `templates` folders if they do not already exist.
5. If `book_details.css` already exists there, back it up elsewhere or rename
   it to `book_details.before-clarity.css` before continuing.
6. Copy this pack's `book_details.css` into `resources/templates`.
7. Restart calibre and select a book to see its details.

Use the folder opened by calibre, not the application or library folder.
There are no personal paths to edit in the stylesheet. Do not load this ZIP
through Plugins or Change icon theme.

## Optional layout recommendations

Record your existing settings or take screenshots first. Change one setting at
a time. Labels can vary with calibre versions and translations.

| Element | Suggested starting point |
| --- | --- |
| Colors | Use a light interface: this stylesheet has a white background. |
| Text | Start with the system font and size; enlarge text if needed. |
| Toolbar | In Look & Feel, use medium icons and keep text labels visible while learning. |
| Frequent actions | In Preferences > Toolbars & menus, keep Add books, Edit metadata, View, Convert books and Preferences accessible. Keep Send to device if you use an e-reader. |
| Search and sorting | Keep the search field and Sort command available. |
| Left sidebar | Drag the divider until category names are readable. About 230 to 280 pixels is a starting point, not a requirement. |
| Cover grid | Show titles, increase cover size and reduce spacing in the grid preferences. The number of columns depends on the screen and visible panels. |
| Categories | Use first-letter grouping for long lists in the Tag browser options, where available. |
| Book details | Use the panel's configuration command to choose fields and their order. |

Suggested details order: title, authors, series, rating, tags, formats,
publication, languages and comments. Add pages if your library already has that
field. This pack does not create custom columns. Keep any technical fields you
need in the full Information window; CSS does not configure field visibility.

## Restore your previous appearance

1. Quit calibre.
2. Move Clarity's `book_details.css` out of `resources/templates`.
3. Restore your backed-up CSS with the exact filename `book_details.css`, if
   you had one. Otherwise calibre will use its built-in stylesheet again.
4. Restart calibre.
5. Restore manually changed layout settings from your notes. Removing the CSS
   does not undo those settings.

Personal resources apply across libraries sharing the same calibre configuration.
The CSS also affects the full book-information window, but not the e-book viewer
or Content server. Existing formatting in book descriptions may affect the result.

Reference testing: calibre 9.13 on macOS. Windows and Linux have not yet been
visually validated. Personal resources usually survive upgrades, but future
changes to calibre's HTML or Qt may require stylesheet updates.

Official documentation:
https://manual.calibre-ebook.com/customize.html#overriding-icons-templates-et-cetera

Project and support: https://github.com/gridaine/calibre-clarity
