# V5 build brief

The complete instruction set for building **v5** of this project. Read it together with `CONTRIBUTING.md`,
`docs/ROADMAP.md` and `docs/PACKAGING.md` — this brief adds the guitar/vocal scope; those files set the
rules. If this brief and the repo docs ever conflict on process (folders, freezing, labeling), the repo
docs win. On scope and naming, this brief wins.

**§8 is the documentation pack.** If you build nothing else from memory, work from §8: it links every
reference needed for each module, so nothing has to be searched for or second-guessed.

---

## 1. Mission

v5 is the canvas where the project becomes a real instrument: **a guitar and vocal rig**. The signal chain
stops being a simulated sound chain and becomes real, playable DSP in the browser: input → drives → amp →
cabinet → modulation → time effects → output.

The one-line identity: **a Teenage Engineering-style music deck whose guitar side replaces a
TONEX/AmpliTube workflow, using only the classic industry-standard sounds, done very well.**

## 2. Scope boundaries — read this before anything else

1. **v5 is a canvas iteration, not the production build.** The project is still in the "design and prove
   it in the browser" stage. v5 does NOT start the Android port, does not write native code, does not
   produce an APK, and does not assume it is the final canvas. The owner has not decided how many live
   demo versions remain after v5 — so v5 must not behave like a last version, must not restructure the
   gallery pattern, and must leave clean seams for a v6.
2. **"Build the full rig" means the full rig in the canvas.** Every module in §6 gets designed and made
   operable in the v5 canvas, with real Web Audio DSP behind it (v4 already synthesizes live audio — the
   rig extends that, not replaces it). Full rig = full design, not "go build the real project."
3. **No neural anything.** No machine learning, no captures, no model loading. Every amp and pedal is
   hand-written DSP modeled on the classic circuit topologies. The bar is "the industry-standard sound,
   done well" — not forensic accuracy of a specific amp on a specific evening.
4. **Input is any line-level or instrument-level source.** An iRig is one example; the rig must accept a
   guitar (or vocal) signal from any audio interface — headset/mic input, USB interface, whatever delivers
   a signal. Never hardcode or brand around a specific interface. The canvas accepts input via
   `getUserMedia` with `echoCancellation: false`, `autoGainControl: false`, `noiseSuppression: false` —
   any of those on and a guitar input sounds like a dial-up modem. Include input gain staging: a trim
   control, a level meter, and a clip indicator, because instrument level and line level differ by an
   order of magnitude.
5. **The guitar rig is also destined for the real Cowon A2 hardware** (it has line-in AV and audio chips
   for it). Do NOT gate any design decision on A2 feasibility, do not cut an effect because the A2 might
   struggle, do not add "A2 can't do this" notes. Build the full rig as designed; hardware tradeoffs are a
   later decision belonging to someone else. RANK feasibility percentages (a v3 feature) simply get
   honest scores like everything else.

## 3. Process rules (from the repo, restated because they matter)

- New folder `v5/`, single file `v5/index.html`, inline CSS/JS, no CDN, no external requests, no external
  fonts/images. Embedded data URIs only.
- Label everything consistently in the same pass: `<title>`, header version text, firmware HUD string,
  Field Notes heading. (v4's changelog still describes v3 — do not fix v4; v5's Field Notes must describe
  v5's actual additions and may note this.)
- Freeze after push. Register in `versions/index.html` and the README Live canvases table. Add
  `assets/preview-v5.png` at 1200×630.
- Small, reviewable commits, message naming version and intent (e.g. `v5: add amp module with gain ladder
  and tone stack`).
- Never edit `v1/`–`v4/`. No accounts, cloud, telemetry, servers. Offline forever.

## 4. Naming system (legwork done — use these, verify, don't improvise)

The rig's models need evocative, trademark-safe names. The industry norm is homage names (Line 6 calls
its Klon model "Minotaur"; Wampler's is "Tumnus"; JHS's is "Notaklön") — clear plays, never the real mark.
Names must be short, UPPERCASE, and fit the 480×272 screen in the canvas's monospace style.

