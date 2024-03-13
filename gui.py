from PySide6.QtGui import QPalette, QPixmap

from PIL import Image, ImageQt
from PySide6 import QtWidgets
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication, QStackedLayout, QWidget, QScrollArea
from PySide6.QtWidgets import QGridLayout

from draw import ToucTile
from pylcf.main import lcf_to_dict

# Create the Qt Application
print("Launching app...")
app = QApplication([])
print("App initialized")

loaded_map = lcf_to_dict(r"E:\games and tools\dev\CU_221109\Map0128.lmu")
# combine map data into 4 byte pieces
loaded_map[71] = [''.join(x) for x in zip(loaded_map[71][1::2], loaded_map[71][0::2])]
loaded_map[72] = [''.join(x) for x in zip(loaded_map[72][1::2], loaded_map[72][0::2])]

cached_tile_images = {}

chipset_image = Image.open(r"maple-cherry.png")
# make index 0 transparent
chipset_transparency_colour = (chipset_image.getpalette()[0], chipset_image.getpalette()[1], chipset_image.getpalette()[2], 255)
chipset_image = chipset_image.convert("RGBA")
pixdata = chipset_image.load()
for y in range(chipset_image.size[1]):
    for x in range(chipset_image.size[0]):
        if pixdata[x, y] == chipset_transparency_colour:
            pixdata[x, y] = (0, 0, 0, 0)
print("converting chipset to pixmap...")
chipset_image = QPixmap.fromImage(ImageQt.ImageQt(chipset_image))
print("done!")
class LayerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def init_layout(self):
        self.layer_gridlayout = QGridLayout()
        self.layer_gridlayout.setHorizontalSpacing(0)
        self.layer_gridlayout.setVerticalSpacing(0)
        self.setLayout(self.layer_gridlayout)
        # Populate grid
        global loaded_map
        # Get the height and width.
        self.height = loaded_map[3]
        self.width = loaded_map[2]



class BottomLayerWidget(LayerWidget):
    def __init__(self):
        super().__init__()
        global chipset_image, cached_tile_images
        self.init_layout()
        # Draw layer

        for i in range(0, len(loaded_map[71])):
            self.current_tile = loaded_map[71][i]
            # Calculate which tile to draw and turn it into a 16x16 QPixmap
            # Autotiles
            # Non-autotiles
            self.pixmapped_tile = ToucTile()
            self.pixmapped_tile.tile_id = int(loaded_map[71][i], 16)
            cached_tile_images = self.pixmapped_tile.draw_normal_tile(cached_tile_images, chipset_image)
            self.layer_gridlayout.addWidget(self.pixmapped_tile, i // self.width, i % self.width)


class UpperLayerWidget(LayerWidget):
    def __init__(self):
        super().__init__()
        global chipset_image, cached_tile_images
        self.init_layout()
        print("honk")
        # Draw layer
        for i in range(0, len(loaded_map[72])):  # height
            self.current_tile = loaded_map[72][i]
            # Calculate which tile to draw and turn it into a 16x16 QPixmap
            self.pixmapped_tile = ToucTile()
            self.pixmapped_tile.tile_id = int(loaded_map[72][i], 16)
            cached_tile_images = self.pixmapped_tile.draw_normal_tile(cached_tile_images, chipset_image)
            self.layer_gridlayout.addWidget(self.pixmapped_tile, i // self.width, i % self.width)




map_widget = QWidget()
background_widget = QWidget()
background_widget.setStyleSheet(r'background-image: url(maple-palace1.png)')
# this is the quickest and dirtiest fix in the history of quick dirty fixes
map_layout = QStackedLayout()
# map_widget.setMaximumSize(loaded_map[2]*16, loaded_map[3]*16)
map_widget.setLayout(map_layout)
map_layout.setStackingMode(QStackedLayout.StackAll)
map_layout.insertWidget(2, UpperLayerWidget())
map_layout.insertWidget(1, BottomLayerWidget())
map_layout.insertWidget(0, background_widget)

map_scroll_area = QScrollArea()
map_scroll_area.setBackgroundRole(QPalette.Dark)
map_scroll_area.setWidget(map_widget)
map_scroll_area.setMaximumSize(800, 600)



print("bogus")
map_scroll_area.show()
app.exec()