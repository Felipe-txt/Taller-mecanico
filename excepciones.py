"""
Módulo de Excepciones de Negocio para el Taller Mecánico
Define la jerarquía de errores específicos del dominio.
"""

class TallerError(Exception):
    """Excepción base para todos los errores del taller mecánico."""
    def __init__(self, mensaje: str = "Error en el sistema del taller mecánico"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self) -> str:
        return f"[TallerError] {self.mensaje}"


class VehiculoNoIngresadoError(TallerError):
    """Lanzada cuando se intenta operar sobre un vehículo que no está físicamente en el taller."""
    def __init__(self, patente: str):
        self.patente = patente
        super().__init__(
            f"El vehículo con patente '{patente}' no se encuentra ingresado en el taller o ya fue entregado."
        )


class SinStockError(TallerError):
    """Lanzada cuando no hay unidades suficientes de un repuesto en el inventario."""
    def __init__(self, codigo: str, solicitado: int, disponible: int):
        self.codigo_repuesto = codigo
        self.solicitado = solicitado
        self.disponible = disponible
        super().__init__(
            f"Stock insuficiente para el repuesto '{codigo}'. Solicitado: {solicitado}, Disponible: {disponible}."
        )


class ClienteConDeudaError(TallerError):
    """Lanzada cuando un cliente con deuda pendiente intenta ingresar un vehículo al taller."""
    def __init__(self, rut: str, monto: float):
        self.rut_cliente = rut
        self.monto = monto
        super().__init__(
            f"El cliente con RUT '{rut}' registra una deuda pendiente de ${monto:,.0f} CLP. "
            f"No puede ingresar nuevos vehículos hasta regularizar su situación."
        )
