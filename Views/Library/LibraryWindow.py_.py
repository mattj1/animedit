from PySide2.QtWidgets import QPushButton, QSplitter, QScrollArea, QHBoxLayout

from Editor import LibraryEditor
from Views.Library import LibraryList
from Views.Library.LibraryStageView import LibraryStageView
from Views.StageCanvas import *


class LibraryWindow(QWidget):
    def __init__(self, library_editor: LibraryEditor, parent=None):
        super(LibraryWindow, self).__init__(parent)
        self.library_editor = library_editor
        self.library_editor.set_view(self)

        self.libraryStageView = LibraryStageView(library_editor=library_editor, parent=self)
        self.libraryList = LibraryList(library_editor=library_editor, parent=self)

        self.setWindowFlags(Qt.Window)

        b = QPushButton("Preview")
        box_layout = QHBoxLayout()
        self.setLayout(box_layout)

        self.setWindowTitle("Library")
        # self.resize(300, 500)
        # pr = parent.frameGeometry()
        #
        # print("parent ", parent, pr, parent.pos(), parent.geometry(), parent.mapToGlobal(QPoint(0,0)))
        #
        self.setGeometry(0, 0, 300, 500)
        # self.move(parent.pos().x() + parent.frameGeometry().width(), parent.y())

        # This window uses a horizontal split to show a preview up top, and a scroll area with
        # some kind of list of library entries inside, which can be dragged into the editor window

        mainSplit = QSplitter()
        mainSplit.setOrientation(Qt.Vertical)

        # TODO: The top area should be some kind of symbol rendering/drawing stage. Maybe have the editor stage inherit from it
        #       It should also support dragging.

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(1)

        scrollArea.setWidget(self.libraryList)

        mainSplit.addWidget(self.libraryStageView)
        mainSplit.addWidget(scrollArea)

        box_layout.addWidget(mainSplit)


    def closeEvent(self, event):
        event.ignore()

    def refresh_view(self):
        self.libraryList.refresh_view()
        self.libraryStageView.refresh_view()

    """ 
    if maybeSave():
        writeSettings()
        event.accept()
    else:
        event.ignore()
    """
