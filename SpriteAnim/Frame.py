from PySide2.QtCore import QPointF, Qt, QRectF, QSizeF, QRect
from PySide2.QtGui import QPen, QColor

import TextureMgr
from TextureMgr import *


class Frame:
    """Frame class"""

    type = 0
    id = 0
    tex = None
    symbol = None

    TYPE_EMPTY = 0  # This should never be used
    TYPE_FRAME = 1
    TYPE_KEY = 2

    CONTENT_EMPTY = 0
    CONTENT_TEXTURE = 1
    CONTENT_SYMBOL = 2
    CONTENT_POINT = 3

    def __init__(self, frameNo, contentType):
        # self.type = type
        self.frameNo = frameNo
        self.contentType = contentType
        self.type = Frame.TYPE_EMPTY
        self.keyFrameStart = None
        self.keyFrameEnd = None

        # set in Layer-> add symbol
        self.layer = None
        self.isTween = 0
        self.pos = QPointF(0, 0)

        self.tex = None
        self.texturePath = None
        self.srcRect = QRect(0, 0, 0, 0)

        self.symbol = None

        # Some editor stuff
        self.isDragging = 0
        self.isSelected = 0

    def clone(self):
        f = Frame(self.frameNo, self.contentType)
        f.type = self.type
        f.keyFrameStart = self.keyFrameStart
        f.keyFrameEnd = self.keyFrameEnd

        f.layer = self.layer
        f.isTween = self.isTween
        f.pos = QPointF(self.pos.x(), self.pos.y())

        f.tex = self.tex
        f.texturePath = self.texturePath
        f.srcRect = self.srcRect.__copy__()

        f.symbol = self.symbol

        return f

    # Set Keyframe functions
    def setTexture(self, path):
        self.texturePath = path
        self.tex = TextureMgr.textureMgr().loadImage(path)
        self.srcRect = QRect(0, 0, self.tex.width(), self.tex.height())
        print("self.tex is ", self.tex)
        self.contentType = Frame.CONTENT_TEXTURE
        self.type = Frame.TYPE_KEY
        self.pos.setX(-self.srcRect.width() / 2)
        self.pos.setY(-self.srcRect.height() / 2)

    def setEmpty(self):
        self.contentType = Frame.CONTENT_EMPTY
        self.type = Frame.TYPE_KEY

    def getOffs(self):
        offs = QPointF(0, 0)
        if self.isDragging:
            # print "Dragpos is ",  self.dragPos
            return self.dragPos

        texToDraw = self.tex
        symToDraw = self.symbol

        if self.type == Frame.TYPE_FRAME:
            kfStart = self.layer.frames[self.keyFrameStart]
            kfEnd = self.layer.frames[self.keyFrameEnd]
            if self.isTween:
                t = (self.frameNo - self.keyFrameStart) / (self.keyFrameEnd - self.keyFrameStart)
                offs.setX(t * (kfEnd.pos.x() - kfStart.pos.x()))
                offs.setY(t * (kfEnd.pos.y() - kfStart.pos.y()))
            else:
                offs.setX(kfStart.pos.x())
                offs.setY(kfStart.pos.y())

        elif self.type == Frame.TYPE_KEY:
            offs = QPointF(self.pos)

        return offs

    def setPos(self, pos):
        if not self.isKey():
            return

        self.pos = pos

    def draw(self, painter):
        texToDraw = self.tex
        symToDraw = self.symbol

        if self.type == Frame.TYPE_FRAME:
            kfStart = self.layer.frames[self.keyFrameStart]
            kfEnd = self.layer.frames[self.keyFrameEnd]

            if self.contentType == Frame.CONTENT_TEXTURE:
                texToDraw = kfStart.tex

            if self.contentType == Frame.CONTENT_SYMBOL:
                print("todo... symbol playback stuff")

        offs = self.getOffs()

        if self.contentType == Frame.CONTENT_TEXTURE:
            painter.drawPixmap(QRect(offs.x(), offs.y(), self.srcRect.width(), self.srcRect.height()),
                               texToDraw,
                               self.srcRect)

        elif self.contentType == Frame.CONTENT_SYMBOL:
            print("todo... symbol drawing")

        if self.isSelected:
            pen = QPen(Qt.SolidLine)
            pen.setColor(QColor(0, 0, 0, 255))
            painter.setPen(pen)

            painter.setBrush(Qt.NoBrush)

            bb = self.boundingBox()

            painter.drawRect(bb)

        # frame = sym.layers[0].frames[f];

    def isKey(self):
        return self.type == Frame.TYPE_KEY

    def isFrame(self):
        return self.type == Frame.TYPE_FRAME

    def boundingBox(self):
        if self.contentType == Frame.CONTENT_EMPTY:
            return None

        if self.contentType == Frame.CONTENT_TEXTURE:
            return QRectF(self.getOffs(), QSizeF(self.srcRect.width(), self.srcRect.height()))

        if self.contentType == Frame.CONTENT_SYMBOL:
            # todo: get frame number at this position:
            return self.symbol.boundingBoxForFrame(self.frameNo)

    def startDragging(self):
        self.dragPos = self.getOffs()
        self.isDragging = True

    def stopDragging(self):
        self.isDragging = False

    def dragDelta(self, d):
        self.dragPos += d

    def setSelected(self, s):
        self.isSelected = s

    def getLayerNo(self):
        return self.layer.layerNo
