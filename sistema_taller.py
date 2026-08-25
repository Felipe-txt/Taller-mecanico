"""
Módulo SistemaTaller
Controlador principal / Fachada (Façade) que centraliza las operaciones del taller mecánico.
"""

from typing import Dict, List, Optional, Any
from cliente import Cliente
from usuario import Usuario
from mecanico import Mecanico
from recepcionista import Recepcionista
from vehiculo import Vehiculo
from auto import Auto
from moto import Moto
from camion import Camion
from bus import Bus
from repuesto import Repuesto
from repuesto_importado import RepuestoImportado
from orden_trabajo import OrdenTrabajo
from repositorio_bd import RepositorioBD
from servicio_dolar import ServicioDolarAPI
from excepciones import TallerError, ClienteConDeudaError, VehiculoNoIngresadoError


class SistemaTaller:
    """Fachada integral para la gestión y orquestación del taller mecánico."""

    def __init__(self, nombre_taller: str = "Taller Mecánico Central", repo_bd: Optional[RepositorioBD] = None):
        self._nombre_taller: str = nombre_taller
        self._repositorio_ordenes: List[OrdenTrabajo] = []
        self._catalogo_repuestos: Dict[str, Repuesto] = {}
        self._clientes_registrados: Dict[str, Cliente] = {}
        self._usuarios_activos: Dict[str, Usuario] = {}
        self._repositorio_bd: RepositorioBD = repo_bd or RepositorioBD()
        self._servicio_dolar: ServicioDolarAPI = ServicioDolarAPI()
        self._contador_ordenes: int = 1

    @property
    def nombre_taller(self) -> str:
        return self._nombre_taller

    @property
    def repositorio_ordenes(self) -> List[OrdenTrabajo]:
        return list(self._repositorio_ordenes)

    @property
    def catalogo_repuestos(self) -> Dict[str, Repuesto]:
        return self._catalogo_repuestos

    @property
    def clientes_registrados(self) -> Dict[str, Cliente]:
        return self._clientes_registrados

    @property
    def usuarios_activos(self) -> Dict[str, Usuario]:
        return self._usuarios_activos

    def registrar_cliente(self, rut: str, nombre: str, tel: str, email: str) -> Cliente:
        """Registra un nuevo cliente o retorna el existente si ya se encuentra registrado."""
        rut_normalizado = rut.replace(".", "").replace("-", "").strip().upper()
        
        # Buscar por RUT limpio
        for c in self._clientes_registrados.values():
            if c.get_rut().replace(".", "").replace("-", "").strip().upper() == rut_normalizado:
                return c
        
        cliente = Cliente(rut=rut, nombre=nombre, telefono=tel, email=email)
        self._clientes_registrados[cliente.get_rut()] = cliente
        self._repositorio_bd.registrar_log_auditoria("SISTEMA", f"Registro de cliente {cliente.get_nombre()} ({cliente.get_rut()})")
        return cliente

    def registrar_usuario(self, usuario: Usuario) -> Usuario:
        """Registra un nuevo usuario/empleado en el sistema."""
        self._usuarios_activos[usuario.username] = usuario
        self._repositorio_bd.registrar_log_auditoria("SISTEMA", f"Registro de usuario @{usuario.username} ({usuario.rol})")
        return usuario

    def registrar_repuesto(self, repuesto: Repuesto) -> Repuesto:
        """Añade un repuesto al catálogo del taller y sincroniza con BD."""
        self._catalogo_repuestos[repuesto.codigo] = repuesto
        self._repositorio_bd.actualizar_stock(repuesto.codigo, repuesto.stock)
        return repuesto

    def recepcionar_vehiculo(
        self,
        rut_cli: str,
        patente: str,
        mod: str,
        tipo: str,
        anio: int = 2020,
        extra_param: Any = None
    ) -> OrdenTrabajo:
        """
        Recepciona un vehículo, instancia la subclase polimórfica adecuada,
        valida deudas del cliente y genera la Orden de Trabajo.
        """
        rut_limpio = rut_cli.replace(".", "").replace("-", "").strip().upper()
        cliente_encontrado: Optional[Cliente] = None
        for c in self._clientes_registrados.values():
            if c.get_rut().replace(".", "").replace("-", "").strip().upper() == rut_limpio:
                cliente_encontrado = c
                break

        if not cliente_encontrado:
            raise TallerError(f"Cliente con RUT '{rut_cli}' no se encuentra registrado en el sistema.")

        if not cliente_encontrado.puede_ingresar_vehiculo():
            raise ClienteConDeudaError(cliente_encontrado.get_rut(), cliente_encontrado.monto_deuda)

        tipo_normalizado = tipo.strip().lower()
        if tipo_normalizado == "auto":
            carroceria = str(extra_param) if extra_param else "Sedán"
            vehiculo: Vehiculo = Auto(patente=patente, modelo=mod, anio=anio, tipo_carroceria=carroceria)
        elif tipo_normalizado == "moto":
            cc = int(extra_param) if extra_param else 150
            vehiculo = Moto(patente=patente, modelo=mod, anio=anio, cilindrada_cc=cc)
        elif tipo_normalizado == "camion":
            ton = float(extra_param) if extra_param else 5.0
            vehiculo = Camion(patente=patente, modelo=mod, anio=anio, capacidad_ton=ton)
        elif tipo_normalizado == "bus":
            asientos = int(extra_param) if extra_param else 40
            vehiculo = Bus(patente=patente, modelo=mod, anio=anio, cantidad_asientos=asientos)
        else:
            raise ValueError(f"Tipo de vehículo inválido: '{tipo}'. Debe ser 'auto', 'moto', 'camion' o 'bus'.")

        num_orden = self._contador_ordenes
        self._contador_ordenes += 1
        
        orden = OrdenTrabajo(num=num_orden, cliente=cliente_encontrado, vehiculo=vehiculo)
        vehiculo.ingresar()
        self._repositorio_ordenes.append(orden)
        self._repositorio_bd.guardar_orden(orden)
        self._repositorio_bd.registrar_log_auditoria(
            "RECEPCION",
            f"Ingreso de vehículo {vehiculo.patente} ({tipo_normalizado}) para orden N°{num_orden}"
        )
        return orden

    def asignar_mecanico(self, num_orden: int, username: str) -> None:
        """Asigna un mecánico activo a una orden de trabajo."""
        orden = self._buscar_orden(num_orden)
        user_key = username.strip().lower()
        if user_key not in self._usuarios_activos:
            raise TallerError(f"Usuario '{username}' no existe en el sistema.")
        
        usuario = self._usuarios_activos[user_key]
        if not isinstance(usuario, Mecanico):
            raise TallerError(f"El usuario @{username} no tiene rol de Mecánico.")
        
        orden.asignar_mecanico(usuario)
        self._repositorio_bd.guardar_orden(orden)
        self._repositorio_bd.registrar_log_auditoria(
            username,
            f"Asignado como técnico a orden N°{num_orden}"
        )

    def agregar_repuesto_orden(self, num_orden: int, cod: str, cant: int) -> None:
        """Agrega repuestos a una orden de trabajo consultando la cotización en vivo."""
        orden = self._buscar_orden(num_orden)
        cod_normalizado = cod.strip().upper()
        if cod_normalizado not in self._catalogo_repuestos:
            raise TallerError(f"El repuesto con código '{cod}' no se encuentra en el catálogo.")
        
        repuesto = self._catalogo_repuestos[cod_normalizado]
        valor_dolar = self._servicio_dolar.obtener_valor_dolar()
        
        orden.agregar_repuesto(repuesto, cant, valor_dolar=valor_dolar)
        self._repositorio_bd.actualizar_stock(repuesto.codigo, repuesto.stock)
        self._repositorio_bd.guardar_orden(orden)
        self._repositorio_bd.registrar_log_auditoria(
            "MECANICO",
            f"Agregado {cant}x '{repuesto.nombre}' a orden N°{num_orden}"
        )

    def finalizar_orden(self, num_orden: int, horas: float) -> float:
        """Registra las horas trabajadas, cierra la orden y retorna el total con IVA."""
        orden = self._buscar_orden(num_orden)
        if orden.mecanico_asignado:
            orden.mecanico_asignado.registrar_horas(orden, horas)
        else:
            orden.registrar_horas(horas)
        
        orden.cerrar_orden()
        self._repositorio_bd.guardar_orden(orden)
        self._repositorio_bd.registrar_log_auditoria(
            "TALLER",
            f"Cierre de orden N°{num_orden} con {horas}h trabajadas"
        )
        return orden.calcular_total_con_iva()

    def entregar_vehiculo_orden(self, num_orden: int) -> None:
        """Entrega formalmente el vehículo reparado al cliente."""
        orden = self._buscar_orden(num_orden)
        orden.entregar_vehiculo()
        self._repositorio_bd.guardar_orden(orden)
        self._repositorio_bd.registrar_log_auditoria(
            "RECEPCION",
            f"Entrega de vehículo {orden.vehiculo.patente} de orden N°{num_orden}"
        )

    def guardar_estado_bd(self) -> bool:
        """Persiste todas las órdenes en la base de datos."""
        exito = True
        for orden in self._repositorio_ordenes:
            if not self._repositorio_bd.guardar_orden(orden):
                exito = False
        return exito

    def _buscar_orden(self, num_orden: int) -> OrdenTrabajo:
        for orden in self._repositorio_ordenes:
            if orden.numero_orden == num_orden:
                return orden
        raise TallerError(f"Orden de trabajo N°{num_orden} no fue encontrada.")
