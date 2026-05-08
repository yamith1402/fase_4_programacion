from abc import ABC, abstractmethod
from datetime import datetime


 #
# FUNCIÓN PARA REGISTRAR LOGS

def registrar_log(mensaje):
    """
    Registra un mensaje en el archivo de logs con la fecha y hora actual.
    Parámetros:
        mensaje (str): Texto del evento o error a registrar.
    """
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now()} - {mensaje}\n")



# EXCEPCIONES PERSONALIZADAS


class ErrorCliente(Exception):
    """Excepción personalizada para errores relacionados con clientes."""
    pass


class ErrorServicio(Exception):
    """Excepción personalizada para errores relacionados con servicios."""
    pass


class ErrorReserva(Exception):
    """Excepción personalizada para errores relacionados con reservas."""
    pass



# CLASE ABSTRACTA PERSONA


class Persona(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    Toda clase que herede de Persona debe implementar mostrar_datos().
    """

    @abstractmethod
    def mostrar_datos(self):
        """Muestra los datos de la persona. Método abstracto."""
        pass


# CLASE CLIENTE


class Cliente(Persona):
    """
    Representa un cliente del sistema Software FJ.
    Aplica encapsulación y validaciones estrictas sobre los datos personales.
    Hereda de Persona e implementa mostrar_datos().
    """

    def __init__(self, nombre, documento, correo, telefono):
        """
        Constructor del cliente con validaciones robustas.
        Parámetros:
            nombre (str): Nombre completo del cliente.
            documento (str): Número de documento de identidad.
            correo (str): Correo electrónico válido.
            telefono (str): Número de teléfono (solo dígitos).
        Lanza:
            ErrorCliente: Si alguna validación falla.
        """
        # Validación: nombre no puede estar vacío
        if not nombre or nombre.strip() == "":
            raise ErrorCliente("El nombre no puede estar vacío")

        # Validación: el correo debe contener '@'
        if "@" not in correo or "." not in correo.split("@")[-1]:
            raise ErrorCliente(f"Correo inválido: '{correo}'")

        # Validación: el teléfono debe ser numérico
        if not telefono.isdigit():
            raise ErrorCliente(f"El teléfono debe contener solo dígitos: '{telefono}'")

        # Validación: el documento no puede estar vacío
        if not documento or documento.strip() == "":
            raise ErrorCliente("El documento no puede estar vacío")

        # Atributos privados (encapsulación)
        self.__nombre = nombre.strip()
        self.__documento = documento.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    # Métodos getter para acceso controlado a atributos privados
    def obtener_nombre(self):
        """Retorna el nombre del cliente."""
        return self.__nombre

    def obtener_documento(self):
        """Retorna el documento del cliente."""
        return self.__documento

    def obtener_correo(self):
        """Retorna el correo del cliente."""
        return self.__correo

    def obtener_telefono(self):
        """Retorna el teléfono del cliente."""
        return self.__telefono

    def mostrar_datos(self):
        """Muestra todos los datos del cliente de forma estructurada."""
        print(f"  Nombre   : {self.__nombre}")
        print(f"  Documento: {self.__documento}")
        print(f"  Correo   : {self.__correo}")
        print(f"  Teléfono : {self.__telefono}")



# CLASE ABSTRACTA SERVICIO


class Servicio(ABC):
    """
    Clase abstracta que representa un servicio ofrecido por Software FJ.
    Define la estructura base que deben implementar todos los servicios.
    """

    def __init__(self, nombre, precio_base):
        """
        Constructor del servicio con validación del precio.
        Parámetros:
            nombre (str): Nombre del servicio.
            precio_base (float): Precio base del servicio (debe ser positivo).
        Lanza:
            ErrorServicio: Si el precio base no es mayor que cero.
        """
        if precio_base <= 0:
            raise ErrorServicio("El precio base debe ser mayor que cero")

        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, descuento=0, impuesto=0.19):
        """
        Calcula el costo total del servicio aplicando descuento e impuesto.
        Método abstracto con parámetros opcionales (sobrecarga simulada).
        Parámetros:
            descuento (float): Porcentaje de descuento entre 0 y 1 (ej: 0.10 = 10%).
            impuesto (float): Porcentaje de impuesto entre 0 y 1 (por defecto 19% IVA).
        """
        pass

    @abstractmethod
    def descripcion(self):
        """Retorna una descripción textual del servicio. Método abstracto."""
        pass

    def validar_parametros(self, valor, nombre_parametro):
        """
        Valida que un parámetro numérico sea mayor que cero.
        Parámetros:
            valor (int/float): El valor a validar.
            nombre_parametro (str): Nombre del parámetro (para el mensaje de error).
        Lanza:
            ErrorServicio: Si el valor no es mayor que cero.
        """
        if valor <= 0:
            raise ErrorServicio(
                f"El parámetro '{nombre_parametro}' debe ser mayor que cero"
            )



# SERVICIO: RESERVA DE SALA


class ReservaSala(Servicio):
    """
    Servicio de reserva de sala de reuniones o trabajo.
    Hereda de Servicio e implementa polimorfismo en calcular_costo y descripcion.
    """

    def __init__(self, horas):
        """
        Constructor del servicio ReservaSala.
        Parámetros:
            horas (int/float): Número de horas a reservar (debe ser positivo).
        Lanza:
            ErrorServicio: Si las horas no son válidas.
        """
        # Validar antes de llamar al padre
        if horas <= 0:
            raise ErrorServicio("Las horas de reserva deben ser mayores que cero")

        super().__init__("Reserva de Sala", 50000)
        self.horas = horas

    def calcular_costo(self, descuento=0, impuesto=0.19):
        """
        Calcula el costo de la reserva de sala.
        Aplica: (precio_base * horas) * (1 + impuesto) * (1 - descuento)
        Parámetros opcionales permiten sobrecarga simulada en Python.
        """
        self.validar_parametros(self.horas, "horas")

        if not (0 <= descuento < 1):
            raise ErrorServicio("El descuento debe estar entre 0 y 0.99")
        if not (0 <= impuesto <= 1):
            raise ErrorServicio("El impuesto debe estar entre 0 y 1")

        base = self.precio_base * self.horas
        total = base * (1 + impuesto) * (1 - descuento)
        return round(total, 2)

    def descripcion(self):
        """Descripción detallada del servicio de reserva de sala."""
        return (
            f"Servicio de reserva de sala por {self.horas} hora(s). "
            f"Precio base: ${self.precio_base:,}/hora."
        )



# SERVICIO: ALQUILER DE EQUIPO


class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    Hereda de Servicio e implementa polimorfismo en calcular_costo y descripcion.
    """

    def __init__(self, dias):
        """
        Constructor del servicio AlquilerEquipo.
        Parámetros:
            dias (int): Número de días de alquiler (debe ser positivo).
        Lanza:
            ErrorServicio: Si los días no son válidos.
        """
        if dias <= 0:
            raise ErrorServicio("Los días de alquiler deben ser mayores que cero")

        super().__init__("Alquiler de Equipo", 80000)
        self.dias = dias

    def calcular_costo(self, descuento=0, impuesto=0.19):
        """
        Calcula el costo del alquiler de equipo.
        Aplica: (precio_base * dias) * (1 + impuesto) * (1 - descuento)
        """
        self.validar_parametros(self.dias, "dias")

        if not (0 <= descuento < 1):
            raise ErrorServicio("El descuento debe estar entre 0 y 0.99")
        if not (0 <= impuesto <= 1):
            raise ErrorServicio("El impuesto debe estar entre 0 y 1")

        base = self.precio_base * self.dias
        total = base * (1 + impuesto) * (1 - descuento)
        return round(total, 2)

    def descripcion(self):
        """Descripción detallada del servicio de alquiler de equipo."""
        return (
            f"Servicio de alquiler de equipos por {self.dias} día(s). "
            f"Precio base: ${self.precio_base:,}/día."
        )



# SERVICIO: ASESORÍA ESPECIALIZADA


class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoría técnica o profesional especializada.
    Hereda de Servicio e implementa polimorfismo en calcular_costo y descripcion.
    """

    def __init__(self, horas):
        """
        Constructor del servicio AsesoriaEspecializada.
        Parámetros:
            horas (int/float): Número de horas de asesoría (debe ser positivo).
        Lanza:
            ErrorServicio: Si las horas no son válidas.
        """
        if horas <= 0:
            raise ErrorServicio("Las horas de asesoría deben ser mayores que cero")

        super().__init__("Asesoría Especializada", 120000)
        self.horas = horas

    def calcular_costo(self, descuento=0, impuesto=0.19):
        """
        Calcula el costo de la asesoría especializada.
        Aplica: (precio_base * horas) * (1 + impuesto) * (1 - descuento)
        """
        self.validar_parametros(self.horas, "horas")

        if not (0 <= descuento < 1):
            raise ErrorServicio("El descuento debe estar entre 0 y 0.99")
        if not (0 <= impuesto <= 1):
            raise ErrorServicio("El impuesto debe estar entre 0 y 1")

        base = self.precio_base * self.horas
        total = base * (1 + impuesto) * (1 - descuento)
        return round(total, 2)

    def descripcion(self):
        """Descripción detallada del servicio de asesoría especializada."""
        return (
            f"Servicio de asesoría especializada por {self.horas} hora(s). "
            f"Precio base: ${self.precio_base:,}/hora."
        )



# CLASE RESERVA


class Reserva:
    """
    Representa una reserva que integra un cliente, un servicio y una duración.
    Gestiona los estados: Pendiente, Confirmada, Cancelada.
    Implementa manejo avanzado de excepciones en su procesamiento.
    """

    def __init__(self, cliente, servicio, duracion):
        """
        Constructor de la reserva con validación de duración.
        Parámetros:
            cliente (Cliente): El cliente que realiza la reserva.
            servicio (Servicio): El servicio a reservar.
            duracion (int/float): Duración adicional en unidades del servicio.
        Lanza:
            ErrorReserva: Si la duración no es válida.
        """
        if duracion <= 0:
            raise ErrorReserva("La duración de la reserva debe ser mayor que cero")

        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Se requiere un objeto Cliente válido")

        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Se requiere un objeto Servicio válido")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        """Cambia el estado de la reserva a Confirmada."""
        if self.estado == "Cancelada":
            raise ErrorReserva("No se puede confirmar una reserva ya cancelada")
        self.estado = "Confirmada"
        print(f"  ✔ Reserva confirmada para: {self.cliente.obtener_nombre()}")

    def cancelar(self):
        """Cambia el estado de la reserva a Cancelada."""
        if self.estado == "Cancelada":
            raise ErrorReserva("La reserva ya está cancelada")
        self.estado = "Cancelada"
        print(f"  ✘ Reserva cancelada para: {self.cliente.obtener_nombre()}")

    def procesar(self, descuento=0, impuesto=0.19):
        """
        Procesa la reserva calculando el costo total.
        Demuestra uso de try/except/else/finally y encadenamiento de excepciones.
        Parámetros opcionales:
            descuento (float): Descuento a aplicar (sobrecarga simulada).
            impuesto (float): Impuesto a aplicar (por defecto 19%).
        """
        try:
            # Intento de cálculo del costo con parámetros opcionales
            costo = self.servicio.calcular_costo(descuento=descuento, impuesto=impuesto)

        except ErrorServicio as error:
            # Encadenamiento de excepciones: ErrorServicio → ErrorReserva
            raise ErrorReserva("Error al procesar la reserva por fallo en el servicio") from error

        except Exception as error:
            # Captura de cualquier error inesperado
            raise ErrorReserva("Error inesperado al procesar la reserva") from error

        else:
            # Se ejecuta SOLO si no hubo excepciones
            print(f"  ✔ Reserva procesada correctamente")
            print(f"    Cliente  : {self.cliente.obtener_nombre()}")
            print(f"    Servicio : {self.servicio.nombre}")
            print(f"    Duración : {self.duracion} unidad(es)")
            print(f"    Descuento: {int(descuento * 100)}%")
            print(f"    Impuesto : {int(impuesto * 100)}%")
            print(f"    Costo    : ${costo:,.2f}")

        finally:
            # Se ejecuta SIEMPRE, haya o no excepción
            registrar_log(
                f"Proceso de reserva ejecutado - Cliente: {self.cliente.obtener_nombre()} "
                f"| Servicio: {self.servicio.nombre} | Estado: {self.estado}"
            )



# PRUEBAS DEL SISTEMA — 10+ OPERACIONES


print("=" * 55)
print("         SISTEMA SOFTWARE FJ")
print("   Gestión de Clientes, Servicios y Reservas")
print("=" * 55)



# BLOQUE 1: REGISTRO DE CLIENTES
# Operaciones 1-6: válidas e inválidas


print("\n--- BLOQUE 1: REGISTRO DE CLIENTES ---\n")

# Datos de prueba: mezcla de registros válidos e inválidos
datos_clientes = [
    # (nombre, documento, correo, telefono) — casos válidos
    ("Juan Pérez",    "123456", "juan@gmail.com",   "3001234567"),  # ✔ válido
    ("Ana Gómez",     "654321", "ana@outlook.com",  "3012345678"),  # ✔ válido
    ("Carlos Ruiz",   "789012", "carlos@unad.edu",  "3109876543"),  # ✔ válido
    # Casos inválidos
    ("",              "456789", "maria@gmail.com",  "3001111111"),  # ✘ nombre vacío
    ("Pedro Mora",    "111222", "pedrogmail.com",   "3002222222"),  # ✘ correo sin @
    ("Laura Silva",   "333444", "laura@yahoo.com",  "telefono"),    # ✘ teléfono no numérico
]

clientes = []  # Lista interna de clientes registrados exitosamente

for datos in datos_clientes:
    try:
        cliente = Cliente(*datos)
        clientes.append(cliente)
        print(f"[OK] Cliente registrado:")
        cliente.mostrar_datos()
        registrar_log(f"Cliente registrado exitosamente: {cliente.obtener_nombre()}")

    except ErrorCliente as error:
        # Captura errores de validación del cliente
        print(f"[ERROR] No se pudo registrar cliente: {error}")
        registrar_log(f"Error al registrar cliente: {error}")

    print()



# BLOQUE 2: CREACIÓN DE SERVICIOS
# Operaciones 7-10: válidos e inválidos


print("\n--- BLOQUE 2: CREACIÓN DE SERVICIOS ---\n")

servicios = []  # Lista interna de servicios disponibles

# Servicio 1: Reserva de Sala — válido (3 horas)
try:
    sala = ReservaSala(3)
    servicios.append(sala)
    print(f"[OK] Servicio creado: {sala.descripcion()}")
    registrar_log(f"Servicio creado: {sala.nombre}")

except ErrorServicio as error:
    print(f"[ERROR] No se pudo crear servicio: {error}")
    registrar_log(f"Error al crear servicio: {error}")

# Servicio 2: Alquiler de Equipo — válido (2 días)
try:
    equipo = AlquilerEquipo(2)
    servicios.append(equipo)
    print(f"[OK] Servicio creado: {equipo.descripcion()}")
    registrar_log(f"Servicio creado: {equipo.nombre}")

except ErrorServicio as error:
    print(f"[ERROR] No se pudo crear servicio: {error}")
    registrar_log(f"Error al crear servicio: {error}")

# Servicio 3: Asesoría Especializada — válido (4 horas)
try:
    asesoria = AsesoriaEspecializada(4)
    servicios.append(asesoria)
    print(f"[OK] Servicio creado: {asesoria.descripcion()}")
    registrar_log(f"Servicio creado: {asesoria.nombre}")

except ErrorServicio as error:
    print(f"[ERROR] No se pudo crear servicio: {error}")
    registrar_log(f"Error al crear servicio: {error}")

# Servicio inválido: horas negativas — debe lanzar ErrorServicio
try:
    sala_mala = ReservaSala(-5)

except ErrorServicio as error:
    print(f"[ERROR] Servicio inválido detectado: {error}")
    registrar_log(f"Intento de crear servicio con parámetros inválidos: {error}")

# Servicio inválido: días en cero — debe lanzar ErrorServicio
try:
    equipo_malo = AlquilerEquipo(0)

except ErrorServicio as error:
    print(f"[ERROR] Servicio inválido detectado: {error}")
    registrar_log(f"Intento de crear servicio con parámetros inválidos: {error}")



# BLOQUE 3: PROCESAMIENTO DE RESERVAS
# Demuestra: confirmar, cancelar, procesar
# con descuentos e impuestos (sobrecarga)


print("\n\n--- BLOQUE 3: RESERVAS CON DESCUENTOS E IMPUESTOS ---\n")

# Reserva 1: Sin descuento ni modificación de impuesto (valores por defecto)
try:
    reserva1 = Reserva(clientes[0], servicios[0], 2)
    reserva1.confirmar()
    reserva1.procesar()  # Usa descuento=0, impuesto=0.19 por defecto

except ErrorReserva as error:
    print(f"[ERROR] Reserva fallida: {error}")
    registrar_log(f"Error en reserva: {error}")

print()

# Reserva 2: Con descuento del 10%
try:
    reserva2 = Reserva(clientes[1], servicios[1], 3)
    reserva2.confirmar()
    reserva2.procesar(descuento=0.10)  # Sobrecarga: con descuento del 10%

except ErrorReserva as error:
    print(f"[ERROR] Reserva fallida: {error}")
    registrar_log(f"Error en reserva: {error}")

print()

# Reserva 3: Con descuento del 20% y sin impuesto (IVA exento)
try:
    reserva3 = Reserva(clientes[2], servicios[2], 1)
    reserva3.confirmar()
    reserva3.procesar(descuento=0.20, impuesto=0.0)  # Sobrecarga completa

except ErrorReserva as error:
    print(f"[ERROR] Reserva fallida: {error}")
    registrar_log(f"Error en reserva: {error}")

print()

# Reserva 4: Reserva que luego se cancela
try:
    reserva4 = Reserva(clientes[0], servicios[2], 2)
    reserva4.confirmar()
    reserva4.cancelar()
    # Intento de confirmar una reserva ya cancelada — debe lanzar ErrorReserva
    reserva4.confirmar()

except ErrorReserva as error:
    print(f"[ERROR] Operación inválida sobre reserva: {error}")
    registrar_log(f"Error en operación de reserva: {error}")

print()

# Reserva 5: Duración inválida (cero) — debe lanzar ErrorReserva
try:
    reserva_mala = Reserva(clientes[0], servicios[0], 0)

except ErrorReserva as error:
    print(f"[ERROR] Reserva inválida detectada: {error}")
    registrar_log(f"Intento de reserva con duración inválida: {error}")

print()

# Reserva 6: Con descuento inválido — debe lanzar ErrorServicio encadenado
try:
    reserva6 = Reserva(clientes[1], servicios[0], 1)
    reserva6.confirmar()
    reserva6.procesar(descuento=1.5)  # Descuento inválido > 1

except ErrorReserva as error:
    # Encadenamiento: ErrorServicio → ErrorReserva
    print(f"[ERROR] Reserva fallida por parámetro inválido: {error}")
    if error.__cause__:
        print(f"  Causa raíz: {error.__cause__}")
    registrar_log(f"Error encadenado en reserva: {error} | Causa: {error.__cause__}")



# Resultado FINAL


print("\n" + "=" * 55)
print("             RESUMEN DEL SISTEMA")
print("=" * 55)
print(f"  Clientes registrados exitosamente : {len(clientes)}")
print(f"  Servicios disponibles             : {len(servicios)}")
print(f"  Log de errores y eventos          : logs.txt")
print("=" * 55)
print("\nSistema Software FJ ejecutado correctamente.\n")
registrar_log("Sistema ejecutado y finalizado correctamente")