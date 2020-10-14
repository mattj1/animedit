import uuid

from PySide2.QtCore import QByteArray

from SpriteAnim import Symbol


class LibraryItem:
    ITEM_NONE = 0
    ITEM_SYMBOL = 1
    ITEM_LINKED_SYMBOL = 2
    ITEM_TEXTURE = 3

    def __init__(self):
        self.type = LibraryItem.ITEM_NONE
        self.mimeString = "none,none"
        self.uuid = uuid.uuid4()
        print("uuid: ", self.uuid)

    def is_texture(self):
        return self.type == LibraryItem.ITEM_TEXTURE

    def is_symbol(self):
        return self.type == LibraryItem.ITEM_SYMBOL

    def setAsLinkedSymbol(self, path):
        self.path = path
        self.type = LibraryItem.ITEM_LINKED_SYMBOL

    def getMimeData(self) -> QByteArray:
        return QByteArray(self.uuid.bytes)

    def getMimeType(self):
        raise NotImplemented()

        # elif self.type == LibraryItem.ITEM_LINKED_SYMBOL:
        #     self.mimeString = "application/x-qt-ampedit-mime-linkedsymbol"
        #
        # return self.mimeString

    def get_name(self):
        return "???"


class TextureLibraryItem(LibraryItem):

    def __init__(self, texture_path: str) -> None:
        super().__init__()

        self.texture_path = texture_path

        self.type = LibraryItem.ITEM_TEXTURE

    def getMimeType(self):
        return "application/x-qt-ampedit-mime-texture"

    def get_name(self):
        return self.texture_path


class SymbolLibraryItem(LibraryItem):

    def __init__(self, symbol: Symbol) -> None:
        super().__init__()

        self.symbol = symbol

        self.type = LibraryItem.ITEM_SYMBOL

    def getMimeType(self):
        return "application/x-qt-ampedit-mime-symbol"

    def get_name(self):
        return self.symbol.name
