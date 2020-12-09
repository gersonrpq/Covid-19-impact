from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import os

prod_credentials = {
    'auth_provider_x509_cert_url': os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    'auth_uri': os.getenv("AUTH_URI"),
    'client_email': os.getenv("CLIENT_EMAIL"),
    'client_id':  os.getenv('CLIENT_ID'),
    'client_x509_cert_url': os.getenv('CLIENT_X509_CERT_URL'),
    'private_key': os.getenv('PRIVATE_KEY').replace("\\n","\n"),
    'private_key_id': os.getenv('PRIVATE_KEY_ID'),
    'project_id': os.getenv('PROJECT_ID'),
    'token_uri': os.getenv('TOKEN_URI'),
    'type': os.getenv('TYPE')
} 

credentials = service_account.Credentials.from_service_account_info(prod_credentials)

client = client = bigquery.Client(credentials=credentials, 
                        project=prod_credentials["project_id"])

def get_data_given_a_country_and_a_case(country: str, case: str):
    query = f'''
    SELECT date, {case}
    FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
    WHERE country_name = "{country}" AND aggregation_level = 0
    '''

    try:
        samples = client.query(query).result().to_dataframe()
    except Exception as error:
        return {
            "status":f"Error {error} has happened please check the arguments"
            }
    samples.dropna(inplace=True)
    return samples

def apply_custom_query(query: str) -> pd.DataFrame:
    try:
        result = client.query(query).result().to_dataframe()
        return result.dropna()
    except Exception as error:
        result = pd.DataFrame()
        result["error"] = [f"error {error} has happened, please check your query"]
        return result

