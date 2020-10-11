from PySide2.QtGui import QPixmap, QImage


class _TextureMgr:
    """
    Texture manager class
    
    Stores a map of file names to QPixmaps
    
    """

    textures = {}

    def __init__(self):
        print("TextureMgr init")

    def loadImage(self, filename) -> QPixmap:
        filename = str(filename)
        pm = self.textures.get(filename)

        if pm is None:
            pm = QPixmap.fromImage(QImage(filename))
            # pm = QPixmap(filename)
            self.textures[filename] = pm

        return pm


_textureMgr = _TextureMgr()


def textureMgr():
    return _textureMgr
