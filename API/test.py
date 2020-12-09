from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

last_day_json = {
  "country": "United States of America",
  "case": "cumulative_confirmed"
}

prediction_on_date_json = {
  "country": "Peru",
  "case": "cumulative_deceased",
  "date": "2021-01-01"
}

query_json = {
  "query": "SELECT date, cumulative_confirmed FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE aggregation_level = 0 AND country_name = \"Venezuela\""
}

def test_index():
    response = client.get('/', allow_redirects = False)
    assert response.status_code == 307

def test_last_day_prediction():
    response = client.post('/predict/last-day', json = last_day_json)
    assert response.status_code == 200

def test_prediction_given_a_date():
    response = client.post('/predict/given-date', json = prediction_on_date_json)
    assert response.status_code == 200

def test_query_result():
    response = client.post('/query', json = query_json)
    assert response.status_code == 200
