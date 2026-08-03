from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene
)

from PySide6.QtGui import (
    QPainter,
    QBrush,
    QColor
)

from PySide6.QtCore import (
    Qt,
    QPoint
)

from engine.canvas_engine import CanvasEngine


class Canvas(QGraphicsView):

    def __init__(self, project):
        super().__init__()

        self.project = project

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.engine = CanvasEngine(self.scene)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.setBackgroundBrush(
            QBrush(QColor(80, 80, 80))
        )

        self.setSceneRect(-3000, -3000, 6000, 6000)

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.zoom_factor = 1.15

        self.engine.draw_project(self.project)

        # Variabili per il PAN
        self._panning = False
        self._last_pos = QPoint()

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:

            self.scale(
                self.zoom_factor,
                self.zoom_factor
            )

        else:

            self.scale(
                1 / self.zoom_factor,
                1 / self.zoom_factor
            )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:

            self._panning = True

            self._last_pos = event.pos()

            self.setCursor(Qt.CursorShape.ClosedHandCursor)

            event.accept()

            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if self._panning:

            delta = event.pos() - self._last_pos

            self._last_pos = event.pos()

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )

            event.accept()

            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:

            self._panning = False

            self.setCursor(Qt.CursorShape.ArrowCursor)

            event.accept()

            return

        super().mouseReleaseEvent(event)
