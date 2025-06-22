import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

Base = declarative_base()

class EVData(Base):
    __tablename__ = 'ev_data'
    dol_vehicle_id = Column(Integer, primary_key=True)
    county = Column(String)
    city = Column(String)
    state = Column(String)
    model_year = Column(Integer)
    make = Column(String)
    model = Column(String)
    electric_vehicle_type = Column(String)
    clean_alternative_fuel_vehicle_cafv_eligibility = Column(String)
    electric_range = Column(Float)
    legislative_district = Column(Float)
    range_category = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    if_urban = Column(String)

class EVUtilities(Base):
    __tablename__ = 'ev_utilities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dol_vehicle_id = Column(Integer, ForeignKey('ev_data.dol_vehicle_id', ondelete='CASCADE'))
    electric_utility = Column(String)

def load_to_postgres():
    # Load environment variables
    load_dotenv(dotenv_path="/opt/airflow/.env")

    # Fetch variables
    host = os.getenv("PG_HOST")
    port = os.getenv("PG_PORT")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    database = os.getenv("PG_DATABASE")

    # Print for debug
    print("PG_HOST:", host)
    print("PG_PORT:", port)
    print("PG_USER:", user)
    print("PG_PASSWORD:", password)
    print("PG_DATABASE:", database)

    # Fail early if any env variable is missing
    if not all([host, port, user, password, database]):
        raise ValueError("One or more PostgreSQL environment variables are missing or not loaded.")

    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(db_url)

    ev_csv = "/opt/airflow/outputs/cleaned_ev.csv"
    utility_csv = "/opt/airflow/outputs/utility_providers.csv"

    try:
        ev_df = pd.read_csv(ev_csv)
        utility_df = pd.read_csv(utility_csv)

        ev_df.columns = [c.lower().replace("(", "").replace(")", "").replace(" ", "_") for c in ev_df.columns]
        utility_df.columns = [c.lower().replace("(", "").replace(")", "").replace(" ", "_") for c in utility_df.columns]

        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS ev_utilities CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS ev_data CASCADE;"))

        Base.metadata.create_all(engine)

        ev_df.to_sql("ev_data", engine, if_exists="append", index=False)
        utility_df.to_sql("ev_utilities", engine, if_exists="append", index=False)

        print("Tables created, data loaded, and constraints applied successfully!")

    except SQLAlchemyError as e:
        print("SQLAlchemy error:", str(e))
        raise
    except Exception as e:
        print("General error:", str(e))
        raise
