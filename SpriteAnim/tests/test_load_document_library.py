from PySide6.QtWidgets import QApplication

from SpriteAnim.library import SymbolLibraryItem
from SpriteAnim.root_symbol import RootSymbol

def test_load_document_library():
    qpp = QApplication.instance()

    root_symbol = RootSymbol.from_file("testimages/embedded_symbol.xml")
    for item in root_symbol.library.item_list:
        print(item)
