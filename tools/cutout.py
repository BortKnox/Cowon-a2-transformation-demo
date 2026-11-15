import json
import sys

import cv2
import numpy as np
from PIL import Image

SRC = sys.argv[1]
OUT_DIR = sys.argv[2]
SCALE = 3

im = Image.open(SRC).convert("RGB")
full = np.array(im)

# --- 1. isolate the front view (middle of the three-view sheet) -------------
# columns that contain any non-white pixel; the sheet has 3 groups (left side, front, right side)
nonwhite_cols = (full.min(axis=2) < 245).any(axis=0)
runs = []
start = None
for x, v in enumerate(nonwhite_cols):
    if v and start is None:
        start = x
    if not v and start is not None:
        runs.append((start, x - 1))
        start = None
if start is not None:
    runs.append((start, len(nonwhite_cols) - 1))
print("column runs:", runs)

# front view = widest run
fx0, fx1 = max(runs, key=lambda r: r[1] - r[0])
rows = (full[:, fx0:fx1 + 1].min(axis=2) < 245).any(axis=1)
fy0, fy1 = np.where(rows)[0][[0, -1]]
pad = 2
fx0 = max(fx0 - pad, 0)
fx1 = min(fx1 + pad, full.shape[1] - 1)
fy0 = max(int(fy0) - pad, 0)
fy1 = min(int(fy1) + pad, full.shape[0] - 1)
front = full[fy0:fy1 + 1, fx0:fx1 + 1]
print("front crop box (src coords):", fx0, fy0, fx1, fy1, "size", front.shape[1], front.shape[0])

# --- 2. upscale -------------------------------------------------------------
H, W = front.shape[:2]
big = cv2.resize(front, (W * SCALE, H * SCALE), interpolation=cv2.INTER_LANCZOS4)
BH, BW = big.shape[:2]

# --- 3. body mask: flood the white background from the border -----------------
near_white = (big.min(axis=2) >= 246).astype(np.uint8)
flood = near_white.copy()
ff_mask = np.zeros((BH + 2, BW + 2), np.uint8)
# seed from every border pixel that is near white
bg = np.zeros((BH, BW), np.uint8)
for (sx, sy) in [(0, 0), (BW - 1, 0), (0, BH - 1), (BW - 1, BH - 1)]:
    pass
n, labels = cv2.connectedComponents(near_white, connectivity=4)
border_labels = set(np.unique(np.concatenate([labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]])))
border_labels.discard(0)
for l in border_labels:
    bg[labels == l] = 1
body = (1 - bg).astype(np.uint8)

# keep largest component only, fill interior holes
n, labels, stats, _ = cv2.connectedComponentsWithStats(body, connectivity=8)
largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
body = (labels == largest).astype(np.uint8)
inv = 1 - body
n, labels = cv2.connectedComponents(inv, connectivity=4)
outer = set(np.unique(np.concatenate([labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]])))
filled = body.copy()
for l in range(1, n):
    if l not in outer:
        filled[labels == l] = 1
body = filled
print("body area frac:", body.mean())

