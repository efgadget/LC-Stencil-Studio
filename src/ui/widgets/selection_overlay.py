"""
LC Stencil Studio
Selection Overlay
Release 0.6.6
Modulo G.3 - Proportional CAD Scale
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


        self.original_ratio = 1.0


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



    def get_handle(self, pos):

        rect = self.parentItem().boundingRect()


        handles = {

            "top_left": rect.topLeft(),

            "top_right": rect.topRight(),

            "bottom_left": rect.bottomLeft(),

            "bottom_right": rect.bottomRight()

        }


        for name, point in handles.items():

            if (

                abs(pos.x()-point.x()) < 15

                and

                abs(pos.y()-point.y()) < 15

            ):

                return name


        return None



    def mousePressEvent(self,event):

        handle = self.get_handle(
            event.pos()
        )


        if handle:


            self.resizing = True

            self.resize_handle = handle


            self.start_mouse = event.scenePos()


            self.start_scale = self.parentItem().scale()


            rect = self.parentItem().boundingRect()


            self.original_ratio = (
                rect.width()
                /
                rect.height()
            )


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


        # scala base

        factor = self.start_scale


        if self.resize_handle in (

            "bottom_right",

            "top_right"

        ):

            factor += delta.x() / 300


        else:

            factor -= delta.x() / 300



        if factor < 0.1:

            factor = 0.1



        # proporzioni bloccate

        if not (
            event.modifiers()
            &
            Qt.KeyboardModifier.ShiftModifier
        ):


            self.parentItem().setScale(
                factor
            )


        else:

            # modalità libera con SHIFT

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