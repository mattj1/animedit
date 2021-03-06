from PySide2.QtCore import QRectF, QMimeData
from PySide2.QtGui import Qt, QColor, QPen, QPainter, QDrag
from PySide2.QtWidgets import QWidget, QHBoxLayout

import TextureMgr
from Editor import LibraryEditor
from SpriteAnim import LibraryItem
from SpriteAnim.Library import Library


class LibraryList(QWidget):
    def __init__(self, library_editor: LibraryEditor, parent=None):
        super(LibraryList, self).__init__(parent)
        self.library_editor = library_editor
        # b = QPushButton("Preview");
        # l.addWidget(b)
        self.setLayout(QHBoxLayout())

        # Row height
        self.ch = 20

    def paintLibraryItem(self, painter, item: LibraryItem, y, selected):
        txt = item.get_name()

        painter.setPen(Qt.NoPen)
        if selected:
            painter.setBrush(QColor(214, 214, 214, 255))
            painter.drawRect(0, y, self.width(), self.ch)

        pen = QPen(Qt.SolidLine)

        # if selected: pen.setColor(QColor(255, 255, 255, 255))
        # else:
        pen.setColor(QColor(0, 0, 0, 255))

        painter.setPen(pen)

        painter.drawText(QRectF(20, y + 3, 150, 18), Qt.AlignLeft, txt)

    def paintEvent(self, event):
        sw = self.width()
        sh = self.height()

        painter = QPainter(self)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 255))
        painter.drawRect(0, 0, sw, sh)

        # render all the entries. Make this code modular so it can do the same thing without the scrollarea
        y = 0
        cnt = 0
        for i in self.library_editor.get_library().item_list():
            self.paintLibraryItem(painter, i, y, cnt == self.library_editor.selected_index)
            y = y + self.ch
            cnt = cnt + 1

        self.setMinimumSize(300, y)

    def dragLeaveEvent(self, event):
        print("drag leave ", event)

    def mousePressEvent(self, event):
        print("mouse press ", event.pos().x(), event.pos().y())
        self.library_editor.set_selected_index(int(event.pos().y() / self.ch))
        library_item = self.library_editor.selected_item()

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setData(library_item.getMimeType(), library_item.getMimeData())
        print("mime data: ", library_item.getMimeType(), mime_data.data(library_item.getMimeType()))
        drag.setMimeData(mime_data)
        drag.start()

    def refresh_view(self):
        self.repaint()
