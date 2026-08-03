"""
LC Stencil Studio
Grid Engine
Versione 0.2.0
"""

from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QColor, QPen


class GridEngine:

    def __init__(self, scene):

        self.scene = scene

        self.minor_spacing = 10
        self.major_spacing = 50
        self.size = 3000

    def draw(self):

        self.draw_vertical_lines()

        self.draw_horizontal_lines()

        self.draw_axis()

    def draw_vertical_lines(self):

        for x in range(
            -self.size,
            self.size + self.minor_spacing,
            self.minor_spacing
        ):

            if x % self.major_spacing == 0:
                color = QColor(105, 105, 105)
            else:
                color = QColor(78, 78, 78)

            pen = QPen(color)
            pen.setWidth(1)

            line = QGraphicsLineItem(
                x,
                -self.size,
                x,
                self.size
            )

            line.setPen(pen)

            self.scene.addItem(line)

    def draw_horizontal_lines(self):

        for y in range(
            -self.size,
            self.size + self.minor_spacing,
            self.minor_spacing
        ):

            if y % self.major_spacing == 0:
                color = QColor(105, 105, 105)
            else:
                color = QColor(78, 78, 78)

            pen = QPen(color)
            pen.setWidth(1)

            line = QGraphicsLineItem(
                -self.size,
                y,
                self.size,
                y
            )

            line.setPen(pen)

            self.scene.addItem(line)

    def draw_axis(self):

        xpen = QPen(QColor(220, 70, 70))
        xpen.setWidth(2)

        axis_x = QGraphicsLineItem(
            -self.size,
            0,
            self.size,
            0
        )

        axis_x.setPen(xpen)

        self.scene.addItem(axis_x)

        ypen = QPen(QColor(70, 220, 70))
        ypen.setWidth(2)

        axis_y = QGraphicsLineItem(
            0,
            -self.size,
            0,
            self.size
        )

        axis_y.setPen(ypen)

        self.scene.addItem(axis_y)
    