from abc import abstractmethod

from PySide2.QtCore import QRect

from Editor import Editor
from SpriteAnim import Symbol, LibraryItem
from SpriteAnim.frame import Frame


class Action(object):
    # Set after the action is instantiated

    # Editor state before the action
    prev_editor_frame: int
    prev_editor_layer: int

    # Selection...

    # Symbol we're editing
    symbol: Symbol

    def __init__(self):
        self.prev_editor_frame = 0
        self.prev_editor_frame = 0
        print("new action")

    @abstractmethod
    def undo(self, editor: Editor):
        print("Action.undo")
        editor.set_frame_number(self.prev_editor_frame)

    @abstractmethod
    def redo(self, editor: Editor):
        print("Action.redo")

    def getFrame(self) -> Frame:
        return self.symbol.getFrame(self.layerNo, self.editor_frame)


class InsertFrameRangeSubAction(Action):
    def __init__(self, symbol, layerNo, x, numFrames):
        super(InsertFrameRangeSubAction, self).__init__()

        self.symbol = symbol
        self.layerNo = layerNo

        # insertion index is x + 1

        # Insert n frames after x
        last = x + numFrames - 1

        # if there's a frame here, then we can just add numFrames new frames after x
        if x > symbol.numFramesInLayer(layerNo):
            x = symbol.numFramesInLayer(layerNo) - 1
            last -= 1

        self.numFrames = last - x + 1
        if self.numFrames == 0:
            self.numFrames = 1

        self.x = x
        self.last = last
        # print "x: ",  self.x,  " numFrames: ",  self.numFrames
        self.frames = []
        for i in range(0, self.numFrames):
            f = Frame(0, Frame.CONTENT_EMPTY)
            f.type = Frame.TYPE_FRAME

            self.frames.append(f)

    # inserting numFrames *AFTER* x
    def redo(self, editor):
        l = self.symbol.layers[self.layerNo]
        j = self.x
        for i in range(0, self.numFrames):
            l.insertFrame(self.frames[i], j, False)
            j += 1

        l.updateFrames()

    def undo(self, editor):
        l = self.symbol.layers[self.layerNo]
        # print "removing range ",  self.x,  self.numFrames
        l.removeRange(self.x + 1, self.numFrames, False)
        # pull out frames in that range
        l.updateFrames()


# Inserts frames after selection.x or currentFrame (eg. Flash Insert > Timeline > Frame )
# If a selection is given, then that many 
# params are x and width
# width frames are inserted AFTER x
# if no selection is given, consider width 1 at current frame (should be supplied), plus it only applies to layers with a frame in it
class InsertFrameAction(Action):
    def __init__(self, symbol, selection, currentFrame):
        super(InsertFrameAction, self).__init__()

        self.actions = []
        self.symbol = symbol
        # insertMode:
        # 0 - use the selection
        # 1 - do all layers where a frame exists at currentFrame
        self.insertMode = 0
        if selection.x() == -1:
            self.insertMode = 1
            self.selection = QRect(currentFrame, 0, 1, self.symbol.num_layers())
        else:
            self.selection = selection

        print(selection)

        startLayer = self.selection.y()
        endLayer = startLayer + self.selection.height()

        # make a series of InsertFrameRangeSubAction for each layer
        for curLayer in range(startLayer, endLayer):
            l = self.symbol.layers[curLayer]
            if l.numFrames() <= self.selection.x() and self.insertMode == 1:
                continue

            act = InsertFrameRangeSubAction(self.symbol, curLayer, self.selection.x(), self.selection.width())
            self.actions.append(act)

    def redo(self, editor):
        for a in self.actions:
            a.redo(editor)
        self.symbol.updateTotalFrames()

    def undo(self, editor):
        # just run this operation on all the layers
        for a in self.actions:
            a.undo(editor)
        self.symbol.updateTotalFrames()


class ConvertKeyFrameSubAction(Action):
    def __init__(self, symbol, layerNo, frameNo):
        super(ConvertKeyFrameSubAction, self).__init__()

        # This is the frame that existed before
        self.prevFrame = None
        self.symbol = symbol
        self.layerNo = layerNo
        self.frameNo = frameNo

    def redo(self, editor):
        l = self.symbol.layers[self.layerNo]

        self.prevFrame = l.getFrame(self.frameNo)

        if self.prevFrame.isKey():
            return

        frame = l.convertToKeyframe(self.frameNo)

        l.replaceFrame(frame, self.frameNo)

    def undo(self, editor):
        if self.prevFrame.isKey():
            return

        l = self.symbol.layers[self.layerNo]

        if self.prevFrame != None:
            l.replaceFrame(self.prevFrame, self.frameNo)

        # else:
        # There was nothing here before
        #    l.removeRange( self.frameNo,  1)


