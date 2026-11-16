# Roadmap

Where the project is, where it is going, and what is still unknown. Statuses are honest: nothing is
"coming soon" unless work has actually started.

## The shape of the thing

It began as a firmware overhaul for a physical COWON iAUDIO A2. Working in a browser canvas made the app
itself the interesting part, and then made the *instrument* the interesting part: tape, loops, a signal
chain, guitar and vocal processing. The hardware is still the north star; the software is what can ship first.

## Phases

### M0 — Canvas (ongoing)

Design and prove the app in the browser.

- [x] v1: photo chassis, 8 modes
- [x] v2: 17 modes, looper, recorder, sound chain, routing
- [x] v3: 24 modes, OP-1 style tape/flow/icons, RANK feasibility scoring
- [x] v4: current canvas, larger music screen (internal labels still say V3)
- [ ] Relabel the canvas internals from V3 to V4
- [ ] Settle the mode map — 24 modes across 3 pages is the ceiling the panel can carry
- [ ] Decide what stays simulated versus what becomes a real audio path

Exit criteria: the interaction model stops changing between versions, and the mode map is stable.

### M1 — One app shell, many platforms (next)

Stop maintaining separate canvases as the product; make the canvas a UI layer over a shared core.

- [ ] Extract the UI from the audio/DSP layer behind a small interface
- [ ] Choose the shell (Tauri or Electron) and prove audio I/O inside it
- [ ] Carry the panel layout over at true 480×272 proportions
- [ ] First desktop development build, keyboard + mouse only

Open question: how much of the Web Audio graph survives the port, and what replaces it natively.

### M2 — Android (planned)

The first build a normal person can install.

- [ ] Audio backend in the app shell, touch mapped to joystick/soft keys
- [ ] Signing key generated offline and backed up; certificate fingerprint published
- [ ] Signed APK attached to a tagged Release
- [ ] Install guide with screenshots
- [ ] Optional: Play Store listing (needs an .aab and a developer account)

Open question: background audio and USB audio-device support vary a lot by manufacturer.

### M3 — Guitar and vocal FX (planned)

The reason this stopped being a media player.

- [ ] Audio input with acceptable round-trip latency on desktop first
- [ ] FX chain: the on-screen chain becomes real nodes, not simulation
- [ ] Presets that survive between desktop and Android
- [ ] Input monitoring without feedback (headphone-detection warnings)

Open question: what latency is acceptable before it stops feeling like an instrument — and whether phones
can reach it without a USB interface.

### M4 — iOS, desktop releases, A2 hardware (research)

- [ ] iOS: requires an Apple Developer account; distribution through TestFlight or the App Store, not sideloading
- [ ] Windows/macOS/Linux installers, per-platform signing
- [ ] A2: determine whether a custom firmware build is possible at all on real hardware

These are deliberately last. Each one has a gate that money, hardware access or platform rules control, not effort.

## Not building yet

- Accounts, cloud sync, telemetry, analytics: none. The app runs offline and the site has no trackers.
- A media library/importer. The A2 heritage is the chassis, not a file-manager feature set.
- Anything that needs a server. Still images and audio are embedded.

## How versions and releases relate

Canvas folders (`v1/` … `v4/`) are design iterations. Release tags (`v0.4.0`, `v0.5.0` …) are shipped
artifacts. The minor number tracks the canvas number, so a `v0.4.x` release is built from the `v4` canvas.
Full rules in [PACKAGING.md](PACKAGING.md).
