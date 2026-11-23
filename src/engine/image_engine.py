"""
LC Stencil Studio
Image Engine
Release 0.6.7
"""

from PySide6.QtGui import QPixmap, QImage, qRgb, qGray
from PySide6.QtCore import Qt

from ui.widgets.resize_pixmap_item import ResizablePixmapItem


class ImageEngine:

    def __init__(self, scene):

        self.scene = scene
        self.image_item = None
        self.original_pixmap = None
        self.threshold = 128


    def clear(self):

        if self.image_item:

            self.scene.removeItem(
                self.image_item
            )

            self.image_item = None
        self.original_pixmap = None


    def load_image(self, filename):

        self.clear()

        pixmap = QPixmap(filename)

        if pixmap.isNull():

            return False


        self.original_pixmap = QPixmap(pixmap)
        self.threshold = 128
        self.image_item = ResizablePixmapItem(
            pixmap
        )


        self.image_item.setTransformationMode(
            Qt.TransformationMode.SmoothTransformation
        )


        rect = self.image_item.boundingRect()


        self.image_item.setPos(
            -rect.width() / 2,
            -rect.height() / 2
        )


        self.scene.addItem(
            self.image_item
        )


        return True



    def has_image(self):

        return self.image_item is not None



    def get_image(self):

        return self.image_item

    def apply_threshold(self, threshold=128):
        """Show a black/white raster preview. This does not generate cut paths."""
        if self.image_item is None or self.original_pixmap is None:
            return False
        source = self.original_pixmap.toImage().convertToFormat(
            QImage.Format.Format_RGB32
        )
        if source.isNull():
            return False
        result = QImage(source.size(), QImage.Format.Format_RGB32)
        for y in range(source.height()):
            for x in range(source.width()):
                gray = qGray(source.pixel(x, y))
                value = 0 if gray < threshold else 255
                result.setPixel(x, y, qRgb(value, value, value))
        self.image_item.setPixmap(QPixmap.fromImage(result))
        self.threshold = threshold
        return True

    def restore_original(self):
        if self.image_item is None or self.original_pixmap is None:
            return False
        self.image_item.setPixmap(self.original_pixmap)
        return True
