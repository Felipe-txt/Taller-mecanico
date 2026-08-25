"""
Módulo RepositorioBD
Manejo de persistencia SQLite para órdenes de trabajo, control de stock y bitácora de auditoría.
"""

import sqlite3
import datetime
from typing import Optional, Dict, Any
from orden_trabajo import OrdenTrabajo


class RepositorioBD:
    """Clase responsable del acceso y persistencia de datos (CRUD)."""

    def __init__(self, connection_string: str = "taller_mecanico.db"):
        self._connection_string: str = connection_string
        self._db_connection: Any = None
        self._inicializar_tablas()

    def _get_connection(self) -> sqlite3.Connection:
        """Retorna una conexión activa a la base de datos SQLite."""
        return sqlite3.connect(self._connection_string)

    def _inicializar_tablas(self) -> None:
        """Crea el esquema relacional en SQLite si no existe previamente."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ordenes (
                    numero_orden INTEGER PRIMARY KEY,
                    fecha_ingreso TEXT,
                    fecha_entrega TEXT,
                    estado TEXT,
                    horas_trabajo REAL,
                    diagnostico TEXT,
                    rut_cliente TEXT,
                    patente_vehiculo TEXT,
                    mecanico TEXT,
                    total_neto REAL,
                    total_iva REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS repuestos_stock (
                    codigo TEXT PRIMARY KEY,
                    stock INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS log_auditoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    usuario TEXT,
                    accion TEXT
                )
            """)
            conn.commit()

    def guardar_orden(self, orden: OrdenTrabajo) -> bool:
        """Inserta o actualiza una orden de trabajo en la base de datos."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO ordenes (
                        numero_orden, fecha_ingreso, fecha_entrega, estado,
                        horas_trabajo, diagnostico, rut_cliente, patente_vehiculo,
                        mecanico, total_neto, total_iva
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    orden.numero_orden,
                    orden.fecha_ingreso.isoformat() if orden.fecha_ingreso else None,
                    orden.fecha_entrega.isoformat() if orden.fecha_entrega else None,
                    orden.estado,
                    orden.horas_trabajo,
                    orden.diagnostico,
                    orden.cliente.get_rut(),
                    orden.vehiculo.patente,
                    orden.mecanico_asignado.username if orden.mecanico_asignado else None,
                    orden.calcular_total_neto(),
                    orden.calcular_total_con_iva()
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al guardar la orden N°{orden.numero_orden} en BD: {e}")
            return False

    def obtener_orden(self, num_orden: int) -> Optional[Dict[str, Any]]:
        """Consulta una orden de trabajo por su número identificador."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ordenes WHERE numero_orden = ?", (num_orden,))
            row = cursor.fetchone()
            if row:
                columnas = [desc[0] for desc in cursor.description]
                return dict(zip(columnas, row))
            return None

    def actualizar_stock(self, codigo: str, stock: int) -> None:
        """Actualiza el nivel de existencias de un repuesto en la base de datos."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO repuestos_stock (codigo, stock)
                VALUES (?, ?)
            """, (codigo.strip().upper(), int(stock)))
            conn.commit()

    def registrar_log_auditoria(self, user: str, accion: str) -> None:
        """Registra una acción en la bitácora de auditoría."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO log_auditoria (fecha, usuario, accion)
                VALUES (?, ?, ?)
            """, (datetime.datetime.now().isoformat(), user, accion))
            conn.commit()
