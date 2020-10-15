# Actions for modifying the properties of individual frames

# does not include timeline modifying stuff.

# This is for setting textures, positions, playback info, and probably tweens
from PySide2.QtCore import QPoint

from Editor import Editor
from Editor.Actions.Action import Action
from SpriteAnim.Frame import Frame
from SpriteAnim.LibraryItem import SymbolLibraryItem


class SetFrameTexturePathAction(Action):

    def __init__(self,  symbol, texturePath, layerNo, frameNo):
        super(SetFrameTexturePathAction,  self).__init__()
        # todo: frame under cursor must exist before drag+drop is even allowed!
        self.symbol = symbol
        self.layerNo = layerNo
        self.frameNo = frameNo
        
        self.prevFrame = symbol.getFrame(layerNo, frameNo)
        self.frame = self.prevFrame.clone()
        self.frame.setTexture(texturePath)
    
    def redo(self, editor: Editor):
        layer = self.symbol.getLayer(self.layerNo)
        layer.replaceFrame(self.frame,  self.frameNo)
        
    def undo(self, editor: Editor):
        layer = self.symbol.getLayer(self.layerNo)
        layer.replaceFrame(self.prevFrame,  self.frameNo)


class SetFrameSymbolAction(Action):

    def __init__(self, symbol, item: SymbolLibraryItem, layer_number, frame_number):
        super(SetFrameSymbolAction, self).__init__()
        # todo: frame under cursor must exist before drag+drop is even allowed!
        self.symbol = symbol
        self.item = item
        self.layer_number = layer_number
        self.frame_number = frame_number

        self.prevFrame = symbol.getFrame(layer_number, frame_number)
        self.frame = self.prevFrame.clone()
        self.frame.setSymbol(item.symbol)

    def redo(self, editor: Editor):
        layer = self.symbol.getLayer(self.layer_number)
        layer.replaceFrame(self.frame, self.frame_number)

    def undo(self, editor: Editor):
        layer = self.symbol.getLayer(self.layer_number)
        layer.replaceFrame(self.prevFrame, self.frame_number)



# Works on keyframes only
class ChangeOffsetAction(Action):
    def __init__(self,  symbol,  layerNo,  frameNo,  oldOffs,  newOffs):
        super(ChangeOffsetAction,  self).__init__()
        
        self.symbol = symbol
        self.layerNo = layerNo
        self.frameNo = frameNo
        self.oldOffs = oldOffs
        self.newOffs = newOffs

    def getFrame(self) -> Frame:
        return self.symbol.getFrame(self.layerNo, self.frameNo)

    def redo(self, editor):
        f = self.getFrame()
        f.setPos(self.newOffs)
    
    def undo(self, editor):
        f = self.getFrame()
        f.setPos(self.oldOffs)


# Move frames sub action
class ChangeMultipleFrameOffsets(Action):
    def __init__(self,  symbol, frames, offsDelta: QPoint):
        super(ChangeMultipleFrameOffsets,  self).__init__()
        
        self.symbol = symbol
        self.actions = []
        self.offsDelta = offsDelta
        
        for f in frames:
            o = f.getOffs()
            # find keyframes if this is a regular frame without tween
            
            # if normal frame with tween, this will be converted to a keyframe, not changeoffsetaction
            self.actions.append(ChangeOffsetAction(self.symbol,  f.getLayerNo(), f.frameNo, o,  o + offsDelta))
            
    def redo(self, editor):
        for a in self.actions:
            a.redo(editor)
    
    def undo(self, editor):
        for a in self.actions:
            a.undo(editor)
        
# Move frames action
#  Requires: Full deltaX,Y, list of frames involved
