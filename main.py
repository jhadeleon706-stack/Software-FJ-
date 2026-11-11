from clientes import GestorClientes, DatoInvalidoError, ClienteNoEncontradoError
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva

def ejecutar_simulacion():
    print("=" * 70)
    print(" INICIANDO SIMULACIÓN DE 10 OPERACIONES - SOFTWARE FJ (FASE 4) ")
    print("=" * 70)
    
    # Inicializamos el gestor de clientes de tu compañero
    gestor_clientes = GestorClientes()
    historial_reservas = []
    
    # --- OPERACIÓN 1: Registro correcto de un cliente ---
    print("\n[Operación 1] Intentando registrar un cliente VÁLIDO...")
    cliente1 = gestor_clientes.registrar("Laura Gómez", "1012345678", "laura@correo.com", "3001234567")

    # --- OPERACIÓN 2: Registro incorrecto de un cliente (Documento corto / inválido) ---
    print("\n[Operación 2] Intentando registrar un cliente con documento INVÁLIDO...")
    gestor_clientes.registrar("Carlos Pérez", "12345", "carlos@correo.com", "3109876543")

    # --- OPERACIÓN 3: Creación correcta de un servicio de Sala ---
    print("\n[Operación 3] Creando servicio de Reservas de Salas...")
    try:
        sala_reuniones = ReservaSala("S001", "Sala Ejecutiva A", 50000.0, 15)
        print(f"-> Éxito: {sala_reuniones.describir_servicio()}")
    except Exception as e:
        print(f"-> Error: {e}")

    # --- OPERACIÓN 4: Creación de servicio con tarifa inválida (Negativa) ---
    print("\n[Operación 4] Intentando crear servicio con tarifa INVÁLIDA (-100)...")
    try:
        sala_error = ReservaSala("S002", "Sala Rota", -100.0, 5)
    except Exception as e:
        print(f"-> Excepción controlada correctamente: {e}")

    # --- OPERACIÓN 5: Creación correcta de Alquiler de Equipo y Asesoría ---
    print("\n[Operación 5] Creando servicios de Equipos y Asesorías...")
    try:
        equipo_camara = AlquilerEquipo("E001", "Cámara Sony 4K", 80000.0, "Audiovisual")
        asesoria_ing = AsesoriaEspecializada("A001", "Asesoría Programación OOP", 60000.0, "Ingeniería")
        print(f"-> Éxito: {equipo_camara.describir_servicio()}")
        print(f"-> Éxito: {asesoria_ing.describir_servicio()}")
    except Exception as e:
        print(f"-> Error: {e}")

    # --- OPERACIÓN 6: Reserva EXITOSA de una Sala (Polimorfismo y descuento) ---
    print("\n[Operación 6] Procesando reserva EXITOSA de Sala (4 horas, 10% descuento)...")
    if cliente1:
        try:
            reserva1 = Reserva(cliente1, sala_reuniones, cantidad_unidad=4, tipo_parametro=10.0)
            historial_reservas.append(reserva1)
            print(f"-> Detalle: {reserva1.obtener_reserva_detalles()}")
        except Exception as e:
            print(f"-> Error: {e}")

    # --- OPERACIÓN 7: Reserva EXITOSA de Alquiler de Equipos (3 días con seguro) ---
    print("\n[Operación 7] Procesando reserva EXITOSA de Equipo (3 días, $20000 seguro)...")
    if cliente1:
        try:
            reserva2 = Reserva(cliente1, equipo_camara, cantidad_unidad=3, tipo_parametro=20000.0)
            historial_reservas.append(reserva2)
            print(f"-> Detalle: {reserva2.obtener_reserva_detalles()}")
        except Exception as e:
            print(f"-> Error: {e}")

    # --- OPERACIÓN 8: Reserva FALLIDA por cantidad de horas inválida ---
    print("\n[Operación 8] Intentando procesar reserva con horas INVÁLIDAS (-2 horas)...")
    if cliente1:
        try:
            reserva_fallida = Reserva(cliente1, sala_reuniones, cantidad_unidad=-2, tipo_parametro=0.0)
        except Exception as e:
            print(f"-> Excepción controlada correctamente (La app sigue viva): {e}")

    # --- OPERACIÓN 9: Registro de segundo cliente válido y creación de Asesoría ---
    print("\n[Operación 9] Registrando segundo cliente y creando Asesoría...")
    cliente2 = gestor_clientes.registrar("Ana Ruiz", "52111222", "ana@correo.com", "3201234567")
    if cliente2:
        try:
            reserva3 = Reserva(cliente2, asesoria_ing, cantidad_unidad=2, tipo_parametro=1.2)
            historial_reservas.append(reserva3)
            print(f"-> Detalle: {reserva3.obtener_reserva_detalles()}")
        except Exception as e:
            print(f"-> Error: {e}")

    # --- OPERACIÓN 10: Cancelación segura de una reserva y búsqueda en gestor ---
    print("\n[Operación 10] Probando cancelación de reserva y búsqueda de cliente...")
    if historial_reservas:
        reserva_a_cancelar = historial_reservas[0]
        reserva_a_cancelar.cancelar_reserva()
    
    try:
        cliente_encontrado = gestor_clientes.buscar("1012345678")
        print(f"-> Cliente encontrado en gestor: {cliente_encontrado.describir()}")
    except Exception as e:
        print(f"-> Error en búsqueda: {e}")

    print("\n" + "=" * 70)
    print(" ¡SIMULACIÓN FINALIZADA CON ÉXITO! REVISA EL ARCHIVO 'logs_software_fj.log' ")
    print("=" * 70)

if __name__ == "__main__":
    ejecutar_simulacion()
