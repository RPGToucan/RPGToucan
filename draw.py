from PIL.ImageQt import ImageQt
from PySide6 import QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPixmap, QColor


class ToucTile(QLabel):
    def __init__(self):
        super().__init__()
        self.tile_id = 0
        self.autotile_corners = [0, 0, 0, 0]

    def draw_normal_tile(self, cached_tile_location, chipset_image):
        """
        Attaches a QPixmap containing the tile graphic to the ToucTile it is used on,
        and returns the cached tiles.

        :param cached_tile_location: Location of the cached tile images in global.
        :param chipset_image: The image to use as a chipset.
        """
        # If the image has been cached before, fetch it; otherwise cache it
        if self.tile_id not in cached_tile_location:
            print("Found new tile", self.tile_id)
            tile_calc = 0
            if 5000 <= self.tile_id <= 5142:
                tile_calc = self.tile_id - 5000
            elif 10000 <= self.tile_id <= 10142:
                tile_calc = self.tile_id - 9856
            # Get image position
            imgpos_x = 192 + ((tile_calc % 6) * 16) + (96 * (tile_calc // 96))# leftmost pixel
            imgpos_y = (tile_calc // 6) * 16 - (256 * (tile_calc // 96)) # uppermost pixel

            # input pixmap is chipset_image
            output_pixmap = QPixmap(16, 16)
            output_pixmap.fill(QColor(0, 0, 0, 0))
            painter = QPainter(output_pixmap)
            painter.drawPixmap(0, 0, chipset_image.copy(imgpos_x, imgpos_y, 16, 16))
            cached_tile_location[self.tile_id] = output_pixmap
            # current_tile_image = PIL.ImageOps.scale(current_tile_image, 1, PIL.Image.Resampling.NEAREST)
            # The above line of code is old scaling implementation.
            # I will hopefully replace it on a QT level sometime...

        self.setPixmap(cached_tile_location[self.tile_id])
        return cached_tile_location
