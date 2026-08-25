"""
Módulo Moto
Representa a las motocicletas atendidas en el taller.
"""

from vehiculo import Vehiculo


class Moto(Vehiculo):
    """Subclase de Vehículo para motocicletas."""

    def __init__(self, patente: str, modelo: str, anio: int = 2020, cilindrada_cc: int = 150):
        super().__init__(patente, modelo, anio)
        self._cilindrada_cc: int = int(cilindrada_cc)

    @property
    def cilindrada_cc(self) -> int:
        """Cilindrada del motor en centímetros cúbicos (cc)."""
        return self._cilindrada_cc

    def tarifa_hora(self) -> float:
        """Tarifa horaria polimórfica para motos: $15.000 CLP/h."""
        return 15000.0

    def __str__(self) -> str:
        return (f"Moto ({self._cilindrada_cc}cc) [{self._patente}] {self._modelo} ({self._anio}) | "
                f"Tarifa: ${self.tarifa_hora():,.0f} CLP/h")
