"""
Módulo Persona
Clase base abstracta para todas las personas en el sistema (Clientes y Usuarios).
Implementa encapsulamiento y validación de RUT chileno.
"""

from abc import ABC, abstractmethod


class Persona(ABC):
    """Clase base abstracta que representa a una persona en el sistema."""

    def __init__(self, rut: str, nombre: str, telefono: str, email: str):
        if not self.validar_rut(rut):
            raise ValueError(f"RUT inválido: '{rut}'. Debe cumplir el formato chileno y dígito verificador válido.")
        
        self._rut: str = rut.strip().upper()
        self._nombre: str = nombre.strip()
        self._telefono: str = telefono.strip()
        self._email: str = email.strip()

    @staticmethod
    def validar_rut(rut: str) -> bool:
        """
        Valida el RUT chileno utilizando el algoritmo de Módulo 11.
        Acepta formatos con o sin puntos y guión (ej: 12.345.678-5, 12345678-K).
        """
        if not isinstance(rut, str):
            return False
        
        rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()
        if len(rut_limpio) < 2:
            return False
        
        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]
        
        if not cuerpo.isdigit():
            return False
        
        # Algoritmo Módulo 11
        suma = 0
        multiplicador = 2
        for d in reversed(cuerpo):
            suma += int(d) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        
        resto = 11 - (suma % 11)
        if resto == 11:
            dv_calculado = "0"
        elif resto == 10:
            dv_calculado = "K"
        else:
            dv_calculado = str(resto)
        
        return dv == dv_calculado

    def get_rut(self) -> str:
        """Obtiene el RUT de la persona."""
        return self._rut

    def get_nombre(self) -> str:
        """Obtiene el nombre completo de la persona."""
        return self._nombre

    def get_telefono(self) -> str:
        """Obtiene el teléfono de contacto."""
        return self._telefono

    def set_telefono(self, telefono: str) -> None:
        """Actualiza el teléfono de contacto."""
        self._telefono = telefono.strip()

    def get_email(self) -> str:
        """Obtiene el correo electrónico."""
        return self._email

    def set_email(self, email: str) -> None:
        """Actualiza el correo electrónico."""
        self._email = email.strip()

    def __str__(self) -> str:
        return f"{self._nombre} (RUT: {self._rut}) - Tel: {self._telefono} - Email: {self._email}"
