"""
LC Stencil Studio
Canvas Widget
Release 0.7.0
"""

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter, QBrush, QColor, QTransform
from PySide6.QtCore import Qt, QPoint

from core.viewport import Viewport
from engine.canvas_engine import CanvasEngine
from engine.image_engine import ImageEngine
from ui.widgets.selection_overlay import SelectionOverlay


class Canvas(QGraphicsView):

    def __init__(self, project):
        super().__init__()
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.project = project
        self.viewport_state = Viewport()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.canvas_engine = CanvasEngine(self.scene)
        self.image_engine = ImageEngine(self.scene)
        self.selection_overlay = None
        self.current_selected_item = None
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor(70, 70, 70)))
        self.setSceneRect(-3000, -3000, 6000, 6000)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self._panning = False
        self._last_pos = QPoint()
        self.canvas_engine.draw_project(project)

    def reset_for_project(self, project):
        self.selection_overlay = None
        self.current_selected_item = None
        self.image_engine.image_item = None
        self.project = project
        self.resetTransform()
        self.viewport_state.reset()
        self._panning = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.canvas_engine.draw_project(project)

    def selected_item(self):
        selected = self.scene.selectedItems()
        return selected[0] if selected else None

    def update_selection(self):
        selected = self.scene.selectedItems()
        if not selected:
            if self.selection_overlay:
                self.selection_overlay.setVisible(False)
            self.current_selected_item = None
            return
        item = selected[0]
        if item == self.current_selected_item:
            return
        self.current_selected_item = item
        if self.selection_overlay:
            self.scene.removeItem(self.selection_overlay)
            self.selection_overlay = None
        self.selection_overlay = SelectionOverlay(item)
        self.selection_overlay.setParentItem(item)
        self.selection_overlay.setVisible(True)
        self.selection_overlay.update()

    def get_selected_geometry(self):
        item = self.selected_item()
        if item is None:
            return None
        rect = item.boundingRect()
        transform = item.transform()
        return {
            "x": item.pos().x(),
            "y": item.pos().y(),
            "width": abs(rect.width() * transform.m11()),
            "height": abs(rect.height() * transform.m22()),
            "rotation": item.rotation(),
        }

    def set_selected_geometry(self, x=None, y=None, width=None, height=None,
                              rotation=None, lock_aspect=True):
        item = self.selected_item()
        if item is None:
            return False
        rect = item.boundingRect()
        current = self.get_selected_geometry()
        if width is None:
            width = current["width"]
        if height is None:
            height = current["height"]
        if lock_aspect and rect.width() > 0 and rect.height() > 0:
            ratio = rect.width() / rect.height()
            if abs(width - current["width"]) >= abs(height - current["height"]):
                height = width / ratio
            else:
                width = height * ratio
        sx = max(width / max(rect.width(), 0.001), 0.001)
        sy = max(height / max(rect.height(), 0.001), 0.001)
        transform = QTransform()
        transform.scale(sx, sy)
        item.setTransform(transform)
        if x is not None or y is not None:
            item.setPos(current["x"] if x is None else x,
                        current["y"] if y is None else y)
        if rotation is not None:
            item.setTransformOriginPoint(rect.center())
            item.setRotation(rotation)
        if self.selection_overlay:
            self.selection_overlay.update()
        self.project.modified = True
        return True

    def center_selected(self):
        item = self.selected_item()
        if item is None:
            return False
        material_rect = self.scene.itemsBoundingRect()
        item_rect = item.sceneBoundingRect()
        delta = material_rect.center() - item_rect.center()
        item.setPos(item.pos() + delta)
        self.project.modified = True
        return True

    def reset_selected_transform(self):
        item = self.selected_item()
        if item is None:
            return False
        item.setTransform(QTransform())
        item.setRotation(0)
        item.setPos(0, 0)
        if self.selection_overlay:
            self.selection_overlay.update()
        self.project.modified = True
        return True

    def delete_selected(self):
        item = self.selected_item()
        if item is None:
            return False
        if self.selection_overlay:
            self.selection_overlay.setParentItem(None)
            self.scene.removeItem(self.selection_overlay)
            self.selection_overlay = None
        self.scene.removeItem(item)
        if item is self.image_engine.image_item:
            self.image_engine.image_item = None
        self.current_selected_item = None
        self.project.modified = True
        return True

    def duplicate_selected(self):
        item = self.selected_item()
        if item is None or not hasattr(item, "pixmap"):
            return False
        from ui.widgets.resize_pixmap_item import ResizablePixmapItem
        clone = ResizablePixmapItem(item.pixmap())
        clone.setTransform(item.transform())
        clone.setRotation(item.rotation())
        clone.setTransformOriginPoint(item.transformOriginPoint())
        clone.setPos(item.pos().x() + 10, item.pos().y() + 10)
        self.scene.addItem(clone)
        item.setSelected(False)
        clone.setSelected(True)
        self.current_selected_item = None
        self.update_selection()
        self.project.modified = True
        return True

    def fit_selected_to_material(self):
        item = self.selected_item()
        if item is None:
            return False
        rect = item.boundingRect()
        if rect.width() <= 0 or rect.height() <= 0:
            return False
        target_w = float(self.project.material.width)
        target_h = float(self.project.material.height)
        scale = min(target_w / rect.width(), target_h / rect.height())
        transform = QTransform()
        transform.scale(scale, scale)
        item.setTransform(transform)
        item.setRotation(0)
        self.center_selected()
        if self.selection_overlay:
            self.selection_overlay.update()
        self.project.modified = True
        return True

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = True
            self._last_pos = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)
        self.update_selection()

    def mouseMoveEvent(self, event):
        if self._panning:
            delta = event.pos() - self._last_pos
            self._last_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
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

    def wheelEvent(self, event):
        old_zoom = self.viewport_state.zoom
        if event.angleDelta().y() > 0:
            self.viewport_state.zoom_in()
        else:
            self.viewport_state.zoom_out()
        factor = self.viewport_state.zoom / old_zoom
        self.scale(factor, factor)

    def fit_material(self):
        self.resetTransform()
        self.viewport_state.reset()
        self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def import_image(self, filename):
        self.selection_overlay = None
        self.current_selected_item = None
        result = self.image_engine.load_image(filename)
        if result and self.image_engine.image_item:
            self.image_engine.image_item.setSelected(True)
            self.update_selection()
            self.project.modified = True
        return result
