# Consulta de calificaciones con SQLAlchemy ORM y analisis con pandas
from sqlalchemy import (
    Column, Integer, Numeric, ForeignKey,
    UniqueConstraint, CheckConstraint, create_engine
)
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

# Datos de conexion a PostgreSQL (ajusta si cambiaron)
USER = "emijon"
PASSWORD = "1234"
HOST = "localhost"
PORT = 5432
DB_NAME = "escuelados"

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DB_NAME,
)
engine = create_engine(DATABASE_URL)
Base = declarative_base()


# Modelo ORM de la tabla existente en PostgreSQL
class Calificaciones(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id", ondelete="CASCADE"))
    materia_id = Column(Integer, ForeignKey("materias.id", ondelete="CASCADE"))
    calificacion = Column(Numeric(precision=5, scale=2))

    __table_args__ = (
        UniqueConstraint("alumno_id", "materia_id", name="un_alumno_materia"),
        CheckConstraint(
            "calificacion >= 0 AND calificacion <= 100",
            name="calificaciones_calificacion_check",
        ),
    )


# Se consulta una tabla que ya existe: no se llama a create_all().
SessionLocal = sessionmaker(bind=engine)
COLUMNAS = ["id", "alumno_id", "materia_id", "calificacion"]


def convertir_a_dataframe(registros):
    return pd.DataFrame(
        [
            {
                "id": registro.id,
                "alumno_id": registro.alumno_id,
                "materia_id": registro.materia_id,
                "calificacion": float(registro.calificacion)
                if registro.calificacion is not None else float("nan"),
            }
            for registro in registros
        ],
        columns=COLUMNAS,
    )


# Se dejan disponibles las variables para inspeccionarlas con IPython -i.
datos = pd.DataFrame(columns=COLUMNAS)
df = pd.DataFrame(columns=COLUMNAS)
media = float("nan")
varianza = float("nan")
desviacion_estandar = float("nan")

try:
    # La sesion ORM se crea antes de realizar las consultas.
    with SessionLocal() as session:
        # Todas las calificaciones, usando solo ORM (sin SQL escrito a mano).
        resultado = session.query(Calificaciones).order_by(Calificaciones.id).all()
        datos = convertir_a_dataframe(resultado)

        # Calificaciones correspondientes a la materia con ID 5.
        resultado_materia_5 = (
            session.query(Calificaciones)
            .filter(Calificaciones.materia_id == 5)
            .order_by(Calificaciones.id)
            .all()
        )
        df = convertir_a_dataframe(resultado_materia_5)

    print("\nTODAS LAS CALIFICACIONES")
    print(datos.to_string(index=False) if not datos.empty else "No hay registros.")
    print("\nCALIFICACIONES DE LA MATERIA ID 5")
    print(df.to_string(index=False) if not df.empty else "No hay registros.")

    # Estadisticas de TODAS las calificaciones, sin valores nulos.
    calificaciones = datos["calificacion"].dropna()
    if not calificaciones.empty:
        media = calificaciones.mean()
        varianza = calificaciones.var()  # Varianza muestral (ddof=1)
        desviacion_estandar = calificaciones.std()  # Desviacion muestral
        print("\nESTADISTICAS DE TODAS LAS CALIFICACIONES")
        print(f"Media: {media:.2f}")
        print(f"Varianza: {varianza:.2f}" if pd.notna(varianza) else "Varianza: no disponible (menos de 2 valores)")
        print(f"Desviacion estandar: {desviacion_estandar:.2f}" if pd.notna(desviacion_estandar) else "Desviacion estandar: no disponible (menos de 2 valores)")
    else:
        print("\nNo hay calificaciones numericas para calcular estadisticas.")

except SQLAlchemyError as error:
    print(f"\nError al consultar PostgreSQL: {error}")
