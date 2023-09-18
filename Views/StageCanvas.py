# generic canvas for rendering a symbol or texture
from abc import abstractmethod
from typing import Optional

import PySide6
from PySide6.QtCore import QPoint, QPointF, Qt, QRect
from PySide6.QtGui import QPainter, QColor, QTransform, QPen, QPixmap, QWheelEvent
from PySide6.QtWidgets import QWidget, QApplication

import TextureMgr
from SpriteAnim import Symbol
from SpriteAnim.frame import Frame
from SpriteAnim.library import TextureLibraryItem, SymbolLibraryItem


class StageCanvas(QWidget):
    def __init__(self, parent=None):
        super(StageCanvas, self).__init__(parent)

        self.symbol: Symbol = None
        self.transform = QTransform()
        self.canDrag = 0

        self.last_mouse_point = QPoint(0, 0)
        self.camera = QPointF(0, 0)

        # Is dragging camera
        self.move_camera = False

        self.zoom = 1.0

        self.isSymbol = 1

        self.moveCamera = False

        self.selecting = False
        self.select0 = None
        self.select1 = None
        self.selectBox0 = QPointF(0, 0)
        self.selectBox1 = QPointF(0, 0)
        self.selectBox = None

        self.setMouseTracking(True)

    @abstractmethod
    def get_symbol(self) -> Symbol:
        raise NotImplemented

    @abstractmethod
    def get_texture(self) -> QPixmap:
        return None

    def is_symbol(self):
        return self.get_symbol() is not None

    def is_texture(self):
        return self.get_texture() is not None

    def draw_symbol_frame(self, symbol: Symbol, frame_no: int, painter: QPainter):
        for i in range(0, symbol.num_layers()):
            layer = symbol.layers[i]
            frame = layer.get_frame(frame_no)
            if not frame:
                continue

            kf0: Frame = frame.key_frame_start

            offs = frame.getOffs()

            self.transform.translate(offs.x(), offs.y())
            painter.setTransform(self.transform)

            # print(f"will draw content {offs} from ", kf0)

            if kf0.contentType == Frame.CONTENT_TEXTURE:
                item: TextureLibraryItem = kf0.texture_ref.get_texture()
                tex: QPixmap = item.get_texture()

                painter.drawPixmap(QRect(0, 0, tex.width(), tex.height()), item.get_texture(), QRect(0, 0, tex.width(), tex.height()))

            if kf0.contentType == Frame.CONTENT_SYMBOL:
                symbol = kf0.symbol_ref.get_symbol()
                # print("draw symbol, frame #", symbol, frame.cached_symbol_frame, "pos", kf0.pos)

                self.draw_symbol_frame(symbol, frame.cached_symbol_frame, painter)

            self.transform.translate(-offs.x(), -offs.y())
            painter.setTransform(self.transform)

    def paintEvent(self, event):
        # Camera position is center of screen
        sw = self.width()
        sh = self.height()
        world_halfwidth = (sw / 2) / self.zoom
        world_halfheight = (sw / 2) / self.zoom

        world_left = -self.camera.x() - world_halfwidth
        world_right = -self.camera.x() + world_halfwidth
        world_top = -self.camera.y() - world_halfheight
        world_bottom = -self.camera.y() + world_halfheight

        # print("Paint canvas, camera: {}, {}, X range: {} {}".format(-self.camera.x(), -self.camera.y(), world_left, world_right))

        painter = QPainter(self)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 255))
        painter.drawRect(0, 0, sw, sh)

        self.transform.reset()
        self.transform.translate(sw / 2, sh / 2)
        self.transform.scale(self.zoom, self.zoom)
        self.transform.translate(self.camera.x(), self.camera.y())
        painter.setTransform(self.transform)

        # painter.translate( sw / 2,  sh / 2 )
        # painter.scale(self.zoom,  self.zoom)
        # painter.translate(self.camera)

        f = self.frame_number()
        """"
        for i in range(0, f):
            self.movie.jumpToNextFrame()
            
        """

        if self.is_symbol():
            symbol = self.get_symbol()
            self.draw_symbol_frame(symbol, f, painter=painter)
        else:
            raise NotImplemented
            tex = self.get_texture()
            if tex:
                painter.drawPixmap(-tex.width() / 2, -tex.height() / 2, tex)

        # Draw pixel grid

        pen = QPen(Qt.SolidLine)
        pen.setColor(QColor(222, 222, 222, 255))
        pen.setWidth(0.1)
        painter.setPen(pen)

        if self.zoom >= 8.0:
            for i in range(int(world_left), int(world_right)):
                if i != 0:
                    painter.drawLine(i, world_top, i, world_bottom)
            for i in range(int(world_top), int(world_bottom)):
                if i != 0:
                    painter.drawLine(world_left, i, world_right, i)

        # Draw origin lines

        pen.setColor(QColor(222, 0, 0, 222))
        pen.setWidth(0.1)
        painter.setPen(pen)

        painter.drawLine(-1000, 0, 1000, 0)
        painter.drawLine(0, -1000, 0, 1000)

        # Draw mouse selection box

        painter.setBrush(Qt.NoBrush)
        painter.resetTransform()

        if self.selecting:
            pen = QPen(Qt.DashLine)
            pen.setColor(QColor(0, 0, 0, 255))
            pen.setWidth(0.1)
            painter.setPen(pen)

            painter.drawRect(self.selectBox0.x(), self.selectBox0.y(), self.selectBox1.x() - self.selectBox0.x(),
                             self.selectBox1.y() - self.selectBox0.y())

        painter.drawText(50, 50, "Frame: {}".format(self.frame_number()))

    def updateSelectionBox(self):
        self.selectBox0.setX(min(self.select0.x(), self.select1.x()))
        self.selectBox0.setY(min(self.select0.y(), self.select1.y()))

        self.selectBox1.setX(max(self.select0.x(), self.select1.x()))
        self.selectBox1.setY(max(self.select0.y(), self.select1.y()))

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent):
        super().mousePressEvent(event)

        self.last_mouse_point = event.pos()

        # if event.button() == Qt.MouseButton.RightButton:
        #     self.move_camera = True
        # else:
        #     self.move_camera = False

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent):
        super().mouseReleaseEvent(event)

        # if event.button() == Qt.MouseButton.RightButton:
        #     self.move_camera = False

    def mouse_move(self, delta, event):
        pass

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent):
        super().mouseMoveEvent(event)
        # print("mouse move event")
        delta = event.pos() - self.last_mouse_point

        self.mouse_move(delta, event)

        if self.move_camera:  # self.canDrag and
            self.camera = self.camera + QPointF(delta) / float(self.zoom)
            self.repaint()

        self.last_mouse_point = event.pos()

    def translateMousePoint(self, pt: QPoint) -> QPoint:
        sw = self.width()
        sh = self.height()

        # Offset from center of canvas (pixels)
        offs = QPointF(pt) - QPointF(sw / 2, sh / 2)
        offs_world = offs / self.zoom

        # print("offs from center: {}, zoom: {}".format(offs, self.zoom))
        # print("offs from center (world): {}".format(offs / self.zoom))

        pt_world = -self.camera + offs_world
        print("Translated mouse point", pt_world)
        return pt_world

    def wheelEvent(self, event: QWheelEvent):
        pointEvent = event.point(0)
        pos = pointEvent.pos()

        new_zoom = self.zoom

        if self.allow_zoom():
            if event.angleDelta().y() > 0:
                new_zoom *= 2
            elif event.angleDelta().y() < 0:
                new_zoom /= 2

        if new_zoom < 1:
            new_zoom = 1

        if new_zoom > 32:
            new_zoom = 32

        if new_zoom != self.zoom:
            # Offset from center of canvas (pixels)
            offs = QPointF(pos) - QPointF(self.width() / 2, self.height() / 2)
            print(offs)
            offs_world = offs / self.zoom
            pt_world = -self.camera + offs_world
            self.camera = -(pt_world - offs / new_zoom)
            self.zoom = new_zoom
            print(new_zoom)
            self.repaint()

    # This gets overridden
    @abstractmethod
    def frame_number(self):
        raise NotImplemented

    def allow_zoom(self) -> bool:
        return True
