from Editor import Editor
from Editor.Actions.Action import Action


class AddLayerAction(Action):
    def __init__(self, symbol, layer):
        super(AddLayerAction, self).__init__()
        print("new Add Layer Action")
        self.symbol = symbol
        self.layer = self.symbol.createNewLayer()
        self.layerNo = layer
        # self.prevSelected = prevSelected

    def redo(self, editor: Editor):
        try:
            editor.clear_selected_frame_range(self.symbol)
        except:
            pass

        self.symbol.insertLayer(self.layer, self.layerNo)
        # perhaps adjust the selected layer?

    def undo(self, editor: Editor):
        # remove this layer from the symbol - I think this will properly undo the selected layer...
        try:
            self.symbol.removeLayer(self.layer)
        except:
            pass

        editor.set_selected_frame_range(self.symbol, self.prevSelected)
