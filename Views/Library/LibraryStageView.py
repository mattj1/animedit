import TextureMgr
from Editor import LibraryEditor
from SpriteAnim import Symbol
from Views import StageCanvas


class LibraryStageView(StageCanvas):

    def __init__(self, library_editor: LibraryEditor, parent=None):
        super().__init__(parent)
        self.library_editor = library_editor

    def get_symbol(self) -> Symbol:
        item = self.library_editor.selected_item()
        if item.is_symbol():
            return item.sym

    def get_texture(self):
        item = self.library_editor.selected_item()
        if item.is_texture():
            return TextureMgr.textureMgr().loadImage(item.texturePath)

    def mouse_move(self, delta, event):
        super().mouse_move(delta, event)
        self.repaint()

    def refresh_view(self):
        self.repaint()
