class UnknownGalleryService:
    def __init__(self):
        self.unknown_captures = []

    def add(self, capture):
        self.unknown_captures.append(capture)

    def list_recent(self, limit=50):
        return self.unknown_captures[-limit:]