from xml.etree.ElementTree import Element

from PySide2.QtCore import QPoint, QRect

import TextureMgr
from SpriteAnim.Frame import Frame


class Layer:
    """Layer class"""

    def __init__(self, symbol):
        self.symbol = symbol
        self.frames: [Frame] = []
        self.name = "Layer"
        print("Layer init")

    def numFrames(self):
        return len(self.frames)

    def getFrame(self, idx):
        if idx >= self.numFrames(): return None
        return self.frames[idx]

    def appendFrame(self, f):
        f.layer = self
        self.frames.append(f)
        self.symbol.updateTotalFrames()

    # i.e. insert frame after frameNo
    def insertFrame(self, f, frameNo, doUpdate=True):
        f.layer = self

        # array.insert inserts before index
        self.frames.insert(frameNo + 1, f)

        if doUpdate:
            self.updateFrames()

    def replaceFrame(self, frame, frameNo, do_update=True):
        f1 = self.frames[0:frameNo]
        f2 = self.frames[frameNo + 1:]

        self.frames = f1
        self.frames.append(frame)
        for f in f2: self.frames.append(f)

        if do_update:
            self.updateFrames()

    def removeRange(self, min, numFrames, do_update=True):
        f1 = self.frames[0:min]
        f2 = self.frames[min + numFrames:]
        self.frames = f1
        for f in f2:
            self.frames.append(f)

        # print "removeRange"
        # print "f1: ",  f1
        # print "f2: ",  f2
        # print "final: ",  self.frames
        if do_update:
            self.updateFrames()

    # Update all frames to have proper content types, textures, symbols, keyframe start/ends
    def updateFrames(self):
        nextKey = self.nextKeyFrameForFrame(0)
        curKeyFrame = self.frames[0]

        symbol_frame = 0

        prevFrame: Frame = None
        f: Frame

        for i in range(0, len(self.frames)):
            f = self.frames[i]
            f.frameNo = i
            if f.isFrame():
                f.contentType = curKeyFrame.contentType
                f.symbol = curKeyFrame.symbol
                f.tex = curKeyFrame.tex

                if f.contentType == Frame.CONTENT_SYMBOL:
                    symbol_frame += 1

                f.keyFrameStart = curKeyFrame.frameNo
                f.keyFrameEnd = nextKey

                # print "set contentType to key ",  curKeyFrame.frameNo,  " contentType ",  curKeyFrame.contentType
            else:
                curKeyFrame = f
                # print "new keyframe... ",  f.frameNo,  f.contentType
                nextKey = self.nextKeyFrameForFrame(i)

                if prevFrame is not None:
                    if not prevFrame.is_same_content_as_frame(f):
                        symbol_frame = 0
                else:
                    symbol_frame = 0

            if f.symbol_frame != -1:
                symbol_frame = f.symbol_frame

            if f.contentType == Frame.CONTENT_SYMBOL:
                if symbol_frame >= f.symbol.totalFrames:
                    symbol_frame = 0

            prevFrame = f
            f.cached_symbol_frame = symbol_frame


    def keyframeForFrame(self, frameNo):
        for i in range(frameNo, 0, -1):
            f = self.frames[i]
            if f.isKey():
                return i

        return 0

    def nextKeyFrameForFrame(self, frameNo):
        for i in range(frameNo + 1, len(self.frames)):
            f = self.frames[i]
            if f.isKey():
                return i

        return 0

    def convertToKeyframe(self, frameNo):
        f = self.frames[frameNo]
        newFrame = f.clone()
        newFrame.type = Frame.TYPE_KEY
        newFrame.pos = f.getOffs()
        return newFrame

    def boundingBoxForFrame(self, frameNo):
        f = self.getFrame(frameNo)
        if not f:
            return None

        return f.boundingBox()

    def load_from_xml(self, node: Element):
        self.name = node.get("name")

        f: Element
        cur_frame = -1
        for f in list(node):

            frame_no = int(f.get("n"))
            content_type = f.get("contentType")

            if frame_no <= cur_frame:
                print("Error, frame number {} not valid here.".format(frame_no))
                continue

            print("frame: ", frame_no, f.tag, f)

            # Fill in frames from last until this (-1)
            print("fill frames {} -> {}".format(cur_frame, frame_no))
            for i in range(cur_frame + 1, frame_no):
                print("fill frame {}".format(i))

                frame = Frame(i, Frame.CONTENT_EMPTY, frame_type=Frame.TYPE_FRAME)
                self.appendFrame(frame)

            frame: Frame

            if f.tag == "keyframe":

                if content_type == "texture":
                    frame = Frame(frame_no, Frame.CONTENT_TEXTURE, frame_type=Frame.TYPE_KEY)
                    frame.texturePath = f.get("path")
                    frame.tex = TextureMgr.textureMgr().loadImage(frame.texturePath)
                    frame.srcRect = QRect(0, 0, frame.tex.width(), frame.tex.height())

                offs_x = int(f.get("x"))
                offs_y = int(f.get("y"))

                frame.setPos(QPoint(offs_x, offs_y))
                print(frame.pos)

            if f.tag == "frame":
                frame = Frame(frame_no, Frame.CONTENT_EMPTY, frame_type=Frame.TYPE_FRAME)

            self.appendFrame(frame)

            cur_frame = frame_no

        print("total frames: {}".format(len(self.frames)))
