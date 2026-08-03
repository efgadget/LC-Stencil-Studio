"""
LC Stencil Studio
Selection Overlay Engine
Release 0.6.2
"""

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QBrush, QColor


class SelectionOverlay(QGraphicsItem):

    def __init__(self, target=None):

        super().__init__()

        self.target = target

        self.handle_size = 10

        self.setZValue(1000)


    def set_target(self, target):

        self.target = target

        self.update()



    def boundingRect(self):

        if self.target is None:

            return QRectF()


        return self.target.boundingRect()



    def paint(
        self,
        painter,
        option,
        widget=None
    ):

        if self.target is None:

            return


        rect = self.target.boundingRect()


        # bordo selezione

        pen = QPen(
            QColor(0,255,0)
        )

        pen.setWidth(2)


        painter.setPen(
            pen
        )


        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )


        painter.drawRect(
            rect
        )


        # maniglie

        painter.setPen(
            QPen(
                QColor(0,0,0)
            )
        )


        painter.setBrush(
            QBrush(
                QColor(255,255,255)
            )
        )


        points = [
            rect.topLeft(),
            rect.topRight(),
            rect.bottomLeft(),
            rect.bottomRight()
        ]


        for point in points:

            painter.drawRect(
                QRectF(
                    point.x()-self.handle_size/2,
                    point.y()-self.handle_size/2,
                    self.handle_size,
                    self.handle_size
                )
            )