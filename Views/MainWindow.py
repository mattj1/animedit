import PySide6.QtGui
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QLabel, QFrame

from Editor import Editor
from Views import LayerListView, StageView
from Views.TimelineView import TimelineView


class MainWindow(QMainWindow):
    def __init__(self, editor: Editor, parent=None):
        super(MainWindow, self).__init__(parent)

        self.layerListView = LayerListView(editor=editor, parent=self)
        self.timelineView = TimelineView(editor=editor, parent=self)
        self.stageView = StageView(editor=editor, parent=self)

        self.editor = editor
        self.editor.set_view(self)

        self.setWindowTitle("Editor")
        self.resize(1024, 768)

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
        timeline_split.addWidget(self.timelineView)

        canvas_time_split.addWidget(self.stageView)
        canvas_time_split.addWidget(timeline_split)

        canvas_time_split.setSizes([475-100, 100])

        self.is_playing = False

        self.timer_id = None

    def start_playback(self):
        if self.is_playing:
            return

        self.is_playing = True
        self.timer_id = self.startTimer(int(1000 / 12), Qt.TimerType.CoarseTimer)

    def stop_playback(self):
        if not self.is_playing:
            return

        self.is_playing = False
        self.killTimer(self.timer_id)
        self.timer_id = None

    def timerEvent(self, event: PySide6.QtCore.QTimerEvent) -> None:
        super().timerEvent(event)
        # print("timerEvent", event)
        fn = self.editor.frame_number + 1

        if fn >= self.editor.current_symbol.totalFrames:
            fn = 0

        self.editor.frame_number = fn

    def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)

        # if event.key() == Qt.Key_Right:
        #     self.editor.frame_number = self.editor.frame_number + 1

        if event.key() == Qt.Key_Space:
            self.stageView.move_camera = True

    def keyReleaseEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        super().keyReleaseEvent(event)


        if event.key() == Qt.Key_Space:
            self.stageView.move_camera = False
