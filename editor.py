# import clock

__version__ = '0.0.0'

import sys

from PySide2.QtWidgets import QApplication

from Editor import Editor
from Views.MainWindow import MainWindow

if __name__ == '__main__':
    editor = Editor()

    app = QApplication(sys.argv)
    frame = MainWindow(editor)
    frame.show()
    frame.postShow()

    sys.exit(app.exec_())

"""
 Symbols can contain images and symbols.
 
 Should probably manage images in a seperate class to save memory?

"""
