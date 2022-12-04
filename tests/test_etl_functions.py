from src.prefect_etl import extract_data_from_api, transform_json_into_dataframe
from src.logger import init_logger
from dotenv import load_dotenv
import pandas as pd
import os


log = init_logger()
# get ENV variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
URL = os.getenv('URL')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')


response_ok = extract_data_from_api.fn(URL, '2022-12-04', API_KEY, log)


def test_extract_data_from_api():
    """Test the behavior of the extract_data_from_api function."""
    response_nok = extract_data_from_api.fn(URL, '2022-12-04', 'not_api_key', log)

    assert response_nok['Message'].startswith('Error in API requests')
    for key in ['links', 'element_count', 'near_earth_objects']:
        assert key in response_ok.keys()
    assert len(response_ok['near_earth_objects']) > 0


def test_transform_json_into_dataframe():
    """Test the shape of the prepared dataframe."""
    transformed_df = transform_json_into_dataframe.fn(response_ok, log)
    cols = transformed_df.columns.tolist()

    assert isinstance(transformed_df, pd.DataFrame)
    for col in ['id', 'name', 'absolute_magnitude_h', 'estimated_diameter_min_km',
                'estimated_diameter_max_km', 'is_potentially_hazardous_asteroid',
                'date']:
        assert col in cols
