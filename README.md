# Cowon-a2-transformation-demo

## [▶ Open the live demo](https://bortknox.github.io/Cowon-a2-transformation-demo/)

**[▶ Try v2 (work in progress: 17 modes, looper, recorder, sound chain)](https://bortknox.github.io/Cowon-a2-transformation-demo/v2/)**  ·  v1 above is kept as the reference and rollback.

**[▶ Try v3 (harmonized: 25 modes, RANK feasibility % for A2 and PC/Mac)](https://bortknox.github.io/Cowon-a2-transformation-demo/v3/)**

Runs in the browser, nothing to download. Click once (or press any key) to arm audio, press Enter on MUSIC, then Enter again to play.

Single-file simulator of the Cowon iAUDIO A2 with a Teenage Engineering-style firmware UI.
Open `index.html` in a browser. No dependencies, no build step.

- `index.html` is the whole demo. The chassis photo is embedded as WebP.
- `assets/cowon_a2_front.png` is the cut-out of the A2 front panel (transparent outside edge and screen window).
- `tools/cutout.py` regenerates that cut-out from a front-view photo (needs Pillow, OpenCV, NumPy).

The 480x272 LCD canvas sits behind the photo's screen window. Audio is synthesised live with the Web Audio API
(one 10 s core looped 3x, plus two randomised clones, 30 s each) and every on-screen visual reads from AnalyserNodes.
See the Field Notes section at the bottom of the page for controls and limits.