**Rules:**

1. Never use a real brand or model name in the UI, presets, or any user-facing copy. "Fender," "Marshall,"
   "Tube Screamer," "Big Muff," "Plexi," "Dual Rectifier," "JCM800," "5150" are all trademarks or
   registered model names.
2. Descriptive technical references are acceptable in Field Notes and docs where needed for clarity (e.g.
   "tone stack modeled on the 5F6-A circuit," "EL84 power-amp character") — keep them technical, never
   promotional.
3. Generic effect-type words are free: chorus, flanger, phaser, tremolo, fuzz, reverb, delay, octave,
   gate, tuner, EQ.
4. **Before shipping any name, run a collision check**: search the name + "guitar pedal" / "amp" /
   "plugin". Several obvious candidates were already checked and are occupied — "Minotaur" (Movall,
   Nembrini, Line 6, Handy FX all use it), "Screech" (Joe Gore), "Tear Jerker" (PedalPCB). That is why the
   table below avoids them. Re-verify the keepers; swap anything that collides.

### 4.1 Amp names (the gain ladder)

| Real reference | In-app name | The play |
|---|---|---|
| Roland JC-120 | **CHORUS LINE** | The Jazz Chorus amp, as a line of dancers |
| Fender Twin Reverb | **GEMINI** | Twins |
| Fender Deluxe Reverb | **VELVETEEN** | Small, soft, breaks up early |
| Fender Bassman 5F6-A | **LOWMAN** | Bass man, low man |
| Vox AC30 Top Boost | **CHIMERA** | The chime, mythologized |
| Marshall 1959 Plexi | **MARCH HARE** | Marshall gone Wonderland |
| Marshall JCM800 | **ARENA** | 80s stadium rock |
| Mesa/Boogie Mark IIC+ | **WOOGIE MK.II** | You know |
| Mesa/Boogie Dual Rectifier | **FULL BRIDGE** | The rectifier topology joke — engineers will get it |
| Peavey/EVH 5150 | **SECTION 8** | Both are codes for "crazy" |

Second wave (optional, same rules): Dumble ODS → **MUMBLE**, Dumble Steel String Singer → **CROONER**,
Hiwatt DR103 → **HI-VOLT**, Soldano SLO-100 → **SLO-MO**, Marshall Silver Jubilee → **GOLDEN JUBILEE**,
Bogner Ecstasy → **RAPTURE**.

### 4.2 Pedal names

| Real reference | In-app name | The play |
|---|---|---|
| Ibanez Tube Screamer | **SHRIEKER** | Screaming, but not "Screech" (taken) |
| Boss BD-2 Blues Driver | **CHAUFFEUR** | A driver, professionally |
| Boss SD-1 Super Overdrive | **SIDEKICK** | The super pal |
| Fulltone OCD | **CDO** | OCD, alphabetized |
| Timmy | **TAMMY** | One letter of respect |
| Klon Centaur | **MYTHIC** | The creature, unnamed (Minotaur is taken by everyone) |
| Pro Co RAT | **RODENT** | The other rat word |
| Boss DS-1 | **XD-1** | Distortion, laughing |
| Boss HM-2 | **STOCKHOLM** | Swedish death, by city |
| EHX Big Muff Pi | **BIG MITT** | Keep your hands warm |
| Arbiter Fuzz Face | **FUZZ VISAGE** | The face, in the mirror |
| Sola Sound Tone Bender | **TONE TWISTER** | Bends, twists |
| Dunlop Cry Baby | **SOB STORY** | Wah = crying (Tear Jerker was taken) |
| MXR Phase 90 | **FAZE** | Homophone, free |
| Uni-Vibe | **OMNI-VIBE** | Uni, omni |
| Boss CE-2 | **CHORISTER** | Choir voice |
| EHX Electric Mistress | **THE MISSUS** | Domestic bliss |
| MXR Dyna Comp | **DINO COMP** | Dyna → Dino |
| Teletronix LA-2A | **EL-A2** | The vocal compressor named after the device this whole project resurrects |
| Urei 1176 | **1177** | One better |
| EHX Deluxe Memory Man | **REMEMBRANCER** | An actual ancient English office; remembers everything |
| Boss DM-2 | **SHORT MEMORY** | Short delay, short memory |
| Echoplex EP-3 | **ECHOCOMPLEX** | The plex, complex |
| Roland Space Echo RE-201 | **ORBIT ECHO** | Space, orbital |
| TC 2290 | **2390** | The future of the reference |
| DigiTech Whammy | **KAPOW** | The sound effect |
| EHX POG | **OCTOPOD** | Polyphonic octopus |
| Boss OC-2 | **SUBMARINE** | Sub octaves, dives |
| Dallas Rangemaster | **RANGEBOSS** | Rules its range |

