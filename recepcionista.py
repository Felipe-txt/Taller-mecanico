"""
Módulo Recepcionista
Representa al personal de recepción encargado de la entrada y salida de vehículos.
"""

from typing import TYPE_CHECKING
from usuario import Usuario
from excepciones import ClienteConDeudaError

if TYPE_CHECKING:
    from cliente import Cliente
    from vehiculo import Vehiculo
    from orden_trabajo import OrdenTrabajo


class Recepcionista(Usuario):
    """Usuario encargado de la atención al cliente, recepción y entrega de vehículos."""

    def __init__(self, rut: str, nombre: str, telefono: str, email: str, username: str, password: str, turno: str):
        super().__init__(rut, nombre, telefono, email, username, password, rol="RECEPCIONISTA")
        self._turno: str = turno

    @property
    def turno(self) -> str:
        return self._turno

    @turno.setter
    def turno(self, nuevo_turno: str) -> None:
        self._turno = nuevo_turno

    def recibir_vehiculo(self, cliente: "Cliente", vehiculo: "Vehiculo", numero_orden: int) -> "OrdenTrabajo":
        """
        Crea una orden de trabajo e ingresa el vehículo al taller
        verificando previamente que el cliente no tenga deudas pendientes.
        """
        from orden_trabajo import OrdenTrabajo

        if not cliente.puede_ingresar_vehiculo():
            raise ClienteConDeudaError(cliente.get_rut(), cliente.monto_deuda)
        
        orden = OrdenTrabajo(num=numero_orden, cliente=cliente, vehiculo=vehiculo)
        vehiculo.ingresar()
        return orden

    def entregar_vehiculo(self, orden: "OrdenTrabajo") -> None:
        """Cierra el ciclo de servicio y entrega el vehículo al cliente."""
        orden.entregar_vehiculo()

    def __str__(self) -> str:
        return f"Recepcionista: {self._nombre} (@{self._username}) - Turno: {self._turno}"
