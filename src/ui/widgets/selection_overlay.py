"""
LC Stencil Studio
Selection Overlay
Release 0.6.4
Modulo G.1 - CAD Resize
"""

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QPen, QBrush, QColor


class SelectionOverlay(QGraphicsItem):

    def __init__(self, parent=None):

        super().__init__(parent)


        self.handle_size = 10


        self.resizing = False

        self.resize_handle = None


        self.start_mouse = QPointF()

        self.start_scale = 1.0


        self.setZValue(1000)



    def boundingRect(self):

        if self.parentItem() is None:

            return QRectF()


        return self.parentItem().boundingRect().adjusted(
            -20,
            -20,
            20,
            20
        )



    def paint(
        self,
        painter,
        option,
        widget=None
    ):

        if self.parentItem() is None:

            return


        rect = self.parentItem().boundingRect()



        # bordo verde

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



        # maniglie bianche

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


        size = self.handle_size



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

        if self.parentItem() is None:

            return


        rect = self.parentItem().boundingRect()


        pos = event.pos()



        # Per ora attiviamo solo basso destra

        if (

            pos.x() > rect.right()-20

            and

            pos.y() > rect.bottom()-20

        ):


            self.resizing = True


            self.resize_handle = "bottom_right"


            self.start_mouse = event.scenePos()


            self.start_scale = self.parentItem().scale()


            event.accept()


            return



        event.ignore()



    def mouseMoveEvent(self,event):

        if not self.resizing:

            return



        delta = (

            event.scenePos()

            -

            self.start_mouse

        )



        factor = (

            self.start_scale

            +

            delta.x() / 300

        )



        if factor < 0.1:

            factor = 0.1



        self.parentItem().setScale(
            factor
        )


        self.update()



        event.accept()



    def mouseReleaseEvent(self,event):

        self.resizing = False

        self.resize_handle = None


        event.accept()



    def update_position(self):

        self.update()