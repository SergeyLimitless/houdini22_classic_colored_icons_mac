# Houdini 22 Classic Icons for macOS

Version 0.400 · © Serj Limitless · MIT License · unofficial, not affiliated with SideFX

Brings back the classic, full-colour UI icons (viewport toolbars, spreadsheet, buttons) in
Houdini 22's new UI on macOS — the same art Houdini 22 shows in its old-UI mode.
Also includes my **Limitless 4** colour theme.

## How it works

Houdini 22 still ships the classic art for ~385 UI icons; its new theme replaces them with
grey-tinted versions. The script builds a small add-on (~1.5 MB per Houdini build) that tells
Houdini to use the classic ones again. Your Houdini installation is never modified, and no SideFX
artwork is included in this download — everything is made from your own Houdini.

Needs: macOS and Houdini 22 installed in the usual place (`/Applications/Houdini`).

## Install the icons

1. **Quit Houdini.**
2. Open **Terminal**.
3. Type `python3` followed by **one space** (don't press Return yet).
4. **Drag the file `houdini22_classic_icons_mac.py`** from Finder into the Terminal window.
   Its location appears after `python3 `.
5. Type **one space**, then `--build`, and press **Return**.

   The line should look like this (your folder may differ):

       python3 /Users/you/Downloads/houdini22_classic_icons_mac/houdini22_classic_icons_mac.py --build

6. Wait for the lines that end with `package houdini21_icons_for_houdini22_….json`, then start Houdini 22.

If macOS asks to install "command line developer tools" at step 5, click **Install**, wait until it
finishes, and repeat steps 3–5.

**Just want to see what it would do first?** Do steps 3–4 and press **Return** without `--build`.
That only prints a summary and changes nothing.

## Remove the icons

Same as installing, but type `--uninstall` instead of `--build` in step 5. Restart Houdini.

## After a Houdini update

Each Houdini 22 build needs its own add-on. After installing a new build, run the install steps again.

## If you see "Cannot write to …/packages"

Some plugin installers (e.g. Redshift) lock Houdini's packages folder. Fix it once: copy the
`sudo chown …` line the script prints, paste it into Terminal, press **Return** and type your Mac
password (nothing appears while typing — that's normal). Then run the install steps again.

## Limitless 4 theme

1. In Finder, press **Cmd + Shift + G**, paste this and press **Return**:

       ~/Library/Preferences/houdini/22.0/config/Themes

   If it says the folder doesn't exist, open `~/Library/Preferences/houdini/22.0/config` instead and
   create a folder named `Themes` there.
2. Copy **`Limitless_4.theme.json`** into that folder.
3. Restart Houdini and choose **Limitless 4** in Houdini's colour theme menu.

## Credits

Idea based on [SalmeInMotion/houdini21-icons-for-houdini22](https://github.com/SalmeInMotion/houdini21-icons-for-houdini22)
(MIT, Windows). This macOS version uses Houdini 22's own classic art instead of Houdini 21's.
Please share this folder, not the files the script generates.
