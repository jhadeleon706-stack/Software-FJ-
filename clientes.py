"""Módulo de clientes - Software FJ (Programación 213023, Fase 4).

Incluye: excepciones personalizadas, clase Cliente con encapsulación y
validaciones, un gestor con lista interna y registro de errores en logs.
"""

import logging                      # Librería estándar para escribir el archivo de logs
import re                           # Expresiones regulares para validar texto
from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas

# ---------------------------------------------------------------- LOGS
logging.basicConfig(
    filename="logs_software_fj.log",  # Archivo donde se guardan errores y eventos
    level=logging.INFO,               # Registra desde eventos informativos hacia arriba
    format="%(asctime)s | %(levelname)s | %(message)s",  # Fecha | nivel | mensaje
    encoding="utf-8",                 # Permite tildes y ñ
)
logger = logging.getLogger("software_fj")  # Logger propio del sistema


# --------------------------------------------------- EXCEPCIONES PROPIAS
class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las del sistema heredan de aquí."""


class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un dato no cumple el formato o la regla esperada."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un dato obligatorio."""


class ClienteDuplicadoError(ErrorSoftwareFJ):
    """Se lanza al registrar un cliente cuyo documento ya existe."""


class ClienteNoEncontradoError(ErrorSoftwareFJ):
    """Se lanza al buscar un cliente que no está registrado."""


# ------------------------------------------- CLASE ABSTRACTA (PLACEHOLDER)
# Si el grupo ya definió la clase abstracta de "entidades generales",
# se borra esta y se importa la del grupo.
class EntidadBase(ABC):
    """Representa cualquier entidad general del sistema."""

    def __init__(self, identificador):
        self._identificador = identificador  # Identificador común a toda entidad

    @property
    def identificador(self):
        return self._identificador           # Solo lectura desde afuera

    @abstractmethod
    def describir(self):
        """Cada entidad debe explicar quién es (polimorfismo)."""


# ------------------------------------------------------------- CLIENTE
class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validados."""

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__(documento)   # El documento es el identificador
        self.nombre = nombre          # Pasa por el setter (valida)
        self.__documento = self._validar_documento(documento)  # Dato privado
        self.correo = correo          # Pasa por el setter (valida)
        self.telefono = telefono      # Pasa por el setter (valida)

    # ---- validaciones (métodos internos reutilizables)
    @staticmethod
    def _validar_obligatorio(valor, campo):
        if valor is None or str(valor).strip() == "":      # Vacío o None
            raise ParametroFaltanteError(f"Falta el dato obligatorio: {campo}")
        return str(valor).strip()                           # Devuelve limpio

    def _validar_documento(self, documento):
        documento = self._validar_obligatorio(documento, "documento")
        if not documento.isdigit() or not 6 <= len(documento) <= 10:
            raise DatoInvalidoError("El documento debe tener entre 6 y 10 dígitos")
        return documento

    # ---- propiedades (getters y setters con validación)
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._validar_obligatorio(valor, "nombre")
        if len(valor) < 3 or not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+", valor):
            raise DatoInvalidoError("El nombre debe tener letras y mínimo 3 caracteres")
        self.__nombre = valor

    @property
    def documento(self):
        return self.__documento       # Sin setter: no se puede cambiar

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        valor = self._validar_obligatorio(valor, "correo")
        if not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", valor):
            raise DatoInvalidoError(f"Correo con formato inválido: {valor}")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._validar_obligatorio(valor, "teléfono")
        if not (valor.isdigit() and len(valor) == 10 and valor.startswith("3")):
            raise DatoInvalidoError("El celular debe tener 10 dígitos y empezar por 3")
        self.__telefono = valor

    def describir(self):
        """Implementa el método abstracto de EntidadBase."""
        return f"Cliente {self.nombre} (doc. {self.documento}) - {self.correo}"

    def __str__(self):
        return self.describir()


# ------------------------------------------------------ GESTOR DE CLIENTES
class GestorClientes:
    """Administra la lista interna de clientes (sin base de datos)."""

    def __init__(self):
        self.__clientes = []          # Lista interna y privada

    def registrar(self, nombre, documento, correo, telefono):
        """Registra un cliente. Devuelve el Cliente o None si hubo error."""
        try:
            try:
                nuevo = Cliente(nombre, documento, correo, telefono)  # Valida todo
            except ValueError as error:                # Error inesperado de Python
                # Encadenamiento: se conserva el error original con "from"
                raise DatoInvalidoError("Datos con formato incorrecto") from error
            if any(c.documento == nuevo.documento for c in self.__clientes):
                raise ClienteDuplicadoError(f"Ya existe el documento {nuevo.documento}")
        except ErrorSoftwareFJ as error:               # Errores propios del sistema
            logger.error("Registro fallido: %s", error)  # Se anota en el log
            print(f"[ERROR] {error}")
            return None                                # El programa sigue activo
        else:                                          # Solo si NO hubo errores
            self.__clientes.append(nuevo)
            logger.info("Cliente registrado: %s", nuevo.documento)
            print(f"[OK] {nuevo}")
            return nuevo
        finally:                                       # Siempre se ejecuta
            logger.info("Intento de registro finalizado (doc. %s)", documento)

    def buscar(self, documento):
        """Busca por documento o lanza ClienteNoEncontradoError."""
        for cliente in self.__clientes:
            if cliente.documento == str(documento):
                return cliente
        raise ClienteNoEncontradoError(f"No existe el cliente con documento {documento}")

    def listar(self):
        return list(self.__clientes)  # Copia, para no exponer la lista interna


# ------------------------------------------------------------------ DEMO
if __name__ == "__main__":
    gestor = GestorClientes()
    # 1 válido, 2 válido, 3 documento duplicado, 4 correo inválido,
    # 5 nombre vacío, 6 celular inválido, 7 documento con letras
    gestor.registrar("Laura Gómez", "1012345678", "laura@correo.com", "3001234567")
    gestor.registrar("Carlos Pérez", "80123456", "carlos@correo.com", "3109876543")
    gestor.registrar("Laura Otra", "1012345678", "otra@correo.com", "3001112233")
    gestor.registrar("Ana Ruiz", "52111222", "ana-correo.com", "3201234567")
    gestor.registrar("", "52333444", "x@correo.com", "3201234567")
    gestor.registrar("Pedro Díaz", "52555666", "pedro@correo.com", "12345")
    gestor.registrar("Marta Solano", "ABC123", "marta@correo.com", "3151234567")
    # 8 búsqueda exitosa y 9 búsqueda de un cliente inexistente
    try:
        print("[BUSCAR]", gestor.buscar("80123456"))
        gestor.buscar("99999999")
    except ClienteNoEncontradoError as error:
        logger.error("Búsqueda fallida: %s", error)
        print(f"[ERROR] {error}")
    print(f"Total de clientes registrados: {len(gestor.listar())}")
