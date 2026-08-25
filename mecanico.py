"""
Módulo Mecanico
Representa a los técnicos del taller encargados del diagnóstico y reparación.
"""

from typing import TYPE_CHECKING
from usuario import Usuario

if TYPE_CHECKING:
    from orden_trabajo import OrdenTrabajo


class Mecanico(Usuario):
    """Especialista técnico que ejecuta labores de diagnóstico y mano de obra."""

    def __init__(self, rut: str, nombre: str, telefono: str, email: str, username: str, password: str, especialidad: str):
        super().__init__(rut, nombre, telefono, email, username, password, rol="MECANICO")
        self._especialidad: str = especialidad.strip()
        self._horas_acumuladas: float = 0.0

    @property
    def especialidad(self) -> str:
        """Especialidad del mecánico (ej: Frenos, Motor, Transmisión, Electricidad)."""
        return self._especialidad

    @property
    def horas_acumuladas(self) -> float:
        """Total de horas de mano de obra realizadas por el mecánico."""
        return self._horas_acumuladas

    def registrar_horas(self, orden: "OrdenTrabajo", horas: float) -> None:
        """Registra horas de trabajo en una orden específica y acumula en su historial."""
        if horas > 0:
            self._horas_acumuladas += float(horas)
            orden.registrar_horas(float(horas))

    def diagnosticar(self, orden: "OrdenTrabajo", desc: str) -> None:
        """Establece el diagnóstico técnico de una orden de trabajo y avanza su estado."""
        orden.diagnostico = desc.strip()
        orden.estado = "EN_REPARACION"

    def __str__(self) -> str:
        return (f"Mecánico: {self._nombre} (@{self._username}) | "
                f"Especialidad: {self._especialidad} | Horas acumuladas: {self._horas_acumuladas:.1f}h")
