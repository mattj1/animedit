# import clock

__version__ = '0.0.0'

import sys

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QApplication

from Editor import Editor
from Views import MainWindow

if __name__ == '__main__':
    editor = Editor()

    app = QApplication(sys.argv)
    frame = MainWindow(editor)
    # frame.resize(1024, 768)
    # frame.move(QPoint(2000, 100))
    frame.show()
    frame.resize(1024, 768)
    frame.resize(1024, 769)
    frame.updateGeometry()
    # frame.postShow()

    sys.exit(app.exec_())