Generic modules need no names: TUNER, GATE, EQ TEN, TREM, SPRING, PLATE, HALL.

## 5. The signal chain (the architecture)

```
GUITAR → TUNER → GATE → COMP → WAH → DRIVE → AMP → CAB → MOD → DELAY → REVERB → OUT
VOCAL  →            COMP → EQ →                     MOD → DELAY → REVERB → OUT
```

- Pre-amp pedals (comp, wah, drives) feed the amp input; modulation sits after the cab; delay and reverb
  last. This is the industry-standard order and must be the chain's fixed topology.
- Vocals get their own branch: compressor → EQ → delay/reverb, sharing the mod/time engines but never the
  drive/amp path.
- The on-screen chain in earlier canvases already implies this routing — v5 makes each link a real audio
  node.

## 6. The canon (the complete ingredient list)

### 6.1 Amps — the gain ladder

One AMP module, one gain axis walking ten reference amps. This is the "glassy clean through total
distortion" range:

| Rung | Real reference | In-app name | Character |
|---|---|---|---|
| 0 | Roland JC-120 | CHORUS LINE | Solid-state pristine, built-in chorus |
| 0 | Fender Twin Reverb | GEMINI | Huge headroom, the clean standard, spring reverb |
| 1 | Fender Deluxe Reverb | VELVETEEN | Early breakup, studio workhorse |
| 1–2 | Vox AC30 Top Boost | CHIMERA | EL84 chime into bite |
| 2 | Fender Bassman 5F6-A | LOWMAN | Warm blues crunch |
| 3 | Marshall 1959 Plexi | MARCH HARE | Classic rock |
| 4 | Marshall JCM800 | ARENA | Hard rock / classic high gain |
| 5 | Mesa Mark IIC+ | WOOGIE MK.II | Cascaded-gain 80s metal |
| 6 | Dual Rectifier | FULL BRIDGE | Modern rock/nu-metal |
| 7 | Peavey 5150 | SECTION 8 | The high-gain benchmark |

Amps are DSP models, not samples: cascaded gain stages with nonlinear transfer curves, a tone stack
(Fender/Marshall-style biquad networks), and power-amp compression/sag character per rung.

### 6.2 Drives

| Real reference | In-app name | Circuit DNA to model |
|---|---|---|
| Tube Screamer | SHRIEKER | Symmetrical soft clipping in the feedback loop, ~1 kHz mid hump, bass rolled off before clipping |
| BD-2 | CHAUFFEUR | Asymmetric clipping, dynamic, touch-sensitive |
| SD-1 | SIDEKICK | Asymmetric TS variant |
| OCD | CDO | Hard/soft clip switching |
| Timmy | TAMMY | Transparent drive, clipping to ground |
| Klon | MYTHIC | Drive with clean blend under the clipped path |
| RAT | RODENT | Hard clipping to ground, low-pass Filter knob that works backwards (more = darker) |
| DS-1 | XD-1 | Hard clip, scooped mids |
| HM-2 | STOCKHOLM | Full bass/treble boost, no mids — the Swedish chainsaw |
| Big Muff | BIG MITT | Two cascaded clipping stages, mid-scooped tone stack, huge sustain |
| Fuzz Face | FUZZ VISAGE | Two-transistor fuzz, interactive with input level (cleans up when guitar volume drops) |
| Tone Bender | TONE TWISTER | Fuzz Face cousin, thicker |
| Octavia | OCTAVIUS | Fuzz + ring-mod octave-up |

