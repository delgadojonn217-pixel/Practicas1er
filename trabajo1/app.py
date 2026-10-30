import math
from datetime import date

from sqlalchemy import (
    Column,
    Date,
    Numeric,
    Integer,
    create_engine
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)


# ============================================================
# 1. DATOS DE CONEXION A POSTGRESQL
# ============================================================

USER = "emijon"
PASSWORD = "1234"

HOST = "localhost"
PORT = "5432"

DB_NAME = "analisis_sexenios"


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ============================================================
# 2. MODELO DE LA TABLA
# ============================================================

Base = declarative_base()


class TipoCambio(Base):
    __tablename__ = "tipo_cambiod"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    fecha = Column(
        Date,
        nullable=False
    )

    determinacion = Column(
        Numeric(
            precision=10,
            scale=4
        )
    )

    publicacion_dof = Column(
        Numeric(
            precision=10,
            scale=4
        )
    )

    solventar_obligaciones = Column(
        Numeric(
            precision=10,
            scale=4
        )
    )


# ============================================================
# 3. CREAR SESION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

session = SessionLocal()


# ============================================================
# 4. FUNCIONES ESTADISTICAS
# ============================================================


def calcular_media_de(lista):

    n = len(lista)

    if n == 0:
        return 0

    media = sum(lista) / n

    return media


def obtener_varianza_de(
    lista,
    poblacional=False
):

    n = len(lista)

    # Si no hay datos
    if n == 0:
        return 0

    # Si queremos varianza muestral,
    # necesitamos por lo menos 2 datos.
    if n < 2 and not poblacional:
        return 0

    # Calcular media
    media = calcular_media_de(lista)

    # Sumatoria de:
    # (dato - media)^2
    suma_cuadrados = sum(
        (x - media) ** 2
        for x in lista
    )

    # Varianza poblacional
    if poblacional:

        return suma_cuadrados / n

    # Varianza muestral
    else:

        return suma_cuadrados / (n - 1)


def obtener_desviacion_estandar(
    lista,
    poblacional=False
):

    varianza = obtener_varianza_de(
        lista,
        poblacional
    )

    desviacion = math.sqrt(varianza)

    return desviacion


def obtener_variacion_porcentual(lista):

    if len(lista) < 2:
        return 0

    valor_inicial = lista[0]
    valor_final = lista[-1]

    if valor_inicial == 0:
        return 0

    variacion = (
        (valor_final - valor_inicial)
        / valor_inicial
    ) * 100

    return variacion


# ============================================================
# 5. FUNCION PARA OBTENER DATOS DE UN PERIODO
# ============================================================


def obtener_datos_periodo(
    fecha_inicio,
    fecha_fin
):

    datos = (
        session
        .query(TipoCambio)
        .filter(
            TipoCambio.fecha.between(
                fecha_inicio,
                fecha_fin
            )
        )
        .order_by(
            TipoCambio.fecha
        )
        .all()
    )

    return datos


# ============================================================
# 6. OBTENER VALORES NUMERICOS
# ============================================================


def obtener_lista_determinacion(datos):

    lista = []

    for dato in datos:

        if dato.determinacion is not None:

            # Convertimos Numeric/Decimal de PostgreSQL
            # a float para facilitar los calculos.
            lista.append(
                float(dato.determinacion)
            )

    return lista


def obtener_lista_publicacion(datos):

    lista = []

    for dato in datos:

        if dato.publicacion_dof is not None:

            lista.append(
                float(dato.publicacion_dof)
            )

    return lista


def obtener_lista_obligaciones(datos):

    lista = []

    for dato in datos:

        if dato.solventar_obligaciones is not None:

            lista.append(
                float(
                    dato.solventar_obligaciones
                )
            )

    return lista


# ============================================================
# 7. MOSTRAR RESULTADOS
# ============================================================


def analizar_indicador(
    nombre,
    lista
):

    print()
    print(
        "============================================"
    )

    print(
        f"INDICADOR: {nombre}"
    )

    print(
        "============================================"
    )

    print(
        f"Cantidad de datos: {len(lista)}"
    )

    if len(lista) == 0:

        print(
            "No existen datos para realizar el calculo."
        )

        return

    media = calcular_media_de(
        lista
    )

    # True = varianza poblacional
    varianza = obtener_varianza_de(
        lista,
        True
    )

    desviacion = obtener_desviacion_estandar(
        lista,
        True
    )

    variacion = obtener_variacion_porcentual(
        lista
    )

    print(
        f"Media: {media:.4f}"
    )

    print(
        f"Varianza: {varianza:.6f}"
    )

    print(
        f"Desviacion estandar: {desviacion:.6f}"
    )

    print(
        f"Variacion porcentual: {variacion:.4f}%"
    )


# ============================================================
# 8. PRIMER PERIODO
# ============================================================


fecha_inicio_1 = date(
    2012,
    1,
    1
)

fecha_fin_1 = date(
    2018,
    12,
    31
)


datos_2012_2018 = obtener_datos_periodo(
    fecha_inicio_1,
    fecha_fin_1
)


determinacion_2012_2018 = (
    obtener_lista_determinacion(
        datos_2012_2018
    )
)


publicacion_2012_2018 = (
    obtener_lista_publicacion(
        datos_2012_2018
    )
)


obligaciones_2012_2018 = (
    obtener_lista_obligaciones(
        datos_2012_2018
    )
)


print()
print()
print(
    "############################################"
)

print(
    "       PERIODO 2012 - 2018"
)

print(
    "############################################"
)


analizar_indicador(
    "Determinacion",
    determinacion_2012_2018
)


analizar_indicador(
    "Publicacion DOF",
    publicacion_2012_2018
)


analizar_indicador(
    "Para solventar obligaciones",
    obligaciones_2012_2018
)


# ============================================================
# 9. SEGUNDO PERIODO
# ============================================================


fecha_inicio_2 = date(
    2019,
    1,
    1
)

fecha_fin_2 = date(
    2024,
    12,
    31
)


datos_2019_2024 = obtener_datos_periodo(
    fecha_inicio_2,
    fecha_fin_2
)


determinacion_2019_2024 = (
    obtener_lista_determinacion(
        datos_2019_2024
    )
)


publicacion_2019_2024 = (
    obtener_lista_publicacion(
        datos_2019_2024
    )
)


obligaciones_2019_2024 = (
    obtener_lista_obligaciones(
        datos_2019_2024
    )
)


print()
print()
print(
    "############################################"
)

print(
    "       PERIODO 2019 - 2024"
)

print(
    "############################################"
)


analizar_indicador(
    "Determinacion",
    determinacion_2019_2024
)


analizar_indicador(
    "Publicacion DOF",
    publicacion_2019_2024
)


analizar_indicador(
    "Para solventar obligaciones",
    obligaciones_2019_2024
)


# ============================================================
# 10. CERRAR SESION
# ============================================================

session.close()


print()

