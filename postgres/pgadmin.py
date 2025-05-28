import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
database = os.getenv("PG_DATABASE")

db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(db_url)
csv_path = r"outputs\cleaned_ev.csv"  

try:
    ev_df = pd.read_csv(csv_path)
    ev_df.to_sql("ev_data", engine, if_exists="replace", index=False)
    print("Data loaded successfully!")
except SQLAlchemyError as e:
    print('Error while uploading df to postgresql: ', str(e))
except Exception as e:
    print('Error: ',str(e))