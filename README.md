# Houdini 22 Classic Icons for macOS

Version 0.100 · © Serj Limitless · MIT License · unofficial, not affiliated with SideFX

Brings back the classic, full-colour UI icons (viewport toolbars, spreadsheet, buttons) in
Houdini 22's new UI on macOS — the same art Houdini 22 shows in its old-UI mode.

## How it works

Houdini 22 still ships the classic art for ~385 UI icons in its own `SVGIcons.index`. Its new
theme takes the new-style versions from `SVGIconsUI.index` and tints them grey. For each installed
Houdini 22 build, the script makes a small overlay (~1.5 MB):

- a copy of that build's `SVGIconsUI.index` without those icons, so Houdini draws the classic art in colour;
- a copy of the stock pre-rendered `SVGIconsUI.cache` without their new-style bitmaps;
- a Houdini package file that loads the overlay only for that exact build, with its own icon cache.

The Houdini installation is never modified. No SideFX artwork is included in this download;
everything is built from your own install.

## Requirements

- macOS, Houdini 22 installed in `/Applications/Houdini/Houdini22.0.xxx`
- `python3` (macOS offers to install it with the Command Line Tools on first use)

## Use

Quit Houdini, then in Terminal, in this folder:

```bash
python3 houdini22_classic_icons_mac.py
```
Dry run: shows what it would do for every Houdini 22 build, writes nothing.

```bash
python3 houdini22_classic_icons_mac.py --build
```
Builds the overlays and package files. Start Houdini 22.

`--h22 22.0.466` limits it to one build.

## Undo

```bash
python3 houdini22_classic_icons_mac.py --uninstall
```
Or delete `~/Library/Preferences/houdini/22.0/packages/houdini21_icons_for_houdini22_<build>.json`
to switch one build back to stock icons.

## Files it writes

```
~/Library/Application Support/Houdini21IconsFor22/overlays/<build>/
├── houdini/config/Icons/SVGIconsUI.index
├── houdini/config/Icons/SVGIconsUI.cache (+ .serial)
├── cache/            Houdini's icon cache for this overlay
└── manifest.json
~/Library/Preferences/houdini/22.0/packages/houdini21_icons_for_houdini22_<build>.json
```

## Notes

- After installing a new Houdini 22 build, run `--build` again (overlays are build-specific).
- "Cannot write to …/packages": some plugin installers (e.g. Redshift) make that folder root-owned.
  Fix it once with `sudo chown "$USER" ~/Library/Preferences/houdini/22.0/packages`.
- About 150 icons have no classic version in Houdini 22; they keep the new style.
- Bigger toolbar icons: the old-UI Preferences "Icon Size" setting (`general.ui.icon_size`) also works in the new UI.
- Do not share the generated overlay files; share this script instead.

## Credits

Idea based on [SalmeInMotion/houdini21-icons-for-houdini22](https://github.com/SalmeInMotion/houdini21-icons-for-houdini22)
(MIT, Windows), which swaps in Houdini 21 artwork. This macOS version uses Houdini 22's own classic art instead.
