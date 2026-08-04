"""
LC Stencil Studio
Canvas Widget
Sprint 011
Release 0.6.3 F.3.3
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


        self.selection_overlay = None

        self.current_selected_item = None



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



    def update_selection(self):

        selected = self.scene.selectedItems()


        if not selected:

            if self.selection_overlay:

                self.selection_overlay.setVisible(
                    False
                )


            self.current_selected_item = None

            return



        item = selected[0]


        if item == self.current_selected_item:

            return


        self.current_selected_item = item


        # elimina vecchio overlay

        if self.selection_overlay:

            self.scene.removeItem(
                self.selection_overlay
            )


            self.selection_overlay = None



        # crea overlay figlio dell'immagine

        self.selection_overlay = SelectionOverlay(
            item
        )


        self.selection_overlay.setParentItem(
            item
        )


        self.selection_overlay.setVisible(
            True
        )


        self.selection_overlay.update()



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