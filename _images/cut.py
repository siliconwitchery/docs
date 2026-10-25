import sys
from pathlib import Path

import numpy as np
import cv2
from PIL import Image
from scipy import ndimage

# Cuts the hardware out of the original white mastheads, which are in
# assets/images at commit 7ba3bef. Pass the folder that holds them.
#
# Each cut: source, crop box, and rectangles (source coordinates) where old
# yellow leaders are painted out.
CUTS = {
    "s1-top": dict(
        src="s1-module-annotated-masthead.png",
        box=(350, 30, 540, 370),
        paint=[(355, 88, 425, 108), (355, 205, 425, 225), (355, 277, 425, 297),
               (470, 213, 530, 233), (470, 290, 530, 310)],
    ),
    "s1-bottom": dict(
        src="s1-module-annotated-masthead.png",
        box=(955, 30, 1145, 375),
        paint=[(955, 170, 985, 190), (955, 245, 985, 265), (955, 320, 985, 340),
               (1062, 195, 1145, 215), (1115, 315, 1145, 335)],
    ),
    "ecg": dict(
        src="s1-ecg-kit-annotated-masthead.png",
        box=(465, 70, 1155, 365),
        paint=[(935, 130, 1155, 150), (885, 222, 1155, 242), (1063, 290, 1155, 310),
               (470, 250, 806, 270), (800, 70, 825, 110), (798, 326, 826, 365),
               (676, 70, 696, 104), (676, 336, 696, 365)],
    ),
    "upy-board": dict(src="s1-micropython-annotated-masthead.png", box=(590, 0, 1270, 410)),
    "upy-snake": dict(src="s1-micropython-annotated-masthead.png", box=(1270, 80, 1530, 345)),
}


def cut(name, src, box, paint=()):
    full = np.array(Image.open(originals / src).convert("RGB"))
    rgb = full[box[1]:box[3], box[0]:box[2]].astype(int)
    white = (rgb.min(-1) > 228) & (rgb.max(-1) - rgb.min(-1) < 30)

    labels, _ = ndimage.label(white)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    fg = ndimage.binary_fill_holes(~np.isin(labels, edge[edge > 0]))
    rgba = np.dstack([rgb, fg * 255]).astype(float)

    painted = 0
    for rect in paint:
        x0, y0, x1, y1 = (v - o for v, o in zip(rect, box[:2] * 2))
        x0, y0 = max(x0, 0), max(y0, 0)
        sub = rgb[y0:y1, x0:x1]
        r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
        leader = (r > 190) & (g > 160) & (b < 140) & (r - b > 100)
        # Grow across the line to catch its blended edges.
        across = 0 if x1 - x0 >= y1 - y0 else 1
        grow = np.ones((7, 3)) if across == 0 else np.ones((3, 7))
        leader = ndimage.binary_dilation(leader, structure=grow)
        painted += leader.sum()
        # Fill each run of leader pixels by interpolating across the line.
        patch = rgba[y0:y1, x0:x1]
        if across:
            patch, leader = patch.transpose(1, 0, 2), leader.T
        for col in range(leader.shape[1]):
            rows = np.flatnonzero(leader[:, col])
            if rows.size == 0:
                continue
            for run in np.split(rows, np.flatnonzero(np.diff(rows) > 1) + 1):
                a, z = run[0] - 1, run[-1] + 1
                if a < 0 and z >= leader.shape[0]:
                    continue
                if a < 0 or z >= leader.shape[0]:
                    patch[run, col] = patch[z if a < 0 else a, col]
                    continue
                t = ((run - a) / (z - a))[:, None]
                patch[run, col] = (1 - t) * patch[a, col] + t * patch[z, col]

    out = rgba[..., :3].astype(np.uint8)
    # Opening with a 7 px square drops leader strands left outside the board.
    fg = ndimage.binary_opening(rgba[..., 3] > 127, structure=np.ones((7, 7)))
    fg = ndimage.binary_erosion(fg, iterations=1)

    alpha = cv2.GaussianBlur(fg.astype(np.float32), (3, 3), 0.8)
    rgba = np.dstack([out, (alpha * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(Path(__file__).parent / "cut" / f"{name}.png")
    print(name, rgba.shape, int(painted), "px painted")


originals = Path(sys.argv[1])
for name in sys.argv[2:] or CUTS:
    cut(name, **CUTS[name])
