class FrameSelection:

    def __init__(self, frame_no: int, layer_no: int):
        self.frame_no = frame_no
        self.layer_no = layer_no


class FrameRef:
    layer_no: int
    frame_no: int

    def __init__(self, frame_no, layer_no) -> None:
        super().__init__()

        self.frame_no = frame_no
        self.layer_no = layer_no
