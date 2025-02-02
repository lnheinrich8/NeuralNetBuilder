from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt


class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basic Drawing Example")
        self.resize(380, 300)
        self.WIDTH = 380
        self.HEIGHT = 300
        self.layer_xpos = []

    # WIDTH=980, HEIGHT=560
    def paintEvent(self, event):
        """This method is called whenever the widget needs to be repainted."""
        painter = QPainter(self)
        # Set up a pen (for drawing lines and outlines)
        pen = QPen(Qt.white, 1)
        painter.setPen(pen)

        # draw layers if any or changed val in spinbox
        for index, x in enumerate(self.layer_xpos):
            if index == 0:
                pen = QPen(Qt.green, 1)
                painter.setPen(pen)
                painter.drawLine(x, 20, x, self.HEIGHT-40)
                pen = QPen(Qt.white, 1)
                painter.setPen(pen)
            elif index == len(self.layer_xpos) - 1:
                pen = QPen(Qt.red, 1)
                painter.setPen(pen)
                painter.drawLine(x, 20, x, self.HEIGHT-40)
                pen = QPen(Qt.white, 1)
                painter.setPen(pen)
            else:
                painter.drawLine(x, 0, x, self.HEIGHT-20)

        painter.end()

    def draw_layers(self, layer_count):
        self.layer_xpos = []
        spacing = (self.WIDTH-20) // (layer_count + 1)
        spacing_c = 0
        for i in range(layer_count+1):
            spacing_c += spacing
            if i != layer_count:
                self.layer_xpos.append(spacing_c)
        self.update()











