from SpriteAnim import Symbol, RootSymbol
from SpriteAnim.library import SymbolLibraryItem
from Views import MainWindow


class Editor:
    view: MainWindow = None

    def __init__(self) -> None:
        super().__init__()
        self.view: MainWindow = None
        self.current_symbol = Symbol.from_empty()
        # root_symbol = RootSymbol.from_file("testimages/smokepuff.xml")
        root_symbol = RootSymbol.from_file("testimages/embedded_symbol.xml")

        for layer in root_symbol.symbol.layers:
            layer.update_frames()
            for frame in layer.frames:
                print(f' frame: {frame}')

        for item in root_symbol.library.item_list:
            if isinstance(item, SymbolLibraryItem):
                for layer in item.symbol.layers:
                    layer.update_frames()

        self.current_symbol = root_symbol.symbol

        self.selected_layer_index = 0
        self.top_layer = 0
        self.__frame_number = 0

    def set_view(self, view: MainWindow):
        self.view = view

    @property
    def current_symbol(self) -> Symbol:
        return self.__current_symbol

    @current_symbol.setter
    def current_symbol(self, var: Symbol):
        self.__current_symbol = var

    @property
    def selected_layer_index(self) -> int:
        return self.__selected_layer_index

    @selected_layer_index.setter
    def selected_layer_index(self, var: int):
        self.__selected_layer_index = var
        if self.view is not None:
            self.view.repaint()

    @property
    def top_layer(self) -> int:
        return self.__top_layer

    @top_layer.setter
    def top_layer(self, var: int):
        self.__top_layer = var
        if self.view is not None:
            self.view.repaint()

    @property
    def frame_number(self) -> int:
        return self.__frame_number

    @frame_number.setter
    def frame_number(self, var: int):
        if var < 0:
            var = 0

        if var != self.__frame_number:
            self.__frame_number = var
            if self.view is not None:
                self.view.repaint()

    def start_playback(self):
        self.view.start_playback()

    def stop_playback(self):
        self.view.stop_playback()
