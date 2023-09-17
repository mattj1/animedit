from SpriteAnim import Symbol
from Views import MainWindow


class Editor:
    view: MainWindow = None

    def __init__(self) -> None:
        super().__init__()
        self.view: MainWindow = None
        self.current_symbol = Symbol.from_empty()
        self.selected_layer_index = 0

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
