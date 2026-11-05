from abc import ABC, abstractmethod
from excepciones_y_logs import ErrorServicioNoDisponible, LoggerSistema

class Servicio(ABC):
    """Clase abstracta Servicio que define la estructura para los servicios de Software FJ."""
    
    def __init__(self, id_servicio, nombre_servicio, tarifa_base):
        self._id_servicio = id_servicio
        self._nombre_servicio = nombre_servicio
        self._tarifa_base = self._validar_tarifa(tarifa_base)

    def _validar_tarifa(self, tarifa):
        try:
            tarifa_float = float(tarifa)
            if tarifa_float < 0:
                raise ValueError("La tarifa no puede ser negativa.")
            return tarifa_float
        except Exception as e:
            LoggerSistema.registrar(f"Tarifa inválida para el servicio {self._nombre_servicio}: {e}", "ERROR")
            raise ErrorServicioNoDisponible(f"Tarifa de servicio no válida: {tarifa}")

    @property
    def id_servicio(self):
        return self._id_servicio

    @property
    def nombre_servicio(self):
        return self._nombre_servicio

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @abstractmethod
    def calcular_costo(self):
        """Método abstracto que será sobrescrito en las clases hijas (Polimorfismo)."""
        pass

    @abstractmethod
    def describir_servicio(self):
        pass


# --- 1. Servicio Especializado: Reserva de Salas ---
class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, capacidad_personas):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        self.capacidad_personas = capacidad_personas

    def calcular_costo(self, horas=1, descuento_porcentaje=0.0):
        """Método sobrecargado: calcula el costo aplicando horas y descuentos opcionales."""
        try:
            if horas <= 0:
                raise ValueError("Las horas de reserva deben ser mayores a cero.")
            
            subtotal = self.tarifa_base * horas
            descuento = subtotal * (descuento_porcentaje / 100)
            total = subtotal - descuento
            return max(0.0, total)
        except Exception as e:
            LoggerSistema.registrar(f"Error calculando costo en ReservaSala: {e}", "ERROR")
            return self.tarifa_base

    def describir_servicio(self):
        return f"[Sala] {self.nombre_servicio} - Capacidad: {self.capacidad_personas} personas - Tarifa base: ${self.tarifa_base}"


# --- 2. Servicio Especializado: Alquiler de Equipos ---
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, tipo_equipo):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias=1, seguro_adicional=0.0):
        """Método sobrecargado: calcula el costo por días y un seguro opcional."""
        try:
            if dias <= 0:
                raise ValueError("Los días de alquiler deben ser mayores a cero.")
            total = (self.tarifa_base * dias) + seguro_adicional
            return total
        except Exception as e:
            LoggerSistema.registrar(f"Error calculando costo en AlquilerEquipo: {e}", "ERROR")
            return self.tarifa_base

    def describir_servicio(self):
        return f"[Equipo] {self.nombre_servicio} ({self.tipo_equipo}) - Tarifa diaria: ${self.tarifa_base}"


# --- 3. Servicio Especializado: Asesorías Especializadas ---
class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, area_especialidad):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        self.area_especialidad = area_especialidad

    def calcular_costo(self, horas=1, complejidad_impuesto=1.0):
        """Método sobrecargado: calcula el costo por horas y un factor de complejidad."""
        try:
            if horas <= 0:
                raise ValueError("Las horas de asesoría deben ser mayores a cero.")
            total = (self.tarifa_base * horas) * complejidad_impuesto
            return total
        except Exception as e:
            LoggerSistema.registrar(f"Error calculando costo en AsesoriaEspecializada: {e}", "ERROR")
            return self.tarifa_base

    def describir_servicio(self):
        return f"[Asesoría] {self.nombre_servicio} - Área: {self.area_especialidad} - Tarifa hora: ${self.tarifa_base}"
    