import pytest
from PySide2.QtWidgets import QApplication

import xml.etree.ElementTree as ET

from SpriteAnim.library import SymbolLibraryItem
from SpriteAnim.root_symbol import RootSymbol


def test_run_main():
    print("Main test")

    qpp = QApplication.instance()

    # tree = ET.parse("testimages/smokepuff.xml")

    root_symbol = RootSymbol.from_file("testimages/embedded_symbol.xml")

    for layer in root_symbol.symbol.layers:
        layer.update_frames()
        print(f'Layer: {layer.name}')
        for frame in layer.frames:
            print(f' frame: {frame}')

    for item in root_symbol.library.item_list:
        if isinstance(item, SymbolLibraryItem):
            print(item.symbol.name, item)

            for layer in item.symbol.layers:
                layer.update_frames()
                print(f'Layer: {layer.name}')
                for frame in layer.frames:
                    print(f' frame: {frame}')