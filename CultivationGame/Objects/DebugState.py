class DebugState:
    """Runtime-only debug state shared by debug UI and controls."""

    def __init__(self, enabled=False):
        self.enabled = bool(enabled)
        self.last_message = ""

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def set_message(self, message):
        self.last_message = str(message)

