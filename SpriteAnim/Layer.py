from SpriteAnim.Frame import Frame


class Layer:
    """Layer class"""
    
    
    
    def __init__(self,  symbol):
        self.symbol = symbol
        self.frames = []
        self.name = "Layer"
        print("Layer init")

    def numFrames(self):
        return len(self.frames)
    
    def getFrame(self,  idx):
        if idx >= self.numFrames(): return None
        return self.frames[idx]
        
    def appendFrame(self, f):
        f.layer = self
        self.frames.append(f)
        self.symbol.updateTotalFrames()

    # i.e. insert frame after frameNo
    def insertFrame(self,  f,  frameNo,  doUpdate = True):
        f.layer = self

        # array.insert inserts before index
        self.frames.insert(frameNo + 1,  f )
        
        if doUpdate: self.updateFrameNumbers()

    def replaceFrame(self, frame, frameNo, do_update = True):
        f1 = self.frames[0:frameNo]
        f2 = self.frames[frameNo+1:]
        
        self.frames = f1
        self.frames.append(frame)
        for f in f2: self.frames.append(f)
        
        if do_update:
            self.updateFrames()
        
    def removeRange(self,  min,  numFrames,  doUpdate = True):
        f1 = self.frames[0:min]
        f2 = self.frames[min+numFrames:]
        self.frames = f1;
        for f in f2: self.frames.append(f)
        
        #print "removeRange"
        #print "f1: ",  f1
        #print "f2: ",  f2
        #print "final: ",  self.frames
        if doUpdate: self.updateFrameNumbers()
        
    # Update all frames to have proper content types, textures, symbols, keyframe start/ends
    def updateFrameNumbers(self):
        nextKey = self.nextKeyFrameForFrame(0)
        curKeyFrame = self.frames[0]
        
        for i in range(0,  len(self.frames)):
            f = self.frames[i]
            f.frameNo = i
            if f.isFrame():
               f.keyFrameStart = curKeyFrame.frameNo 
               f.keyFrameEnd = nextKey
               f.contentType = curKeyFrame.contentType
               #print "set contentType to key ",  curKeyFrame.frameNo,  " contentType ",  curKeyFrame.contentType
               f.tex = curKeyFrame.tex
               f.symbol = curKeyFrame.symbol
            else:
                curKeyFrame = f
                #print "new keyframe... ",  f.frameNo,  f.contentType
                nextKey = self.nextKeyFrameForFrame(i)
    
    def updateFrames(self):
        self.updateFrameNumbers()
        
    def keyframeForFrame(self,  frameNo):
        for i in range(frameNo, 0, -1):
            f = self.frames[i]
            if f.isKey():
                return i
                
        return 0
        
    def nextKeyFrameForFrame(self,  frameNo):
        for i in range(frameNo + 1,  len(self.frames)):
            f = self.frames[i]
            if f.isKey():
                return i
                
        return 0    

    def convertToKeyframe(self,  frameNo):
        f = self.frames[frameNo]
        newFrame = f.clone()
        newFrame.type = Frame.TYPE_KEY
        newFrame.pos = f.getOffs()
        return newFrame
        

    def boundingBoxForFrame(self,  frameNo):
        f = self.getFrame(frameNo)
        if f == None: return None
        
        return f.boundingBox()
