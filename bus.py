"""
Módulo Bus
Representa a los autobuses y microbuses de pasajeros atendidos en el taller.
"""

from vehiculo import Vehiculo


class Bus(Vehiculo):
    """Subclase de Vehículo para buses de transporte de pasajeros."""

    def __init__(self, patente: str, modelo: str, anio: int = 2020, cantidad_asientos: int = 40):
        super().__init__(patente, modelo, anio)
        self._cantidad_asientos: int = int(cantidad_asientos)

    @property
    def cantidad_asientos(self) -> int:
        """Cantidad total de asientos disponibles en el bus."""
        return self._cantidad_asientos

    def tarifa_hora(self) -> float:
        """Tarifa horaria polimórfica para buses: $35.000 CLP/h."""
        return 35000.0

    def __str__(self) -> str:
        return (f"Bus ({self._cantidad_asientos} asientos) [{self._patente}] {self._modelo} ({self._anio}) | "
                f"Tarifa: ${self.tarifa_hora():,.0f} CLP/h")
