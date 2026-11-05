import datetime
import os

class SistemaGestionError(Exception):
    """Clase base para todas las excepciones personalizadas del sistema."""
    pass

class ErrorClienteInvalido(SistemaGestionError):
    """Excepción lanzada cuando los datos del cliente no cumplen con las validaciones."""
    pass

class ErrorServicioNoDisponible(SistemaGestionError):
    """Excepción lanzada cuando se intenta acceder a un servicio inválido o inactivo."""
    pass

class ErrorReserva(SistemaGestionError):
    """Excepción lanzada cuando ocurre un fallo durante la creación, confirmación o cancelación de una reserva."""
    pass


class LoggerSistema:
    """Clase encargada de registrar eventos y errores en un archivo de logs externo."""
    ARCHIVO_LOG = "sistema.log"

    @staticmethod
    def registrar(mensaje, tipo="INFO"):
        """Registra un evento o error con fecha, hora y nivel en el archivo de log."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{tipo}] {mensaje}\n"
        try:
            with open(LoggerSistema.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
                archivo.write(log_entry)
        except Exception as e:
            print(f"Error crítico al escribir en el archivo de logs: {e}")
            