### 6.3 Modulation (post-cab)

| Effect | Model |
|---|---|
| Phaser | 4-stage all-pass sweep (Phase 90 DNA), one speed knob |
| Uni-Vibe-style | OMNI-VIBE — lamp/LDR character, slower, vocal, not a plain phaser |
| Chorus | CHORISTER — modulated delay line, subtle warble |
| Flanger | THE MISSUS — short modulated delay + feedback |
| Tremolo | TREM — amplitude LFO; two flavors (optical and bias-vary asymmetric) |
| Octave | SUBMARINE (monophonic down), OCTOPOD (polyphonic up/down) |

### 6.4 Time effects

| Effect | Model |
|---|---|
| Tape delay | ECHOCOMPLEX — delay line + saturation + wow/flutter wobble |
| Analog delay | SHORT MEMORY — dark, warm repeats |
| Digital delay | 2390 — clean delay line, tone-shaped repeats |
| Spring reverb | SPRING — short, bouncy, drippy |
| Plate / hall reverb | PLATE / HALL — algorithmic; plate is the vocal default |

### 6.5 Utility

- **TUNER** — first in chain, always live, mute option.
- **GATE** — downward expander, essential at high gain.
- **COMP** — DINO COMP (OTA squash, guitar) and EL-A2 (opto curve, vocals).
- **SOB STORY** (wah) — resonant filter swept by envelope follower or LFO/pedal control.
- **EQ TEN** — 10-band graphic, also the mid-boost trick for high gain.
- **RANGEBOSS** — treble boost, the classic-boost-into-cranked-amp sound.
- **CAB** — IR-based cabinet sim (see §9).

## 7. Web Audio implementation map

- **AudioWorklet** for everything stateful or nonlinear: amp gain stages, drive circuits, fuzz
  interaction, tape wow/flutter, gate, tuner, octave. Waveshaper curves are acceptable for the simple
  diode-clip stages; the amp's cascaded stages and tone interaction need worklet code.
- **BiquadFilterNode** networks for tone stacks, wah SVF, delay tone shaping.
- **ConvolverNode** for cabinet IRs and plate/hall reverb.
- **DelayNode + LFO** for chorus/flanger/vibrato where a worklet is overkill.
- Input: `getUserMedia` with processing disabled (§2.4). Meter everything from real analyser nodes as the
  canvases already do.
- The existing synth/music-screen engine stays — the guitar rig is added alongside it, not replacing it.

## 8. Documentation pack — what to read, per module

**Honest difficulty assessment.** The plumbing and the simple effects are straightforward, well-documented
textbook work. The amp and drive modeling is where reference material separates a convincing rig from a
fizzy mess — that work has been done below. Build order recommendation: plumbing → metering/tuner/gate →
mod/time effects → drives → amps → cab. Each tier only needs its own row of the table.

### 8.1 Difficulty map — where references are actually needed

| Module | Difficulty | References needed? |
|---|---|---|
| Input plumbing, gain staging, meters | Easy | §8.2 only |
| TUNER, GATE, EQ TEN | Easy | §8.2 + YIN (§8.6) |
| COMP, WAH, chorus/flanger/phaser/trem, digital delay | Easy–medium | §8.2 + §8.3 (JOS filters, Zavalishin) |
| Tape delay wow/flutter, spring reverb | Medium | §8.3 + §8.5 (read existing implementations) |
| Drive pedals (all of §6.2) | Medium | §8.4 — **required**: Yeh's TS/DS-1 papers + ElectroSmash |
| Amp gain stages + tone stacks | Hard | §8.4 — **required**: Yeh thesis + Duncan TSC + Robinette |
| Cab IR (embedded/synthesized) | Easy–medium | §8.2 ConvolverNode + §8.4 cab modeling |

