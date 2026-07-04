import cv2
import numpy as np


def overlay_png(background, overlay, x, y, scale=1.0):

    if overlay is None:
        return background

    h, w = overlay.shape[:2]

    w = int(w * scale)
    h = int(h * scale)

    overlay = cv2.resize(overlay, (w, h))

    x -= w // 2
    y -= h // 2

    if x < 0 or y < 0:
        return background

    if x + w > background.shape[1]:
        return background

    if y + h > background.shape[0]:
        return background

    if overlay.shape[2] == 4:

        alpha = overlay[:, :, 3] / 255.0

        for c in range(3):

            background[y:y+h, x:x+w, c] = (
                alpha * overlay[:, :, c] +
                (1-alpha) * background[y:y+h, x:x+w, c]
            )

    else:

        background[y:y+h, x:x+w] = overlay

    return background
