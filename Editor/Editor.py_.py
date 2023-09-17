import xml.etree.ElementTree as ET

from PySide2.QtCore import QRect, QPoint

from Editor.Actions.Action import Action, ConvertKeyframeAction, InsertFrameAction, ClearKeyframeAction
from Editor.Actions.FrameActions import SetFrameTexturePathAction, ChangeMultipleFrameOffsets, SetFrameSymbolAction
from Editor.Actions.LayerActions import AddLayerAction
from Editor.Actions.SelectionActions import SelectFramesAction, ClearSelectionAction, SelectLayerAction, \
    ChangeSelectionAction
from Editor.LibraryEditor import LibraryEditor
from Editor.Selection import FrameRef
from SpriteAnim import Symbol, RootSymbol
from SpriteAnim.Library import Library
from SpriteAnim.LibraryItem import LibraryItem, SymbolLibraryItem, TextureLibraryItem
from Views.MainWindow import MainWindow, Frame


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
        self.root_symbol: RootSymbol = RootSymbol()
        self.cur_symbol = self.root_symbol.symbol

        self.selected_frames: [FrameRef] = []

    def set_view(self, view: MainWindow):
        self.view = view

    def new_document(self):

        # What we're editing (currently)
        self.cur_symbol = Symbol()
        self.root_symbol.setSymbol(self.cur_symbol)

        a = AddLayerAction(self.cur_symbol, 1)
        self.run_action(a)

        # Can't undo the AddLayerAction
        self.actions.clear()
        self.redoActions.clear()

        # test: add some test data to the library
        item = TextureLibraryItem("testimages/player.png")
        self.root_symbol.library.addItem(item)
        item = TextureLibraryItem("testimages/rock.png")
        self.root_symbol.library.addItem(item)

        tree = ET.parse("testimages/smokepuff.xml")
        library = tree.getroot()
        rootsymbol = library.find("rootsymbol")
        ts = Symbol.from_xml(rootsymbol)

        item = SymbolLibraryItem(ts)
        self.root_symbol.library.addItem(item)

        tree = ET.parse("testimages/movietest.xml")
        library = tree.getroot()
        rootsymbol = library.find("rootsymbol")
        ts = Symbol.from_xml(rootsymbol)
        # item = LibraryItem()
        # testSymbol = Symbol()
        # testSymbol.name = "Test Symbol"
        # item.setAsSymbol(testSymbol)
        # self.root_symbol.library.addItem(item)

        # self.root_symbol = ts
        self.cur_symbol = ts
        self.view.refresh_view()


    # Undo/redo
    def run_action(self, action: Action):
        action.editor_frame = self.current_frame
        action.editor_layer = self.current_layer
        action.symbol = self.current_symbol()

        # print "run: layer: ",  action.editor_layer

        self.actions.append(action)
        self.redoActions.clear()
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
        return self.cur_symbol
        # return self.root_symbol.symbol

    def current_library(self) -> Library:
        return self.root_symbol.library

    def frame_number(self):
        return self.current_frame

    def layer_index(self):
        return self.current_layer

    def set_layer_index(self, layer_idx):
        self.current_layer = layer_idx
        self.view.refresh_view()

    # Get the bounded frame number (prevent <0 or >max frames)
    def adjusted_frame_number_for_frame_number(self, frame_number) -> int:
        # print("set_frame_number: {}".format(frame_number))
        if frame_number < 0:
            return 0

        sym = self.current_symbol()

        if frame_number >= sym.totalFrames:
            frame_number = sym.totalFrames - 1

        if frame_number < 0:
            frame_number = 0

        return frame_number

    def set_frame_number(self, frame_number):
        self.current_frame = self.adjusted_frame_number_for_frame_number(frame_number)
        self.view.refresh_view()

    def set_selected_frames(self, selected: [FrameRef]):

        fr: FrameRef

        # Unselect previous frames
        for fr in self.selected_frames:
            frame = self.current_symbol().getFrame(fr.layer_no, fr.frame_no)

            if frame:
                frame.setSelected(False)

        print("set_selected_frames: ", selected)
        self.selected_frames = selected

        for fr in self.selected_frames:
            frame = self.current_symbol().getFrame(fr.layer_no, fr.frame_no)

            if frame:
                frame.setSelected(True)

    def is_frame_selected(self, layer_index, frame_index):
        for fr in self.selected_frames:
            if fr.layer_no == layer_index and fr.frame_no == frame_index:
                return True

        return False

    def set_top_layer(self, _top_layer):
        self.top_layer = _top_layer
        self.view.refresh_view()

    def set_frame_texture_action(self, texture_path: str):

        if self.current_symbol().getFrame(self.current_layer, self.frame_number()) is None:
            return

        key_frame_number = self.current_symbol().layers[self.current_layer].keyframeForFrame(self.current_frame)

        self.run_action(
            SetFrameTexturePathAction(self.current_symbol(), texture_path, self.current_layer, key_frame_number))

        # frame = self.curSymbol.getFrame( self.layerView.selectedLayer,  self.framesView.curFrame )
        # print "setting ",  texturePath
        # frame.setTexure( texturePath.data() )
        # self.curSymbol.layers[self.layerView.selectedLayer].updateFrames()

    def set_frame_symbol_action(self, item: SymbolLibraryItem):

        if self.current_symbol().getFrame(self.current_layer, self.frame_number()) is None:
            return

        key_frame_number = self.current_symbol().layers[self.current_layer].keyframeForFrame(self.current_frame)

        self.run_action(
            SetFrameSymbolAction(self.current_symbol(), item, self.current_layer, key_frame_number))

    def add_layer_action(self):
        self.run_action(AddLayerAction(self.current_symbol(), self.layer_index(), self.selected_frame_range))

    def change_multiple_frame_offsets_action(self, delta: QPoint):
        self.run_action(ChangeMultipleFrameOffsets(self.current_symbol(), self.current_symbol().dragItems, delta))

    def change_selection_action(self, frame_number: int, append: bool):
        frame_number = self.adjusted_frame_number_for_frame_number(frame_number)

        # if the selection and frame number haven't changed, do nothing.
        # (can happen during draggin
        if frame_number == self.frame_number():
            return

        if append and len(self.actions) > 0:
            last_action = self.actions[-1]
            if isinstance(last_action, ChangeSelectionAction):
                # print("Is appending Change Selection")
                last_action.frame_number = frame_number
                last_action.redo(self)
                self.view.refresh_view()
                return

        action = ChangeSelectionAction(frame_number)
        self.run_action(action)

    def clear_keyframe_action(self):
        if self.selected_frame_range.x() != -1:
            self.run_action(ClearKeyframeAction(self.current_symbol(), self.selected_frame_range))

    def convert_to_keyframe_action(self):
        self.run_action(ConvertKeyframeAction(self.current_symbol(), self.selected_frame_range, self.layer_index(),
                                              self.frame_number()))

    def insert_frame_action(self):
        self.run_action(InsertFrameAction(self.current_symbol(), self.selected_frame_range, self.frame_number()))

    def select_frames_action(self, frames: [FrameRef]):


        print("select_frames_action: ", frames)

        self.run_action(SelectFramesAction(self.current_symbol(),
                                           frames,  # New
                                           self.selected_frames))  # Current


    def select_layer_action(self, layer_index):
        self.run_action(
            SelectLayerAction(self.current_symbol(), layer_index, self.layer_index(), self.selected_frames))

