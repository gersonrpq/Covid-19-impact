from fastapi import status
import pandas as pd
from app.prod_model import CaseLogisticModel
from app.database import get_data_given_a_country_and_a_case, apply_custom_query
from app.utils import date_validation, data_frame_to_dict

def get_last_day_coditions(request, response):
    
    if request.case not in ["cumulative_confirmed", "cumulative_deceased"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "Please verify your case is either 'cumulative_confirmed' or 'cumulative_deceased'"
        }
    
    data = get_data_given_a_country_and_a_case(request.country, request.case)
    
    if isinstance(data, pd.DataFrame) and not data.empty:
        try:
            model = CaseLogisticModel(request.country, request.case)
            if request.p0_log:
                model.fit(data, printing=False, p0_log=request.p0_log)
            else:
                model.fit(data, printing=False)

            last_day = model.predict_last_day()
            amount_of_case_last_day = model.predict_last_day_amount_case()
        except:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {
                "status": "An error has happened, to ensure the best performance of the mode, please modify e.g. p0_log [100,500,10000000]"
            }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": f"The country {request.country} is not in the data base, please choose another country"
        }

    response.status_code = status.HTTP_200_OK
    return {
        "predicted_last_day": str(last_day),
        f"predicted_amount_of_{request.case}": str(amount_of_case_last_day),
        "country": request.country,
        "status": "Thank for using the API :)"
        }

def get_case_given_a_date(request, response):

    if request.case not in ["cumulative_confirmed", "cumulative_deceased"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "Please verify your case is either 'cumulative_confirmed' or 'cumulative_deceased'"
        }
    
    if date_validation(request.date):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "Please check the date is in the correct format YYYY-MM-DD"
        }

    data = get_data_given_a_country_and_a_case(request.country, request.case)
    
    if isinstance(data, pd.DataFrame) and not data.empty:
        try:
            model = CaseLogisticModel(request.country, request.case)

            
            if request.p0_log:
                model.fit(data, printing=False, p0_log=request.p0_log)
            else:
                model.fit(data, printing=False)

            if pd.to_datetime(request.date) > pd.to_datetime(str(model.day_0)):
                case_given_date = model.predict_given_a_date(request.date)
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                first_day = str(model.day_0)
                return {
                    "status": f"Please use a date greater than {first_day}"
                }
        except:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {
                "status": "An error has happened, to ensure the best performance of the mode, please modify e.g. p0_log [100,500,10000000]"
            }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": f"The country {request.country} is not in the data base, please choose another country"
        }

    response.status_code = status.HTTP_200_OK
    return {
        "date": request.date,
        f"predicted_amount_of_{request.case}": str(case_given_date),
        "country": request.country,
        "status": "Thank for using the API :)"
        }
    
def run_query(request, response):
    result = apply_custom_query(request.query)
    return data_frame_to_dict(result)