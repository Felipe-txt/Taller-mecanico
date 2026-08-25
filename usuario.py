"""
Módulo Usuario
Clase base abstracta para el personal del taller con autenticación segura por hash y permisos.
"""

from abc import ABC
import hashlib
from persona import Persona


class Usuario(Persona, ABC):
    """Clase base para los empleados/usuarios con acceso al sistema del taller."""

    def __init__(self, rut: str, nombre: str, telefono: str, email: str, username: str, password: str, rol: str):
        super().__init__(rut, nombre, telefono, email)
        self._username: str = username.strip().lower()
        self._password_hash: str = self._hash_password(password)
        self._rol: str = rol.strip().upper()
        self._activo: bool = True

    @staticmethod
    def _hash_password(raw_pwd: str) -> str:
        """Genera un hash SHA-256 de la contraseña proporcionada."""
        return hashlib.sha256(raw_pwd.encode("utf-8")).hexdigest()

    def autenticar(self, password: str) -> bool:
        """Verifica si la contraseña ingresada coincide con el hash almacenado."""
        if not self._activo:
            return False
        return self._hash_password(password) == self._password_hash

    def cambiar_password(self, password_actual: str, password_nueva: str) -> bool:
        """Permite actualizar la contraseña previa validación de la anterior."""
        if self.autenticar(password_actual):
            self._password_hash = self._hash_password(password_nueva)
            return True
        return False

    def tiene_permiso(self, accion: str) -> bool:
        """Verifica si el rol del usuario cuenta con autorización para realizar una acción."""
        permisos_por_rol = {
            "ADMIN": ["*"],
            "RECEPCIONISTA": ["recibir_vehiculo", "entregar_vehiculo", "consultar_orden", "registrar_cliente"],
            "MECANICO": ["diagnosticar", "registrar_horas", "agregar_repuesto", "consultar_orden"]
        }
        permisos = permisos_por_rol.get(self._rol, [])
        return "*" in permisos or accion.lower() in [p.lower() for p in permisos]

    @property
    def username(self) -> str:
        return self._username

    @property
    def rol(self) -> str:
        return self._rol

    @property
    def activo(self) -> bool:
        return self._activo

    def desactivar(self) -> None:
        self._activo = False

    def activar(self) -> None:
        self._activo = True

    def __str__(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        return f"Usuario: {self._username} ({self._nombre}) | Rol: {self._rol} | Estado: {estado}"
