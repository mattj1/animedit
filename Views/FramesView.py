import math

from PySide2.QtCore import QPoint, QRect, Qt, QRectF
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor, QPen
from PySide2.QtWidgets import QWidget

from Editor import Editor
from SpriteAnim.Frame import Frame


class FramesView(QWidget):
    def __init__(self, editor: Editor, parent=None):
        super(FramesView, self).__init__(parent)

        self.editor = editor

        self.setAutoFillBackground(False)

        self.leftFrame = 0
        self.topHeight = 25

        self.parent = parent

        self.selectingFrames = 0

        # actual mouse select points
        self.select0 = QPoint(0, 0)
        self.select1 = QPoint(0, 0)

        # selection box rendering - draw if self.selectingFrames
        self.selectBox0 = QPoint(0, 0)
        self.selectBox1 = QPoint(0, 0)

    def top_layer(self):
        return self.editor.top_layer

    def paintEvent(self, event):
        sym = self.editor.current_symbol()

        sw = self.width()
        sh = self.height()

        cw = 8
        ch = 18

        tw = sw
        th = sh - self.topHeight

        tTop = self.topHeight

        numCol = int(math.floor(sw / cw)) + 1
        numRow = int(math.floor(th / ch)) + 1
        # if( self.layerView.topLayer + numRow > sym.numLayers())

        lastRow = self.top_layer() + numRow

        if lastRow > sym.numLayers():
            lastRow = sym.numLayers()

        if self.top_layer() + numRow > lastRow:
            numRow = lastRow - self.top_layer()

        if numRow < 0:
            numRow = 0

        rightFrame = self.leftFrame + numCol

        painter = QPainter(self)

        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(214, 214, 214, 255))
        painter.drawRect(0, 0, sw, self.topHeight)

        painter.setBrush(QColor(255, 255, 255, 255))
        painter.drawRect(0, tTop, sw, sh)

        pen = QPen(Qt.SolidLine)
        pen.setColor(QColor(222, 222, 222, 255))
        painter.setPen(pen)

        keyframePen = QPen(Qt.SolidLine)
        keyframePen.setColor(QColor(0, 0, 0, 255))
        # painter.save()

        # painter.drawLine(0,0, self.width(), self.height() )

        # draw highlighted columns
        painter.setBrush(QColor(237, 237, 237, 255))

        hf = self.leftFrame
        if self.leftFrame % 5 != 0:
            hf = 5 + (self.leftFrame - (self.leftFrame % 5))

        for x in range(hf, rightFrame, 5):
            f = x - self.leftFrame
            painter.drawRect(f * cw, tTop, cw, numRow * ch)

        pen.setColor(QColor(222, 222, 222, 255))
        painter.setPen(pen)

        # draw grid
        painter.setBrush(QColor(222, 222, 222, 255))
        for x in range(0, numCol):
            painter.drawLine(x * cw, tTop - 2, x * cw, tTop + numRow * ch)

        for y in range(0, numRow + 1):
            painter.drawLine(0, tTop + y * ch, sw, tTop + y * ch)

        # draw layer frame info

        frameColor = QColor(127, 127, 127, 255)

        y = 0

        for l in range(self.top_layer(), lastRow):
            x = 0
            for f in range(self.leftFrame, rightFrame):
                cx = x * cw
                cy = tTop + y * ch
                if f < sym.layers[l].numFrames():
                    frame = sym.layers[l].frames[f]

                    # also, figure out the color if the frame is selected
                    # print "Drawing contentType ",  frame.contentType
                    if frame.contentType == Frame.CONTENT_EMPTY:
                        fill = QColor(255, 255, 255, 255)
                    else:
                        fill = frameColor;

                    if frame.type == Frame.TYPE_KEY:
                        painter.setBrush(fill)
                        painter.setPen(Qt.NoPen)
                        painter.drawRect(x * cw, tTop + y * ch, cw, ch)

                        if frame.contentType == Frame.CONTENT_EMPTY:
                            painter.setBrush(QColor(255, 255, 255, 255))
                        else:
                            painter.setBrush(QColor(0, 0, 0, 255))
                        painter.setPen(keyframePen)

                        painter.drawEllipse(cx + 2, cy + 8, 4, 4)

                        painter.setPen(keyframePen)
                        painter.drawLine(cx, cy, cx + cw, cy)
                        painter.drawLine(cx, cy, cx, cy + ch)
                        painter.drawLine(cx, cy + ch, cx + cw, cy + ch)

                    elif frame.type == Frame.TYPE_FRAME:
                        # print "Drawing basic frame"
                        painter.setBrush(fill)
                        painter.setPen(Qt.NoPen)
                        painter.drawRect(x * cw, tTop + y * ch, cw, ch)

                        painter.setPen(keyframePen)
                        painter.drawLine(cx, cy, cx + cw, cy)
                        painter.drawLine(cx, cy + ch, cx + cw, cy + ch)

                    # painter.drawLine(x  *cw , tTop + y * ch, x*cw+cw, tTop + y * ch + ch )

                    if f == sym.layers[l].numFrames() - 1:
                        painter.setPen(keyframePen)
                        painter.drawLine(cx + cw, cy, cx + cw, cy + ch)

                if self.editor.selected_frame_range.contains(f, l):
                    painter.setBrush(QColor(0, 0, 255, 127))
                    painter.drawRect(x * cw, tTop + y * ch, cw, ch)
                x += 1

            y += 1

        topLayer = self.top_layer()
        framesRect = QRect(self.leftFrame, topLayer, numCol - self.leftFrame, numRow - topLayer)

        # draw mouse selection box
        if self.selectingFrames:
            selectRect = QRect(self.selectBox0.x(), self.selectBox0.y(), self.selectBox1.x() - self.selectBox0.x() + 1,
                               self.selectBox1.y() - self.selectBox0.y() + 1)

            r = selectRect.intersected(framesRect)

            # print r
            painter.setBrush(QColor(0, 0, 255, 127))
            painter.drawRect((r.x() - self.leftFrame) * cw, tTop + (r.y() - topLayer) * ch, r.width() * cw,
                             r.height() * ch)

        # draw frame numbers
        pen.setColor(QColor(0, 0, 0, 255))
        painter.setPen(pen)

        for x in range(hf, rightFrame, 5):
            f = x - self.leftFrame
            painter.drawText(QRectF(f * cw + 4 - 16, 0, 32, ch), Qt.AlignHCenter, str(x))

        # Draw play position
        pen.setColor(QColor(255, 0, 0, 255))
        painter.setPen(pen)
        current_frame = self.editor.frame_number()

        if current_frame >= self.leftFrame and current_frame <= rightFrame:
            x = (current_frame - self.leftFrame)
            painter.drawLine(x * cw + 4, tTop - 4, x * cw + 4, sh)

        painter.resetTransform()

    def updateSelectionBox(self):
        self.selectBox0.setX(min(self.select0.x(), self.select1.x()))
        self.selectBox0.setY(min(self.select0.y(), self.select1.y()))

        self.selectBox1.setX(max(self.select0.x(), self.select1.x()))
        self.selectBox1.setY(max(self.select0.y(), self.select1.y()))

    def pixelToFrameNo(self, x):
        return int(self.leftFrame + (x - (x % 8)) / 8)

    def pixelToLayerNo(self, y):
        _layer_no = int(self.editor.top_layer + (y - (y % 18)) / 18)

        if _layer_no < 0:
            _layer_no = 0

        return _layer_no

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        deselect = False

        self.setFrameEvent(self.leftFrame + (x - (x % 8)) / 8)

        # if( y < self.topHeight):
        #    self.setFrameEvent(self.leftFrame + (x - (x%8))/8)
        # else:
        if y >= self.topHeight:

            sym = self.editor.current_symbol()

            layerNo = int(self.pixelToLayerNo(y - self.topHeight))

            if layerNo >= sym.numLayers():
                # layerNo = sym.numLayers() - 1;
                deselect = True
            else:
                self.selectingFrames = 1
                self.select0.setX(self.pixelToFrameNo(x))
                self.select1.setX(self.select0.x())

                self.select0.setY(layerNo)
                self.select1.setY(self.select0.y())

                self.updateSelectionBox()
                self.repaint()
        else:
            deselect = True

        if deselect:
            self.editor.clear_selected_frame_range_action()

    def mouseReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if self.selectingFrames == 1:
            sym = self.editor.current_symbol()

            if self.selectBox1.y() < 0:
                self.selectBox1.setY(0)

            selected_frames = QRect(self.selectBox0.x(), self.selectBox0.y(),
                                    self.selectBox1.x() - self.selectBox0.x() + 1,
                                    self.selectBox1.y() - self.selectBox0.y() + 1)

            layerNo = int(self.pixelToLayerNo(y - self.topHeight))
            if layerNo >= sym.numLayers():
                layerNo = sym.numLayers() - 1

            # self.parent.setSelectedLayer( layerNo )

            self.editor.select_frames_action(selected_frames, layerNo)

            self.selectingFrames = 0
            self.repaint()

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if self.selectingFrames == 1:
            # update the selection

            sym = self.editor.current_symbol()

            layerNo = int(self.pixelToLayerNo(y - self.topHeight))

            if layerNo >= sym.numLayers():
                layerNo = sym.numLayers() - 1

            self.select1.setX(self.pixelToFrameNo(x))
            self.select1.setY(layerNo)
            self.updateSelectionBox()
            self.repaint()

        self.setFrameEvent(self.leftFrame + (x - (x % 8)) / 8)

    def setFrameEvent(self, f):
        self.editor.set_frame_number(int(f))

    def setLeftFrame(self, f):
        self.leftFrame = f
        self.repaint()
