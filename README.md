# Cowon A2 — Field OS simulator

An independent, zero-runtime-dependency HTML5 interface study for the 2005 Cowon iAUDIO A2. The **device screen is the product**: a strict 480×272 black Canvas UI with a five-tile moving carousel, eight actual mode pages, hardware/key controls, live telemetry and generated content. The optional demo-media reel is below the chassis and can be ignored while operating the simulator.

## Run it

Serve the repository root so the browser treats the page as an application:

```sh
python3 -m http.server 4173
```

Open <http://localhost:4173>. The simulator, generated still, video-like animation, and procedural music are all inline in `index.html`: there are no asset downloads, npm packages, network requests, or build steps. Sound is synthesized in-browser with Web Audio after a user gesture (browsers block automatic audio playback).

## Hardware controls

| Physical control | Keyboard | Behavior |
| --- | --- | --- |
| Four-way joystick | Arrow keys | Navigate the home carousel and operate the current mode |
| Center click | Enter | Open, play/pause, or select the focused item |
| Back | Escape / Backspace | Return to the previous screen |
| A / B / C soft keys | `1` / `2` / `3` | Context-sensitive orange / cyan / lime actions |
| LCD / AV-OUT / HOLD slide | Click one of the three hardware positions | Change output or lock all hardware/key inputs |
| Display tile | Click a visible home tile | Open that mode directly |

On HOME, left/right move the five-tile window across all eight modes; the focused tile remains on-screen. Enter opens it. A/B/C are quick jumps to Music, Playlists, and Browser bookmarks.

## Screen map and actions

1. **MOVIE** — generated moving vector reel; Enter play/pause, left/right scrub, A aspect, B subtitles, C soundtrack.
2. **MUSIC** — animated tape deck and frequency-reactive spectrum. Left/right cycle three original procedural tracks (about 27–30 seconds each); Enter plays/pauses; A changes synth/EQ voicing, B repeat/shuffle, C marks/clears an A–B loop; up/down changes output volume.
3. **PHOTO** — generated RAW-style frame; A rule-of-thirds grid, B zoom, joystick pan, C next frame; live RGB histogram and camera telemetry.
4. **TEXT** — paged field notes with scrolling, font sizing, markers and bookmarks.
5. **RADIO** — FM dial, 25 presets, tuning/seek, preset selection and record-state trigger.
6. **RECORD** — MIC / LINE-IN / AV-IN source selection, animated level meters, record toggle, bitrate and auto-sync controls.
7. **BROWSER** — dual HDD / CF-card panes, multi-select, switch panes and copy marked files into the simulated HDD list.
8. **SETUP** — eight clearly labelled submenus. Open any category with Enter; up/down chooses an option and left/right changes it. The visible value and setting bar update immediately.

The A/B/C legend stays at the bottom edge of every screen. The A2 slide switch remains usable in HOLD so the user can unlock the device.

## Demo media and sound

The optional section after the hardware shows an inline Optical Bench still, an interactive 12-second generated vector-animation loop, and the same live synthesizer used in Music mode. The three original cues are sequenced from oscillators in JavaScript; there are no embedded audio files or third-party samples. Frequency bars in the Music screen read the live Web Audio analyser output while playing. All sound/visual patterns are original demo code and can be treated as CC0/public-domain demo material.

## Implementation and checks

Everything ships in `index.html`: styles, Canvas 2D screen renderer, UI/state logic, procedural video-like canvas, and Web Audio synth. No external JS or media paths are required. The page maintains a 480×272 display backing canvas and updates with `requestAnimationFrame`.

Smoke checks run for JavaScript syntax and simulated browser interactions across all eight screens, including Home → Movie, the last carousel item → Setup, synth play/track cycling, and HOLD input lock. Browser-specific audio output still depends on a modern browser with Web Audio support and a user gesture to start sound.
