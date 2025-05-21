import threading

class RendezvousDEchange:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.first_value = None
        self.second_value = None
        self.first_arrived = False
        self.exchange_complete = False

    def echanger(self, item):
        with self.condition:
            if not self.first_arrived:
                # Este es el primer hilo que llega
                self.first_value = item
                self.first_arrived = True
                
                # Espera a que el segundo hilo llegue y complete el intercambio
                while not self.exchange_complete:
                    self.condition.wait()
                
                # Obtiene el valor del segundo hilo
                result = self.second_value
                
                # Reinicia el estado para la próxima operación
                self.first_arrived = False
                self.exchange_complete = False
                self.first_value = None
                self.second_value = None
                
                # Notifica a cualquier hilo esperando que el rendezvous está disponible
                self.condition.notify_all()
            else:
                # Este es el segundo hilo que llega
                self.second_value = item
                self.exchange_complete = True
                
                # Notifica al primer hilo que el intercambio está listo
                self.condition.notify_all()
                
                # Devuelve el valor del primer hilo
                result = self.first_value
                
            return result