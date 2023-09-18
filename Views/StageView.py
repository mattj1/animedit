from uuid import uuid4, UUID

import PySide6.QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QFrame, QHBoxLayout, QPushButton, QSpacerItem, QSlider

from Editor import Editor
from Views.StageCanvas import StageCanvas


class StageControls(QFrame):
    def __init__(self, editor: Editor, parent=None):
        super(StageControls, self).__init__(parent)
        self.editor = editor

        self.setFixedHeight(48)

        self.setAutoFillBackground(True)
        toolbar_layout = QHBoxLayout()
        self.setLayout(toolbar_layout)
        button = QPushButton('Play')
        button.clicked.connect(self.play_pressed)
        toolbar_layout.addWidget(button)
        button = QPushButton('Stop')
        button.clicked.connect(self.stopPressed)
        toolbar_layout.addWidget(button)

        slider = QSlider()
        slider.setMaximum(30)
        slider.setMinimum(1)
        slider.setMaximumWidth(128)
        slider.setOrientation(Qt.Horizontal)
        toolbar_layout.addWidget(slider)

        self.zoomSlider = slider

        slider.valueChanged.connect(self.valueChanged)

    def valueChanged(self, event):
        print(event)
        self.repaint()

    def play_pressed(self):
        self.editor.start_playback()

    def stopPressed(self):
        self.editor.stop_playback()

