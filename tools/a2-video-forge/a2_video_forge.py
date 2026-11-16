#!/usr/bin/env python3
"""
A2 Video Forge
A Windows folder-watching GUI transcoder for the Cowon iAUDIO A2.

Requires:
  - Python 3.10+
  - FFmpeg (ffmpeg.exe) with libxvid and libmp3lame encoders
  - Tkinter (included with standard Windows Python installations)

The application converts source video to 480x272 XviD AVI so the Cowon A2
receives frames at its native LCD resolution. Source resizing, when needed,
happens once during transcoding rather than during playback.
"""

from __future__ import annotations

import json
import os
import queue
import shutil
import subprocess
import threading
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from tkinter import (
    Tk, StringVar, BooleanVar, IntVar, filedialog, messagebox, ttk,
    Listbox, END, BOTH, LEFT, RIGHT, X, Y, W, E, N, S
)
from tkinter.scrolledtext import ScrolledText


APP_NAME = "A2 Video Forge"
APP_VERSION = "1.0.0"
SUPPORTED_EXTENSIONS = {
    ".mkv", ".mp4", ".m4v", ".mov", ".avi", ".wmv", ".asf",
    ".webm", ".mpg", ".mpeg", ".ts", ".m2ts", ".mts", ".vob"
}
DEFAULT_CONFIG = {
    "input_dir": str(Path.home() / "Videos" / "A2_INBOX"),
    "output_dir": str(Path.home() / "Videos" / "A2_READY"),
    "ffmpeg_path": "",
    "video_bitrate": "1000k",
    "audio_bitrate": "160k",
    "fps": "24",
    "fit_mode": "pad",
    "watch_enabled": True,
    "delete_source": False,
    "overwrite": False,
    "stable_seconds": 3,
    "poll_seconds": 3,
}

BG = "#171A1C"
PANEL = "#222729"
PANEL2 = "#292F31"
FG = "#F1EEE6"
MUTED = "#A4AAA7"
ACCENT = "#F07835"
GREEN = "#8DBB83"
RED = "#E16B63"
BORDER = "#41494B"
FONT = ("Consolas", 9)
FONT_BOLD = ("Consolas", 10, "bold")


@dataclass
class Job:
    source: Path
    output: Path


class ForgeApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title(f"{APP_NAME}  //  FIELD OS")
        self.root.geometry("920x720")
        self.root.minsize(780, 620)
        self.root.configure(bg=BG)

        self.config_path = Path(os.environ.get("APPDATA", str(Path.home()))) / "A2VideoForge" / "settings.json"
        self.config = self.load_config()

        self.events: queue.Queue = queue.Queue()
        self.jobs: queue.Queue[Job | None] = queue.Queue()
        self.queued_sources: set[str] = set()
        self.completed_sources: set[str] = set()
        self.stability: dict[str, tuple[int, int]] = {}
        self.worker_running = True
        self.watching = False
        self.processing = False
        self.current_process: subprocess.Popen | None = None
        self.stop_requested = False
        self.total_added = 0
        self.total_done = 0
        self.total_failed = 0

        self.input_var = StringVar(value=self.config["input_dir"])
        self.output_var = StringVar(value=self.config["output_dir"])
        self.ffmpeg_var = StringVar(value=self.config.get("ffmpeg_path", ""))
        self.video_bitrate_var = StringVar(value=self.config["video_bitrate"])
        self.audio_bitrate_var = StringVar(value=self.config["audio_bitrate"])
        self.fps_var = StringVar(value=self.config["fps"])
        self.fit_var = StringVar(value=self.config["fit_mode"])
        self.watch_var = BooleanVar(value=self.config["watch_enabled"])
        self.delete_var = BooleanVar(value=self.config["delete_source"])
        self.overwrite_var = BooleanVar(value=self.config["overwrite"])
        self.status_var = StringVar(value="INITIALISING")
        self.progress_var = IntVar(value=0)
        self.now_var = StringVar(value="Waiting for files")
        self.count_var = StringVar(value="0 QUEUED  /  0 DONE  /  0 FAILED")

        self.setup_style()
        self.build_ui()
        self.ensure_folders()
        self.detect_ffmpeg()
        self.worker = threading.Thread(target=self.worker_loop, daemon=True)
        self.worker.start()

        if self.watch_var.get():
            self.start_watching()
        self.root.after(250, self.process_events)
        self.root.after(1500, self.poll_inbox)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_config(self):
        cfg = DEFAULT_CONFIG.copy()
        try:
            if self.config_path.exists():
                cfg.update(json.loads(self.config_path.read_text(encoding="utf-8")))
        except Exception:
            pass
        return cfg

    def save_config(self):
        self.config.update({
            "input_dir": self.input_var.get().strip(),
            "output_dir": self.output_var.get().strip(),
            "ffmpeg_path": self.ffmpeg_var.get().strip(),
            "video_bitrate": self.video_bitrate_var.get().strip(),
            "audio_bitrate": self.audio_bitrate_var.get().strip(),
            "fps": self.fps_var.get().strip(),
            "fit_mode": self.fit_var.get(),
            "watch_enabled": self.watch_var.get(),
            "delete_source": self.delete_var.get(),
            "overwrite": self.overwrite_var.get(),
        })
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(json.dumps(self.config, indent=2), encoding="utf-8")
        except Exception as exc:
            self.log(f"Could not save settings: {exc}", "WARN")

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(".", background=BG, foreground=FG, font=FONT)
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=FG, font=FONT)
        style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=FONT)
        style.configure("Panel.TLabel", background=PANEL, foreground=FG, font=FONT)
        style.configure("Header.TLabel", background=BG, foreground=FG, font=("Consolas", 17, "bold"))
        style.configure("Accent.TLabel", background=BG, foreground=ACCENT, font=FONT_BOLD)
        style.configure("TButton", background=PANEL2, foreground=FG, borderwidth=0, padding=(12, 8), font=FONT_BOLD)
        style.map("TButton", background=[("active", ACCENT), ("disabled", PANEL)])
        style.configure("Accent.TButton", background=ACCENT, foreground="#171A1C")
        style.map("Accent.TButton", background=[("active", "#FF9458")])
        style.configure("TEntry", fieldbackground=PANEL2, foreground=FG, insertcolor=FG, bordercolor=BORDER, padding=6)
        style.configure("TCombobox", fieldbackground=PANEL2, foreground=FG, background=PANEL2, arrowcolor=ACCENT)
        style.map("TCombobox", fieldbackground=[("readonly", PANEL2)], foreground=[("readonly", FG)])
        style.configure("TCheckbutton", background=BG, foreground=FG)
        style.map("TCheckbutton", background=[("active", BG)])
        style.configure("Horizontal.TProgressbar", troughcolor=PANEL2, background=ACCENT, bordercolor=PANEL2, lightcolor=ACCENT, darkcolor=ACCENT)
        style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=FG, rowheight=25, borderwidth=0)
        style.configure("Treeview.Heading", background=PANEL2, foreground=ACCENT, font=FONT_BOLD, relief="flat")
        style.map("Treeview", background=[("selected", "#41494B")], foreground=[("selected", FG)])

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill=BOTH, expand=True)

        top = ttk.Frame(outer)
        top.pack(fill=X)
        ttk.Label(top, text="A2 / VIDEO FORGE", style="Header.TLabel").pack(side=LEFT)
        ttk.Label(top, text=f"FIELD OS   ·   v{APP_VERSION}", style="Accent.TLabel").pack(side=RIGHT)
        ttk.Label(outer, text="COWON iAUDIO A2  //  NATIVE-RESOLUTION VIDEO PREPARATION", style="Muted.TLabel").pack(anchor=W, pady=(3, 14))

        # Folder routing
        folders = ttk.Frame(outer, style="Panel.TFrame", padding=13)
        folders.pack(fill=X, pady=(0, 12))
        ttk.Label(folders, text="01  /  FOLDER ROUTING", style="Panel.TLabel", font=FONT_BOLD).grid(row=0, column=0, columnspan=3, sticky=W, pady=(0, 9))
        ttk.Label(folders, text="DROP ZONE", style="Panel.TLabel").grid(row=1, column=0, sticky=W, padx=(0, 10), pady=4)
        ttk.Entry(folders, textvariable=self.input_var).grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Button(folders, text="BROWSE", command=self.choose_input).grid(row=1, column=2, padx=(8, 0))
        ttk.Label(folders, text="OUTPUT", style="Panel.TLabel").grid(row=2, column=0, sticky=W, padx=(0, 10), pady=4)
        ttk.Entry(folders, textvariable=self.output_var).grid(row=2, column=1, sticky="ew", pady=4)
        ttk.Button(folders, text="BROWSE", command=self.choose_output).grid(row=2, column=2, padx=(8, 0))
        folders.columnconfigure(1, weight=1)

        # Main status
        status = ttk.Frame(outer, style="Panel.TFrame", padding=13)
        status.pack(fill=X, pady=(0, 12))
        row = ttk.Frame(status, style="Panel.TFrame")
        row.pack(fill=X)
        ttk.Label(row, text="02  /  ENCODER STATUS", style="Panel.TLabel", font=FONT_BOLD).pack(side=LEFT)
        self.status_label = ttk.Label(row, textvariable=self.status_var, style="Panel.TLabel", foreground=GREEN)
        self.status_label.pack(side=RIGHT)
        ttk.Label(status, textvariable=self.now_var, style="Panel.TLabel").pack(anchor=W, pady=(10, 7))
        self.progress = ttk.Progressbar(status, variable=self.progress_var, maximum=100, mode="determinate")
        self.progress.pack(fill=X)
        ttk.Label(status, textvariable=self.count_var, style="Panel.TLabel").pack(anchor=W, pady=(8, 0))

        # Queue and log
        middle = ttk.Frame(outer)
        middle.pack(fill=BOTH, expand=True, pady=(0, 12))
        queue_panel = ttk.Frame(middle, style="Panel.TFrame", padding=10)
        queue_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 6))
        ttk.Label(queue_panel, text="03  /  JOB QUEUE", style="Panel.TLabel", font=FONT_BOLD).pack(anchor=W, pady=(0, 7))
        self.tree = ttk.Treeview(queue_panel, columns=("state", "file"), show="headings", height=9)
        self.tree.heading("state", text="STATE")
        self.tree.heading("file", text="FILE")
        self.tree.column("state", width=90, stretch=False)
        self.tree.column("file", width=300, stretch=True)
        self.tree.pack(fill=BOTH, expand=True)
        log_panel = ttk.Frame(middle, style="Panel.TFrame", padding=10)
        log_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=(6, 0))
        ttk.Label(log_panel, text="04  /  ACTIVITY LOG", style="Panel.TLabel", font=FONT_BOLD).pack(anchor=W, pady=(0, 7))
        self.log_box = ScrolledText(log_panel, height=9, bg="#151819", fg=FG, insertbackground=FG, font=("Consolas", 8), relief="flat", wrap="word")
        self.log_box.pack(fill=BOTH, expand=True)
        self.log_box.configure(state="disabled")

        # Settings
        settings = ttk.Frame(outer, style="Panel.TFrame", padding=13)
        settings.pack(fill=X, pady=(0, 12))
        ttk.Label(settings, text="05  /  ENCODING PROFILE", style="Panel.TLabel", font=FONT_BOLD).grid(row=0, column=0, columnspan=6, sticky=W, pady=(0, 9))
        ttk.Label(settings, text="VIDEO", style="Panel.TLabel").grid(row=1, column=0, sticky=W)
        ttk.Entry(settings, textvariable=self.video_bitrate_var, width=10).grid(row=1, column=1, padx=(6, 16))
        ttk.Label(settings, text="AUDIO", style="Panel.TLabel").grid(row=1, column=2, sticky=W)
        ttk.Entry(settings, textvariable=self.audio_bitrate_var, width=10).grid(row=1, column=3, padx=(6, 16))
        ttk.Label(settings, text="FPS", style="Panel.TLabel").grid(row=1, column=4, sticky=W)
        ttk.Combobox(settings, textvariable=self.fps_var, values=("23.976", "24", "25", "29.97", "30"), width=8, state="readonly").grid(row=1, column=5, padx=(6, 0))
        ttk.Label(settings, text="FIT", style="Panel.TLabel").grid(row=2, column=0, sticky=W, pady=(10, 0))
        ttk.Combobox(settings, textvariable=self.fit_var, values=("pad", "crop", "stretch"), width=10, state="readonly").grid(row=2, column=1, sticky=W, padx=(6, 16), pady=(10, 0))
        ttk.Checkbutton(settings, text="Watch inbox automatically", variable=self.watch_var, command=self.toggle_watching).grid(row=2, column=2, columnspan=2, sticky=W, pady=(10, 0))
        ttk.Checkbutton(settings, text="Overwrite existing output", variable=self.overwrite_var).grid(row=2, column=4, columnspan=2, sticky=W, pady=(10, 0))
        ttk.Checkbutton(settings, text="Delete source after successful conversion", variable=self.delete_var).grid(row=3, column=0, columnspan=4, sticky=W, pady=(8, 0))
        ttk.Label(settings, text="FFMPEG", style="Panel.TLabel").grid(row=4, column=0, sticky=W, pady=(9, 0))
        ttk.Entry(settings, textvariable=self.ffmpeg_var).grid(row=4, column=1, columnspan=4, sticky="ew", padx=(6, 6), pady=(9, 0))
        ttk.Button(settings, text="LOCATE", command=self.choose_ffmpeg).grid(row=4, column=5, pady=(9, 0))
        settings.columnconfigure(4, weight=1)

        # Controls
        controls = ttk.Frame(outer)
        controls.pack(fill=X)
        ttk.Button(controls, text="SCAN INBOX NOW", command=self.scan_now).pack(side=LEFT)
        ttk.Button(controls, text="OPEN DROP ZONE", command=lambda: self.open_folder(self.input_var.get())).pack(side=LEFT, padx=(7, 0))
        ttk.Button(controls, text="OPEN OUTPUT", command=lambda: self.open_folder(self.output_var.get())).pack(side=LEFT, padx=(7, 0))
        ttk.Button(controls, text="SAVE SETTINGS", command=self.save_settings).pack(side=RIGHT)
        ttk.Button(controls, text="EXIT", command=self.on_close).pack(side=RIGHT, padx=(0, 7))

        ttk.Label(outer, text="XVID / AVI  ·  480×272  ·  YUV420P  ·  MP3 STEREO     //     ORIGINALS ARE PRESERVED BY DEFAULT", style="Muted.TLabel").pack(anchor=W, pady=(12, 0))

    def log(self, message: str, level="INFO"):
        stamp = time.strftime("%H:%M:%S")
        self.events.put(("log", f"{stamp}  [{level}]  {message}"))

    def ensure_folders(self):
        for value in (self.input_var.get(), self.output_var.get()):
            if value.strip():
                Path(value).expanduser().mkdir(parents=True, exist_ok=True)

    def detect_ffmpeg(self):
        configured = self.ffmpeg_var.get().strip()
        found = configured if configured and Path(configured).is_file() else shutil.which("ffmpeg")
        if found:
            self.ffmpeg_var.set(str(found))
            self.status_var.set("FFMPEG READY")
            self.log(f"FFmpeg found: {found}")
        else:
            self.status_var.set("FFMPEG NOT FOUND")
            self.log("FFmpeg was not found. Install FFmpeg or use LOCATE to select ffmpeg.exe.", "WARN")

    def choose_input(self):
        path = filedialog.askdirectory(title="Choose A2 drop folder", initialdir=self.input_var.get() or str(Path.home()))
        if path:
            self.input_var.set(path)
            Path(path).mkdir(parents=True, exist_ok=True)
            self.save_settings()
            self.log(f"Drop folder set: {path}")

    def choose_output(self):
        path = filedialog.askdirectory(title="Choose converted video folder", initialdir=self.output_var.get() or str(Path.home()))
        if path:
            self.output_var.set(path)
            Path(path).mkdir(parents=True, exist_ok=True)
            self.save_settings()
            self.log(f"Output folder set: {path}")

    def choose_ffmpeg(self):
        path = filedialog.askopenfilename(title="Locate ffmpeg.exe", filetypes=[("FFmpeg executable", "ffmpeg.exe"), ("All files", "*.*")])
        if path:
            self.ffmpeg_var.set(path)
            self.save_settings()
            self.detect_ffmpeg()

    def save_settings(self):
        try:
            self.ensure_folders()
            self.save_config()
            self.log("Settings saved.")
            self.status_var.set("SETTINGS SAVED")
        except Exception as exc:
            messagebox.showerror(APP_NAME, str(exc))

    def toggle_watching(self):
        if self.watch_var.get():
            self.start_watching()
        else:
            self.watching = False
            self.status_var.set("WATCHER PAUSED")
            self.log("Automatic folder monitoring paused.")
        self.save_config()

    def start_watching(self):
        self.ensure_folders()
        self.watching = True
        self.status_var.set("WATCHING INBOX")
        self.log(f"Watching: {self.input_var.get()}")

    def scan_now(self):
        self.scan_inbox(force=True)

    def scan_inbox(self, force=False):
        folder = Path(self.input_var.get()).expanduser()
        if not folder.is_dir():
            self.log(f"Drop folder does not exist: {folder}", "WARN")
            return
        try:
            candidates = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)
        except OSError as exc:
            self.log(f"Could not scan inbox: {exc}", "ERROR")
            return

        for path in candidates:
            key = str(path.resolve()).lower()
            if key in self.queued_sources or key in self.completed_sources:
                continue
            if path.name.startswith("~") or path.name.endswith((".part", ".tmp", ".download", ".crdownload")):
                continue
            try:
                size = path.stat().st_size
                previous = self.stability.get(key)
                now = time.monotonic()
                if force:
                    stable = True
                elif previous and previous[0] == size and now - previous[1] >= self.config.get("stable_seconds", 3):
                    stable = True
                else:
                    self.stability[key] = (size, int(now))
                    stable = False
                if not stable:
                    continue
                output = Path(self.output_var.get()).expanduser() / f"{path.stem}_A2.avi"
                if output.exists() and not self.overwrite_var.get():
                    self.completed_sources.add(key)
                    self.log(f"Skipped existing output: {output.name}")
                    continue
                self.queued_sources.add(key)
                self.total_added += 1
                self.jobs.put(Job(path, output))
                self.events.put(("queue_add", (key, path.name)))
                self.log(f"Queued: {path.name}")
            except OSError as exc:
                self.log(f"Cannot inspect {path.name}: {exc}", "WARN")
        self.update_counts()

    def poll_inbox(self):
        if self.watching:
            self.scan_inbox()
        self.root.after(max(1, int(self.config.get("poll_seconds", 3))) * 1000, self.poll_inbox)

    def make_filter(self, fit_mode):
        if fit_mode == "crop":
            return "scale=480:272:force_original_aspect_ratio=increase:flags=lanczos,crop=480:272,setsar=1"
        if fit_mode == "stretch":
            return "scale=480:272:flags=lanczos,setsar=1"
        return "scale=480:272:force_original_aspect_ratio=decrease:flags=lanczos,pad=480:272:(ow-iw)/2:(oh-ih)/2:black,setsar=1"

    def build_command(self, job: Job, temp_output: Path):
        ffmpeg = self.ffmpeg_var.get().strip() or shutil.which("ffmpeg")
        if not ffmpeg:
            raise RuntimeError("FFmpeg executable is not configured.")
        fps = self.fps_var.get().strip()
        vb = self.video_bitrate_var.get().strip()
        ab = self.audio_bitrate_var.get().strip()
        if not vb or not ab:
            raise ValueError("Video and audio bitrates cannot be empty.")
        cmd = [
            ffmpeg, "-hide_banner", "-nostdin", "-y",
            "-i", str(job.source),
            "-map", "0:v:0", "-map", "0:a:0?",
            "-sn", "-dn",
            "-vf", self.make_filter(self.fit_var.get()),
            "-c:v", "libxvid",
            "-vtag", "XVID",
            "-pix_fmt", "yuv420p",
            "-b:v", vb,
            "-maxrate", "1500k",
            "-bufsize", "2000k",
            "-r", fps,
            "-fps_mode", "cfr",
            "-bf", "0",
            "-g", "240",
            "-c:a", "libmp3lame",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", ab,
            "-map_metadata", "-1",
            "-f", "avi",
            str(temp_output),
        ]
        return cmd

    def worker_loop(self):
        while self.worker_running:
            job = self.jobs.get()
            if job is None:
                break
            self.processing = True
            key = str(job.source.resolve()).lower()
            temp_output = job.output.with_name(job.output.stem + ".working.avi")
            try:
                if job.output.exists() and not self.overwrite_var.get():
                    self.events.put(("job_done", (key, job.source.name, "SKIPPED")))
                    continue
                self.events.put(("job_start", (key, job.source.name)))
                if temp_output.exists():
                    temp_output.unlink()
                cmd = self.build_command(job, temp_output)
                self.log(f"Encoding: {job.source.name}")
                self.log("Output target: 480x272 XviD AVI")
                creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
                self.current_process = subprocess.Popen(
                    cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                    text=True, encoding="utf-8", errors="replace",
                    creationflags=creationflags
                )
                stderr_lines = []
                # Read FFmpeg diagnostics without blocking the GUI thread.
                while True:
                    line = self.current_process.stderr.readline()
                    if line:
                        stderr_lines.append(line.rstrip())
                        if len(stderr_lines) > 30:
                            stderr_lines.pop(0)
                        if "frame=" in line or "time=" in line:
                            self.events.put(("ffmpeg_progress", line.strip()))
                    if not line and self.current_process.poll() is not None:
                        break
                    if self.stop_requested:
                        self.current_process.terminate()
                        raise RuntimeError("Conversion cancelled by user.")
                return_code = self.current_process.wait()
                self.current_process = None
                if return_code != 0:
                    raise RuntimeError("\n".join(stderr_lines[-12:]) or f"FFmpeg exited with code {return_code}")
                if not temp_output.exists() or temp_output.stat().st_size < 1024:
                    raise RuntimeError("FFmpeg did not produce a valid output file.")
                if job.output.exists():
                    job.output.unlink()
                temp_output.replace(job.output)
                if self.delete_var.get():
                    try:
                        job.source.unlink()
                    except OSError as exc:
                        self.log(f"Converted, but could not delete source: {exc}", "WARN")
                self.events.put(("job_done", (key, job.source.name, "DONE")))
                self.log(f"Completed: {job.output.name}", "DONE")
            except Exception as exc:
                self.current_process = None
                try:
                    if temp_output.exists():
                        temp_output.unlink()
                except OSError:
                    pass
                self.events.put(("job_done", (key, job.source.name, "FAILED")))
                self.log(f"Failed {job.source.name}: {exc}", "ERROR")
            finally:
                self.processing = False
                self.stop_requested = False
                self.jobs.task_done()

    def process_events(self):
        try:
            while True:
                event, payload = self.events.get_nowait()
                if event == "log":
                    self.log_box.configure(state="normal")
                    self.log_box.insert(END, payload + "\n")
                    self.log_box.see(END)
                    self.log_box.configure(state="disabled")
                elif event == "queue_add":
                    key, name = payload
                    self.tree.insert("", END, iid=key, values=("QUEUED", name))
                elif event == "job_start":
                    key, name = payload
                    if self.tree.exists(key):
                        self.tree.item(key, values=("ENCODING", name))
                    self.now_var.set(f"ENCODING  //  {name}")
                    self.progress_var.set(0)
                    self.status_var.set("ENCODING")
                elif event == "ffmpeg_progress":
                    self.now_var.set("ENCODING  //  " + payload[:100])
                elif event == "job_done":
                    key, name, result = payload
                    if self.tree.exists(key):
                        self.tree.item(key, values=(result, name))
                    self.queued_sources.discard(key)
                    if result in ("DONE", "SKIPPED"):
                        self.completed_sources.add(key)
                        self.total_done += 1
                    else:
                        self.total_failed += 1
                    self.update_counts()
                    self.now_var.set(f"{result}  //  {name}")
                    if not self.processing and self.jobs.empty():
                        self.status_var.set("WATCHING INBOX" if self.watching else "IDLE")
        except queue.Empty:
            pass
        self.root.after(250, self.process_events)

    def update_counts(self):
        pending = self.jobs.qsize()
        self.count_var.set(f"{pending} QUEUED  /  {self.total_done} DONE  /  {self.total_failed} FAILED")

    def open_folder(self, folder):
        path = Path(folder).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        try:
            os.startfile(str(path))
        except Exception as exc:
            messagebox.showerror(APP_NAME, str(exc))

    def on_close(self):
        if self.processing:
            answer = messagebox.askyesno(APP_NAME, "A conversion is running. Exit and interrupt it?")
            if not answer:
                return
            self.stop_requested = True
        self.save_config()
        self.worker_running = False
        self.jobs.put(None)
        self.root.destroy()


def main():
    root = Tk()
    ForgeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
