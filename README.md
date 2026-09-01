# Calibre Clarity

Calibre Clarity is a selectable visual profile designed to make calibre easier
to understand, calmer to scan, and more accessible to a broad range of users.

Its design priorities are:

- clear hierarchy and familiar actions;
- restrained, consistent icons;
- readable contrast and typography;
- compact spacing without crowding;
- predictable search, sorting, navigation, and book details;
- platform-neutral resources and system-font compatibility.

## Install

Calibre Clarity is distributed without an executable installer. Once the theme
is included in calibre's public icon-theme catalogue, install it directly from:

**Preferences > Interface > Look & Feel > Change icon theme**

Select **Calibre Clarity**, apply the change, then restart calibre if prompted.
Use the same screen to return to calibre's default icons.

Before the theme is listed in the public catalogue, contributors can create and
install it from the editable resources by opening:

**Preferences > Advanced > Miscellaneous > Create icon theme**

Select the `icon-theme-png` folder and use the metadata already included in
that folder.

The optional layout profile and book-details stylesheet are kept in this
repository as development resources. They are not applied by the native icon
theme and are not part of the no-installer user workflow.

## Native icon archive

The ready-to-use `calibre-clarity-icon-theme.zip` archive is published with
each [GitHub release](https://github.com/gridaine/calibre-clarity/releases/latest)
instead of being stored in the source tree. The editable source artwork remains
in `icon-sources-svg`; calibre converts the artwork to the resources required by
its theme packager.

## Icon readability and development

The artwork uses reduced transparent margins so most symbols occupy about
14 pixels within a 16-pixel menu icon slot. Neutral icons use a darker gray
(`#636366`) for clearer contrast. Menu dimensions are controlled by Qt and
the operating system; the theme improves the visible artwork without changing
menu spacing or calibre's code. The same artwork is used in toolbars.

SVG files in `icon-sources-svg` are the editable originals. After editing them,
render the PNG resources with calibre's bundled Python and Qt runtime:

```sh
calibre-debug -e render_icons.py
calibre-debug -e build_native_theme.py -- icon-theme-png ../release-assets/calibre-clarity-icon-theme.zip
```

On macOS, `calibre-debug` is available at
`/Applications/calibre.app/Contents/MacOS/calibre-debug`.
The renderer's optional `--normalize` flag adjusts margins and neutral colors
in previously unnormalized SVG artwork; repeated normalization is idempotent.
PNG files are generated assets, not the editable source.

## Licenses

Calibre Clarity uses separate licenses for code and artwork:

- scripts, CSS, configuration profiles and technical documentation are
  available under the [MIT License](LICENSE);
- original SVG, PNG and JPEG artwork is available under the
  [Creative Commons Attribution 4.0 International License](LICENSE-ASSETS.md).

The generated icon-theme archive contains CC BY 4.0 artwork. Product names,
logos and trademarks remain the property of their respective owners. Calibre
Clarity is an independent project and is not endorsed by the calibre project
or by third-party services represented by compatibility icons.
