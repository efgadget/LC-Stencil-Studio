"""Raster bridge preview for stencil islands (not vector cutting geometry)."""
from collections import deque
from PySide6.QtGui import QImage, QPainter, QPen, QColor
from PySide6.QtCore import Qt


def add_island_bridges(source, bridge_pixels, orientation="horizontal"):
    """Connect enclosed white regions to edge-connected white background.

    Uses four-connected white components and straight horizontal/vertical
    bridges. Returns (QImage, number_of_bridges). The image is not a
    laser-ready vector and requires visual inspection.
    """
    image = source.convertToFormat(QImage.Format.Format_RGB32)
    width, height = image.width(), image.height()
    if width <= 0 or height <= 0:
        raise ValueError("Immagine vuota")
    if width * height > 2_000_000:
        raise ValueError("Immagine troppo grande (massimo 2 milioni di pixel)")
    bridge_pixels = max(1, int(bridge_pixels))
    if orientation not in ("horizontal", "vertical", "shortest"):
        raise ValueError("Orientamento ponticelli non valido")
    white = bytearray(width * height)
    for y in range(height):
        for x in range(width):
            white[y * width + x] = image.pixelColor(x, y).red() >= 128

    labels = [-1] * (width * height)
    components = []
    for start in range(width * height):
        if not white[start] or labels[start] != -1:
            continue
        label = len(components)
        labels[start] = label
        queue = deque([start])
        pixels = []
        edge = False
        while queue:
            pos = queue.popleft()
            pixels.append(pos)
            x, y = pos % width, pos // width
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                edge = True
            for nxt in (pos - 1 if x else -1,
                        pos + 1 if x < width - 1 else -1,
                        pos - width if y else -1,
                        pos + width if y < height - 1 else -1):
                if nxt >= 0 and white[nxt] and labels[nxt] == -1:
                    labels[nxt] = label
                    queue.append(nxt)
        components.append((pixels, edge))

    # Only edge-connected white areas are safe anchors. A closed image
    # without white background is left unchanged, not guessed.
    exterior = {i for i, (_, edge) in enumerate(components) if edge}
    if not exterior:
        return image, 0

    # Keep a full bridge stroke inside the raster, and avoid cutting
    # through a second white island. Horizontal mode favors side exits
    # for lettering inside a black nameplate.
    half_width = (bridge_pixels + 1) // 2

    def stroke_is_safe(x1, y1, x2, y2, label):
        if x1 == x2:
            if x1 - half_width < 0 or x1 + half_width >= width:
                return False
            for yy in range(min(y1, y2), max(y1, y2) + 1):
                for xx in range(x1 - half_width, x1 + half_width + 1):
                    other = labels[yy * width + xx]
                    if other != -1 and other != label and other not in exterior:
                        return False
        else:
            if y1 - half_width < 0 or y1 + half_width >= height:
                return False
            for xx in range(min(x1, x2), max(x1, x2) + 1):
                for yy in range(y1 - half_width, y1 + half_width + 1):
                    other = labels[yy * width + xx]
                    if other != -1 and other != label and other not in exterior:
                        return False
        return True

    painter = QPainter(image)
    pen = QPen(QColor("white"), bridge_pixels, Qt.PenStyle.SolidLine,
               Qt.PenCapStyle.FlatCap)
    painter.setPen(pen)
    count = 0
    try:
        for label, (pixels, edge) in enumerate(components):
            if edge:
                continue
            best = None
            # Search straight paths from the island boundary toward
            # the existing exterior white background.
            # Sample component boundary only, not every interior pixel.
            # Stable middle-out scan reduces corner attachments.
            for pos in pixels:
                x, y = pos % width, pos // width
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy, distance = x + dx, y + dy, 1
                    while 0 <= xx < width and 0 <= yy < height:
                        other = labels[yy * width + xx]
                        if other == label:
                            break
                        if other in exterior:
                            if stroke_is_safe(x, y, xx, yy, label):
                                horizontal = dy == 0
                                penalty = (3 if orientation == "horizontal" and not horizontal
                                           else 3 if orientation == "vertical" and horizontal
                                           else 1)
                                score = distance * penalty
                                if best is None or score < best[0]:
                                    best = (score, x, y, xx, yy)
                            break
                        if other != -1:
                            break
                        if best is not None and distance >= best[0]:
                            break
                        xx += dx
                        yy += dy
                        distance += 1
            if best:
                _, x1, y1, x2, y2 = best
                painter.drawLine(x1, y1, x2, y2)
                count += 1
    finally:
        painter.end()
    return image, count
