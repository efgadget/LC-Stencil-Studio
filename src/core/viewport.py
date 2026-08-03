"""
LC Stencil Studio
Viewport Engine
Versione 0.2.0
"""


class Viewport:

    MIN_ZOOM = 0.20
    MAX_ZOOM = 10.00
    ZOOM_STEP = 1.15

    def __init__(self):

        self.zoom = 1.0

        self.center_x = 0.0
        self.center_y = 0.0

    def zoom_in(self):

        self.zoom *= self.ZOOM_STEP

        if self.zoom > self.MAX_ZOOM:
            self.zoom = self.MAX_ZOOM

    def zoom_out(self):

        self.zoom /= self.ZOOM_STEP

        if self.zoom < self.MIN_ZOOM:
            self.zoom = self.MIN_ZOOM

    def reset(self):

        self.zoom = 1.0

        self.center_x = 0.0
        self.center_y = 0.0