"""
LC Stencil Studio
Canvas Widget
Sprint 011
"""

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

from core.viewport import Viewport
from engine.canvas_engine import CanvasEngine
from engine.image_engine import ImageEngine


class Canvas(QGraphicsView):

    def __init__(self, project):

        super().__init__()

        self.project = project

        self.viewport_state = Viewport()

        self.scene = QGraphicsScene(self)

        self.setScene(self.scene)

        self.canvas_engine = CanvasEngine(self.scene)

        self.image_engine = ImageEngine(self.scene)

        self.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        self.setBackgroundBrush(
            QBrush(QColor(70, 70, 70))
        )

        self.setSceneRect(
            -3000,
            -3000,
            6000,
            6000
        )

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self._panning = False

        self._last_pos = QPoint()

        self.canvas_engine.draw_project(project)

    def wheelEvent(self, event):

        old_zoom = self.viewport_state.zoom

        if event.angleDelta().y() > 0:

            self.viewport_state.zoom_in()

        else:

            self.viewport_state.zoom_out()

        factor = self.viewport_state.zoom / old_zoom

        self.scale(
            factor,
            factor
        )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:

            self._panning = True

            self._last_pos = event.pos()

            self.setCursor(
                Qt.CursorShape.ClosedHandCursor
            )

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

            self.setCursor(
                Qt.CursorShape.ArrowCursor
            )

            event.accept()

            return

        super().mouseReleaseEvent(event)

    def fit_material(self):

        self.resetTransform()

        self.viewport_state.reset()

        self.fitInView(
            self.scene.itemsBoundingRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

    def import_image(self, filename):

        return self.image_engine.load_image(filename)