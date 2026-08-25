"""
Módulo ServicioDolarAPI
Permite obtener el valor del dólar observado en tiempo real desde APIs públicas
con mecanismo de fallback y caché local.
"""

import json
import urllib.request
import urllib.error


class ServicioDolarAPI:
    """Cliente de servicio para consultar tipos de cambio de divisas."""

    def __init__(self, endpoint_url: str = "https://mindicador.cl/api/dolar", timeout: int = 5):
        self._endpoint_url: str = endpoint_url
        self._timeout: int = timeout
        self._cache_valor: float = 950.0  # Caché de contingencia

    @property
    def endpoint_url(self) -> str:
        return self._endpoint_url

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def cache_valor(self) -> float:
        return self._cache_valor

    def _consultar_api_externa(self) -> float:
        """Realiza la solicitud HTTP GET a la API externa de indicadores económicos."""
        req = urllib.request.Request(
            self._endpoint_url,
            headers={"User-Agent": "Antigravity-TallerMecanico/1.0"}
        )
        with urllib.request.urlopen(req, timeout=self._timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                
                # Compatible con formato mindicador.cl {"serie": [{"valor": 950.2, ...}]}
                if "serie" in data and len(data["serie"]) > 0:
                    return float(data["serie"][0]["valor"])
                elif "dolar" in data and "valor" in data["dolar"]:
                    return float(data["dolar"]["valor"])
                elif "valor" in data:
                    return float(data["valor"])
                
        raise ValueError("Estructura JSON de la API no contiene el valor esperado del dólar.")

    def obtener_valor_dolar(self) -> float:
        """
        Obtiene el valor actual del dólar en CLP.
        Si la conexión falla o no hay internet, retorna el último valor cacheado con seguridad.
        """
        try:
            valor = self._consultar_api_externa()
            self._cache_valor = valor
            return valor
        except Exception:
            # Fallback transparente para garantizar continuidad operativa
            return self._cache_valor
