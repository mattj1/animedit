import math

import PySide6.QtGui
from PySide6.QtCore import QRect, QLineF, Qt
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QWidget, QSlider, QVBoxLayout

from Editor import Editor
from SpriteAnim.frame import Frame


class TimelineView(QWidget):
    def __init__(self, editor: Editor, parent=None):
        super(TimelineView, self).__init__(parent)

        self.editor = editor

        layout = QVBoxLayout()

        # self.setAutoFillBackground(True)

    def get_frame_width(self):
        return 12 + 0 #self.zoomSlider.value()



    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)

        # self.zoomSlider.move(self.width() - 140, -22)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        f = event.pos().x() / self.get_frame_width()
        self.editor.frame_number = int(f)

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        f = event.pos().x() / self.get_frame_width()
        self.editor.frame_number = int(f)

    def paintEvent(self, event):
        symbol = self.editor.current_symbol

        painter = QPainter(self)
        brush = QBrush(QColor(255, 255, 255, 255))
        painter.fillRect(QRect(0, 0, self.width(), self.height()), brush)

        th = (self.height() - 25)
        num_rows = int(math.floor(th / 25)) + 1

        first_row = self.editor.top_layer
        last_row = first_row + num_rows

        if last_row >= symbol.num_layers():
            last_row = symbol.num_layers() - 1

        brush = QBrush(QColor(222, 222, 222, 255))
        painter.fillRect(QRect(0, 0, self.width(), 25), brush)

        painter.setPen(QColor(220, 220, 220, 255))

        frame_width = 12 + 0 #self.zoomSlider.value()

        for i in range(0, (last_row - first_row) + 2):
            painter.drawLine(QLineF(0, 25 + i * 25, self.width(), 25 + i * 25))

        for i in range(0, 200):
            painter.drawLine(QLineF(i * frame_width, 25, i * frame_width, (last_row + 2 - first_row) * 25))

        y = 25

        brush_empty = QBrush(QColor(255, 255, 255, 255))
        brush = QBrush(QColor(127, 127, 127, 255))
        brush_black = QBrush(QColor(0, 0, 0, 255))
        brush_motion = QBrush(QColor(127, 192, 255, 255))
        painter.setPen(QColor(0, 0, 0, 255))
        for i in range(first_row, last_row + 1):
            x = 0
            layer = symbol.layers[i]
            for frame_no in range(0, layer.num_frames()):
                frame: Frame = layer.frames[frame_no]

                painter.drawRect(QRect(x, y, frame_width, 25))
                #
                if frame.key_frame_start.contentType != Frame.CONTENT_EMPTY:
                    if frame.key_frame_start.isTween:
                        painter.fillRect(QRect(x, y + 1, frame_width, 24), brush_motion)
                    else:
                        painter.fillRect(QRect(x, y + 1, frame_width, 24), brush)


                if frame.isKey():
                    if frame.contentType == Frame.CONTENT_EMPTY:
                        painter.drawEllipse(frame_no * frame_width + frame_width / 2 - 2.5, y + 11, 6, 6)
                    else:
                        # painter.setBrush(None)
                        # painter.fillRect(QRect(x, y + 1, frame_width, 24), brush)
                        painter.setBrush(brush_black)
                        painter.drawEllipse(frame_no * frame_width + frame_width / 2 - 2.5, y + 11, 6, 6)
                else:
                    if frame.key_frame_start.contentType == Frame.CONTENT_EMPTY:
                        pass
                        # painter.fillRect(QRect(x, y + 1, frame_width, 24), brush_empty)
                    else:
                        if frame.key_frame_start.isTween:
                            # painter.fillRect(QRect(x, y + 1, frame_width, 24), brush_motion)
                            painter.drawLine(x, y + 14, x + frame_width, y + 14)
                        # else:
                        #     painter.fillRect(QRect(x, y + 1, frame_width, 24), brush)

                x += frame_width

            y += 25

        painter.drawLine(self.editor.frame_number * frame_width + frame_width / 2, 0,
                         self.editor.frame_number * frame_width + frame_width / 2, self.height())
