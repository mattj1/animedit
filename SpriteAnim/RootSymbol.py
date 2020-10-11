
# Root symbol contains a library and a symbol. It also can be written to a file

# This is typically the thing you edit and save to a file.
# The library, which is saved in the root symbol file, will contain embedded symbols, and
# references to textures and other (root?) symbols
from SpriteAnim.Library import Library


class RootSymbol:
    def __init__(self):
        print("Root Symbol init")
        self.path = ""
        self.symbol = None
        self.library = Library()
    
    def setSymbol(self,  sym):
        self.symbol = sym
        
    def loadFromFile(self,  path):
        print("Loading from file...")
        self.path = path
        # initialize library etc
