import math

from PySide2.QtCore import QRectF, QSize
from PySide2.QtGui import QPainter, Qt, QColor, QPen
from PySide2.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton

from Editor import Editor


class LayerListView(QWidget):
    def __init__(self, editor: Editor, parent=None):
        super(LayerListView, self).__init__(parent)
        self.editor = editor
        self.topHeight = 25

        self.setMinimumWidth(280)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        # self.setMinimumHeight(280)
        self.ch = 18

        self.box_layout = QVBoxLayout()
        self.box_layout.setContentsMargins(0, 25, 0, 0)

        self.setLayout(self.box_layout)

        addLayerButton = QPushButton('+')
        addLayerButton.setMaximumSize(16, 16)
        self.box_layout.addWidget(addLayerButton)

        # self.listwidget = QListWidget(self)
        # self.listwidget.setSpacing(0)
        #
        # for i in range(0, 10):
        #     item = QListWidgetItem()
        #     item.setText("TEST")
        #     item.setSizeHint(QSize(0, 18))
        #     item.setBackgroundColor(QColor.fromRgb(255,0,0,255))
        #     item.
        #
        #     self.listwidget.addItem(item)
        #
        # self.box_layout.addWidget(self.listwidget)

    def top_layer(self):
        return self.editor.top_layer

    def paintEvent(self, event):
        sw = self.width()
        sh = self.height()
        tTop = self.topHeight
        ch = 18

        tw = sw
        th = sh - self.topHeight

        current_symbol = self.editor.current_symbol()

        numRow = int(math.floor(th / ch)) + 1

        lastRow = self.top_layer() + numRow
        if lastRow > current_symbol.numLayers():
            lastRow = current_symbol.numLayers()

        # Figure out what layers to render

        painter = QPainter(self)

        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(214, 214, 214, 255))
        painter.drawRect(0, 0, sw, self.topHeight)

        pen = QPen(Qt.SolidLine)
        pen.setColor(QColor(222, 222, 222, 255))
        painter.setPen(pen)

        y = 0

        for l in range(self.top_layer(), lastRow):

            pen.setColor(QColor(222, 222, 222, 255))
            painter.setPen(pen)

            if l == self.editor.layer_index():
                painter.setBrush(QColor(0, 0, 127, 255))
            else:
                painter.setBrush(QColor(255, 255, 255, 255))

            painter.drawRect(0, tTop + y * ch, sw, ch)

            if l == self.editor.layer_index():
                pen.setColor(QColor(255, 255, 255, 255))
            else:
                pen.setColor(QColor(0, 0, 0, 255))

            painter.setPen(pen)

            painter.drawText(QRectF(20, tTop + y * ch + 3, 150, ch), Qt.AlignLeft,
                             current_symbol.layers[l].name)

            y += 1

    def mousePressEvent(self, event):
        y = event.pos().y() - self.topHeight

        if y < 0:
            return

        l = int(self.top_layer() + (y - (y % self.ch)) / self.ch)

        if l >= self.editor.current_symbol().numLayers():
            return

        self.editor.select_layer_action(l)

    def wheelEvent(self, event):

        _top_layer = self.top_layer()

        if event.delta() < 0:
            _top_layer += 1
        elif event.delta() > 0:
            _top_layer -= 1

        if _top_layer < 0:
            _top_layer = 0
        # todo: max

        self.editor.set_top_layer(_top_layer)

    def setLayer(self, n):
        self.selectedLayer = n
        self.repaint()
