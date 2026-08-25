"""
Módulo Principal de Ejecución (Demo del Sistema Taller Mecánico POO)
Demuestra el funcionamiento integral de todas las clases, relaciones UML,
polimorfismo, manejo de excepciones y persistencia.
"""

from excepciones import TallerError, SinStockError, ClienteConDeudaError, VehiculoNoIngresadoError
from cliente import Cliente
from mecanico import Mecanico
from recepcionista import Recepcionista
from auto import Auto
from moto import Moto
from camion import Camion
from bus import Bus
from repuesto import Repuesto
from repuesto_importado import RepuestoImportado
from servicio_dolar import ServicioDolarAPI
from sistema_taller import SistemaTaller


def imprimir_separador(titulo: str = ""):
    print("\n" + "=" * 70)
    if titulo:
        print(f"  {titulo.upper()}")
        print("=" * 70)


def main():
    imprimir_separador("INICIANDO SISTEMA TALLER MECÁNICO POO")
    
    # 1. Inicializar la fachada del taller
    sistema = SistemaTaller("Taller Mecánico Cordillera SpA")
    print(f"Sistema inicializado: {sistema.nombre_taller}")

    # 2. Registrar Personal (Usuarios con RUT chileno válido)
    imprimir_separador("1. REGISTRO DE USUARIOS Y PERSONAL")
    recepcionista = Recepcionista(
        rut="19.876.543-0",
        nombre="Valeria Gómez",
        telefono="+56911223344",
        email="valeria.gomez@tallercordillera.cl",
        username="vgomez",
        password="Password123!",
        turno="Mañana"
    )
    mecanico1 = Mecanico(
        rut="17.654.321-3",
        nombre="Carlos Mendoza",
        telefono="+56988776655",
        email="carlos.mendoza@tallercordillera.cl",
        username="cmendoza",
        password="Mecanico2026*",
        especialidad="Motor y Transmisión"
    )
    mecanico2 = Mecanico(
        rut="16.543.210-K",
        nombre="Andrea Morales",
        telefono="+56977665544",
        email="andrea.morales@tallercordillera.cl",
        username="amorales",
        password="Mecanico2026*",
        especialidad="Frenos y Suspensión"
    )

    sistema.registrar_usuario(recepcionista)
    sistema.registrar_usuario(mecanico1)
    sistema.registrar_usuario(mecanico2)
    print(f"[OK] Recepcionista registrada: {recepcionista}")
    print(f"[OK] Mecánico 1 registrado: {mecanico1}")
    print(f"[OK] Mecánico 2 registrado: {mecanico2}")

    # Prueba de autenticación con hash
    autenticado = recepcionista.autenticar("Password123!")
    print(f"[AUTH] Autenticación @{recepcionista.username} con clave correcta: {autenticado}")

    # 3. Registrar Clientes
    imprimir_separador("2. REGISTRO DE CLIENTES")
    cliente1 = sistema.registrar_cliente(
        rut="18.234.567-9",
        nombre="Juan Pérez Soto",
        tel="+56999887766",
        email="juan.perez@gmail.com"
    )
    cliente2 = sistema.registrar_cliente(
        rut="15.432.109-8",
        nombre="María José Valdés",
        tel="+56955443322",
        email="mj.valdes@empresa.cl"
    )
    print(f"[OK] {cliente1}")
    print(f"[OK] {cliente2}")

    # 4. Catálogo de Repuestos (Nacionales e Importados en USD)
    imprimir_separador("3. INVENTARIO DE REPUESTOS Y API DÓLAR")
    dolar_api = ServicioDolarAPI()
    valor_dolar = dolar_api.obtener_valor_dolar()
    print(f"[INFO] Cotización Dólar Observado obtenida: ${valor_dolar:,.2f} CLP")

    rep1 = Repuesto("ACE-5W30", "Aceite Sintético 5W30 4L", stock=15, precio_base_clp=38000.0)
    rep2 = Repuesto("FIL-01", "Filtro de Aceite Universal", stock=20, precio_base_clp=12500.0)
    rep3_imp = RepuestoImportado("KIT-EMB-09", "Kit de Embrague Reforzado", stock=4, precio_usd=120.0, arancel_porcentaje=0.06)
    rep4_imp = RepuestoImportado("DISC-CER", "Juego Discos de Freno Cerámicos", stock=2, precio_usd=85.0, arancel_porcentaje=0.06)

    sistema.registrar_repuesto(rep1)
    sistema.registrar_repuesto(rep2)
    sistema.registrar_repuesto(rep3_imp)
    sistema.registrar_repuesto(rep4_imp)

    print(f"[OK] {rep1}")
    print(f"[OK] {rep2}")
    print(f"[OK] {rep3_imp} -> Precio CLP estimado: ${rep3_imp.get_precio_clp(valor_dolar):,.0f} CLP")
    print(f"[OK] {rep4_imp} -> Precio CLP estimado: ${rep4_imp.get_precio_clp(valor_dolar):,.0f} CLP")

    # 5. Recepción de Vehículos (Demostración de Polimorfismo)
    imprimir_separador("4. RECEPCIÓN Y POLIMORFISMO DE VEHÍCULOS")
    
    # Orden 1: Auto Particular
    orden_auto = sistema.recepcionar_vehiculo(
        rut_cli="18.234.567-9",
        patente="ABCD12",
        mod="Toyota Corolla",
        tipo="auto",
        anio=2021,
        extra_param="Sedán"
    )
    print(f"[RECEPCIÓN] Auto ingresado con Orden N°{orden_auto.numero_orden}")
    print(f"            Tarifa mano de obra: ${orden_auto.vehiculo.tarifa_hora():,.0f} CLP/hora")

    # Orden 2: Moto
    orden_moto = sistema.recepcionar_vehiculo(
        rut_cli="18.234.567-9",
        patente="XY1234",
        mod="Yamaha MT-03",
        tipo="moto",
        anio=2022,
        extra_param=321
    )
    print(f"[RECEPCIÓN] Moto ingresada con Orden N°{orden_moto.numero_orden}")
    print(f"            Tarifa mano de obra: ${orden_moto.vehiculo.tarifa_hora():,.0f} CLP/hora")

    # Orden 3: Camión
    orden_camion = sistema.recepcionar_vehiculo(
        rut_cli="15.432.109-8",
        patente="GHJK56",
        mod="Volvo FH 500",
        tipo="camion",
        anio=2019,
        extra_param=18.5
    )
    print(f"[RECEPCIÓN] Camión ingresado con Orden N°{orden_camion.numero_orden}")
    print(f"            Tarifa mano de obra: ${orden_camion.vehiculo.tarifa_hora():,.0f} CLP/hora")

    # 6. Diagnóstico y Asignación de Mecánico
    imprimir_separador("5. ASIGNACIÓN, DIAGNÓSTICO Y CONSUMO DE REPUESTOS")
    sistema.asignar_mecanico(orden_auto.numero_orden, "cmendoza")
    mecanico1.diagnosticar(orden_auto, "Mantenimiento preventivo 40.000 km y cambio de embrague.")
    
    # Agregar repuestos a la orden
    sistema.agregar_repuesto_orden(orden_auto.numero_orden, "ACE-5W30", cant=1)
    sistema.agregar_repuesto_orden(orden_auto.numero_orden, "FIL-01", cant=1)
    sistema.agregar_repuesto_orden(orden_auto.numero_orden, "KIT-EMB-09", cant=1)

    print(f"[DIAGNÓSTICO] Orden N°{orden_auto.numero_orden}: {orden_auto.diagnostico}")
    print(f"[REPUESTOS CONSUMIDOS EN ORDEN N°{orden_auto.numero_orden}]:")
    for det in orden_auto.detalles_repuestos:
        print(f"  {det}")

    # 7. Finalizar Reparación y Liquidación
    imprimir_separador("6. CIERRE DE ORDEN, LIQUIDACIÓN Y CÁLCULO DE TOTALES")
    total_con_iva = sistema.finalizar_orden(orden_auto.numero_orden, horas=3.5)
    print(str(orden_auto))
    print(f"\n[TOTAL A PAGAR]: ${total_con_iva:,.0f} CLP")

    # 8. Entrega del Vehículo
    imprimir_separador("7. ENTREGA DEL VEHÍCULO")
    sistema.entregar_vehiculo_orden(orden_auto.numero_orden)
    print(f"[OK] Vehículo {orden_auto.vehiculo.patente} entregado. ¿En taller?: {orden_auto.vehiculo.esta_en_taller()}")

    # 9. Prueba de Excepciones del Negocio
    imprimir_separador("8. PRUEBAS DE EXCEPCIONES PROPIAS DEL NEGOCIO")
    
    # Error 1: Vehículo no ingresado (intentar entregar de nuevo)
    print("-> Probando VehiculoNoIngresadoError:")
    try:
        sistema.entregar_vehiculo_orden(orden_auto.numero_orden)
    except VehiculoNoIngresadoError as e:
        print(f"  [CAPTURADO] {e}")

    # Error 2: Sin Stock
    print("\n-> Probando SinStockError (solicitando más existencias de las disponibles):")
    try:
        sistema.agregar_repuesto_orden(orden_moto.numero_orden, "DISC-CER", cant=10)
    except SinStockError as e:
        print(f"  [CAPTURADO] {e}")

    # Error 3: Cliente con Deuda
    print("\n-> Probando ClienteConDeudaError:")
    cliente_moroso = sistema.registrar_cliente("12.345.678-5", "Pedro Picapiedra", "+56912345678", "pedro@piedra.cl")
    cliente_moroso.registrar_deuda(150000.0)
    print(f"  Estado del cliente: {cliente_moroso}")
    try:
        sistema.recepcionar_vehiculo("12.345.678-5", "JJWW99", "Troncomóvil", "auto")
    except ClienteConDeudaError as e:
        print(f"  [CAPTURADO] {e}")

    # 10. Persistencia SQLite
    imprimir_separador("9. CONSULTA EN BASE DE DATOS SQLITE")
    orden_db = sistema._repositorio_bd.obtener_orden(orden_auto.numero_orden)
    print(f"[BD SQLITE] Registro recuperado de la orden N°{orden_auto.numero_orden}:")
    for k, v in orden_db.items():
        print(f"   {k}: {v}")

    imprimir_separador("DEMOSTRACIÓN FINALIZADA CON ÉXITO")


if __name__ == "__main__":
    main()
