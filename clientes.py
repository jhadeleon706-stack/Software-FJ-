from abc import ABC, abstractmethod
from excepciones_y_logs import ErrorClienteInvalido, LoggerSistema

class EntidadBase(ABC):
    """Clase abstracta general que representa entidades del sistema (requisito de la guía)."""
    
    @abstractmethod
    def obtener_detalles(self):
        pass

class Cliente(EntidadBase):
    """Clase Cliente con validaciones estrictas y encapsulación de datos personales."""
    
    def __init__(self, cedula, nombre, correo, telefono):
        self.__cedula = self.__validar_cedula(cedula)
        self.__nombre = self.__validar_nombre(nombre)
        self.__correo = self.__validar_correo(correo)
        self.__telefono = self.__validar_telefono(telefono)
        LoggerSistema.registrar(f"Cliente creado exitosamente: {self.__nombre} (CC: {self.__cedula})", "INFO")

    # --- Métodos de Validación y Encapsulación (Getters) ---
    @property
    def cedula(self):
        return self.__cedula

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def __validar_cedula(self, cedula):
        cedula_str = str(cedula).strip()
        if not cedula_str.isdigit() or len(cedula_str) < 6:
            error_msg = f"Cédula inválida ('{cedula}'). Debe contener solo números y al menos 6 dígitos."
            LoggerSistema.registrar(error_msg, "ERROR")
            raise ErrorClienteInvalido(error_msg)
        return cedula_str

    def __validar_nombre(self, nombre):
        nombre_str = str(nombre).strip()
        if len(nombre_str) < 3:
            error_msg = f"Nombre inválido ('{nombre}'). Demasiado corto."
            LoggerSistema.registrar(error_msg, "ERROR")
            raise ErrorClienteInvalido(error_msg)
        return nombre_str

    def __validar_correo(self, correo):
        correo_str = str(correo).strip()
        if "@" not in correo_str or "." not in correo_str:
            error_msg = f"Correo electrónico inválido ('{correo}')."
            LoggerSistema.registrar(error_msg, "ERROR")
            raise ErrorClienteInvalido(error_msg)
        return correo_str

    def __validar_telefono(self, telefono):
        tel_str = str(telefono).strip()
        if not tel_str.isdigit() or len(tel_str) < 7:
            error_msg = f"Teléfono inválido ('{telefono}')."
            LoggerSistema.registrar(error_msg, "ERROR")
            raise ErrorClienteInvalido(error_msg)
        return tel_str

    def obtener_detalles(self):
        return f"Cliente: {self.__nombre} | CC: {self.__cedula} | Correo: {self.__correo}"
    