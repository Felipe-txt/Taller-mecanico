"""
Módulo Repuesto
Representa a los repuestos del inventario nacional cotizados en CLP.
"""

from excepciones import SinStockError


class Repuesto:
    """Clase base para repuestos e insumos del taller."""

    def __init__(self, codigo: str, nombre: str, stock: int, precio_base_clp: float):
        self._codigo: str = codigo.strip().upper()
        self._nombre: str = nombre.strip()
        self._stock: int = max(0, int(stock))
        self._precio_base_clp: float = max(0.0, float(precio_base_clp))

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def stock(self) -> int:
        return self._stock

    def hay_stock(self, cantidad: int) -> bool:
        """Verifica si existe inventario suficiente para suplir la cantidad requerida."""
        return self._stock >= cantidad

    def descontar_stock(self, cantidad: int) -> None:
        """
        Disminuye las unidades disponibles en inventario.
        Lanza SinStockError si la cantidad solicitada excede el stock disponible.
        """
        if cantidad <= 0:
            return
        
        if not self.hay_stock(cantidad):
            raise SinStockError(self._codigo, cantidad, self._stock)
        
        self._stock -= cantidad

    def reponer_stock(self, cantidad: int) -> None:
        """Incrementa el stock disponible del repuesto."""
        if cantidad > 0:
            self._stock += int(cantidad)

    def get_precio_clp(self, **kwargs) -> float:
        """Retorna el precio unitario del repuesto en Pesos Chilenos (CLP)."""
        return self._precio_base_clp

    def __str__(self) -> str:
        return f"Repuesto [{self._codigo}] {self._nombre} | Stock: {self._stock} un. | Precio: ${self.get_precio_clp():,.0f} CLP"
