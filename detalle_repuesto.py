"""
Módulo DetalleRepuesto
Representa una línea de detalle de repuesto utilizado dentro de una orden de trabajo.
"""

from repuesto import Repuesto
from repuesto_importado import RepuestoImportado


class DetalleRepuesto:
    """Línea de repuesto con cantidad y precio unitario congelado al momento de su adición."""

    def __init__(self, repuesto: Repuesto, cant: int, valor_dolar: float = 950.0):
        if cant <= 0:
            raise ValueError("La cantidad de repuestos debe ser un entero mayor a cero.")
        
        self._repuesto: Repuesto = repuesto
        self._cantidad: int = int(cant)
        
        # Congela el precio unitario en CLP (considerando dólar si es importado)
        if isinstance(repuesto, RepuestoImportado):
            self._precio_unitario_aplicado: float = repuesto.get_precio_clp(valor_dolar)
        else:
            self._precio_unitario_aplicado: float = repuesto.get_precio_clp()

    def calcular_subtotal(self) -> float:
        """Calcula el subtotal en CLP (cantidad * precio unitario)."""
        return self._cantidad * self._precio_unitario_aplicado

    def get_cantidad(self) -> int:
        """Retorna la cantidad de unidades."""
        return self._cantidad

    def get_repuesto(self) -> Repuesto:
        """Retorna la referencia al objeto Repuesto."""
        return self._repuesto

    def get_precio_unitario(self) -> float:
        """Retorna el precio unitario aplicado."""
        return self._precio_unitario_aplicado

    def __str__(self) -> str:
        return (f"Detalle: {self._repuesto.nombre} | Cant: {self._cantidad} un. | "
                f"P.Unit: ${self._precio_unitario_aplicado:,.0f} CLP | Subtotal: ${self.calcular_subtotal():,.0f} CLP")
