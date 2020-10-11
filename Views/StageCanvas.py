# generic canvas for rendering a symbol or texture
from abc import abstractmethod
from typing import Optional

import PySide2
from PySide2.QtCore import QPoint, QPointF
from PySide2.QtGui import QPainter, Qt, QColor, QTransform, QPen, QPixmap
from PySide2.QtWidgets import QWidget

from SpriteAnim import Symbol


class StageCanvas(QWidget):
    def __init__(self, parent=None):
        super(StageCanvas, self).__init__(parent)
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

    @abstractmethod
    def get_symbol(self) -> Symbol:
        return self.editor.current_symbol()

    @abstractmethod
    def get_texture(self) -> QPixmap:
        return None

    def is_symbol(self):
        return self.get_symbol() is not None

    def is_texture(self):
        return self.get_texture() is not None



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

        print("Paint canvas, camera: {}, {}, X range: {} {}".format(-self.camera.x(), -self.camera.y(), world_left, world_right))

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

        # draw origin lines

        pen = QPen(Qt.SolidLine)
        pen.setColor(QColor(222, 222, 222, 255))
        pen.setWidth(0.1)
        painter.setPen(pen)

        painter.drawLine(-1000, 0, 1000, 0)
        painter.drawLine(0, -1000, 0, 1000)
        # self.movie.jumpToFrame(0);



        f = self.frame_number()
        """"
        for i in range(0, f):
            self.movie.jumpToNextFrame()
            
        """

        if self.is_symbol():
            symbol = self.get_symbol()
            if symbol:
                symbol.drawFrame(f, painter)
        else:
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
                painter.drawLine(i, world_top, i, world_bottom)
            for i in range(int(world_top), int(world_bottom)):
                painter.drawLine(world_left, i, world_right, i)

        pen = QPen(Qt.SolidLine)
        pen.setColor(QColor(0, 0, 0, 255))
        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)
        painter.resetTransform()

        if self.selecting:
            painter.drawRect(self.selectBox0.x(), self.selectBox0.y(), self.selectBox1.x() - self.selectBox0.x(),
                             self.selectBox1.y() - self.selectBox0.y())

        painter.drawText(50, 50, "Frame: {}".format(self.frame_number()))

    def updateSelectionBox(self):
        self.selectBox0.setX(min(self.select0.x(), self.select1.x()))
        self.selectBox0.setY(min(self.select0.y(), self.select1.y()))

        self.selectBox1.setX(max(self.select0.x(), self.select1.x()))
        self.selectBox1.setY(max(self.select0.y(), self.select1.y()))

    def mousePressEvent(self, event: PySide2.QtGui.QMouseEvent):
        super().mousePressEvent(event)

        self.last_mouse_point = event.pos()

        if event.button() == Qt.MouseButton.RightButton:
            self.move_camera = True
        else:
            self.move_camera = False

    def mouseReleaseEvent(self, event: PySide2.QtGui.QMouseEvent):
        super().mouseReleaseEvent(event)

        if event.button() == Qt.MouseButton.RightButton:
            self.move_camera = False

    def mouse_move(self, delta, event):
        pass

    def mouseMoveEvent(self, event: PySide2.QtGui.QMouseEvent):
        super().mouseMoveEvent(event)

        delta = event.pos() - self.last_mouse_point

        self.mouse_move(delta, event)

        if self.move_camera:  # self.canDrag and
            self.camera = self.camera + QPointF(delta) / float(self.zoom)

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

    def wheelEvent(self, event):

        new_zoom = self.zoom

        if self.allow_zoom():
            if event.delta() > 0:
                new_zoom *= 2
            else:
                new_zoom /= 2

        if new_zoom < 1:
            new_zoom = 1

        if new_zoom > 32:
            new_zoom = 32

        if new_zoom != self.zoom:
            # Offset from center of canvas (pixels)
            offs = QPointF(event.pos()) - QPointF(self.width() / 2, self.height() / 2)
            offs_world = offs / self.zoom
            pt_world = -self.camera + offs_world
            self.camera = -(pt_world - offs / new_zoom)
            self.zoom = new_zoom
            print(new_zoom)
            self.repaint()

    # This gets overridden
    @abstractmethod
    def frame_number(self):
        return 0

    def allow_zoom(self) -> bool:
        return True