# --- 4. screen hole -----------------------------------------------------------
b = big[..., 2].astype(int)
r = big[..., 0].astype(int)
lum = big.astype(int).sum(axis=2)
screenish = ((b - r > 14) | (lum < 150)).astype(np.uint8)
screenish &= body
# the screen is by far the largest blue/dark region inside the body
n, labels, stats, _ = cv2.connectedComponentsWithStats(screenish, connectivity=8)
seed_label = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
print("screen component label", seed_label, "area", stats[seed_label, cv2.CC_STAT_AREA])
hole = (labels == seed_label).astype(np.uint8)
# fill bright content (logo, text) inside the screen
inv = 1 - hole
n2, lab2 = cv2.connectedComponents(inv, connectivity=4)
outer = set(np.unique(np.concatenate([lab2[0, :], lab2[-1, :], lab2[:, 0], lab2[:, -1]])))
for l in range(1, n2):
    if l not in outer:
        hole[lab2 == l] = 1
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
hole = cv2.morphologyEx(hole, cv2.MORPH_CLOSE, k)
hole = cv2.morphologyEx(hole, cv2.MORPH_OPEN, k)
# the raw blob is ragged where the bezel shading is dark, so fit a clean rounded
# rectangle from the median position of each edge instead
ys, xs = np.where(hole)
ry0, ry1 = int(ys.min()), int(ys.max())
rx0, rx1 = int(xs.min()), int(xs.max())
band_y = range(ry0 + int(0.3 * (ry1 - ry0)), ry0 + int(0.7 * (ry1 - ry0)))
band_x = range(rx0 + int(0.3 * (rx1 - rx0)), rx0 + int(0.7 * (rx1 - rx0)))
lefts = [np.where(hole[y])[0].min() for y in band_y if hole[y].any()]
rights = [np.where(hole[y])[0].max() for y in band_y if hole[y].any()]
tops = [np.where(hole[:, x])[0].min() for x in band_x if hole[:, x].any()]
bots = [np.where(hole[:, x])[0].max() for x in band_x if hole[:, x].any()]
hx0, hx1 = int(np.median(lefts)), int(np.median(rights))
hy0, hy1 = int(np.median(tops)), int(np.median(bots))
print("edge spread (min/median/max): L", min(lefts), hx0, max(lefts), " R", min(rights), hx1, max(rights),
      " T", min(tops), hy0, max(tops), " B", min(bots), hy1, max(bots))
RADIUS = 16
hole = np.zeros((BH, BW), np.uint8)
cv2.rectangle(hole, (hx0 + RADIUS, hy0), (hx1 - RADIUS, hy1), 1, -1)
cv2.rectangle(hole, (hx0, hy0 + RADIUS), (hx1, hy1 - RADIUS), 1, -1)
for (cx_, cy_) in [(hx0 + RADIUS, hy0 + RADIUS), (hx1 - RADIUS, hy0 + RADIUS),
                   (hx0 + RADIUS, hy1 - RADIUS), (hx1 - RADIUS, hy1 - RADIUS)]:
    cv2.circle(hole, (cx_, cy_), RADIUS, 1, -1)
print("hole bbox (big px):", hx0, hy0, hx1, hy1, "size", hx1 - hx0 + 1, hy1 - hy0 + 1,
      "aspect", (hx1 - hx0 + 1) / (hy1 - hy0 + 1), "(target 480/272 = %.4f)" % (480 / 272))

# --- 5. alpha: feathered edges, trim the white fringe --------------------------
body_f = cv2.erode(body, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
alpha_body = cv2.GaussianBlur(body_f.astype(np.float32), (0, 0), 1.1)
alpha_hole = cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 1.1)
alpha = np.clip(alpha_body - alpha_hole, 0, 1)
# inside the body proper alpha_body is 1; hole subtracts; edge of hole stays soft
alpha = (alpha * 255).astype(np.uint8)

rgba = np.dstack([big, alpha])
Image.fromarray(rgba, "RGBA").save(f"{OUT_DIR}/cowon_a2_front.png", optimize=True)

# preview composited on a mid-grey with a magenta "behind" layer so the hole is obvious
prev = np.zeros((BH, BW, 3), np.uint8)
prev[:] = (214, 60, 160)
a = alpha[..., None].astype(np.float32) / 255
comp = (big.astype(np.float32) * a + prev.astype(np.float32) * (1 - a)).astype(np.uint8)
Image.fromarray(comp).save(f"{OUT_DIR}/cutout_preview.png")

meta = {
    "src_crop": [fx0, fy0, fx1, fy1],
    "scale": SCALE,
    "size": [BW, BH],
    "hole": [hx0, hy0, hx1, hy1],
}
json.dump(meta, open(f"{OUT_DIR}/cutout_meta.json", "w"), indent=2)
print(json.dumps(meta))
