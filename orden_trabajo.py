"""
Módulo OrdenTrabajo
Representa la orden de servicio principal que articula cliente, vehículo, mecánico y repuestos.
Calcula la mano de obra polimórfica y los totales de facturación con IVA.
"""

from datetime import datetime
from typing import List, Optional
from cliente import Cliente
from vehiculo import Vehiculo
from mecanico import Mecanico
from repuesto import Repuesto
from detalle_repuesto import DetalleRepuesto
from excepciones import VehiculoNoIngresadoError


class OrdenTrabajo:
    """Entidad transaccional central para la atención técnica de vehículos."""

    def __init__(self, num: int, cliente: Cliente, vehiculo: Vehiculo):
        self._numero_orden: int = int(num)
        self._fecha_ingreso: datetime = datetime.now()
        self._fecha_entrega: Optional[datetime] = None
        self._estado: str = "INGRESADO"
        self._horas_trabajo: float = 0.0
        self._diagnostico: str = ""
        self._cliente: Cliente = cliente
        self._vehiculo: Vehiculo = vehiculo
        self._mecanico_asignado: Optional[Mecanico] = None
        self._detalles_repuestos: List[DetalleRepuesto] = []

    @property
    def numero_orden(self) -> int:
        return self._numero_orden

    @property
    def fecha_ingreso(self) -> datetime:
        return self._fecha_ingreso

    @property
    def fecha_entrega(self) -> Optional[datetime]:
        return self._fecha_entrega

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: str) -> None:
        self._estado = nuevo_estado.strip().upper()

    @property
    def horas_trabajo(self) -> float:
        return self._horas_trabajo

    @property
    def diagnostico(self) -> str:
        return self._diagnostico

    @diagnostico.setter
    def diagnostico(self, diag: str) -> None:
        self._diagnostico = diag.strip()

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def vehiculo(self) -> Vehiculo:
        return self._vehiculo

    @property
    def mecanico_asignado(self) -> Optional[Mecanico]:
        return self._mecanico_asignado

    @property
    def detalles_repuestos(self) -> List[DetalleRepuesto]:
        return list(self._detalles_repuestos)

    def asignar_mecanico(self, mecanico: Mecanico) -> None:
        """Asigna un técnico responsable a la orden y cambia estado a EN_DIAGNOSTICO."""
        self._mecanico_asignado = mecanico
        self._estado = "EN_DIAGNOSTICO"

    def registrar_horas(self, horas: float) -> None:
        """Suma horas de mano de obra trabajadas en esta orden."""
        if horas > 0:
            self._horas_trabajo += float(horas)

    def agregar_repuesto(self, repuesto: Repuesto, cant: int, valor_dolar: float = 950.0) -> None:
        """
        Descuenta el stock del repuesto y lo añade como línea de detalle a la orden.
        Lanza SinStockError si no hay existencias.
        """
        repuesto.descontar_stock(cant)
        detalle = DetalleRepuesto(repuesto, cant, valor_dolar)
        self._detalles_repuestos.append(detalle)

    def calcular_mano_obra(self) -> float:
        """
        Cálculo polimórfico de mano de obra:
        Multiplica las horas registradas por la tarifa horaria propia de la subclase del vehículo.
        """
        return self._horas_trabajo * self._vehiculo.tarifa_hora()

    def calcular_total_repuestos(self) -> float:
        """Calcula la suma de subtotales de todos los repuestos utilizados."""
        return sum(d.calcular_subtotal() for d in self._detalles_repuestos)

    def calcular_total_neto(self) -> float:
        """Calcula el total neto (Mano de obra + Repuestos)."""
        return self.calcular_mano_obra() + self.calcular_total_repuestos()

    def calcular_total_con_iva(self, iva: float = 0.19) -> float:
        """Calcula el total a pagar incluyendo el Impuesto al Valor Agregado (IVA 19%)."""
        return self.calcular_total_neto() * (1.0 + float(iva))

    def cerrar_orden(self) -> None:
        """Finaliza los trabajos técnicos de la orden."""
        self._estado = "FINALIZADO"

    def entregar_vehiculo(self) -> None:
        """
        Marca la orden como ENTREGADO, registra la fecha de salida
        y libera el vehículo de las dependencias del taller.
        """
        if not self._vehiculo.esta_en_taller():
            raise VehiculoNoIngresadoError(self._vehiculo.patente)
        
        self._estado = "ENTREGADO"
        self._fecha_entrega = datetime.now()
        self._vehiculo.entregar()

    def __str__(self) -> str:
        mecanico_str = self._mecanico_asignado.username if self._mecanico_asignado else "Sin asignar"
        return (
            f"=== ORDEN DE TRABAJO N°{self._numero_orden} [{self._estado}] ===\n"
            f"Cliente: {self._cliente.get_nombre()} ({self._cliente.get_rut()})\n"
            f"Vehículo: {self._vehiculo.patente} - {self._vehiculo.modelo} ({self._vehiculo.__class__.__name__})\n"
            f"Mecánico: {mecanico_str}\n"
            f"Horas: {self._horas_trabajo:.1f}h | Mano de obra: ${self.calcular_mano_obra():,.0f} CLP\n"
            f"Repuestos ({len(self._detalles_repuestos)}): ${self.calcular_total_repuestos():,.0f} CLP\n"
            f"Total Neto: ${self.calcular_total_neto():,.0f} CLP | Total c/IVA (19%): ${self.calcular_total_con_iva():,.0f} CLP\n"
            f"Diagnóstico: {self._diagnostico or 'Sin diagnóstico aún'}"
        )
