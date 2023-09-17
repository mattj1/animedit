# Root symbol contains a library and a symbol. It also can be written to a file
# This is typically the thing you edit and save to a file.
# The library, which is saved in the root symbol file, will contain embedded symbols, and
# references to textures and other (root?) symbols
import xml.etree.ElementTree as ET

from SpriteAnim.library import Library, SymbolLibraryItem, TextureLibraryItem
from SpriteAnim.symbol import Symbol


class RootSymbol:
    def __init__(self):
        print("Root Symbol init")
        self.path = ""
        self.symbol = None
        self.library = Library()

    @staticmethod
    def from_element(element):
        root_symbol = RootSymbol()
        for elem in element:
            if elem.tag == 'rootsymbol':
                print("<rootsymbol>", elem)
                symbol = Symbol.from_xml(elem, root_symbol.library)
                root_symbol.symbol = symbol
                continue

            if elem.tag == 'symbol':
                symbol = Symbol.from_xml(elem, root_symbol.library)
                root_symbol.library.addItem(SymbolLibraryItem(symbol=symbol))
                continue

            if elem.tag == 'texture':
                texture_item = TextureLibraryItem(texture_path=elem.get('path'))
                root_symbol.library.addItem(texture_item)
                continue

            raise Exception(f'Unknown tag in rootsymbol: {elem.tag}')

        return root_symbol

    @staticmethod
    def from_file(path):
        tree = ET.parse(path)
        return RootSymbol.from_element(tree.getroot())
