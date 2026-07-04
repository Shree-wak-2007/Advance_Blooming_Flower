import cv2
from utils import overlay_png


class Flower:

    def __init__(self):

        self.growth = 0

        self.x = 320
        self.y = 430

        self.max_stem = 220

        self.flower = cv2.imread(
            "assets/flower.png",
            cv2.IMREAD_UNCHANGED
        )

        self.leaf = cv2.imread(
            "assets/leaf.png",
            cv2.IMREAD_UNCHANGED
        )

        self.glow = cv2.imread(
            "assets/glow.png",
            cv2.IMREAD_UNCHANGED
        )

        
        if self.flower is not None:
            print("Flower shape:", self.flower.shape)

        if self.leaf is not None:
            print("Leaf shape:", self.leaf.shape)

        if self.glow is not None:
            print("Glow shape:", self.glow.shape)

    def draw(self, frame):

        stem = int(self.max_stem * self.growth)

        top_x = self.x
        top_y = self.y - stem

        # Stem
        cv2.line(
            frame,
            (self.x, self.y),
            (top_x, top_y),
            (0, 170, 0),
            5
        )

        # Seed
        cv2.circle(
            frame,
            (self.x, self.y),
            7,
            (60, 60, 150),
            -1
        )

        # Leaves
        if self.growth > 0.30:

            overlay_png(
                frame,
                self.leaf,
                self.x-25,
                self.y-80,
                0.015
            )

            overlay_png(
                frame,
                self.leaf,
                self.x+25,
                self.y-120,
                0.015
            )

        # Glow
        if self.growth > 0.75:

            overlay_png(
                frame,
                self.glow,
                top_x,
                top_y,
                0.08
            )

        # Flower
        if self.growth > 0.80:

            scale = 0.03 + self.growth * 0.02
            overlay_png(
                frame,
                self.flower,
                top_x,
                top_y,
                scale
            )
