"""
LC Stencil Studio
Selection Overlay
Release 0.6.3
"""

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QBrush, QColor


class SelectionOverlay(QGraphicsItem):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.handle_size = 10

        self.setZValue(1000)



    def boundingRect(self):

        if self.parentItem() is None:

            return QRectF()


        return self.parentItem().boundingRect().adjusted(
            -15,
            -15,
            15,
            15
        )



    def paint(
        self,
        painter,
        option,
        widget=None
    ):

        parent = self.parentItem()

        if parent is None:

            return


        rect = parent.boundingRect()


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


        for point in [
            rect.topLeft(),
            rect.topRight(),
            rect.bottomLeft(),
            rect.bottomRight()
        ]:

            painter.drawRect(
                QRectF(
                    point.x()-5,
                    point.y()-5,
                    10,
                    10
                )
            )