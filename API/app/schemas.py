from pydantic import BaseModel
from typing import Union, List, Optional

class LastDayPredictionRequest(BaseModel):
    country: str
    case: str
    p0_log: Optional[List[int]]

    class Config:
        schema_extra = {
            "example":{
                "country":"United States of America",
                "case": "cumulative_confirmed"
            }
        }

class DatePredictionRequest(BaseModel):
    country: str
    case: str
    date: str
    p0_log: Optional[List[int]]

    class Config:
        schema_extra = {
            "example":{
                "country": "Peru",
                "case": "cumulative_deceased",
                "date": "2021-01-01"
            }
        }

class QueryRequest(BaseModel):
    query: str

    class Config:
        schema_extra = {
            "example": {
                "query": 'SELECT date, cumulative_confirmed FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE aggregation_level = 0 AND country_name = "Venezuela"'
            }
        }