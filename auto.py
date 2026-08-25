"""
Módulo Auto
Representa a los automóviles particulares atendidos en el taller.
"""

from vehiculo import Vehiculo


class Auto(Vehiculo):
    """Subclase de Vehículo para automóviles particulares."""

    def __init__(self, patente: str, modelo: str, anio: int = 2020, tipo_carroceria: str = "Sedán"):
        super().__init__(patente, modelo, anio)
        self._tipo_carroceria: str = tipo_carroceria.strip()

    @property
    def tipo_carroceria(self) -> str:
        """Tipo de carrocería del auto (ej: Sedán, Hatchback, SUV, Coupé)."""
        return self._tipo_carroceria

    def tarifa_hora(self) -> float:
        """Tarifa horaria polimórfica para automóviles: $25.000 CLP/h."""
        return 25000.0

    def __str__(self) -> str:
        return (f"Auto ({self._tipo_carroceria}) [{self._patente}] {self._modelo} ({self._anio}) | "
                f"Tarifa: ${self.tarifa_hora():,.0f} CLP/h")
