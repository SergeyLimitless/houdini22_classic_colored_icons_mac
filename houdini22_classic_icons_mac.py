#!/usr/bin/env python3
"""Houdini 22 Classic Icons for macOS — Version 0.100
© Serj Limitless — MIT License (see LICENSE). Unofficial; not affiliated with or endorsed by SideFX.
Idea based on SalmeInMotion/houdini21-icons-for-houdini22 (MIT, Windows).
Contains no SideFX artwork: everything is built locally from your own Houdini install.
Do not redistribute the generated overlay files.

Houdini 22 keeps the old-style art for most UI icons in its own main SVGIcons.index; the new themed
art lives in SVGIconsUI.index, where Houdini tints it with the Pluto theme. This builds, per H22
build, an overlay SVGIconsUI.index (from that build's own file) WITHOUT the icons whose main-index
version differs, so Houdini falls back to the main index and draws the old art in full colour.
Icons with no old version stay as they are. The Houdini install is never modified.

Usage:
  python3 houdini22_classic_icons_mac.py              dry run for all H22 builds (writes nothing)
  python3 houdini22_classic_icons_mac.py --build      build/refresh overlays + package files
  python3 houdini22_classic_icons_mac.py --uninstall  remove overlays + package files
Options: --h22 <build>   (default: every installed Houdini 22 build)

Writes per build:
  ~/Library/Application Support/Houdini21IconsFor22/overlays/<build>/houdini/config/Icons/SVGIconsUI.index
  ~/Library/Application Support/Houdini21IconsFor22/overlays/<build>/cache/   (icon cache, emptied on build)
  ~/Library/Application Support/Houdini21IconsFor22/overlays/<build>/manifest.json
  ~/Library/Preferences/houdini/22.0/packages/houdini21_icons_for_houdini22_<build>.json
  .../overlays/<build>/houdini/config/Icons/SVGIconsUI.cache (+ .serial)   (pruned stock pre-rendered cache)
"""
import argparse, datetime, json, os, re, shutil, struct, sys
from pathlib import Path

__version__ = "0.100"
# Internal IDs/paths keep the original names so installs stay compatible with earlier builds of this tool.
MOD_ID = "houdini21-icons-for-22"
APPS = Path("/Applications/Houdini")
REL_ICONS = "Frameworks/Houdini.framework/Versions/Current/Resources/houdini/config/Icons"
BASE = Path.home() / "Library/Application Support/Houdini21IconsFor22/overlays"
OWNED_FILES = {"SVGIcons.index", "SVGIconsUI.index", "SVGIconsUI.index.bak_before_test",
               "SVGIconsUI.cache", "SVGIconsUI.cache.serial"}


def all_versions(major):
    return sorted((p.name[7:] for p in APPS.glob(f"Houdini{major}.*") if (p / REL_ICONS / "SVGIconsUI.index").is_file()),
                  key=lambda v: tuple(int(x) for x in v.split(".")))


def read_index(path):
    """Return (description, [(name, offset, length, stamp)], data_start) of a Houdini INDX file."""
    with open(path, "rb") as f:
        if f.read(4) != b"INDX":
            raise ValueError(f"bad magic in {path}")
        (dlen,) = struct.unpack(">Q", f.read(8))
        if dlen > 1 << 20:
            raise ValueError("bad description length")
        desc = f.read(dlen)
        (count,) = struct.unpack(">I", f.read(4))
        if count > 100000:
            raise ValueError("bad icon count")
        entries = []
        for _ in range(count):
            (nlen,) = struct.unpack(">I", f.read(4))
            name = f.read(nlen).decode("utf-8")
            off, ln, stamp = struct.unpack(">III", f.read(12))
            entries.append((name, off, ln, stamp))
        data_start = f.tell()
    size = os.path.getsize(path)
    for name, off, ln, _ in entries:
        if data_start + off + ln > size:
            raise ValueError(f"section {name} beyond end of {path}")
    return desc, entries, data_start


def read_sections(path, names=None):
    _, entries, ds = read_index(path)
    out = {}
    with open(path, "rb") as f:
        for n, off, ln, _ in entries:
            if names is None or n in names:
                f.seek(ds + off)
                out[n] = f.read(ln)
    return out


def write_pruned(src, dst, drop):
    desc, entries, ds = read_index(src)
    keep = [e for e in entries if e[0] not in drop]
    tmp = dst.with_name(dst.name + ".tmp")
    with open(src, "rb") as s, open(tmp, "wb") as o:
        o.write(b"INDX" + struct.pack(">Q", len(desc)) + desc + struct.pack(">I", len(keep)))
        off = 0
        for n, _, ln, st in keep:
            nb = n.encode("utf-8")
            o.write(struct.pack(">I", len(nb)) + nb + struct.pack(">III", off, ln, st))
            off += ln
        for n, eo, ln, _ in keep:
            s.seek(ds + eo)
            o.write(s.read(ln))
    read_index(tmp)  # validate before replacing
    tmp.replace(dst)
    return len(entries), len(keep)


