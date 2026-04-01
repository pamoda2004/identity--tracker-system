class UnknownGalleryService:
    def __init__(self):
        self.unknown_captures = []

    def add(self, capture):
        self.unknown_captures.append(capture)

    def list_recent(self, limit=50):
        return self.unknown_captures[-limit:]

    def find_by_unknown_id(self, unknown_id: str):
        for item in self.unknown_captures:
            if item["unknown_id"] == unknown_id:
                return item
        return None

    def assign_name(self, unknown_id: str, name: str):
        item = self.find_by_unknown_id(unknown_id)
        if item:
            item["assigned_name"] = name
        return item