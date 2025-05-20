import threading

class RendezvousDEchange:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = None
        self.full = False
        self.condition = threading.Condition(self.lock)

    def put(self, item):
        # Implementación pendiente
        pass

    def get(self):
        # Implementación pendiente
        pass