class StageView(StageCanvas):
    def __init__(self, editor: Editor, parent=None):
        super(StageView, self).__init__(parent)
        self.editor = editor

        self.stage_controls = StageControls(editor=editor, parent=self)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0 ,0)
        layout.addStretch()
        layout.addWidget(self.stage_controls)
        self.setLayout(layout)


    # def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
    #     super().resizeEvent(event)
    #     print("resize, height", self.height())
    #     self.toolbar_frame.move(0, self.height() - 48)
    #     self.toolbar_frame.resize(self.width(), 48)
    #     print(self.height())


    def get_symbol(self):
        return self.editor.current_symbol

    def is_symbol(self):
        return True

    def frame_number(self):
        return self.editor.frame_number

    #     self.canDrag = 1
    #
    #     # Set externally
    #     self.framesView = None
    #
    #     # Mouse drag delta, in world coords
    #     self.dragDeltaWorld = QPointF(0, 0)
    #
    #     print("init", self.parent)
    #     #        self.movie = QMovie('../sonic3.gif')
    #     self.setMinimumWidth(640)
    #     # if self.movie.isValid():
    #     #     print("Is valid movie ", self.movie.frameCount())
    #
    #     # self.movie.jumpToFrame(0)
    #
    #     # for i in range(0, self.movie.frameCount()):
    #     #     #print i,  " ", self.movie.nextFrameDelay()
    #     #     self.movie.jumpToNextFrame()
    #     #
    #     # self.pm2 = QPixmap(self.movie.currentPixmap())
    #
    #     self.setAcceptDrops(True)
    #     self.isDragging = False
    #
    # def get_symbol(self) -> Symbol:
    #     return self.editor.current_symbol()
    #
    # def get_texture(self) -> QPixmap:
    #     pass
    #
    # def startFrameDragging(self):
    #     self.isDragging = True
    #
    #     for i in self.get_symbol().dragItems:
    #         i.startDragging()
    #
    # def mousePressEvent(self, event):
    #     super(StageView, self).mousePressEvent(event)
    #
    #     symbol = self.get_symbol()
    #
    #     # Check if this intersects anything, otherwise, start the selection box
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         # If there are selected items, check to see if we're in the bounding box of any of the dragItems
    #         startSelect = True
    #
    #         if symbol.numDragItems() > 0:
    #             startDragging = False
    #             self.dragDeltaWorld = QPointF(0, 0)
    #             self.initialDragPoint = self.translateMousePoint(event.pos())
    #             for i in symbol.dragItems:
    #                 # if i's bounding box contains the mouse point, then we are now dragging the selected items
    #                 bb = i.boundingBox()
    #                 if bb != None and bb.contains(self.translateMousePoint(event.pos())):
    #                     startDragging = True
    #                     break
    #
    #             if startDragging:
    #                 startSelect = False
    #                 # all mouse movements will drag these now
    #                 self.startFrameDragging()
    #
    #         if startSelect:
    #             symbol.clearDragItems()
    #
    #             self.selecting = True
    #             self.select0 = QPointF(event.pos().x(), event.pos().y())
    #             self.select1 = QPointF(event.pos().x(), event.pos().y())
    #             self.updateSelectionBox()
    #
    #         self.repaint()
    #
    # def mouseReleaseEvent(self, event):
    #
    #     if self.isDragging:
    #         for i in self.get_symbol().dragItems:
    #             # modify the respective frames!
    #             i.stopDragging()
    #
    #         self.editor.change_multiple_frame_offsets_action(
    #             QPoint(int(self.dragDeltaWorld.x()), int(self.dragDeltaWorld.y())))
    #
    #         self.isDragging = False
    #
    #     if self.selecting:
    #         self.selecting = False
    #         sw = self.width()
    #         sh = self.height()
    #
    #         # doesn't work with zoom
    #
    #         ox = sw / 2 + self.camera.x()
    #         oy = sh / 2 + self.camera.y()
    #
    #         p0 = QPoint(self.selectBox0.x() - ox, self.selectBox0.y() - oy)
    #         p1 = QPoint(self.selectBox1.x() - ox, self.selectBox1.y() - oy)
    #         print(p0, p1)
    #         self.select_frames(QRect(p0, p1))
    #
    #     self.repaint()
    #
    # def mouse_move(self, delta: QPoint, event):
    #
    #     if self.isDragging:
    #         self.dragDeltaWorld += QPointF(delta.x() / self.zoom, delta.y() / self.zoom)
    #         # print("deltaworld: ", self.dragDeltaWorld)
    #         # print("mouse_move:", delta, delta / self.zoom, self.dragDeltaWorld)
    #
    #         for i in self.get_symbol().dragItems:
    #             i.set_temp_offset(int(self.dragDeltaWorld.x()), int(self.dragDeltaWorld.y()))
    #
    #     if self.selecting:
    #         self.select1 = event.pos()
    #         self.updateSelectionBox()
    #
    #     self.repaint()
    #
    # def get_selectable_frames_in_rect(self, rect, only_keyframes=True) -> [Frame]:
    #     frames = []
    #     symbol = self.get_symbol()
    #
    #     # Find selectable frame content in this box
    #
    #     # go through all the layers for this frame
    #     for layer in symbol.layers:
    #         frame = layer.getFrame(self.frame_number())
    #         if frame is None:
    #             continue
    #
    #         if only_keyframes and not frame.isKey():
    #             continue
    #
    #         bb = frame.boundingBox()
    #         if bb is None:
    #             continue
    #
    #         print("Checking for frames in bounding box ", rect, bb)
    #         if bb.intersects(rect):
    #             frames.append(frame)
    #             print("intersects!")
    #
    #     return frames
    #
    # def select_frames(self, rect):
    #
    #     frames = self.get_selectable_frames_in_rect(rect)
    #     self.editor.select_frames_action(frames)
    #
    #     #symbol = self.get_symbol()
    #
    #     #for frame in frames:
    #      #   frame.setSelected(True)
    #       #  symbol.addDragItem(frame)
    #
    #         # self.symbol.drawFrame( f,  painter );
    #
    # def dragEnterEvent(self, event):
    #     data = event.mimeData().data("application/x-qt-ampedit-mime-symbol")
    #     if data is not None:
    #         event.acceptProposedAction()
    #
    #     data = event.mimeData().data("application/x-qt-ampedit-mime-texture")
    #     if data is not None:
    #         event.acceptProposedAction()
    #
    # def dropEvent(self, event):
    #     mime_data = event.mimeData()
    #
    #     data = mime_data.data("application/x-qt-ampedit-mime-texture")
    #     if data is not None and len(data) > 0:
    #         print("Drop texture...", len(data), data)
    #         item_uuid = UUID(bytes=bytes(data), version=4)
    #         print("insert...", item_uuid)
    #
    #         tex_item: TextureLibraryItem
    #         tex_item = self.editor.current_library().item_for_uuid(item_uuid)
    #         self.editor.set_frame_texture_action(texture_path=tex_item.texture_path)
    #         return
    #
    #     data = event.mimeData().data("application/x-qt-ampedit-mime-symbol")
    #     if data is not None and len(data) > 0:
    #         item_uuid = UUID(bytes=bytes(data), version=4)
    #         print("Drop symbol...", item_uuid, len(data), data)
    #         symbol_item: SymbolLibraryItem
    #         symbol_item = self.editor.current_library().item_for_uuid(item_uuid)
    #         print(symbol_item)
    #
    #         self.editor.set_frame_symbol_action(item=symbol_item)
    #         return
    #
    # def frame_number(self):
    #     return self.editor.frame_number()
    #
    def paintEvent(self, event):
        super().paintEvent(event)

        # painter = QPainter(self)
        #
        # if self.isSymbol:
        #     # What's selected?
        #     # self.symbol.
        #     # frame = self.symbol.
        #     painter.drawText(50, 70, "*SYMBOL* {}".format(self.frame_number()))
