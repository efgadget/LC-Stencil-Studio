"""
LC Stencil Studio
Selection Overlay
Release 0.6.7
Four-corner resize: proportional by default, free with SHIFT
"""

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QPen, QBrush, QColor, QTransform


class SelectionOverlay(QGraphicsItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.handle_size = 12
        self.handle_hit_size = 22
        self.resizing = False
        self.resize_handle = None
        self.start_mouse = QPointF()
        self.start_transform = QTransform()
        self.start_scale_x = 1.0
        self.start_scale_y = 1.0
        self.start_vector = QPointF(1.0, 1.0)
        self.start_distance = 1.0
        self.anchor_local = QPointF()
        self.anchor_scene = QPointF()

        self.setZValue(1000)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)

    def boundingRect(self):
        if self.parentItem() is None:
            return QRectF()
        return self.parentItem().boundingRect()

    def _handles(self):
        rect = self.parentItem().boundingRect()
        inset = self.handle_size / 2 + 1
        return {
            "top_left": QPointF(rect.left() + inset, rect.top() + inset),
            "top_right": QPointF(rect.right() - inset, rect.top() + inset),
            "bottom_left": QPointF(rect.left() + inset, rect.bottom() - inset),
            "bottom_right": QPointF(rect.right() - inset, rect.bottom() - inset),
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
        painter.drawRect(rect.adjusted(1, 1, -1, -1))

        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setBrush(QBrush(QColor(255, 255, 255)))

        size = self.handle_size
        for point in self._handles().values():
            painter.drawRect(QRectF(
                point.x() - size / 2,
                point.y() - size / 2,
                size,
                size,
            ))

    def get_handle(self, pos):
        half = self.handle_hit_size / 2
        for name, point in self._handles().items():
            if QRectF(
                point.x() - half,
                point.y() - half,
                self.handle_hit_size,
                self.handle_hit_size,
            ).contains(pos):
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
        self.start_transform = QTransform(parent.transform())
        self.start_scale_x = max(abs(self.start_transform.m11()), 0.001)
        self.start_scale_y = max(abs(self.start_transform.m22()), 0.001)
        self.anchor_local = self._opposite_corner(handle)
        self.anchor_scene = parent.mapToScene(self.anchor_local)
        self.start_vector = self.start_mouse - self.anchor_scene
        self.start_distance = max(
            (self.start_vector.x() ** 2 + self.start_vector.y() ** 2) ** 0.5,
            1.0,
        )
        event.accept()

    def mouseMoveEvent(self, event):
        if not self.resizing or self.parentItem() is None:
            event.ignore()
            return

        parent = self.parentItem()
        current_vector = event.scenePos() - self.anchor_scene
        shift_free = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)

        if shift_free:
            sx_ratio = (
                current_vector.x() / self.start_vector.x()
                if abs(self.start_vector.x()) > 0.001 else 1.0
            )
            sy_ratio = (
                current_vector.y() / self.start_vector.y()
                if abs(self.start_vector.y()) > 0.001 else 1.0
            )
            scale_x = max(self.start_scale_x * sx_ratio, 0.05)
            scale_y = max(self.start_scale_y * sy_ratio, 0.05)
        else:
            current_distance = (
                current_vector.x() ** 2 + current_vector.y() ** 2
            ) ** 0.5
            ratio = max(current_distance / self.start_distance, 0.05)
            scale_x = self.start_scale_x * ratio
            scale_y = self.start_scale_y * ratio

        transform = QTransform()
        transform.scale(scale_x, scale_y)
        parent.setTransform(transform)

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
