class RegistryService:
    def __init__(self, tracker):
        self.tracker = tracker

    def get_active_people(self):
        return self.tracker.active_people()