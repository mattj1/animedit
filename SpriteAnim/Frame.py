from PySide6.QtCore import QPoint, QPointF, QRect

import TextureMgr


class Frame:
    """Frame class"""

    type = 0
    id = 0
    tex = None
    symbol = None

    TYPE_FRAME = 1
    TYPE_KEY = 2

    CONTENT_EMPTY = 0
    CONTENT_TEXTURE = 1
    CONTENT_SYMBOL = 2
    CONTENT_POINT = 3

    pos: QPoint

    def __init__(self, frame_no, content_type, frame_type=TYPE_FRAME):
        self.type = frame_type
        self.frameNo = frame_no
        self.layer = None

        # Keyframe data ---------------------------------------------
        self.contentType = content_type
        self.pos = QPoint(0, 0)
        self.isTween = 0

        # Texture content
        self.texture_ref = None

        # self.tex = None
        self.srcRect = QRect(0, 0, 0, 0)

        # Reference to the symbol content
        self.symbol_ref = None

        # Set the frame of the symbol content. -1 means do not set the frame
        self.symbol_frame = -1

        # Cached frame data (re-calculated often) -------------------
        self.key_frame_start = None
        self.key_frame_end = None
        self.cached_symbol_frame = -1

        # UI/Editor stuff -------------------------------------------
        self.tempOffset = QPoint(0, 0)
        self.isDragging = 0
        self.isSelected = 0

    def __repr__(self) -> str:
        s = f"<Frame {self.frameNo}: "
        if self.isKey():
            s += "\u23fa "

            s += "contentType="
            if self.contentType == Frame.CONTENT_EMPTY:
                s += "EMPTY"

            if self.contentType == Frame.CONTENT_TEXTURE:
                s += "TEXTURE "
                s += f" {self.texture_ref.path} {self.get_texture()}"

            if self.contentType == Frame.CONTENT_SYMBOL:
                s += f"SYMBOL {self.symbol_ref.name} {self.get_symbol()}"

            if self.contentType == Frame.CONTENT_POINT:
                s += "POINT"

        else:
            if self.key_frame_start is None:
                s += "(No starting keyframe)"
            else:
                s += f"{self.key_frame_start.frameNo}"

            s += " -> "
            if self.key_frame_end is None:
                s += "(No ending keyframe)"
            else:
                s += f"{self.key_frame_end.frameNo}"

        s += f' [ {self.cached_symbol_frame} ]'
        s += ">"
        return s

    def clone(self):
        f = Frame(self.frameNo, self.contentType)
        f.type = self.type
        f.keyFrameStart = self.keyFrameStart
        f.keyFrameEnd = self.keyFrameEnd

        f.layer = self.layer
        f.isTween = self.isTween
        f.pos = QPoint(self.pos.x(), self.pos.y())

        f.tex = self.tex
        f.texturePath = self.texturePath
        f.srcRect = self.srcRect.__copy__()

        f.symbol_ref = self.symbol_ref

        return f

    def get_key_frame_start(self):
        if self.isKey():
            return self

        return self.key_frame_start

    def get_symbol(self):
        if self.get_key_frame_start().contentType == Frame.CONTENT_SYMBOL:
            return self.get_key_frame_start().symbol_ref.get_symbol()

        return None

    def get_texture(self):
        if self.get_key_frame_start().contentType == Frame.CONTENT_TEXTURE:
            return self.get_key_frame_start().texture_ref.get_texture()

        return None

    def is_same_content_as_frame(self, other):
        raise "WIP"
        other: Frame

        key_frame = self.layer.keyframeForFrame(self.frameNo)

        if key_frame.contentType != other.contentType:
            return False

        if key_frame.contentType == Frame.CONTENT_TEXTURE:
            if key_frame.texturePath != other.texturePath:
                return False

        if key_frame.contentType == Frame.CONTENT_SYMBOL:
            if key_frame.symbol_ref != other.symbol_ref:
                return False

        return True

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

    def setSymbol(self, symbol):
        assert "No longer implemented"

        self.symbol = symbol
        self.contentType = Frame.CONTENT_SYMBOL
        # self.type = Frame.TYPE_KEY
        self.pos.setX(0)
        self.pos.setY(0)

    def setEmpty(self):
        self.contentType = Frame.CONTENT_EMPTY
        self.type = Frame.TYPE_KEY

    def getOffs(self) -> QPointF:

        if self.isDragging:
            # print "Dragpos is ",  self.dragPos
            return QPointF(self.pos.x() + self.tempOffset.x(), self.pos.y() + self.tempOffset.y())

        offs = QPointF(0, 0)

        assert "WIP"

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

        tex_to_draw = None

        key_frame = self

        if self.type == Frame.TYPE_FRAME:
            key_frame = self.layer.frames[self.keyFrameStart]
            kfEnd = self.layer.frames[self.keyFrameEnd]

            if self.contentType == Frame.CONTENT_SYMBOL:
                print("todo... symbol playback stuff")

        offs = key_frame.getOffs()

        if key_frame.contentType == Frame.CONTENT_TEXTURE:
            painter.drawPixmap(QRect(offs.x(), offs.y(), key_frame.srcRect.width(), key_frame.srcRect.height()),
                               key_frame.tex,
                               key_frame.srcRect)

        elif key_frame.contentType == Frame.CONTENT_SYMBOL:
            print("todo... symbol drawing")

            print("Playing symbol {}: {}".format(key_frame.symbol.name, self.cached_symbol_frame))
            key_frame.symbol.drawFrame(frame_number=self.cached_symbol_frame, painter=painter)

        if self.isSelected:
            pen = QPen(Qt.SolidLine)
            pen.setColor(QColor(0, 0, 0, 255))
            painter.setPen(pen)

            painter.setBrush(Qt.NoBrush)

            bb = self.boundingBox()
            if bb:
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
            return self.symbol.boundingBoxForFrame(self.cached_symbol_frame)

    def startDragging(self):
        self.tempOffset = QPointF(0, 0)
        self.isDragging = True

    def stopDragging(self):
        self.isDragging = False

    def set_temp_offset(self, offs_x, offs_y):
        self.tempOffset.setX(offs_x)
        self.tempOffset.setY(offs_y)

    def setSelected(self, s):
        self.isSelected = s

    def getLayerNo(self):
        return self.layer.layerNo
