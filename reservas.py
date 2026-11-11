import logging
from clientes import DatoInvalidoError, ErrorSoftwareFJ

logger = logging.getLogger("software_fj")

class Reserva:
    """Clase Reserva que integra cliente, servicio, duración y estado con manejo avanzado de errores."""
    
    contador_ids = 1

    def __init__(self, cliente, servicio, cantidad_unidad, tipo_parametro=0.0):
        self.__id_reserva = Reserva.contador_ids
        Reserva.contador_ids += 1
        self.__cliente = cliente
        self.__servicio = servicio
        self.__cantidad_unidad = cantidad_unidad
        self.__tipo_parametro = tipo_parametro  
        self.__estado = "Creada"
        self.__costo_total = 0.0
        
        self.procesar_reserva()

    @property
    def id_reserva(self):
        return self.__id_reserva

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def procesar_reserva(self):
        """Procesa la reserva utilizando try/except/else y try/except/finally para máxima robustez."""
        try:
            if not self.__cliente or not self.__servicio:
                raise ValueError("La reserva debe tener un cliente y un servicio válidos asignados.")
            
            self.__costo_total = self.__servicio.calcular_costo(self.__cantidad_unidad, self.__tipo_parametro)
            
        except ValueError as ve:
            self.__estado = "Fallida"
            error_msg = f"Error de validación en Reserva #{self.__id_reserva}: {ve}"
            logger.error(error_msg)
            raise DatoInvalidoError(error_msg)
            
        except Exception as e:
            self.__estado = "Error Crítico"
            error_msg = f"Error inesperado procesando Reserva #{self.__id_reserva}: {e}"
            logger.critical(error_msg)
            raise ErrorSoftwareFJ(error_msg)
            
        else:
            self.__estado = "Confirmada"
            logger.info(f"Reserva #{self.__id_reserva} confirmada con éxito para {self.__cliente.nombre}. Total: ${self.__costo_total}")
            
        finally:
            print(f"[Transacción Finalizada] Intento de procesamiento para la Reserva #{self.__id_reserva} - Estado final: {self.__estado}")

    def cancelar_reserva(self):
        """Cancela la reserva de manera segura controlando excepciones."""
        try:
            if self.__estado == "Cancelada":
                raise ErrorSoftwareFJ(f"La reserva #{self.__id_reserva} ya se encontraba cancelada.")
            
            self.__estado = "Cancelada"
            logger.warning(f"Reserva #{self.__id_reserva} cancelada correctamente.")
            print(f"La reserva #{self.__id_reserva} ha sido cancelada exitosamente.")
            
        except Exception as e:
            logger.error(f"No se pudo cancelar la reserva #{self.__id_reserva}: {e}")
            print(f"Error al cancelar la reserva: {e}")

    def obtener_reserva_detalles(self):
        return (f"Reserva ID: {self.__id_reserva} | "
                f"Cliente: {self.__cliente.nombre} | "
                f"Servicio: {self.__servicio.nombre_servicio} | "
                f"Estado: {self.__estado} | "
                f"Costo Total: ${self.__costo_total:.2f}")
