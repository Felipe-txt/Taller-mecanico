"""
Módulo Vehiculo
Clase base abstracta para todos los vehículos atendidos en el taller.
Implementa validación de patente y cálculo polimórfico de tarifa por hora.
"""

from abc import ABC, abstractmethod
import re


class Vehiculo(ABC):
    """Clase base abstracta para vehículos motorizados."""

    def __init__(self, patente: str, modelo: str, anio: int = 2020):
        if not self.validar_patente(patente):
            raise ValueError(
                f"Patente '{patente}' inválida. Debe tener formato chileno válido (ej: ABCD12 o AB1234)."
            )
        
        self._patente: str = patente.replace("-", "").replace(" ", "").strip().upper()
        self._modelo: str = modelo.strip()
        self._anio: int = int(anio)
        self._en_taller: bool = False

    @staticmethod
    def validar_patente(patente: str) -> bool:
        """
        Valida el formato oficial de patentes en Chile:
        - Formato nuevo (desde 2007): 4 letras seguidas de 2 dígitos (ej: ABCD12)
        - Formato antiguo: 2 letras seguidas de 4 dígitos (ej: AB1234)
        """
        if not isinstance(patente, str):
            return False
        
        limpia = patente.replace("-", "").replace(" ", "").strip().upper()
        patron = r"^([A-Z]{4}\d{2}|[A-Z]{2}\d{4})$"
        return bool(re.match(patron, limpia))

    def ingresar(self) -> None:
        """Marca el vehículo como presente en el taller."""
        self._en_taller = True

    def entregar(self) -> None:
        """Marca el vehículo como entregado fuera del taller."""
        self._en_taller = False

    def esta_en_taller(self) -> bool:
        """Verifica si el vehículo está actualmente en las dependencias del taller."""
        return self._en_taller

    @property
    def patente(self) -> str:
        return self._patente

    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def anio(self) -> int:
        return self._anio

    @abstractmethod
    def tarifa_hora(self) -> float:
        """
        Método polimórfico abstracto.
        Cada tipo de vehículo define su costo de mano de obra por hora sin 'if/else'.
        """
        pass

    def __str__(self) -> str:
        estado = "En taller" if self._en_taller else "Fuera de taller"
        return f"{self.__class__.__name__} [{self._patente}] {self._modelo} ({self._anio}) - {estado}"
