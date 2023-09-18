import uuid
from uuid import uuid4

from PySide6.QtCore import QByteArray

import TextureMgr
from SpriteAnim.symbol import Symbol


class LibraryItem:
    ITEM_NONE = 0
    ITEM_SYMBOL = 1
    ITEM_LINKED_SYMBOL = 2
    ITEM_TEXTURE = 3

    def __init__(self):
        self.type = LibraryItem.ITEM_NONE
        self.mimeString = "none,none"
        self.uuid = uuid.uuid4()
        self.symbol = None
        print("uuid: ", self.uuid)

    def is_texture(self):
        return self.type == LibraryItem.ITEM_TEXTURE

    def is_symbol(self):
        return self.type == LibraryItem.ITEM_SYMBOL

    # def setAsLinkedSymbol(self, path):
    #     self.path = path
    #     self.type = LibraryItem.ITEM_LINKED_SYMBOL

    def getMimeData(self) -> QByteArray:
        return QByteArray(self.uuid.bytes)

    def getMimeType(self):
        raise NotImplemented()

        # elif self.type == LibraryItem.ITEM_LINKED_SYMBOL:
        #     self.mimeString = "application/x-qt-ampedit-mime-linkedsymbol"
        #
        # return self.mimeString

    def get_name(self):
        raise NotImplemented()


class TextureLibraryItem(LibraryItem):

    def __init__(self, texture_path: str) -> None:
        super().__init__()

        self.texture_path = texture_path

        self.type = LibraryItem.ITEM_TEXTURE
        self.texture = None

    def getMimeType(self):
        return "application/x-qt-ampedit-mime-texture"

    def get_name(self):
        return self.texture_path

    def __repr__(self) -> str:
        return f'<TextureLibraryItem texture_path={self.texture_path}>'

    def get_texture(self):
        if not self.texture:
            self.texture = TextureMgr.textureMgr().loadImage(self.texture_path)

        return self.texture


class SymbolLibraryItem(LibraryItem):

    def __init__(self, symbol: Symbol) -> None:
        super().__init__()

        self.symbol = symbol

        self.type = LibraryItem.ITEM_SYMBOL

    def getMimeType(self):
        return "application/x-qt-ampedit-mime-symbol"

    def get_name(self):
        return self.symbol.name

    def __repr__(self) -> str:
        return f'<SymbolLibraryItem name={self.symbol.name}>'

class SymbolRef:
    def __init__(self, name, library):
        self.symbol = None
        self.name = name
        self.library = library

    def get_symbol(self):
        if not self.symbol:
            self.symbol = self.library.get_symbol_for_name(self.name)

        assert self.symbol is not None

        return self.symbol


class TextureRef:
    def __init__(self, path, library):
        assert path is not None
        assert library is not None
        self.texture = None
        self.path = path
        self.library = library

    def get_texture(self):
        if not self.texture:
            self.texture = self.library.get_texture_for_name(self.path)

        if self.texture is None:
            print(f"Didn't find {self.path}")
            assert True
        # assert self.texture is not None, f"{self.path}"

        return self.texture

class Library:

    # The library can store the following things:
    #  Symbols
    #  Linked symbols
    #  Textures

    def __init__(self):
        self.items = {}
        self.item_list = []
        self.symbol_refs = {}
        self.texture_refs = {}

        print("Library init")

    def item_for_index(self, index):
        return self.item_list[index]

    def item_for_uuid(self, uuid: uuid4):
        return self.items[uuid]

    def get_symbol_ref(self, name):
        if name not in self.symbol_refs:
            self.symbol_refs[name] = SymbolRef(name=name, library=self)

        return self.symbol_refs[name]

    def get_texture_ref(self, name):
        if name not in self.texture_refs:
            self.texture_refs[name] = TextureRef(path=name, library=self)

        return self.texture_refs[name]

    def get_item_for_name(self, name, item_type):
        for i in self.item_list:
            if isinstance(i, item_type):
                if i.get_name() == name:
                    return i
        return None

    def get_symbol_for_name(self, name):
        item = self.get_item_for_name(name, SymbolLibraryItem)
        if item:
            return item.symbol

        return None

    def get_texture_for_name(self, name):
        item = self.get_item_for_name(name, TextureLibraryItem)
        if item:
            return item

        return None

    # Add an item. Can be called during importing, or loading, etc.
    def addItem(self, item: LibraryItem):
        self.items[item.uuid] = item
        self.item_list.append(item)

        # self.items.append(item)

    def removeItem(self, item):
        self.items.pop(item.uuid)
        self.item_list.remove(item)

