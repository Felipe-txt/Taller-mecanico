"""
Módulo Camion
Representa a los camiones y vehículos de carga pesada atendidos en el taller.
"""

from vehiculo import Vehiculo


class Camion(Vehiculo):
    """Subclase de Vehículo para camiones de carga."""

    def __init__(self, patente: str, modelo: str, anio: int = 2020, capacidad_ton: float = 5.0):
        super().__init__(patente, modelo, anio)
        self._capacidad_ton: float = float(capacidad_ton)

    @property
    def capacidad_ton(self) -> float:
        """Capacidad máxima de carga en toneladas."""
        return self._capacidad_ton

    def tarifa_hora(self) -> float:
        """Tarifa horaria polimórfica para camiones: $40.000 CLP/h."""
        return 40000.0

    def __str__(self) -> str:
        return (f"Camión ({self._capacidad_ton:.1f} Ton) [{self._patente}] {self._modelo} ({self._anio}) | "
                f"Tarifa: ${self.tarifa_hora():,.0f} CLP/h")
