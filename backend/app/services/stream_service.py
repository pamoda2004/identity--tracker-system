class StreamService:
    def __init__(self):
        self.latest_frame_path = None

    def set_latest_frame(self, frame_path: str):
        self.latest_frame_path = frame_path

    def get_latest_frame(self):
        return self.latest_frame_path