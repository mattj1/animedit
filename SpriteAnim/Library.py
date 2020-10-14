from uuid import uuid4

from SpriteAnim import LibraryItem


class Library:
    
    # The library can store the following things:
    #  Symbols
    #  Linked symbols
    #  Textures

    def __init__(self):
        self.__items = {}
        self.__item_list = []

        print("Library init")

    def item_for_index(self, index):
        return self.__item_list[index]

    def item_for_uuid(self, uuid: uuid4):
        return self.__items[uuid]

    # Add an item. Can be called during importing, or loading, etc.
    def addItem(self,  item: LibraryItem):
        self.__items[item.uuid] = item
        self.__item_list.append(item)

        #self.items.append(item)

    def removeItem(self,  item):
        self.__items.pop(item.uuid)
        self.__item_list.remove(item)

    # Save/load this to file
    def save(self):
        print("Saving...")
        # Do we need to catalog them in any way first?
        # Go through all the library entries and store them
        
    def load(self):
        print("Loading...")

    def item_list(self):
        return self.__item_list
