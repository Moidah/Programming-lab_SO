import threading

class RendezvousDEchange:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.put_value = None
        self.put_ready = False
        self.get_ready = False
        self.exchanged_value = None

    def put(self, item):
        with self.condition:
            # Guardamos el valor del productor
            while self.put_ready:  # Espera si ya hay otro productor esperando
                self.condition.wait()
            self.put_value = item
            self.put_ready = True

            # Notifica al consumidor que hay valor disponible
            self.condition.notify_all()

            # Espera a que un consumidor esté listo
            while not self.get_ready:
                self.condition.wait()

            # El consumidor ya tomó el valor, obtenemos el suyo
            result = self.exchanged_value

            # Reiniciamos estado
            self.put_value = None
            self.put_ready = False
            self.get_ready = False

            self.condition.notify_all()
            return result

    def get(self):
        with self.condition:
            # Espera hasta que haya un productor listo
            while not self.put_ready:
                self.condition.wait()

            # Ahora, intercambiamos valores
            self.exchanged_value = self.put_value
            self.get_ready = True

            self.condition.notify_all()

            # Esperamos a que el productor termine de intercambiar
            while self.get_ready:
                self.condition.wait()

            return self.put_value
