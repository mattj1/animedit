import PySide6.QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QLabel, QFrame

from Editor import Editor
from Views import LayerListView, StageView


class MainWindow(QMainWindow):
    def __init__(self, editor: Editor, parent=None):
        super(MainWindow, self).__init__(parent)

        self.layerListView = LayerListView(editor=editor, parent=self)
        self.stageView = StageView(editor=editor, parent=self)

        self.editor = editor
        self.editor.set_view(self)

        self.setWindowTitle("Editor")
        self.resize(731, 475)

        layout = QVBoxLayout()
        # layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        canvas_time_split = QSplitter()
        canvas_time_split.setOrientation(Qt.Vertical)
        # canvas_time_split.setHandleWidth(1)
        layout.addWidget(canvas_time_split)

        timeline_split = QSplitter()
        timeline_split.setOrientation(Qt.Horizontal)
        # timeline_split.setHandleWidth(1)

        timeline_split.addWidget(self.layerListView)
        timeline_split.addWidget(QLabel("Timeline"))

        canvas_time_split.addWidget(self.stageView)
        canvas_time_split.addWidget(timeline_split)

    def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)

        print("keyPressEvent", event, event.key())

        if event.key() == Qt.Key_Space:
            print("drag...")
            self.stageView.move_camera = True

    def keyReleaseEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        super().keyReleaseEvent(event)

        print("keyPressEvent", event, event.key())

        if event.key() == Qt.Key_Space:
            self.stageView.move_camera = False
