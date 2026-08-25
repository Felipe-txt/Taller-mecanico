"""
Módulo Cliente
Representa al cliente del taller mecánico con control de deudas.
"""

from persona import Persona


class Cliente(Persona):
    """Clase que representa a un cliente que solicita servicios en el taller."""

    def __init__(self, rut: str, nombre: str, telefono: str, email: str):
        super().__init__(rut, nombre, telefono, email)
        self._tiene_deuda: bool = False
        self._monto_deuda: float = 0.0

    @property
    def tiene_deuda(self) -> bool:
        """Indica si el cliente posee deuda registrada."""
        return self._tiene_deuda

    @property
    def monto_deuda(self) -> float:
        """Obtiene el monto total adeudado por el cliente."""
        return self._monto_deuda

    def puede_ingresar_vehiculo(self) -> bool:
        """
        Regla de negocio: Un cliente solo puede ingresar vehículos
        si no tiene deudas pendientes.
        """
        return not self._tiene_deuda and self._monto_deuda <= 0.0

    def registrar_deuda(self, monto: float) -> None:
        """Registra un nuevo cargo por pagar al cliente."""
        if monto > 0:
            self._monto_deuda += float(monto)
            self._tiene_deuda = True

    def pagar_deuda(self, monto: float) -> None:
        """Abona o paga la totalidad de la deuda pendiente."""
        if monto <= 0:
            return
        
        self._monto_deuda = max(0.0, self._monto_deuda - float(monto))
        if self._monto_deuda == 0.0:
            self._tiene_deuda = False

    def __str__(self) -> str:
        estado_deuda = f"Con Deuda: ${self._monto_deuda:,.0f} CLP" if self._tiene_deuda else "Al día (Sin deuda)"
        return f"Cliente: {self._nombre} | RUT: {self._rut} | Estado: {estado_deuda}"
