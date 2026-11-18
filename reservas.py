"""Módulo de reservas y excepciones avanzadas - Software FJ."""

import itertools                                    # Para generar números de reserva
from clientes import (                       # Piezas del módulo de clientes
    Cliente, EntidadBase, ErrorSoftwareFJ, logger,
)
from servicios import Servicio                 # Clase abstracta de servicios


# ------------------------------------------------- EXCEPCIONES AVANZADAS
class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva no se pudo crear o procesar."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado no está disponible."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """La acción no es válida para el estado actual de la reserva."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """El cálculo del costo dio un resultado imposible."""


# ----------------------------------------------------------------- RESERVA
class Reserva(EntidadBase):
    """Une cliente, servicio, duración y estado."""

    PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"
    _contador = itertools.count(1)                  # 1, 2, 3... para cada reserva

    def __init__(self, cliente, servicio, horas, descuento=0.0):
        super().__init__(f"R{next(Reserva._contador):03d}")  # Ej.: R001
        if not isinstance(cliente, Cliente):        # Cliente debe ser un Cliente real
            raise ReservaInvalidaError("La reserva necesita un cliente válido")
        if not isinstance(servicio, Servicio):      # Servicio debe ser un Servicio real
            raise ReservaInvalidaError("La reserva necesita un servicio válido")
        if not isinstance(horas, (int, float)):     # Duración numérica
            raise ReservaInvalidaError("La duración debe ser un número de horas")
        servicio.validar_parametros(horas)          # Polimorfismo: cada servicio valida lo suyo
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.descuento = descuento
        self.estado = Reserva.PENDIENTE             # Toda reserva nace pendiente
        self.costo = None                           # Se calcula al confirmar

    def confirmar(self):
        """PENDIENTE -> CONFIRMADA (si hay disponibilidad y el cálculo es coherente)."""
        if self.estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"{self.identificador} está {self.estado}: solo se confirma una PENDIENTE")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f"'{self.servicio.nombre}' no está disponible")
        if not 0 <= self.descuento < 1:
            raise CalculoInconsistenteError(f"Descuento imposible: {self.descuento}")
        costo = self.servicio.calcular_costo(self.horas, self.descuento)
        if costo <= 0:
            raise CalculoInconsistenteError(f"Costo no válido: {costo}")
        self.costo = costo
        self.estado = Reserva.CONFIRMADA

    def cancelar(self):
        """Cancela una reserva que no esté ya cancelada."""
        if self.estado == Reserva.CANCELADA:
            raise OperacionNoPermitidaError(f"{self.identificador} ya estaba cancelada")
        self.estado = Reserva.CANCELADA

    def procesar(self):
        """Confirma con try/except/else/finally y encadenamiento de errores."""
        try:
            self.confirmar()
        except ErrorSoftwareFJ as error:
            logger.error("Reserva %s no procesada: %s", self.identificador, error)
            # "from error" conserva la causa original (encadenamiento)
            raise ReservaInvalidaError(f"No se pudo procesar {self.identificador}") from error
        else:
            logger.info("Reserva %s confirmada. Costo: %s", self.identificador, self.costo)
        finally:
            logger.info("Fin del procesamiento de %s", self.identificador)

    def describir(self):
        return (f"{self.identificador} | {self.cliente.nombre} | {self.servicio.nombre} | "
                f"{self.horas} h | {self.estado} | costo: {self.costo}")

    def __str__(self):
        return self.describir()


# ------------------------------------------------------------------ GESTOR
class GestorReservas:
    """Lista interna de reservas; ningún error detiene el programa."""

    def __init__(self):
        self.__reservas = []

    def crear(self, cliente, servicio, horas, descuento=0.0):
        """Crea y guarda una reserva. Devuelve la reserva o None si falló."""
        try:
            reserva = Reserva(cliente, servicio, horas, descuento)
        except ErrorSoftwareFJ as error:
            logger.error("Creación de reserva fallida: %s", error)
            print(f"[ERROR] {error}")
            return None
        self.__reservas.append(reserva)
        logger.info("Reserva creada: %s", reserva.identificador)
        print(f"[OK] Creada {reserva.identificador}")
        return reserva

    def procesar(self, reserva):
        """Procesa una reserva. Devuelve True si quedó confirmada."""
        try:
            reserva.procesar()
        except ErrorSoftwareFJ as error:
            causa = error.__cause__                 # Error original encadenado
            print(f"[ERROR] {error} -> causa: {causa}")
            return False
        print(f"[OK] {reserva}")
        return True

    def cancelar(self, reserva):
        try:
            reserva.cancelar()
        except ErrorSoftwareFJ as error:
            logger.error("Cancelación fallida: %s", error)
            print(f"[ERROR] {error}")
            return False
        logger.info("Reserva %s cancelada", reserva.identificador)
        print(f"[OK] Cancelada {reserva.identificador}")
        return True

    def listar(self):
        return list(self.__reservas)
