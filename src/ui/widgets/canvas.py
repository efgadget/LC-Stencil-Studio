"""
LC Stencil Studio
Canvas Widget
Sprint 011
Release 0.6.2
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

from ui.widgets.selection_overlay import SelectionOverlay



class Canvas(QGraphicsView):

    def __init__(self, project):

        super().__init__()


        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )


        self.project = project


        self.viewport_state = Viewport()


        self.scene = QGraphicsScene(
            self
        )

        self.setScene(
            self.scene
        )


        self.canvas_engine = CanvasEngine(
            self.scene
        )


        self.image_engine = ImageEngine(
            self.scene
        )


        # Overlay selezione
        # Non viene aggiunto direttamente alla scena
        # per evitare cancellazioni Qt C++

        self.selection_overlay = SelectionOverlay()


        self.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )


        self.setBackgroundBrush(
            QBrush(
                QColor(70,70,70)
            )
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


        self.canvas_engine.draw_project(
            project
        )



    def wheelEvent(self,event):

        old_zoom = self.viewport_state.zoom


        if event.angleDelta().y() > 0:

            self.viewport_state.zoom_in()

        else:

            self.viewport_state.zoom_out()


        factor = (
            self.viewport_state.zoom /
            old_zoom
        )


        self.scale(
            factor,
            factor
        )



    def mousePressEvent(self,event):

        if event.button() == Qt.MouseButton.MiddleButton:

            self._panning = True

            self._last_pos = event.pos()


            self.setCursor(
                Qt.CursorShape.ClosedHandCursor
            )


            event.accept()

            return


        super().mousePressEvent(
            event
        )


        self.update_selection()



    def mouseMoveEvent(self,event):

        if self._panning:

            delta = (
                event.pos()
                -
                self._last_pos
            )


            self._last_pos = event.pos()


            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value()
                -
                delta.x()
            )


            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value()
                -
                delta.y()
            )


            event.accept()

            return


        super().mouseMoveEvent(
            event
        )



    def mouseReleaseEvent(self,event):

        if event.button() == Qt.MouseButton.MiddleButton:

            self._panning = False


            self.setCursor(
                Qt.CursorShape.ArrowCursor
            )


            event.accept()

            return


        super().mouseReleaseEvent(
            event
        )



    def update_selection(self):

        selected = self.scene.selectedItems()


        if selected:

            item = selected[0]


            self.selection_overlay.set_target(
                item
            )


        else:

            self.selection_overlay.set_target(
                None
            )



    def fit_material(self):

        self.resetTransform()


        self.viewport_state.reset()


        self.fitInView(
            self.scene.itemsBoundingRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )



    def import_image(self,filename):

        return self.image_engine.load_image(
            filename
        )