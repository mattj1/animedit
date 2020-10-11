class Library:
    
    # The library can store the following things:
    #  Symbols
    #  Linked symbols
    #  Textures
    
    ITEM_NONE = 0
    ITEM_SYMBOL = 1
    ITEM_LINKED_SYMBOL = 2
    ITEM_TEXTURE = 3
    
    def __init__(self):
        self.items = []
        print("Library init")

    # Add an item. Can be called during importing, or loading, etc.
    def addItem(self,  item):
        self.items.append(item)

    def removeItem(self,  item):
        self.items.remove(item)
        
    # Save/load this to file
    def save(self):
        print("Saving...")
        # Do we need to catalog them in any way first?
        # Go through all the library entries and store them
        
    def load(self):
        print("Loading...")


class LibraryItem:
    def __init__(self):
        self.type = Library.ITEM_NONE
        self.mimeString = "none,none"

    def is_texture(self):
        return self.type == Library.ITEM_TEXTURE

    def is_symbol(self):
        return self.type == Library.ITEM_SYMBOL

    # Embedded symbol
    def setAsSymbol(self,  sym):
        self.sym = sym
        self.type = Library.ITEM_SYMBOL
        
    # A texture. The library does not have to store the actual data. Use texture manager for this.
    def setAsTexture(self, path):
        self.texturePath = path
        self.type = Library.ITEM_TEXTURE
        
    def setAsLinkedSymbol(self,  path):
        self.path = path
        self.type = Library.LINKED_SYMBOL
        
    def getMimeString(self):
        if self.type == Library.ITEM_SYMBOL:
            self.mimeString = "symbol," + self.sym.name
        elif self.type == Library.ITEM_TEXTURE:
            self.mimeString = "texture," + self.texturePath
        elif self.type == Library.LINKED_SYMBOL:
            self.mimeString = "linkedsymbol," + self.path
        
        return self.mimeString
        
