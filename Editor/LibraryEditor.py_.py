from Editor import Editor
from SpriteAnim import Library, LibraryItem


class LibraryEditor:

    def __init__(self, editor: Editor) -> None:
        super().__init__()

        self.editor = editor

        self.selected_index = -1

        self.view = None

    # def set_view(self, view: LibraryWindow):
    #     self.view = view

    def set_selected_index(self, new_index):
        if new_index < len(self.get_library().item_list()):
            self.selected_index = new_index

            # item = self.get_library().items[self.selected_index]
            #
            # if item.type == Library.ITEM_TEXTURE:
            #     self.parent.stageCanvas.setTexture(TextureMgr.textureMgr().loadImage(item.texturePath))
            #
            # elif item.type == Library.ITEM_SYMBOL:
            #     self.parent.stageCanvas.setSymbol(item.sym)

        self.view.refresh_view()

    def get_library(self) -> Library:
        return self.editor.current_library()

    def selected_item(self) -> LibraryItem:
        return self.get_library().item_list()[self.selected_index]