"""            
class UpdateFramesSubAction(Action):
    def __init__(self,  symbol,  layerNo):
        super(UpdateFramesSubAction,  self).__init__()
"""


class ConvertKeyframeAction(Action):

    def __init__(self, symbol, selection, layerNo, currentFrame):
        super(ConvertKeyframeAction, self).__init__()

        usingSelection = selection.x() != -1

        if not usingSelection:
            selection = QRect(currentFrame, layerNo, 1, 1)

        self.symbol = symbol
        # frame/layer start, width/height info
        self.selection = QRect(selection.x(), selection.y(), selection.width(), selection.height())
        self.actions = []

        startLayer = self.selection.y()
        endLayer = startLayer + self.selection.height()

        if usingSelection and self.selection.width() == 1 and self.selection.height() == 1:
            f = self.symbol.getFrame(startLayer, selection.x())
            if f != None and f.isKey():
                print("Special case...", self.selection)
                selection.moveLeft(self.selection.x() + 1)
                self.selection = selection

                print(self.selection)

        # make a series of InsertFrameRangeSubAction for each layer
        for curLayer in range(startLayer, endLayer):
            l = self.symbol.layers[curLayer]
            # 1. insert any new empty frames up till this point if there aren't any (InsertFrameRangeSubAction)
            if l.numFrames() < self.selection.x() + self.selection.width():
                act = InsertFrameRangeSubAction(self.symbol, curLayer, l.numFrames() - 1,
                                                self.selection.x() + self.selection.width() - l.numFrames())
                self.actions.append(act)

            # for each frame in range: ConvertKeyFrameSubAction, if it's not a keyframe already (todo)
            for x in range(self.selection.x(), self.selection.x() + self.selection.width()):
                act = ConvertKeyFrameSubAction(self.symbol, curLayer, x)
                self.actions.append(act)

        # on nonexistent frames, new keyfames will be created
        # on normal frames, they will be converted to a keyframe
        # on keyframes, do nothing

        # for undo, it might be best to just store the original frames?

        # Also, for the leftmost side of the selection, create normal frames for any empty frame before the keyframe

        # for each layer:

    def redo(self, editor):
        for a in self.actions:
            a.redo(editor)

        self.symbol.updateTotalFrames()

    def undo(self, editor):
        # undo the actions in reverse

        for i in range(len(self.actions) - 1, -1, -1):
            self.actions[i].undo(editor)

        self.symbol.updateTotalFrames()


class ReplaceFrameSubAction(Action):
    def __init__(self, symbol, layerNo, frameNo, newFrame):
        super(ReplaceFrameSubAction, self).__init__()
        # frame at layerNo/frameNo should exist otherwise this does nothing
        self.symbol = symbol
        self.layerNo = layerNo
        self.frameNo = frameNo
        self.newFrame = newFrame

        l = self.symbol.layers[self.layerNo]
        self.prevFrame = l.getFrame(self.frameNo)

    def redo(self, editor):
        l = self.symbol.layers[self.layerNo]
        l.replaceFrame(self.newFrame, self.frameNo)

    def undo(self, editor):
        if self.prevFrame == None:
            return

        l = self.symbol.layers[self.layerNo]
        l.replaceFrame(self.prevFrame, self.frameNo)


# converts keyframes to regular frames        
class ClearKeyframeAction(Action):

    def __init__(self, symbol, selection):
        super(ClearKeyframeAction, self).__init__()
        self.symbol = symbol
        self.selection = selection
        self.actions: [Action] = []
        # requires a selection
        startLayer = self.selection.y()
        endLayer = startLayer + self.selection.height()

        # make a series of InsertFrameRangeSubAction for each layer
        for curLayer in range(startLayer, endLayer):
            l = self.symbol.layers[curLayer]
            for x in range(self.selection.x(), self.selection.x() + self.selection.width()):
                f = l.getFrame(x)
                if f == None or f.isFrame():
                    continue

                newFrame = f.clone()
                if x == 0:
                    newFrame.setEmpty()
                else:
                    newFrame.type = Frame.TYPE_FRAME

                act = ReplaceFrameSubAction(self.symbol, curLayer, x, newFrame)
                self.actions.append(act)

    def redo(self, editor):
        for a in self.actions:
            a.redo(editor)

    def undo(self, editor):
        for a in self.actions:
            a.undo(editor)


class NewSymbolAction(Action):
    def __init__(self, library, symbolName):
        super(NewSymbolAction, self).__init__()

        self.library = library
        self.symbol = Symbol()
        self.symbol.name = symbolName

        self.item = LibraryItem()
        self.item.setAsSymbol(self.symbol)

    def redo(self, editor):
        self.library.addItem(self.item)
        editor.libraryWindow.repaint()

    def undo(self, editor):
        self.library.removeItem(self.item)
        editor.libraryWindow.repaint()
