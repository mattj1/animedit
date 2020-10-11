from PySide2.QtCore import QRect

from Editor.Actions.Action import AddLayerAction, Action, ConvertKeyframeAction, InsertFrameAction, ClearKeyframeAction
from Editor.Actions.FrameActions import SetFrameTexturePathAction, ChangeMultipleFrameOffsets
from Editor.Actions.SelectionActions import SelectFramesAction, ClearSelectionAction, SelectLayerAction
from Editor.LibraryEditor import LibraryEditor
from SpriteAnim import Symbol, RootSymbol
from SpriteAnim.Frame import Frame
from SpriteAnim.Library import LibraryItem, Library
from Views.MainWindow import MainWindow


class Editor:
    view: MainWindow = None

    def __init__(self) -> None:
        super().__init__()

        self.library_editor = LibraryEditor(editor=self)

        self.current_frame = 0
        self.current_layer = 0

        # Top layer shown in the layer list/frames view
        self.top_layer = 0

        self.actions = []
        self.redoActions = []

        # What we're editing (document). Contains the Library.
        self.root_symbol = RootSymbol()

        # Rectangle representing selected frame range in the time line
        # 0x0 for nothing, 1x1 for one frame
        self.selected_frame_range = QRect(-1, -1, 0, 0)

    def set_view(self, view: MainWindow):
        self.view = view

    def new_document(self):

        # What we're editing (currently)
        self.cur_symbol = Symbol()
        self.root_symbol.setSymbol(self.cur_symbol)

        a = AddLayerAction(self.cur_symbol, 1, QRect(-1, -1, 0, 0))
        self.run_action(a)

        # Can't undo the AddLayerAction
        self.actions.clear()
        self.redoActions.clear()

        # test: add some test data to the library
        item = LibraryItem()
        item.setAsTexture("testimages/player.png")
        self.root_symbol.library.addItem(item)
        item = LibraryItem()
        item.setAsTexture("testimages/rock.png")
        self.root_symbol.library.addItem(item)

        #item = LibraryItem()
        #testSymbol = Symbol()
        #testSymbol.name = "Test Symbol"
        #item.setAsSymbol(testSymbol)
        #self.root_symbol.library.addItem(item)

        self.view.refresh_view()

    # Undo/redo
    def run_action(self, action: Action):
        action.editor_frame = self.current_frame
        # action.editor_layer = self.layerView.selectedLayer
        # print "run: layer: ",  action.editor_layer

        self.actions.append(action)
        action.redo(self)
        self.view.refresh_view()

    def undo(self):

        if len(self.actions) == 0:
            return

        print("--- undo ---")

        action = self.actions.pop()
        self.redoActions.append(action)
        action.undo(self)

        self.current_frame = action.editor_frame
        # self.layerView.setLayer( action.editor_layer )

        self.view.refresh_view()

    def redo(self):

        if len(self.redoActions) == 0:
            return

        print("--- redo ---")

        action = self.redoActions.pop()
        self.actions.append(action)
        action.redo(self)

        self.current_frame = action.editor_frame

        # self.layerView.setLayer( action.editor_layer )
        self.view.refresh_view()

    def current_symbol(self) -> Symbol:
        return self.root_symbol.symbol

    def current_library(self) -> Library:
        return self.root_symbol.library

    def frame_number(self):
        return self.current_frame

    def layer_index(self):
        return self.current_layer

    def set_layer_index(self, layer_idx):
        self.current_layer = layer_idx
        self.view.refresh_view()

    def set_frame_number(self, frame_number):

        # print("set_frame_number: {}".format(frame_number))
        if frame_number < 0:
            return

        sym = self.current_symbol()

        if frame_number >= sym.totalFrames:
            frame_number = sym.totalFrames - 1

        if frame_number < 0:
            frame_number = 0

        self.current_frame = frame_number

        self.view.refresh_view()

    def set_selected_frame_range(self, symbol, selected):
        self.selected_frame_range = selected

    def clear_selected_frame_range(self, symbol):
        self.selected_frame_range = QRect(-1, -1, 0, 0)

    def set_top_layer(self, _top_layer):
        self.top_layer = _top_layer
        self.view.refresh_view()

    def set_frame_texture_action(self, texture_path: str):

        if self.current_symbol().getFrame(self.current_layer, self.frame_number()) == None:
            return

        key_frame_number = self.current_symbol().layers[self.current_layer].keyframeForFrame(self.current_frame)

        self.run_action(
            SetFrameTexturePathAction(self.current_symbol(), texture_path, self.current_layer, key_frame_number))

        # frame = self.curSymbol.getFrame( self.layerView.selectedLayer,  self.framesView.curFrame )
        # print "setting ",  texturePath
        # frame.setTexure( texturePath.data() )
        # self.curSymbol.layers[self.layerView.selectedLayer].updateFrameNumbers()

        self.view.refresh_view()

    def add_layer_action(self):
        self.run_action(AddLayerAction(self.current_symbol(), self.layer_index(), self.selected_frame_range))

    def change_multiple_frame_offsets_action(self, delta):
        self.run_action(ChangeMultipleFrameOffsets(self.current_symbol(), self.current_symbol().dragItems, delta))

    def clear_keyframe_action(self):
        if self.selected_frame_range.x() != -1:
            self.run_action(ClearKeyframeAction(self.current_symbol(), self.selected_frame_range))

    def convert_to_keyframe_action(self):
        self.run_action(ConvertKeyframeAction(self.current_symbol(), self.selected_frame_range, self.layer_index(),
                                              self.frame_number()))

    def insert_frame_action(self):
        self.run_action(InsertFrameAction(self.current_symbol(), self.selected_frame_range, self.frame_number()))

    def select_frames_action(self, selected_frames, layerNo):
        # selected_frames is the rectangle chosen in the timeline.

        print("selected: ", selected_frames)

        self.run_action(SelectFramesAction(self.current_symbol(),
                                           selected_frames,             # New
                                           self.selected_frame_range,    # Current
                                           layerNo, self.layer_index()))

    def select_layer_action(self, layer_index):
        self.run_action(SelectLayerAction(self.current_symbol(), layer_index, self.layer_index(), self.selected_frame_range))

    def clear_selected_frame_range_action(self):
        if self.selected_frame_range.x() != -1:
            self.run_action(ClearSelectionAction(self.current_symbol(), self.selected_frame_range))
