from typing import Any
from xml.etree.ElementTree import Element

from PySide6.QtCore import QPoint, QRect

import TextureMgr
from SpriteAnim.frame import Frame


class Layer:
    """Layer class"""

    def __init__(self, symbol):
        self.symbol = symbol

        from SpriteAnim.frame import Frame
        self.frames: [Frame] = []
        self.name = "Layer"
        print("Layer init")

    def num_frames(self):
        return len(self.frames)


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

    def keyframeForFrame(self, frameNo):
        for i in range(frameNo, 0, -1):
            f = self.frames[i]
            if f.isKey():
                return f

        return None

    def nextKeyFrameForFrame(self, frameNo):
        for i in range(frameNo + 1, len(self.frames)):
            f = self.frames[i]
            if f.isKey():
                return f

        return None

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

    def load_from_xml(self, node: Element, library):
        self.name = node.get("name")
        print(f"Layer load_from_xml {self.name}")

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
            print("Layer.load_from_xml: Fill frames {} -> {}".format(cur_frame, frame_no))
            for i in range(cur_frame + 1, frame_no):
                print("fill frame {}".format(i))

                frame = Frame(i, Frame.CONTENT_EMPTY, frame_type=Frame.TYPE_FRAME)
                self.appendFrame(frame)

            frame: Frame = None

            if f.tag == "keyframe":

                # print("content_type", content_type)
                if content_type == "texture":
                    frame = Frame(frame_no, Frame.CONTENT_TEXTURE, frame_type=Frame.TYPE_KEY)
                    frame.texture_ref = library.get_texture_ref(f.get('name'))

                    # frame.texturePath = f.get("path")
                    # tex = TextureMgr.textureMgr().loadImage(frame.texturePath)
                    # frame.srcRect = QRect(0, 0, frame.tex.width(), frame.tex.height())
                    frame.srcRect = QRect(0, 0, 20, 31)

                if content_type == "symbol":
                    frame = Frame(frame_no, Frame.CONTENT_SYMBOL, frame_type=Frame.TYPE_KEY)
                    frame.symbol_ref = library.get_symbol_ref(f.get('symbol'))

                assert frame is not None

                offs_x = int(f.get("x"))
                offs_y = int(f.get("y"))

                frame.setPos(QPoint(offs_x, offs_y))
                frame.isTween = f.get('tween') == 'true'
                print(frame.pos)

            if f.tag == "frame":
                frame = Frame(frame_no, Frame.CONTENT_EMPTY, frame_type=Frame.TYPE_FRAME)

            self.appendFrame(frame)

            cur_frame = frame_no

        print("total frames: {}".format(len(self.frames)))


    def get_frame(self, frame_number: int) -> Frame | None:
        if frame_number >= self.num_frames():
            return None

        return self.frames[frame_number]

    # Update all frames to have proper content types, textures, symbols, keyframe start/ends
    def update_frames(self):
        cur_key_frame = self.frames[0]
        next_key_frame = self.nextKeyFrameForFrame(0)

        print("layer update_frames: ", self.symbol.name, cur_key_frame, next_key_frame)

        symbol_frame = 0

        prevFrame: Frame = None
        f: Frame

        for i in range(0, len(self.frames)):
            f = self.frames[i]
            f.frameNo = i

            if not f.isKey():
                # If we're processing a regular frame, ...
                f.key_frame_start = cur_key_frame
                f.key_frame_end = next_key_frame

                # print "set contentType to key ",  curKeyFrame.frameNo,  " contentType ",  curKeyFrame.contentType
            else:
                cur_key_frame = f
                next_key_frame = self.nextKeyFrameForFrame(i)

                f.key_frame_start = f
                f.key_frame_end = f

                # TODO: This is only the case if the content didn't change
                if f.symbol_frame != -1:
                    symbol_frame = f.symbol_frame
                # else:
                #     symbol_frame += 1

                # print "new keyframe... ",  f.frameNo,  f.contentType

                # if prevFrame is not None:
                #     if not prevFrame.is_same_content_as_frame(f):
                #         symbol_frame = 0
                # else:
                #     symbol_frame = 0

            if f.get_symbol() is not None:
                if symbol_frame >= f.get_symbol().get_total_frames():
                    symbol_frame = 0

            prevFrame = f
            f.cached_symbol_frame = symbol_frame
            symbol_frame += 1