### 8.2 Platform plumbing — Web Audio, AudioWorklet, input

- **MDN Web Audio API** — the API reference and concepts:
  https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- **MDN AudioWorklet** — the custom-DSP entry point:
  https://developer.mozilla.org/en-US/docs/Web/API/AudioWorklet
- **MDN "Background audio processing using AudioWorklet"** — the practical walkthrough (processor class,
  `addModule`, parameter setup): https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Using_AudioWorklet
- **MDN AudioWorkletProcessor** — the `process()` contract, 128-frame blocks:
  https://developer.mozilla.org/en-US/docs/Web/API/AudioWorkletProcessor
- **Chrome Developers: AudioWorklet** — the original guide with diagrams:
  https://developer.chrome.com/blog/audio-worklet/
- **Chrome Developers: Audio Worklet Design Patterns** — single/multiple worklets, WASM integration,
  parameter smoothing: https://developer.chrome.com/blog/audio-worklet-design-pattern/
- **web.dev: Processing microphone audio** — getUserMedia → worklet chain with low latency:
  https://web.dev/articles/media/microphone-process
- **MDN MediaDevices.getUserMedia** — the constraint flags (echoCancellation etc.):
  https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
- **GoogleChromeLabs web-audio-samples** — runnable reference projects incl. worklet + WASM examples:
  https://github.com/GoogleChromeLabs/web-audio-samples
- Node references as needed: MDN pages for `BiquadFilterNode`, `WaveShaperNode`, `DelayNode`,
  `ConvolverNode`, `AnalyserNode` (standard MDN URLs, pattern:
  `developer.mozilla.org/en-US/docs/Web/API/<NodeName>`).

### 8.3 DSP foundations — filters, nonlinearities, time effects

- **Julius O. Smith (CCRMA Stanford), free online books** — the canonical references:
  - *Introduction to Digital Filters*: https://ccrma.stanford.edu/~jos/filters/
  - *Physical Audio Signal Processing* (delay lines, feedback loops, all the time-effect machinery):
    https://ccrma.stanford.edu/~jos/pasp/
  - *Mathematics of the DFT* / spectral methods (convolution, IRs): https://ccrma.stanford.edu/~jos/mdft/
- **Vadim Zavalishin, *The Art of VA Filter Design*** (free PDF, rev 2.1.0) — TPT/state-space filter
  design, the standard text for virtual-analog biquads (tone stacks, wah SVF, delay tone):
  https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.0.pdf — HTML
  mirror: https://github.com/isabelgk/va-filter-design
- **music-dsp source code archive** — decades of compact effect recipes: https://www.musicdsp.org/
- Books if preferred: Will Pirkle, *Designing Audio Effect Plugins in C++* (practical, per-effect
  chapters); Udo Zölzer (ed.), *DAFX: Digital Audio Effects* (academic, exhaustive).

### 8.4 Guitar circuit modeling — the amps and drives (REQUIRED reading for these modules)

- **David Yeh, *Digital Implementation of Musical Distortion Circuits by Analysis and Simulation***
  (Stanford PhD thesis, 2009) — THE reference for digitally modeling distortion pedals and tube amps;
  covers the TS and DS-1 circuits in depth:
  https://ccrma.stanford.edu/~dtyeh/papers/DavidYehThesissinglesided.pdf
- **Yeh's full publication list** (all papers below, plus slides and sound examples):
  https://ccrma.stanford.edu/~dtyeh/papers/pubs.html
- **Yeh, Abel & Smith, "Simplified, Physically-Informed Models of Distortion and Overdrive Guitar
  Effects Pedals"** (DAFx-07) — the Tube Screamer and Distortion pedal models, simplified for real-time:
  https://ccrma.stanford.edu/~dtyeh/papers/yeh07_dafx_distortion.pdf
