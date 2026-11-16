# Packaging and releases

How this repo stays a source repository while shipping installable builds, and the rules that keep it that way.

## Principles

1. **Source in git, binaries in Releases.** APKs, IPAs, installers and archives are attached to a tagged
   GitHub Release. They are never committed. A repo that accumulates 100 MB binaries cannot be cloned, and
   git never forgets them.
2. **Canvas folders are frozen.** `v1/` … `v4/` are design history. Fixes ship in the next folder, not by
   editing an old one.
3. **Pages serves source, not builds.** The site at
   <https://bortknox.github.io/Cowon-a2-transformation-demo/> is this repository's own HTML. There is no
   separate build step to break — see [Publishing](#publishing) for which branch is served.
4. **Nothing secret is stored here.** Keystores, passwords and tokens live on the machine that signs, and in
   GitHub *Secrets* if CI ever signs automatically.

## Publishing

GitHub Pages builds **one branch, one folder**, chosen in *Settings → Pages*. That branch is what the world
sees; a push to a different branch changes the repo but not the live site. This is the single most common
way a Pages project silently goes stale.

- **Intended setting:** *Deploy from a branch* → `main` → `/ (root)`. The hub is `index.html`, the canvases
  are the `vN/` folders, and Pages serves the committed files unchanged.
- **If another branch is selected**, either point Pages back at `main`, or fast-forward that branch to `main`
  after every site change (`git push origin main:<branch>`). Two branches drifting apart is how the site
  ends up showing a version that no longer exists in the repo.
- **Never rename the repo or the Pages path casually** — every demo link is public and the URLs are the
  product's address.
- No `.nojekyll` is needed: there are no underscored files and no Jekyll-specific syntax in use, but if a
  future folder starts with `_` or contains `{{ }}`-style text, add an empty `.nojekyll` at the root.

## Version numbers

Two systems, deliberately separate:

| Thing | Scheme | Example | Meaning |
|---|---|---|---|
| Canvas folder | `vN` | `v4/` | design iteration, published as a demo |
| Release tag | `v0.N.P` | `v0.4.0` | shipped artifact built from canvas `N` |
| Tool release tag | `a2vf-vX.Y.Z` | `a2vf-v1.0.0` | companion tool in `tools/`, versioned independently |

While the project is pre-1.0 the major stays `0`. The minor tracks the canvas number; the patch counts
rebuilds or fixes for that same canvas (e.g. `v0.4.1` = another APK from the same design). When the app is
store-ready and the canvas stops changing every week, the first `v1.0.0` can be cut.

Tags are annotated and prefixed with `v`: `git tag -a v0.4.0 -m "Android: first installable build"`.

## Companion tool releases

`tools/a2-video-forge/` ships on its own schedule. Zip the folder, tag `a2vf-v1.0.0`, attach
`a2-video-forge-1.0.0-windows.zip`, and state the FFmpeg requirement in the release notes — the tool cannot
run without an FFmpeg build containing `libxvid` and `libmp3lame`, and that is the first question every user
will have.

## Artifact names

Predictable names make the download page readable and scripts simple:

| Platform | File |
|---|---|
| Android (direct install) | `cowon-te-0.4.0-android.apk` |
| Android (Play Store) | `cowon-te-0.4.0-android.aab` — uploaded to Play, never attached publicly |
| Windows | `cowon-te-0.4.0-windows-x64.zip` (or `.msi`) |
| macOS | `cowon-te-0.4.0-macos-arm64.dmg` |
| Linux | `cowon-te-0.4.0-linux-x86_64.AppImage` |
| A2 Video Forge (Windows) | `a2-video-forge-1.0.0-windows.zip` |
| Checksums | `SHA256SUMS.txt` |

Attach the source that produced the build to the Release as well — GitHub's automatic
"Source code (zip/tar.gz)" links cover the repo at that tag, which is usually enough.

## Android signing

- One release keystore, generated **once**, stored offline with a password in a password manager. Losing it
  means the app can never be updated in place on an installed device.
- `keystore.properties` and `*.jks` / `*.keystore` are gitignored. Verify with `git status` before committing.
- Publish the certificate's SHA-256 fingerprint in the Release notes, so users can confirm an APK is yours.
- Debug builds for testing are unsigned for distribution and must not be published as releases.

## Release checklist

1. Canvas for this version is frozen and registered in `versions/index.html`.
2. `README.md` status table matches reality (no download listed that does not exist).
3. Version bumped in the app shell and the file names below match exactly.
4. Build, install on a clean device/VM, play audio, quit, relaunch — the boring test that catches most bugs.
5. `SHA256SUMS.txt` regenerated for every artifact.
6. Draft a Release titled `v0.N.P`, tag it on `main`, attach artifacts, write honest notes: what works,
   what does not, known device quirks.
7. Publish, then check the download links from a logged-out browser.
8. If something is broken after publishing, edit the Release notes rather than silently replacing binaries;
   replacing an APK under the same version trains users not to trust checksums.

## What not to do

- Do not commit `node_modules/`, build output, APKs, keystores or `.env` files.
- Do not delete or rewrite old tags. Old canvases stay reachable; old releases stay honest.
- Do not rename the repo or the Pages path casually — every demo link is public and hard to chase down.
- Do not present a canvas as an app. "Canvas" is a demo; an "installer" is a Release.
