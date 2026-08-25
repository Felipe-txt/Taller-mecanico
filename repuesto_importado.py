"""
Módulo RepuestoImportado
Representa a los repuestos cotizados en Dólares Estadounidenses (USD) con arancel aduanero.
"""

from typing import Optional
from repuesto import Repuesto


class RepuestoImportado(Repuesto):
    """Repuesto importado cuyo costo base está en USD y requiere conversión a CLP más aranceles."""

    def __init__(self, codigo: str, nombre: str, stock: int, precio_usd: float, arancel_porcentaje: float = 0.06):
        super().__init__(codigo=codigo, nombre=nombre, stock=stock, precio_base_clp=0.0)
        self._precio_usd: float = max(0.0, float(precio_usd))
        self._arancel_porcentaje: float = float(arancel_porcentaje)

    @property
    def precio_usd(self) -> float:
        """Precio unitario del repuesto en dólares estadounidenses."""
        return self._precio_usd

    @property
    def arancel_porcentaje(self) -> float:
        """Porcentaje de recargo por arancel de importación (por defecto 6% = 0.06)."""
        return self._arancel_porcentaje

    def calcular_impuesto_clp(self, valor_dolar: float) -> float:
        """Calcula el costo en CLP generado por el arancel de aduana según el tipo de cambio."""
        if valor_dolar <= 0:
            raise ValueError("El valor del dólar debe ser mayor a 0.")
        return self._precio_usd * valor_dolar * self._arancel_porcentaje

    def get_precio_clp(self, valor_dolar: Optional[float] = None) -> float:
        """
        Calcula el precio final en CLP convirtiendo el precio USD al tipo de cambio
        y adicionando el arancel de importación.
        """
        if valor_dolar is None or valor_dolar <= 0:
            valor_dolar = 950.0  # Tipo de cambio por defecto en caso de no suministrarse
        
        precio_cif = self._precio_usd * float(valor_dolar)
        arancel = self.calcular_impuesto_clp(float(valor_dolar))
        return precio_cif + arancel

    def __str__(self) -> str:
        return (f"Repuesto Importado [{self._codigo}] {self._nombre} | Stock: {self._stock} un. | "
                f"USD: ${self._precio_usd:.2f} (Arancel: {self._arancel_porcentaje * 100:.1f}%)")
