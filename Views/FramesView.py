import math

from PySide2.QtCore import QPoint, QRect, Qt, QRectF
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor, QPen, QBrush
from PySide2.QtWidgets import QWidget, QMenu, QAction

from Editor import Editor
from SpriteAnim.Frame import Frame


class FramesView(QWidget):
    DRAG_OP_NONE = 0
    DRAG_OP_SCRUB = 1
    DRAG_OP_SELECT = 2

    def __init__(self, editor: Editor, parent=None):
        super(FramesView, self).__init__(parent)

        self.editor = editor

        self.setAutoFillBackground(False)

        self.leftFrame = 0
        self.topHeight = 25

        self.parent = parent

        # actual mouse select points
        self.select0 = QPoint(0, 0)
        self.select1 = QPoint(0, 0)

        # selection box rendering - draw if self.selectingFrames
        self.selectBox0 = QPoint(0, 0)
        self.selectBox1 = QPoint(0, 0)

        self.drag_operation = FramesView.DRAG_OP_NONE

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

                    next_frame: Frame = sym.layers[l].get_frame(f + 1)

                    content_type_ends = False

                    if next_frame:
                        if not next_frame.is_same_content_as_frame(frame):
                            content_type_ends = True

                    # also, figure out the color if the frame is selected
                    # print "Drawing contentType ",  frame.contentType
                    if frame.contentType == Frame.CONTENT_EMPTY:
                        fill = QColor(255, 255, 255, 255)
                    else:
                        fill = frameColor

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

                    if content_type_ends and frame.type == Frame.TYPE_FRAME:
                        painter.setBrush(QColor.fromRgb(255, 255, 255, 255))
                        painter.setPen(keyframePen)
                        brush = QBrush(QColor(255, 255, 255, 255))

                        stop_rect = QRectF(cx + 2, cy + 7, 4, 6)
                        painter.fillRect(stop_rect, brush)
                        painter.drawRect(stop_rect)

                if self.editor.selected_frame_range.contains(f, l):
                    painter.setBrush(QColor(0, 0, 255, 127))
                    painter.drawRect(x * cw, tTop + y * ch, cw, ch)
                x += 1

            y += 1

        topLayer = self.top_layer()
        framesRect = QRect(self.leftFrame, topLayer, numCol - self.leftFrame, numRow - topLayer)

        # draw mouse selection box
        if self.drag_operation == FramesView.DRAG_OP_SELECT:
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

    def frame_number_at_pixel_x(self, x):
        return int(self.leftFrame + (x - (x % 8)) / 8)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if event.button() == Qt.MouseButton.LeftButton and y < self.topHeight:
            self.drag_operation = FramesView.DRAG_OP_SCRUB
            self.editor.change_selection_action(self.frame_number_at_pixel_x(x), append=False)
            return

        if y >= self.topHeight:
            self.drag_operation = FramesView.DRAG_OP_SELECT

            layerNo = int(self.pixelToLayerNo(y - self.topHeight))

            self.select0.setX(self.pixelToFrameNo(x))
            self.select1.setX(self.select0.x())

            self.select0.setY(layerNo)
            self.select1.setY(self.select0.y())

            self.updateSelectionBox()
            self.repaint()

    def action_create_motion_tween(self):
        return

    def mouseReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if event.button() == Qt.MouseButton.RightButton:
            # Maybe select the frame under the cursor?
            menu = QMenu(self)
            menu.addAction(QAction("Create &Motion Tween", self, statusTip="Create Motion Tween", triggered=self.action_create_motion_tween))
            menu.exec_(self.mapToGlobal(event.pos()))
            return

        if event.button() == Qt.MouseButton.LeftButton:
            if self.drag_operation == FramesView.DRAG_OP_SCRUB:
                self.editor.change_selection_action(self.frame_number_at_pixel_x(x), append=True)

            if self.drag_operation == FramesView.DRAG_OP_SELECT:
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

                # TODO: The current frame and layer should be updated here
                self.editor.select_frames_action(selected_frames, layerNo)

                self.repaint()

            self.drag_operation = FramesView.DRAG_OP_NONE

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if self.drag_operation == FramesView.DRAG_OP_SCRUB:
            self.editor.change_selection_action(self.frame_number_at_pixel_x(x), append=True)

        if self.drag_operation == FramesView.DRAG_OP_SELECT:
            # update the selection

            sym = self.editor.current_symbol()

            layerNo = int(self.pixelToLayerNo(y - self.topHeight))

            if layerNo >= sym.numLayers():
                layerNo = sym.numLayers() - 1

            self.select1.setX(self.pixelToFrameNo(x))
            self.select1.setY(layerNo)
            self.updateSelectionBox()
            self.repaint()


    def setFrameEvent(self, f):
        self.editor.set_frame_number(int(f))

    def setLeftFrame(self, f):
        self.leftFrame = f
        self.repaint()
