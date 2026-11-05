from excepciones_y_logs import ErrorReserva, LoggerSistema

class Reserva:
    """Clase Reserva que integra cliente, servicio, duración y estado con manejo avanzado de errores."""
    
    contador_ids = 1

    def __init__(self, cliente, servicio, cantidad_unidad, tipo_parametro=0.0):
        self.__id_reserva = Reserva.contador_ids
        Reserva.contador_ids += 1
        self.__cliente = cliente
        self.__servicio = servicio
        self.__cantidad_unidad = cantidad_unidad
        self.__tipo_parametro = tipo_parametro  # Descuento, seguro o complejidad según el servicio
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
            # Validación previa de objetos
            if not self.__cliente or not self.__servicio:
                raise ValueError("La reserva debe tener un cliente y un servicio válidos asignados.")
            
            # Cálculo del costo usando el polimorfismo del servicio
            # Python evaluará dinámicamente el método calcular_costo según el tipo de servicio
            self.__costo_total = self.__servicio.calcular_costo(self.__cantidad_unidad, self.__tipo_parametro)
            
        except ValueError as ve:
            # Bloque try/except para errores de parámetros lógicos
            self.__estado = "Fallida"
            error_msg = f"Error de validación en Reserva #{self.__id_reserva}: {ve}"
            LoggerSistema.registrar(error_msg, "ERROR")
            raise ErrorReserva(error_msg)
            
        except Exception as e:
            # Bloque para cualquier otro error inesperado
            self.__estado = "Error Crítico"
            error_msg = f"Error inesperado procesando Reserva #{self.__id_reserva}: {e}"
            LoggerSistema.registrar(error_msg, "CRITICAL")
            raise ErrorReserva(error_msg)
            
        else:
            # Se ejecuta SOLO si todo salió exitosamente (try/except/else requerido por la guía)
            self.__estado = "Confirmada"
            LoggerSistema.registrar(f"Reserva #{self.__id_reserva} confirmada con éxito para {self.__cliente.nombre}. Total: ${self.__costo_total}", "INFO")
            
        finally:
            # Se ejecuta siempre, asegurando el cierre o registro final de la transacción
            print(f"[Transacción Finalizada] Intento de procesamiento para la Reserva #{self.__id_reserva} - Estado final: {self.__estado}")

    def cancelar_reserva(self):
        """Cancela la reserva de manera segura controlando excepciones."""
        try:
            if self.__estado == "Cancelada":
                raise ErrorReserva(f"La reserva #{self.__id_reserva} ya se encontraba cancelada.")
            
            self.__estado = "Cancelada"
            LoggerSistema.registrar(f"Reserva #{self.__id_reserva} cancelada correctamente.", "WARNING")
            print(f"La reserva #{self.__id_reserva} ha sido cancelada exitosamente.")
            
        except Exception as e:
            LoggerSistema.registrar(f"No se pudo cancelar la reserva #{self.__id_reserva}: {e}", "ERROR")
            print(f"Error al cancelar la reserva: {e}")

    def obtener_reserva_detalles(self):
        return (f"Reserva ID: {self.__id_reserva} | "
                f"Cliente: {self.__cliente.nombre} | "
                f"Servicio: {self.__servicio.nombre_servicio} | "
                f"Estado: {self.__estado} | "
                f"Costo Total: ${self.__costo_total:.2f}")