from src.prefect_etl import asteroid_etl
from sqlalchemy import create_engine
from src.logger import init_logger
from dotenv import load_dotenv
from datetime import date
import os


if __name__ == "__main__":
    log = init_logger()
    # get ENV variables
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    URL = os.getenv('URL')
    PG_USER = os.getenv('PG_USER')
    PG_PASSWORD = os.getenv('PG_PASSWORD')
    PG_HOST = os.getenv('PG_HOST')
    log.info('All ENV variables have been loaded')

    start_date = str(date.today())
    # build engine using credentials
    engine = create_engine(f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/postgres')
    log.info('Engine has been successfully created')

    # launch the ETL flow
    asteroid_etl(URL, start_date, API_KEY, engine, log)