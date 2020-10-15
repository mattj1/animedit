from xml.etree.ElementTree import Element

from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainter

import TextureMgr
from SpriteAnim.Frame import Frame
from SpriteAnim.Layer import Layer
from TextureMgr import *


class Symbol:
    """Symbol class"""

    def __init__(self):
        print("Symbol init")

        self.layers: [Layer] = []
        self.totalFrames = 0
        self.name = "Symbol"

        # List of frames inside this symbol which have been selected for drag+drop or arrow moving
        self.dragItems: [Frame] = []

    def numLayers(self):
        return len(self.layers)

    def createNewLayer(self):
        l = Layer(self)
        l.name = "Layer %d" % (len(self.layers) + 1)

        # Add in an empty keyframe
        f = Frame(0, Frame.CONTENT_EMPTY)
        f.type = Frame.TYPE_KEY
        l.appendFrame(f)

        return l

    def getFrame(self, layerNo, frameNo) -> Frame:
        return self.layers[layerNo].getFrame(frameNo)

    # insert layer before index idx
    def insertLayer(self, layer, idx):
        self.layers.insert(idx, layer)
        self.updateLayers()

    def getLayer(self, idx):
        return self.layers[idx]

    # Remove layer from layers array
    def removeLayer(self, layer):
        self.layers.remove(layer)
        self.updateLayers()

    def updateTotalFrames(self):
        self.totalFrames = 0
        for i in range(0, len(self.layers)):
            if self.layers[i].numFrames() > self.totalFrames:
                self.totalFrames = self.layers[i].numFrames()

    def updateLayers(self):
        c = 0
        for l in self.layers:
            l.layerNo = c
            c += 1

    def drawFrame(self, frame_number: int, painter: QPainter):
        n = self.numLayers()
        for i in range(n - 1, -1, -1):
            l = self.layers[i]
            if frame_number >= l.numFrames():
                continue
            # print "drawing ",  frameNo,  l.numFrames()
            l.frames[frame_number].draw(painter)

    def numFramesInLayer(self, layerNo):
        return self.layers[layerNo].numFrames()

    def boundingBoxForFrame(self, frame_number: int):
        bb = QRectF(0, 0, 0, 0)
        # Run through all the frames and get their bounding box
        for l in self.layers:
            f = l.getFrame(frame_number)
            if f is None:
                continue

            box = f.boundingBox()
            if box is not None:
                bb = bb.united(box)

        return bb

    def clearDragItems(self):
        for frame in self.dragItems:
            frame.setSelected(0)

        self.dragItems = []

    def numDragItems(self):
        return len(self.dragItems)

    def addDragItem(self, i):
        self.dragItems.append(i)

    def load_from_xml(self, node: Element):
        self.name = node.get("name")

        for n in node.iterfind("layer"):
            layer = Layer(self)
            layer.load_from_xml(n)
            self.layers.append(layer)

            layer.updateFrames()

        self.updateTotalFrames()

    # Parse a <symbol> item
    @staticmethod
    def from_xml(node: Element):
        print("from_xml", node)
        symbol = Symbol()
        symbol.load_from_xml(node)

        return symbol

