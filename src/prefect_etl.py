from prefect.task_runners import SequentialTaskRunner
from prefect import flow, task
import sqlalchemy.engine
import pandas as pd
import requests


@task(retries=2, retry_delay_seconds=60, log_prints=True)
def extract_data_from_api(url: str, start_date: str, api_key: str, log) -> dict:
    """
    Extract daily asteroid near to the Earth from Nasa API using given url, start_date & api key.

    Args:
        url: the API url
        start_date: the start date of the weekly extraction - format 'YYYY-MM-dd
        api_key: the api key that you can download free at Nasa API website
        log: a configured logger

    Returns
        a dictionnary containing the data or an error message
    """
    response = requests.get(url=url, params={'start_date': start_date, 'api_key': api_key})

    if response.status_code != 200:
        log.critical('The API response is not 200 --> the data are not retrieved')
        return {'Message': f'Error in API requests - get a {response.status_code} status code.'}
    else:
        log.info('Request was a sucess --> returns the data')
        return response.json()


@task(log_prints=True)
def transform_json_into_dataframe(json_data: dict, log) -> pd.DataFrame:
    """
    Transform previous download data from the Nasa API into a dataframe.

    Args:
        json_data: previous downloaded data
        log: a logger

    Returns:
        daily_asteroids_data_df: prepared data that we want to store
    """
    daily_asteroids_data_df = pd.DataFrame()

    for day_in_week in json_data['near_earth_objects'].keys():
        for asteroid_data in json_data['near_earth_objects'][day_in_week]:
            try:
                asteroid_df = pd.DataFrame({
                    'id': [asteroid_data['id']], 'name': [asteroid_data['name']],
                    'absolute_magnitude_h': [asteroid_data['absolute_magnitude_h']],
                    'estimated_diameter_min_km': [asteroid_data['estimated_diameter']['kilometers']['estimated_diameter_min']],
                    'estimated_diameter_max_km': [asteroid_data['estimated_diameter']['kilometers']['estimated_diameter_max']],
                    'is_potentially_hazardous_asteroid': [asteroid_data['is_potentially_hazardous_asteroid']],
                    'date': [day_in_week]
                })
                daily_asteroids_data_df = pd.concat([daily_asteroids_data_df, asteroid_df])

            except Exception as e:
                log.error(f'Get this error for day {day_in_week} & asteroid {asteroid_data} \n Error message: {e}')

        log.info(f'Processing worked for {day_in_week}')
    log.info(f'Final shape: {daily_asteroids_data_df.shape}')
    return daily_asteroids_data_df


@task(log_prints=True)
def load_to_gcp(dataframe: pd.DataFrame, engine: sqlalchemy.engine.Engine, log):
    """Saves a dataframe into the given database using the engine."""
    try:
        dataframe.to_sql('asteroid', engine, if_exists='append', index=False)
        log.info('Data successfully loaded')
    except Exception as e:
        log.critical(f'There is an error in the loading process --> {e}')


@flow(name='ELT Nasa asteroid flow',
      description='The ETL process to get asteroid data from the Nasa API and store \
      these informations into a PostgreSQL database',
      task_runner=SequentialTaskRunner(), log_prints=True
      )
def asteroid_etl(url: str, start_date: str, api_key: str, engine, log):
    """
    ETL process to get asteroid data from the Nasa API and store these informations into a PostgreSQL database.

    Args:
        url: api's url
        start_date: start date of the wanted week
        api_key: Nasa api's key
        log: a logger

    Returns:
        Boolean: True if the process works correctly, False otherwise
    """
    try:
        data = extract_data_from_api(url, start_date, api_key, log)
        daily_asteroids_data_df = transform_json_into_dataframe(data, log)
        load_to_gcp(daily_asteroids_data_df, engine, log)
        log.info('ETL finished its process corretly')
        return True
    except Exception as e:
        log.error(e)
        return False
"Feature (v1 of the ETL using prefect): create the ETL process using prefect package & add corresponding tests & deployment files"