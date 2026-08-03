"""
LC Stencil Studio
Resizable Pixmap Item
Release 0.6.1
"""

from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QBrush, QColor


class ResizablePixmapItem(QGraphicsPixmapItem):

    def __init__(self, pixmap):

        super().__init__(pixmap)

        self.setFlags(
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        self.setTransformationMode(
            Qt.TransformationMode.SmoothTransformation
        )

        self.resizing = False
        self.start_y = 0
        self.start_scale = 1.0


    def paint(
        self,
        painter,
        option,
        widget=None
    ):

        super().paint(
            painter,
            option,
            widget
        )


        if self.isSelected():

            rect = self.boundingRect()


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


            size = 10


            for point in [
                rect.topLeft(),
                rect.topRight(),
                rect.bottomLeft(),
                rect.bottomRight()
            ]:

                painter.drawRect(
                    QRectF(
                        point.x()-size/2,
                        point.y()-size/2,
                        size,
                        size
                    )
                )


    def mousePressEvent(self,event):

        rect = self.boundingRect()

        pos = event.pos()


        if (
            pos.x() > rect.right()-15
            and
            pos.y() > rect.bottom()-15
        ):

            self.resizing = True

            self.start_y = event.scenePos().y()

            self.start_scale = self.scale()

            event.accept()

            return


        super().mousePressEvent(event)



    def mouseMoveEvent(self,event):

        if self.resizing:

            delta = (
                event.scenePos().y()
                -
                self.start_y
            )

            factor = (
                self.start_scale +
                delta / 250
            )

            if factor > 0.1:

                self.setScale(
                    factor
                )

            event.accept()

            return


        super().mouseMoveEvent(event)



    def mouseReleaseEvent(self,event):

        self.resizing = False

        super().mouseReleaseEvent(event)