- **Yeh, Abel & Smith, "Simulation of the Diode Limiter in Guitar Distortion Circuits"** (DAFx-07) — the
  clipping stage math used by nearly every drive pedal:
  https://ccrma.stanford.edu/~dtyeh/papers/yeh07_dafx_clipode.pdf
- **Yeh & Smith, "Simulating Guitar Distortion Circuits using Wave Digital and Nonlinear State-Space
  Formulations"** (DAFx-08) — the bright switch, diode clipper, transistor and triode amplifier stages:
  https://ccrma.stanford.edu/~dtyeh/papers/yeh08_dafx_sim.pdf
- **Yeh, "Automated Physical Modeling of Nonlinear Audio Circuits — Part II: BJT and Vacuum Tube
  Examples"** (IEEE TASLP 2012) — tube stage models:
  https://ccrma.stanford.edu/~dtyeh/papers/yeh12_taslp.pdf
- **ElectroSmash circuit analyses** — plain-language stage-by-stage breakdowns with schematics and
  transfer functions, the fastest path from circuit to DSP: Tube Screamer, Big Muff, Fuzz Face, RAT,
  Phase 90, Cry Baby, Echoplex and more, all under https://www.electrosmash.com/ (e.g.
  https://www.electrosmash.com/tube-screamer-analysis)
- **Duncan Amps Tone Stack Calculator** — free Windows tool: dial in Fender/Vox/Marshall/James/Hiwatt/Big
  Muff tone stacks and see the frequency response; use it to extract the biquad targets for each amp's
  tone stack: https://www.duncanamps.com/tsc/
- **Rob Robinette, "How The TMB Tone Stack Works"** — the 5F6-A/blackface tone stack explained with TSC
  graphs: https://robrobinette.com/How_The_TMB_Tone_Stack_Works.htm ; also his amp voicing page:
  https://robrobinette.com/Voicing_an_Amp.htm
- **Open-source implementations to read** (license-check before copying code; reading for technique is
  always fine):
  - **Guitarix** (GPL) — Linux amp sim, tube preamp models, full effects set:
    https://sourceforge.net/projects/guitarix/
  - **Chowdhury-DSP BYOD** (GPL-3) — modular circuit-modeled pedals in JUCE:
    https://github.com/Chowdhury-DSP/BYOD ; their WDF library:
    https://github.com/Chowdhury-DSP/chowdsp_wdf ; and the tape model (wow/flutter for ECHOCOMPLEX):
    https://github.com/Chowdhury-DSP/AnalogTapeModel
  - **Airwindows** (permissive) — ~200 compact DSP algorithms, ideal for utility effects:
    https://github.com/airwindows/airwindows

### 8.5 Existing web guitar implementations — proof and patterns

- **"Real time tube guitar amplifier simulation using WebAudio"** (a JCM800 model in the browser — paper
  with implementation approach): https://univ-cotedazur.hal.science/hal-01589229/document
- **Web Audio Modules (WAM) 2.0** — open plugin standard; their ecosystem includes a working **guitar
  pedalboard host with pedal and tube-amp plugins**: https://www.webaudiomodules.org/ and
  https://github.com/webaudiomodules ; the guitar-rack paper: https://inria.hal.science/hal-03812948/document
- **Chris Wilson's Input Effects demo and Pedalboard.js** — the original Web Audio guitar input chains
  (delay, distortion, wah): https://github.com/cwilso/Pedalboard.js
- **The Faust shortcut** — write effects in the Faust DSL (its libraries already implement phasers,
  choruses, delays, reverbs) and compile straight to an AudioWorklet/WebAssembly module:
  https://faust.grame.fr/ — libraries: https://faustlibraries.grame.fr/ — docs: https://faustdoc.grame.fr/

### 8.6 Tuner reference

