# store the currently selected layer in the action

# select frames
from PySide2.QtCore import QRect

from Editor.Actions.Action import Action


class ChangeSelectionAction(Action):

    def __init__(self, frame_number: int):
        super(ChangeSelectionAction, self).__init__()

        self.frame_number = frame_number

    def redo(self, editor):
        editor.set_frame_number(self.frame_number)

    def undo(self, editor):
        super().undo(editor)


class SelectFramesAction(Action):
    def __init__(self, symbol, selected, prevSelected, layerNo, prevLayerNo):
        super(SelectFramesAction, self).__init__()

        self.symbol = symbol
        self.selected = selected
        self.prevSelected = prevSelected
        self.layerNo = layerNo
        self.prevLayerNo = prevLayerNo

    def redo(self, editor):
        editor.set_selected_frame_range(self.symbol, self.selected)
        editor.set_layer_index(self.layerNo)

    def undo(self, editor):
        editor.set_layer_index(self.prevLayerNo)
        editor.set_selected_frame_range(self.symbol, self.prevSelected)


# clear frame selection - happens if user clicks on a part of framesview with no frames or the top time thing

class ClearSelectionAction(Action):
    def __init__(self, symbol, prevSelected):
        super(ClearSelectionAction, self).__init__()
        self.symbol = symbol
        self.prevSelected = prevSelected

    def redo(self, editor):
        editor.clear_selected_frame_range(self.symbol)

    def undo(self, editor):
        editor.set_selected_frame_range(self.symbol, self.prevSelected)


# select layer
class SelectLayerAction(Action):
    def __init__(self, symbol, layerNo, prevLayerNo, prevSelected):
        super(SelectLayerAction, self).__init__()
        self.symbol = symbol
        self.layerNo = layerNo
        self.prevLayerNo = prevLayerNo
        self.prevSelected = prevSelected

        l = self.symbol.getLayer(layerNo)
        self.selected = QRect(0, layerNo, l.numFrames(), 1)

    def redo(self, editor):
        editor.set_layer_index(self.layerNo)
        editor.set_selected_frame_range(self.symbol, self.selected)

    def undo(self, editor):
        editor.set_layer_index(self.prevLayerNo)
        editor.set_selected_frame_range(self.symbol, self.prevSelected)
