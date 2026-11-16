# A2 Video Forge

A small Windows GUI that watches a folder and transcodes any video dropped into it into something the
**COWON iAUDIO A2** will actually play: an AVI containing **XviD video at 480×272** and **MP3 stereo** audio —
the A2's native LCD resolution.

This is the companion tool to the [TE Bench canvases](../../README.md): the canvases imagine the A2's future,
this keeps the real device useful today.

## What it does

Drop videos into the inbox folder. A2 Video Forge waits until a file stops changing, then converts it and
writes the result into the output folder. Originals are preserved by default; conversion happens once, on the
PC, so the player never has to scale video in real time.

- Watches one folder (not subfolders), one job at a time, so it behaves on an old PC.
- Existing outputs are skipped unless **Overwrite existing output** is enabled.
- **Delete source after successful conversion** is off by default.
- The queue lives in memory: files still in the inbox are picked up again next launch.

Default folders:

- `%USERPROFILE%\Videos\A2_INBOX`
- `%USERPROFILE%\Videos\A2_READY`

## Requirements

- Windows 10 or 11
- Python 3.10+ (`Add Python to PATH` during install)
- FFmpeg built with `libxvid` and `libmp3lame`

No pip packages. The GUI is Tkinter, which ships with standard Windows Python.

## Install

1. Install Python: <https://www.python.org/downloads/windows/>
2. Install FFmpeg (for example the *release essentials* build from <https://www.gyan.dev/ffmpeg/builds/>),
   extract somewhere permanent such as `C:\Tools\ffmpeg` — the binary ends up at
   `C:\Tools\ffmpeg\bin\ffmpeg.exe`.
3. Download the [v1.0.0 Windows ZIP](https://github.com/BortKnox/Cowon-a2-transformation-demo/releases/download/a2vf-v1.0.0/a2-video-forge-1.0.0-windows.zip)
   and extract it to a permanent folder, e.g. `C:\Tools\A2VideoForge`.
4. Double-click `Run_A2_Video_Forge.bat`.
5. If FFmpeg is not detected automatically, click **LOCATE** and point it at `ffmpeg.exe`.

You can also run it straight from this folder: `python a2_video_forge.py` (console visible) or
`pythonw a2_video_forge.pyw` (no console).

## Everyday use

1. Open A2 Video Forge.
2. Click **OPEN DROP ZONE**.
3. Put video files in that folder.
4. Leave it running.
5. Converted AVIs appear in the output folder.

## Encoding defaults

| Setting | Value |
|---|---|
| Container | AVI |
| Video | XviD (`libxvid`), 480×272, YUV420P, 24 fps, 1000 kbps target, no B-frames |
| Audio | MP3 stereo, 44.1 kHz, 160 kbps |
| Fit | aspect-preserving letterbox/pillarbox (`pad`) |

These are conservative starting points, **not** a guarantee for every A2 firmware revision. Encode one short
representative file and confirm it plays on the actual player before converting a whole library.

### Fit modes

- `pad` — keeps the whole picture and adds black bars. Recommended default.
- `crop` — fills 480×272 but trims edges when the aspect ratio differs.
- `stretch` — fills the LCD exactly, can distort.

## Troubleshooting

| Symptom | Fix |
|---|---|
| FFmpeg not found | Use **LOCATE** to select `ffmpeg.exe`; keep FFmpeg in a permanent folder |
| `Unknown encoder 'libxvid'` / `'libmp3lame'` | Install an FFmpeg build that includes both encoders |
| A video is not detected | Check the extension is supported, that the file sits directly in the inbox, then **SCAN INBOX NOW** |
| Playback problems | Try 480×272, 24 fps, 800–1000 kbps video, 128–160 kbps MP3, `pad` fit |

Some sources carry unusual timestamps, variable frame rates, damaged streams or audio formats that need extra
handling; those are source problems, not A2 problems.

## Files

- `a2_video_forge.pyw` — GUI application, no console window.
- `a2_video_forge.py` — the same application source, for terminal use and troubleshooting.
- `Run_A2_Video_Forge.bat` — double-click launcher.
- `README.md` — this guide.

The `.py` and `.pyw` files are identical by design (Windows decides whether to open a console from the
extension). If you change one, change both.

## License

MIT — see [LICENSE](../../LICENSE).