- **YIN algorithm** — de Cheveigné & Kawahara, "YIN, a fundamental frequency estimator for speech and
  music," *Journal of the Acoustical Society of America*, 2002 — the standard robust pitch-detection
  method (autocorrelation with harmonic-error correction); search the title for free PDFs.
- **Chris Wilson's PitchDetector** — the classic JavaScript autocorrelation pitch detector built on Web
  Audio, the usual starting point: https://github.com/cwilso/pitchdetector

## 9. Cabinets without network calls

The repo rule is absolute: no external requests, one file, offline. Cabinet IRs therefore must be either
(a) tiny data-URI WAVs embedded in the file, or (b) procedurally synthesized cab responses (comb
filtering + low-pass + speaker character — a 1x12 vs 4x12 can be convincingly sketched this way). Choose
one, keep the cab module an IR loader in architecture (so real IR WAVs can be loaded by the user later
via file input), and document the choice in Field Notes.

## 10. Repo copy when v5 lands

The roadmap and README already link this brief and record the guitar-first shift. What remains is the
registration copy when the v5 canvas ships: apply the drafted rows in Appendix B, keep statuses honest
per the repo's own style, and never touch `v1/`–`v4/` or their history.

## 11. Addition checklist

- [ ] `v5/index.html` — new canvas, guitar/vocal rig edition
- [ ] Real input path: getUserMedia, processing flags off, input trim, level meter, clip indicator,
      feedback warning (headphone note from roadmap M3)
- [ ] AMP mode: gain ladder (10 rungs, §4.1 names), tone stack, presence, master
- [ ] DRIVE mode: pedal board of §6.2 circuits, gain/tone/level each, §4.2 names
- [ ] MOD mode: §6.3 effects, one at a time per chain slot
- [ ] TIME mode: §6.4 delay + reverb engines
- [ ] CAB mode: IR loader + cab selection
- [ ] Front-of-chain mode: TUNER, GATE, COMP, SOB STORY, EQ TEN, RANGEBOSS
- [ ] Vocal chain branch: EL-A2 → EQ → delay/reverb
- [ ] Factory presets: at least one landmark tone per amp rung (glassy, edge, crunch, classic rock,
      hard rock, metal)
- [ ] Mode map settled — the 24-mode / 3-page ceiling must absorb the rig; merge or retire existing
      modes rather than exceeding the panel's capacity
- [ ] RANK feasibility percentages updated for A2 and PC targets (v3 feature, keep honest)
- [ ] Field Notes written for v5's actual changes (start from Appendix A, adjust to what shipped)
- [ ] Repo copy updates per §10 and Appendix B
- [ ] Registered in `versions/index.html` + README table, `assets/preview-v5.png` (1200×630), frozen
      after push

## 12. Explicitly out of scope for v5

- The production port: no APK, no native audio code, no shell (Tauri/Electron) work — that stays in
  roadmap M1/M2.
- Neural/capture/ML anything.
- A2 hardware feasibility decisions or limitations-based design cuts.
- Editing v1–v4 for any reason.
- Accounts, cloud sync, telemetry, any network dependency.
- Assuming v5 is the last canvas — the version count after v5 is undecided; leave clean seams.

## 13. Definition of done

A guitar (or vocal mic) signal from any interface, entering the v5 canvas in a browser, produces: a
tuned, gated, driven, amplified, cab-simmed, modulated, time-effected signal at the output — with at
least one factory preset per amp rung that a guitarist would recognize as "glassy clean," "Plexi
crunch," or "modern gain" — and the file still passes the repo rules: one HTML file, zero network calls,
runs from the local filesystem, frozen and registered after push, with the README and roadmap honestly
reflecting the new direction.

---

## Appendix A — Field Notes draft for v5

Draft in the house style (matches the v4 `NOTES_HTML` format). Adjust every line to match what actually
shipped — a Field Note that describes an unbuilt feature is worse than none.

