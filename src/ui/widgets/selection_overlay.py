"""
LC Stencil Studio
Selection Overlay
Release 0.6.7
Four-corner proportional resize
"""

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QPen, QBrush, QColor


class SelectionOverlay(QGraphicsItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.handle_size = 10
        self.handle_hit_size = 18
        self.resizing = False
        self.resize_handle = None
        self.start_mouse = QPointF()
        self.start_scale = 1.0
        self.start_distance = 1.0
        self.anchor_local = QPointF()
        self.anchor_scene = QPointF()

        self.setZValue(1000)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)

    def boundingRect(self):
        if self.parentItem() is None:
            return QRectF()

        margin = max(20, self.handle_hit_size)
        return self.parentItem().boundingRect().adjusted(
            -margin, -margin, margin, margin
        )

    def _handles(self):
        rect = self.parentItem().boundingRect()
        return {
            "top_left": rect.topLeft(),
            "top_right": rect.topRight(),
            "bottom_left": rect.bottomLeft(),
            "bottom_right": rect.bottomRight(),
        }

    def _opposite_corner(self, handle):
        rect = self.parentItem().boundingRect()
        return {
            "top_left": rect.bottomRight(),
            "top_right": rect.bottomLeft(),
            "bottom_left": rect.topRight(),
            "bottom_right": rect.topLeft(),
        }[handle]

    def paint(self, painter, option, widget=None):
        if self.parentItem() is None:
            return

        rect = self.parentItem().boundingRect()

        pen = QPen(QColor(0, 255, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(rect)

        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setBrush(QBrush(QColor(255, 255, 255)))

        size = self.handle_size
        for point in self._handles().values():
            painter.drawRect(
                QRectF(
                    point.x() - size / 2,
                    point.y() - size / 2,
                    size,
                    size,
                )
            )

    def get_handle(self, pos):
        half = self.handle_hit_size / 2

        for name, point in self._handles().items():
            hit_rect = QRectF(
                point.x() - half,
                point.y() - half,
                self.handle_hit_size,
                self.handle_hit_size,
            )
            if hit_rect.contains(pos):
                return name

        return None

    def mousePressEvent(self, event):
        handle = self.get_handle(event.pos())

        if not handle:
            event.ignore()
            return

        parent = self.parentItem()
        self.resizing = True
        self.resize_handle = handle
        self.start_mouse = event.scenePos()
        self.start_scale = max(parent.scale(), 0.001)

        self.anchor_local = self._opposite_corner(handle)
        self.anchor_scene = parent.mapToScene(self.anchor_local)

        start_vector = self.start_mouse - self.anchor_scene
        self.start_distance = max(
            (start_vector.x() ** 2 + start_vector.y() ** 2) ** 0.5,
            1.0,
        )

        event.accept()

    def mouseMoveEvent(self, event):
        if not self.resizing or self.parentItem() is None:
            event.ignore()
            return

        parent = self.parentItem()
        current_vector = event.scenePos() - self.anchor_scene
        current_distance = (
            current_vector.x() ** 2 + current_vector.y() ** 2
        ) ** 0.5

        factor = self.start_scale * (current_distance / self.start_distance)
        factor = max(factor, 0.05)

        # Default resize is proportional. SHIFT free resize is implemented
        # in the next 0.6.7 foundation step.
        parent.setScale(factor)

        # Keep the opposite corner fixed while dragging any of the 4 handles.
        new_anchor_scene = parent.mapToScene(self.anchor_local)
        correction = self.anchor_scene - new_anchor_scene
        parent.setPos(parent.pos() + correction)

        self.update()
        event.accept()

    def mouseReleaseEvent(self, event):
        if self.resizing:
            self.resizing = False
            self.resize_handle = None
            event.accept()
            return

        event.ignore()

    def update_position(self):
        self.update()
