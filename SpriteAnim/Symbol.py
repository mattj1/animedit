from xml.etree.ElementTree import Element

import TextureMgr
from SpriteAnim.frame import Frame
from SpriteAnim.layer import Layer
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

    def num_layers(self):
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
        layer = self.get_layer(layerNo)
        if layer:
            return layer.get_frame(frameNo)

        return None

    def get_layer(self, idx):
        if idx >= len(self.layers):
            return None

        return self.layers[idx]

    def add_layer(self, layer):
        self.layers.append(layer)
        self.update_layers()

    # insert layer before index idx
    def insert_layer(self, layer, idx):
        self.layers.insert(idx, layer)
        self.update_layers()

    def remove_layer(self, layer):
        self.layers.remove(layer)
        self.update_layers()

    def update_layers(self):
        c = 0
        for layer in self.layers:
            layer.layerNo = c
            c += 1

        self.updateTotalFrames()

    def updateTotalFrames(self):
        self.totalFrames = 0
        for layer in self.layers:
            if layer.num_frames() > self.totalFrames:
                self.totalFrames = layer.num_frames()

    # def drawFrame(self, frame_number: int, painter: QPainter):
    #     n = self.numLayers()
    #     for i in range(n - 1, -1, -1):
    #         l = self.layers[i]
    #         if frame_number >= l.numFrames():
    #             continue
    #         # print "drawing ",  frameNo,  l.numFrames()
    #         l.frames[frame_number].draw(painter)

    def numFramesInLayer(self, layerNo):
        return self.layers[layerNo].numFrames()

    # def boundingBoxForFrame(self, frame_number: int):
    #     bb = QRectF(0, 0, 0, 0)
    #     # Run through all the frames and get their bounding box
    #     for l in self.layers:
    #         f = l.getFrame(frame_number)
    #         if f is None:
    #             continue
    #
    #         box = f.boundingBox()
    #         if box is not None:
    #             bb = bb.united(box)
    #
    #     return bb

    def clearDragItems(self):
        for frame in self.dragItems:
            frame.setSelected(0)

        self.dragItems = []

    def numDragItems(self):
        return len(self.dragItems)

    def addDragItem(self, i):
        self.dragItems.append(i)

    def load_from_xml(self, node: Element, library):
        self.name = node.get("name")
        print(f'Symbol load_from_xml {self.name}')

        for n in node.iterfind("layer"):
            layer = Layer(self)
            layer.load_from_xml(n, library)
            self.add_layer(layer)

            # layer.updateFrames()

        # self.updateTotalFrames()

    def get_total_frames(self):
        self.updateTotalFrames()
        return self.totalFrames

    # Parse a <symbol> item
    @staticmethod
    def from_xml(node: Element, library):
        print("from_xml", node)
        symbol = Symbol()
        symbol.load_from_xml(node, library)

        return symbol

    @staticmethod
    def from_empty():
        symbol = Symbol()

        layer = Layer(symbol)
        layer.name = "Layer 0"
        frame = Frame(0, Frame.CONTENT_EMPTY, Frame.TYPE_KEY)
        layer.frames.append(frame)
        symbol.add_layer(layer)

        layer = Layer(symbol)
        layer.name = "Layer 1"
        layer.frames.append(Frame(0, Frame.CONTENT_EMPTY, Frame.TYPE_KEY))
        layer.frames.append(Frame(1, Frame.CONTENT_EMPTY, Frame.TYPE_FRAME))
        layer.frames.append(Frame(2, Frame.CONTENT_EMPTY, Frame.TYPE_FRAME))
        layer.frames.append(Frame(3, Frame.CONTENT_EMPTY, Frame.TYPE_KEY))
        layer.frames.append(Frame(4, Frame.CONTENT_EMPTY, Frame.TYPE_KEY))
        # layer.frames
        symbol.add_layer(layer)

        for layer in symbol.layers:
            layer.update_frames()

        symbol.update_layers()
        return symbol
