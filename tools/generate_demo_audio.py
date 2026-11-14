#!/usr/bin/env python3
"""Generate three original, loopable Cowon A2 demo cues (standard library only)."""
from array import array
from math import exp, pi, sin
from pathlib import Path
import random
import wave

OUT = Path(__file__).resolve().parents[1] / "assets" / "audio"
RATE = 22050

TRACKS = [
    {"title": "SIGNAL PATH", "bpm": 112, "root": 48, "style": 0},
    {"title": "TANGERINE CIRCUIT", "bpm": 104, "root": 53, "style": 1},
    {"title": "NIGHT DRIVE", "bpm": 120, "root": 45, "style": 2},
]

def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)

def render(track):
    rng = random.Random(4100 + track["style"])
    beat = 60.0 / track["bpm"]
    duration = 32 * beat  # eight bars, cleanly loopable
    count = int(duration * RATE)
    mix = array("f", [0.0]) * count

    def add(start, length, fn, gain):
        first = max(0, int(start * RATE))
        end = min(count, int((start + length) * RATE))
        for i in range(first, end):
            t = i / RATE - start
            mix[i] += fn(t) * gain

    # A compact chord loop; every cue has its own harmonic colour.
    chord_offsets = [(0, 3, 7, 10), (5, 8, 12, 15), (3, 7, 10, 14), (7, 10, 14, 17)]
    if track["style"] == 1:
        chord_offsets = [(0, 4, 7, 11), (5, 9, 12, 16), (2, 5, 9, 12), (7, 11, 14, 17)]
    if track["style"] == 2:
        chord_offsets = [(0, 3, 7, 10), (8, 12, 15, 19), (5, 8, 12, 15), (10, 14, 17, 21)]
    scale = [0, 3, 5, 7, 10, 12, 15, 17]
    if track["style"] == 1:
        scale = [0, 2, 4, 7, 9, 12, 14, 16]
    if track["style"] == 2:
        scale = [0, 3, 5, 7, 10, 12, 15, 17]

    for bar in range(8):
        chord = chord_offsets[bar % len(chord_offsets)]
        t0 = bar * beat * 4
        # Soft analogue-style chord bed, slowly beating sine partials.
        for tone in chord:
            f = midi(track["root"] + 48 + tone)
            def pad(t, f=f, bar=bar):
                env = min(1.0, t / .18) * min(1.0, (beat * 4 - t) / .24)
                return env * (sin(2*pi*f*t) + .25*sin(2*pi*f*1.003*t) + .15*sin(2*pi*f*2*t))
            add(t0, beat * 4, pad, .035)
        for step in range(8):
            st = t0 + step * beat / 2
            note = track["root"] + 36 + scale[(step + bar * 2 + track["style"]) % len(scale)]
            f = midi(note)
            def pluck(t, f=f, style=track["style"]):
                env = exp(-t * (5.5 if style == 2 else 8.5))
                return env * (sin(2*pi*f*t) + .34*sin(2*pi*f*2*t) + .12*sin(2*pi*f*3*t))
            add(st, beat * .48, pluck, .12)
        for step in range(4):
            st = t0 + step * beat
            bass_note = track["root"] + chord[step % len(chord)]
            f = midi(bass_note)
            def bass(t, f=f):
                env = exp(-t * 4.2)
                sweep = f * (1 + .018 * exp(-t * 22))
                return env * (sin(2*pi*sweep*t) + .18*sin(2*pi*sweep*2*t))
            add(st, beat * .82, bass, .18)
            # Alternating kick and dry clap/snare.
            if step in (0, 2):
                def kick(t):
                    f = 78 - 35 * min(1, t / .11)
                    return exp(-t*10) * sin(2*pi*f*t)
                add(st, .22, kick, .34)
            else:
                noise = [rng.uniform(-1, 1) for _ in range(int(.13 * RATE))]
                def snare(t, noise=noise):
                    i = min(len(noise)-1, int(t*RATE))
                    return noise[i] * exp(-t*26) + .15*sin(2*pi*185*t)*exp(-t*22)
                add(st, .13, snare, .11)
        for step in range(8):
            st = t0 + step * beat / 2
            noise = [rng.uniform(-1, 1) for _ in range(int(.035 * RATE))]
            def hat(t, noise=noise):
                i = min(len(noise)-1, int(t*RATE))
                return noise[i] * exp(-t*90)
            add(st, .035, hat, .035 if step % 2 else .05)

    # Gentle edge fades make the eight-bar loop pop-free.
    fade = int(RATE * .045)
    peak = max(abs(v) for v in mix) or 1.0
    scale_out = .78 / peak
    pcm = array("h")
    for i, sample in enumerate(mix):
        edge = min(1.0, i / fade, (count - 1 - i) / fade)
        value = max(-1.0, min(1.0, sample * scale_out * edge))
        pcm.append(int(value * 32767))
    return pcm, duration

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for index, track in enumerate(TRACKS, 1):
        pcm, duration = render(track)
        path = OUT / f"track-{index:02d}.wav"
        with wave.open(str(path), "wb") as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(RATE)
            file.writeframes(pcm.tobytes())
        print(f"{path.name}: {track['title']} / {duration:.1f}s / {path.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