```html
<h2>FIELD NOTES // V5 — THE RIG</h2>
<h3>WHAT THIS IS</h3>
<p>The sound chain stops being a picture. Any line-level source — interface, headset input, iRig — comes in through a trim, a meter and a clip light, and leaves through ten amps, the classic pedalboard, an IR cab and the mod and time engines. No neural anything: every amp and pedal is hand-written DSP on the circuit that made it famous. The scope, the names and every reference live in docs/V5-BRIEF.md.</p>
<h3>THE GAIN LADDER</h3>
<p>One AMP module, one axis: CHORUS LINE and GEMINI for glassy clean, VELVETEEN, CHIMERA and LOWMAN for edge and crunch, MARCH HARE and ARENA for classic drive, WOOGIE MK.II, FULL BRIDGE and SECTION 8 for total destruction. Tone stacks are modeled per circuit, not one generic EQ.</p>
<h3>THE PEDALBOARD</h3>
<table>
<tr><th>PEDAL</th><th>WHAT IT DOES</th></tr>
<tr><td>SHRIEKER</td><td>Mid-hump overdrive — the one every other drive is described against.</td></tr>
<tr><td>CHAUFFEUR</td><td>Touch-sensitive asymmetric drive, dynamic like a tube.</td></tr>
<tr><td>RODENT</td><td>Hard clipping with a filter knob that runs backwards.</td></tr>
<tr><td>BIG MITT</td><td>Two clipping stages, scooped mids, sustain that does not stop.</td></tr>
<tr><td>FUZZ VISAGE</td><td>Two-transistor fuzz that cleans up when the guitar volume drops.</td></tr>
<tr><td>MYTHIC</td><td>Transparent drive with the clean signal blended underneath.</td></tr>
</table>
<p>Plus SOB STORY (wah), FAZE (phaser), OMNI-VIBE, CHORISTER, THE MISSUS, TREM, SUBMARINE and OCTOPOD — the classic modulation set, each modeled on its circuit.</p>
<h3>TIME AND SPACE</h3>
<p>ECHOCOMPLEX (tape, with wow and flutter), SHORT MEMORY (analog-dark repeats), 2390 (digital), SPRING, PLATE and HALL. The vocal channel gets its own path: EL-A2 compression into EQ into plate.</p>
<h3>NAMES</h3>
<p>Every model name is a play on the original, never the original: homage without infringement. The rule and the full list live in the brief.</p>
```

## Appendix B — copy to apply when v5 lands

Applied at registration time, per CONTRIBUTING rules. Nothing here is applied by this brief.

**README.md — Live canvases table** (v5 becomes latest, v4 stable, v3 archive):

```markdown
| **v5** | latest | Guitar/vocal rig canvas: the sound chain becomes real DSP — ten-amp gain ladder, classic pedalboard, IR cabs, mod/time engines, vocal channel. Scope: [docs/V5-BRIEF.md](docs/V5-BRIEF.md). | [open v5](https://bortknox.github.io/Cowon-a2-transformation-demo/v5/) |
```

Update the v4 row's State from `latest` to `stable` and the v3 row's from `stable` to `archive` in the
same pass.

**versions/index.html** — new card above the v4 card, tags demoted the same way:

```html
<a class="c" href="../v5/"><b>V5<span class="tag">LATEST</span></b><span>Guitar/vocal rig: the sound chain becomes real DSP. Ten amps on one gain ladder, the classic pedalboard, IR cabs, mod and time engines.</span></a>
```

**docs/ROADMAP.md** — tick the v5 checkbox under M0.

**README hero** — point `assets/preview-v4.png` at `assets/preview-v5.png` only when v5 becomes the
showcase.

---

*Naming collision spot-checks performed: Minotaur (occupied — Movall/Nembrini/Line 6/Handy FX), Screech
(occupied — Joe Gore), Tear Jerker (occupied — PedalPCB); FULL BRIDGE, REMEMBRANCER, CHORISTER returned no
guitar-product collisions in first-pass checks. Re-verify before public release.*

*All §8 links verified live as of the date of this brief. If a link has died, search the exact title in
quotes — every item is a canonical, widely mirrored reference.*
