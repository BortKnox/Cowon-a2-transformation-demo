# Contributing

This repo is a **gallery of frozen design canvases** plus the hub that presents them. The rules below keep
old links working and keep the history honest.

## The one hard rule

**Never edit a released canvas.** `v1/`, `v2/`, `v3/`, `v4/` … are snapshots. A bug in an old canvas is
preserved on purpose, because that canvas is the record of what the design looked like at that point.
Fixes and improvements go into the *next* version folder.

## Adding a canvas version

1. **Pick the next number.** If the highest folder is `v4/`, the new one is `v5/`. Never reuse or renumber.
2. **Create the folder** and put the new canvas at `v5/index.html`.
3. **Keep it one file.** Inline CSS and JS. No CDN links, no bundler, no external fonts or images — the
   chassis photo must stay embedded as a data URI so the file works offline.
4. **Label it inside the file.** Update `<title>`, the header version text and the Field Notes heading in
   the same pass. (v4 still reads "V3" internally; that is the kind of drift to avoid.)
5. **Freeze it.** Once pushed, stop editing `v5/index.html`. Further work becomes `v6/`.
6. **Register it** in `versions/index.html` and in the Live canvases table in `README.md`.
7. **Add a preview**: screenshot the canvas at **1200×630** and save it as `assets/preview-v5.png`. The hub
   uses `assets/preview-v4.png` as its hero; update that reference only when a version becomes the showcase.
8. **Commit** with a message that names the version and the change, e.g.
   `v5: add arrangement view and per-track FX sends`.

## Working on the shell

`index.html` (the hub), `versions/`, `docs/` and `README.md` are ordinary maintained pages — improve them
freely. Keep the visual language: light grey grid, monospace uppercase, 1px black rules, one orange accent
(`#FF6A1F`). No trackers, no external requests.

## Binaries and secrets

- **Never commit** APKs, IPAs, installers, keystores, `node_modules/` or build output. Artifacts belong in
  a tagged Release — see [docs/PACKAGING.md](docs/PACKAGING.md).
- **Never commit** tokens, keystore passwords or `.env` files. If a secret lands in a commit, rotate it;
  deleting the file in a later commit does not remove it from history.

## If you are an AI agent

You are welcome here, with the same rules:

- Read this file and [docs/PACKAGING.md](docs/PACKAGING.md) before changing anything.
- Do not "tidy" old version folders, do not reformat or minify canvases, do not change a canvas's embedded
  image or audio.
- Do not invent downloads. If an installer does not exist, the table says *planned*.
- Prefer small, reviewable commits whose message states the version and the intent.
