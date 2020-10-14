from uuid import uuid4, UUID

from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QMovie

from Editor import Editor
from SpriteAnim.LibraryItem import TextureLibraryItem, SymbolLibraryItem
from Views.StageCanvas import *


class StageView(StageCanvas):
    def __init__(self, editor: Editor, parent=None):
        super(StageView, self).__init__(parent)

        self.editor = editor
        self.canDrag = 1

        # Set externally
        self.framesView = None

        # Mouse drag delta, in world coords
        self.dragDeltaWorld = QPointF(0, 0)

        print("init", self.parent)
        #        self.movie = QMovie('../sonic3.gif')
        self.setMinimumWidth(640)
        # if self.movie.isValid():
        #     print("Is valid movie ", self.movie.frameCount())

        # self.movie.jumpToFrame(0)

        # for i in range(0, self.movie.frameCount()):
        #     #print i,  " ", self.movie.nextFrameDelay()
        #     self.movie.jumpToNextFrame()
        #
        # self.pm2 = QPixmap(self.movie.currentPixmap())

        self.setAcceptDrops(True)
        self.isDragging = False

    def get_symbol(self) -> Symbol:
        return self.editor.current_symbol()

    def get_texture(self) -> QPixmap:
        pass

    def startFrameDragging(self):
        self.isDragging = True

        for i in self.get_symbol().dragItems:
            i.startDragging()

    def mousePressEvent(self, event):
        super(StageView, self).mousePressEvent(event)

        symbol = self.get_symbol()

        # Check if this intersects anything, otherwise, start the selection box
        if event.button() == Qt.MouseButton.LeftButton:
            # If there are selected items, check to see if we're in the bounding box of any of the dragItems
            startSelect = True

            if symbol.numDragItems() > 0:
                startDragging = False
                self.dragDeltaWorld = QPointF(0, 0)
                self.initialDragPoint = self.translateMousePoint(event.pos())
                for i in symbol.dragItems:
                    # if i's bounding box contains the mouse point, then we are now dragging the selected items
                    bb = i.boundingBox()
                    if bb != None and bb.contains(self.translateMousePoint(event.pos())):
                        startDragging = True
                        break

                if startDragging:
                    startSelect = False
                    # all mouse movements will drag these now
                    self.startFrameDragging()

            if startSelect:
                symbol.clearDragItems()

                self.selecting = True
                self.select0 = QPointF(event.pos().x(), event.pos().y())
                self.select1 = QPointF(event.pos().x(), event.pos().y())
                self.updateSelectionBox()

            self.repaint()

    def mouseReleaseEvent(self, event):

        if self.isDragging:
            for i in self.get_symbol().dragItems:
                # modify the respective frames!
                i.stopDragging()

            self.editor.change_multiple_frame_offsets_action(
                QPoint(int(self.dragDeltaWorld.x()), int(self.dragDeltaWorld.y())))

            self.isDragging = False

        if self.selecting:
            self.selecting = False
            sw = self.width()
            sh = self.height()

            # doesn't work with zoom

            ox = sw / 2 + self.camera.x()
            oy = sh / 2 + self.camera.y()

            p0 = QPoint(self.selectBox0.x() - ox, self.selectBox0.y() - oy)
            p1 = QPoint(self.selectBox1.x() - ox, self.selectBox1.y() - oy)
            print(p0, p1)
            self.selectSymbols(QRect(p0, p1))

        self.repaint()

    def mouse_move(self, delta: QPoint, event):

        if self.isDragging:
            self.dragDeltaWorld += QPointF(delta.x() / self.zoom, delta.y() / self.zoom)
            # print("deltaworld: ", self.dragDeltaWorld)
            # print("mouse_move:", delta, delta / self.zoom, self.dragDeltaWorld)

            for i in self.get_symbol().dragItems:
                i.set_temp_offset(int(self.dragDeltaWorld.x()), int(self.dragDeltaWorld.y()))

        if self.selecting:
            self.select1 = event.pos()
            self.updateSelectionBox()

        self.repaint()

    def selectSymbols(self, rect):

        # go through all the layers for this frame

        # check if this frame intersects this box

        f = self.frame_number()

        symbol = self.get_symbol()

        for l in symbol.layers:
            frame = l.getFrame(f)
            if frame is None:
                continue

            bb = frame.boundingBox()
            if bb is None:
                continue

            print("Checking for frames in bounding box ", rect, bb)
            if bb.intersects(rect):
                print("intersects!")
                frame.setSelected(1)
                symbol.addDragItem(frame)

            # self.symbol.drawFrame( f,  painter );

    def dragEnterEvent(self, event):
        data = event.mimeData().data("application/x-qt-ampedit-mime-symbol")
        if data is not None:
            event.acceptProposedAction()

        data = event.mimeData().data("application/x-qt-ampedit-mime-texture")
        if data is not None:
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()

        data = mime_data.data("application/x-qt-ampedit-mime-texture")
        if data is not None and len(data) > 0:
            print("Drop texture...", len(data), data)
            item_uuid = UUID(bytes=bytes(data), version=4)
            print("insert...", item_uuid)

            tex_item: TextureLibraryItem
            tex_item = self.editor.current_library().item_for_uuid(item_uuid)
            self.editor.set_frame_texture_action(texture_path=tex_item.texture_path)
            return

        data = event.mimeData().data("application/x-qt-ampedit-mime-symbol")
        if data is not None and len(data) > 0:
            item_uuid = UUID(bytes=bytes(data), version=4)
            print("Drop symbol...", item_uuid, len(data), data)
            symbol_item: SymbolLibraryItem
            symbol_item = self.editor.current_library().item_for_uuid(item_uuid)
            print(symbol_item)

            self.editor.set_frame_symbol_action(item=symbol_item)
            return

    def frame_number(self):
        return self.editor.frame_number()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        if self.isSymbol:
            # What's selected?
            # self.symbol.
            # frame = self.symbol.
            painter.drawText(50, 70, "*SYMBOL* {}".format(self.frame_number()))
