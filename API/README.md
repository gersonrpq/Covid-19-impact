# API

This folder is intended for the documentation of the API that uses the model developed in [_/notebooks/study_case_2.ipynb_](https://github.com/gersonrpq/Covid-19-impact/blob/main/notebooks/study_case_2.ipynb)

## Endpoints

### _/_

#### **METHOD:**

GET

#### **Succesful response:**

Redirects to https://platzi.com

###  _/predict/last-day_

Predicts approximately tha last day of the infection given a case and a country.

* Avaliable cases
  - cumulative_confirmed
  - cumulative_deceased

#### **METHOD:**

POST

#### **Data Params example**


```
json = {
  "country": "United States of America",
  "case": "cumulative_confirmed"
}
```

### _/predict/given-date_

Predicts approximately the amount of the case given a country and a date.

* Avaliable cases
  - cumulative_confirmed
  - cumulative_deceased

#### **METHOD:**

POST

#### **Data Params example**
```
json = {
  "country": "Peru",
  "case": "cumulative_deceased",
  "date": "2021-01-01"
}
```

### _/query_

Sends a query to database.

#### **METHOD:**

POST

#### **Data Params example**
```
json = {
  "query": "SELECT date, cumulative_confirmed FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE aggregation_level = 0 AND country_name = \"Venezuela\""
}
```

### _/docs_

An environment where the API can be tested directly on the browser.

#### **METHOD:**

GET
