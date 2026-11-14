# Cowon A2 / Field OS

An independent, zero-runtime-dependency HTML5 hardware simulator and interface study for the 2005 Cowon iAUDIO A2. The visual language takes cues from compact Teenage Engineering instruments: black LCD, crisp monospaced telemetry, hard 1 px vector lines, aluminum chassis, and orange / cyan / lime controls.

## Run the demo

The easiest way to try it is to serve the repository root locally (the music and video are separate, original media files):

```sh
python3 -m http.server 4173
```

Then open <http://localhost:4173> in a modern browser. No npm install, build step, network access, or browser extension is required. Audio starts only after a user presses Play or enters Music mode and presses Enter, in keeping with browser autoplay rules.

## Controls

| Hardware | Keyboard | Action |
| --- | --- | --- |
| Four-way joystick | Arrow keys | Navigate, tune, pan, or change settings |
| Center click | Enter | Select / play / pause |
| Back button | Escape or Backspace | Return one level |
| Soft key A | `1` | Current screen's orange action |
| Soft key B | `2` | Current screen's cyan action |
| Soft key C | `3` | Current screen's lime action |
| Slide switch | Click LCD / AV-OUT / HOLD | Resume LCD, show AV output, or lock hardware inputs |

In Music mode, left/right cycle through the three original tracks; Enter toggles playback; A cycles BBE/EQ presets; B changes repeat mode; C toggles the A-B loop marker. A separate player below the chassis provides mouse/touch controls for the tracks. The other screens include Movie, Music, Photo/RAW, Text, Radio, Record, Browser/USB Host, and Setup.

## Demo media

- **Three playable, loopable synth cues:** Signal Path, Tangerine Circuit, and Night Drive (`assets/audio/`).
- **Demo still:** Optical Bench RAW viewer (`assets/field-os-still.svg`).
- **Demo video:** silent, six-second looping tape-deck animation (`assets/field-os-demo.webm`).
- All media is original work created for this demo and dedicated to the public domain under CC0 1.0; see [`assets/README.md`](assets/README.md) for provenance. The audio can be regenerated with the Python standard-library script `tools/generate_demo_audio.py`.

## Implementation

`index.html` contains the application, styling, Canvas drawings and control logic. The screen backing canvas and viewport are both exactly 480×272. The UI is drawn with native Canvas 2D primitives and updated with `requestAnimationFrame`; the chassis, multimedia player, and generated demo media are browser-native. The simulator uses no third-party JavaScript libraries or runtime services.

## Smoke tests performed

- JavaScript syntax checked with Node.js.
- All three WAV files checked for mono PCM format, sample rate, and duration.
- WebM video decoded successfully with FFmpeg during asset generation/verification.
- All local media references checked for existence.