def owned(data_root):
    m = data_root / "manifest.json"
    try:
        return json.load(open(m)).get("modId") == MOD_ID
    except Exception:
        return False


def run(a, h22):
    data_root = BASE / h22
    prefs_pkgs = Path.home() / f"Library/Preferences/houdini/{h22.rsplit('.', 1)[0]}/packages"
    pkg_path = prefs_pkgs / f"houdini21_icons_for_houdini22_{h22}.json"

    if a.uninstall:
        if owned(data_root):
            shutil.rmtree(data_root); print(f"Removed overlay {data_root}")
        if pkg_path.is_file() and MOD_ID in pkg_path.read_text():
            pkg_path.unlink(); print(f"Removed package {pkg_path}")
        return

    stock = APPS / f"Houdini{h22}" / REL_ICONS
    ui = read_sections(stock / "SVGIconsUI.index")
    main = read_sections(stock / "SVGIcons.index", set(ui))
    # v003: drop every UI icon that also exists in the main index — differing art (classic look) AND
    # identical art (untinted, e.g. TRS / precision / snap) — so all of them draw from main, untinted.
    drop = {n for n in ui if n in main}
    differ = sum(1 for n in drop if main[n] != ui[n])
    no_old = len(ui) - len(drop)
    print(f"H{h22}: UI icons {len(ui)} | classic art: {differ} | same art, untinted: {len(drop) - differ} | "
          f"no old version (stay new, tinted): {no_old}")
    if not a.build:
        return

    prefs_pkgs.mkdir(parents=True, exist_ok=True)
    if not os.access(prefs_pkgs, os.W_OK):
        sys.exit(f"Cannot write to {prefs_pkgs} (often made root-owned by a plugin installer).\n"
                 f"Fix it once with:\n  sudo chown \"$USER\" \"{prefs_pkgs}\"\nthen run --build again.")
    if data_root.exists() and not owned(data_root):
        sys.exit(f"{data_root} exists but is not owned by this mod; aborting.")
    if pkg_path.exists() and MOD_ID not in pkg_path.read_text():
        sys.exit(f"{pkg_path} exists and is not owned by this mod; aborting.")

    icons_out = data_root / "houdini/config/Icons"
    icons_out.mkdir(parents=True, exist_ok=True)
    for f in icons_out.iterdir():  # remove only files this mod made (v001 H21 copy, test backup)
        if f.name in OWNED_FILES and not f.name.startswith("SVGIconsUI."):
            f.unlink(); print(f"  removed old {f.name}")
    total, kept = write_pruned(stock / "SVGIconsUI.index", icons_out / "SVGIconsUI.index", drop)
    # v004: Houdini seeds its icon cache from the first SVGIconsUI.cache on HOUDINI_PATH. The stock one holds
    # pre-rendered NEW-art bitmaps (e.g. BUTTONS_gear16x16.rgba) that show untinted red once the icon left the
    # UI index. Ship a pruned copy (stock minus bitmaps of dropped icons) so those sizes get re-rendered.
    _, centries, _ = read_index(stock / "SVGIconsUI.cache")
    cdrop = {n for n, *_ in centries
             if (mm := re.match(r"^(.*?)\d+x\d+\.rgba$", n)) and mm.group(1) + ".svg" in drop}
    ctotal, ckept = write_pruned(stock / "SVGIconsUI.cache", icons_out / "SVGIconsUI.cache", cdrop)
    shutil.copy2(stock / "SVGIconsUI.cache.serial", icons_out / "SVGIconsUI.cache.serial")
    print(f"  pre-rendered cache {ctotal} -> {ckept} bitmaps")
    cache = data_root / "cache"
    if cache.exists():
        shutil.rmtree(cache)
    cache.mkdir()
    json.dump({"modId": MOD_ID, "method": "v004 classic-from-H22-main-index, same-art untinted, pruned UI cache", "target": h22,
               "builtAt": datetime.datetime.now().isoformat(timespec="seconds"),
               "uiIndexEntries": total, "uiIndexKept": kept, "classicIcons": sorted(drop)},
              open(data_root / "manifest.json", "w"), indent=2)
    pkg = {"enable": f"houdini_version == '{h22}'", "show": True,
           "env": [{"HOUDINI21_ICONS_FOR_22": MOD_ID}, {"HOUDINI_ICON_CACHE_DIR": str(cache)}],
           "hpath": str(data_root / "houdini")}
    json.dump(pkg, open(pkg_path, "w"), indent=4)
    print(f"  UI index {total} -> {kept} entries; overlay {data_root}; package {pkg_path.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h22", help="one build (default: all installed Houdini 22 builds)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--build", action="store_true"); g.add_argument("--uninstall", action="store_true")
    a = ap.parse_args()
    for h22 in ([a.h22] if a.h22 else all_versions(22)):
        run(a, h22)
    if not (a.build or a.uninstall):
        print("\nDry run — nothing written. Re-run with --build.")


if __name__ == "__main__":
    main()
