from datetime import datetime, timedelta
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
import pandas as pd
import numpy as np

DATE_FORMAT = "%Y-%m-%d"

class CaseLogisticModel:
    
    def __init__(self, country: str, case: str):
        self.country = country
        self.case = case
        self.data_case = pd.DataFrame()
        self.logistic_params_case = {"a": None, "b": None, "c": None}
        self.logistic_params_error_case = {"a_error": None, "b_error": None, "c_error": None}
        self.logistic_model = lambda x,a,b,c: c/(1 + np.exp(-(x-b)/a))
    
    def _clean_process(self, df: pd.DataFrame) -> pd.DataFrame:        
            df = df[["date",self.case]]
            df = df.dropna()
            df = df[df[self.case] > 0]
            return df
        
    def _transforming_dates(self, date_timestamp: pd._libs.tslibs.timestamps.Timestamp) -> int:
        return (datetime.strptime(str(date_timestamp), DATE_FORMAT) - \
                datetime.strptime(str(self.day_0), DATE_FORMAT)).days
    
    def _transforming_integers(self, day: int) -> pd._libs.tslibs.timestamps.Timestamp:
        first_day = datetime.strptime(str(self.day_0), DATE_FORMAT)
        current_day = first_day + timedelta(days=day)
        return datetime.date(current_day)
        
    def fit(self, df: pd.DataFrame,  p0_log: list = [50,20,4000000], 
            printing: bool = True) -> None:
        
        try:
            self.data_case = self._clean_process(df)
        except KeyError:
            raise KeyError("Please verify the study case is well specified")
            
            
        X = self.data_case["date"]
        self.day_0 = X.min()
        X = X.map(self._transforming_dates)        
        y = self.data_case[self.case]
        
        try:
            fit = curve_fit(self.logistic_model,X, y,p0 = p0_log, maxfev=2000)
        except Exception as error:
            print(f"Error {error} has happened, please check the parameters")
            return None
        
        errors = [np.sqrt(fit[1][i][i]) for i in [0,1,2]]
        a,b,c = fit[0]
        
        self.logistic_params_case = {
            key:value for key,value in zip(self.logistic_params_case.keys(),[a,b,c])
        }
        self.logistic_params_error_case = {
            key:value for key, value in zip(self.logistic_params_error_case.keys(),errors)
        }
        self._last_day_amount_of_case = self.logistic_params_case["c"]
        
        if printing:
            print(f"Logistic Model for {self.country} has been fited")
            print(f'''
                    Params and errors:
                    a = {self.logistic_params_case["a"]} +/- {self.logistic_params_error_case["a_error"]}
                    b = {self.logistic_params_case["b"]} +/- {self.logistic_params_error_case["b_error"]}
                    c = {self.logistic_params_case["c"]} +/- {self.logistic_params_error_case["c_error"]}
            ''')
        return None
        
    def predict_last_day(self) -> pd._libs.tslibs.timestamps.Timestamp:
        if self.logistic_params_case["a"] == None:
            print("Fit method must be used to predict last day")
            return None
        a = self.logistic_params_case["a"]
        b = self.logistic_params_case["b"]
        c = self.logistic_params_case["c"]
        last_day = int(fsolve(lambda x : self.logistic_model(x,a,b,c) - int(c),b))
        self.last_day = self._transforming_integers(last_day)
        return self.last_day
    
    def predict_last_day_amount_case(self) -> int:
        return int(self._last_day_amount_of_case)
    
    def _predict(self, day_as_int: int) -> int:
        a = self.logistic_params_case["a"]
        b = self.logistic_params_case["b"]
        c = self.logistic_params_case["c"]
        return int(self.logistic_model(day_as_int, a, b ,c))
        
    def get_behavior_until_a_date(self, date: str) -> pd.DataFrame:
        
        try:
            datetime.strptime(date, DATE_FORMAT)
        except ValueError:
            raise ValueError("Incorrect data format, it should be "+ DATE_FORMAT)
        
        if self.logistic_params_case["a"] == None:
            print("Fit method must be used to predict last day")
            return None
        
        date_as_int = self._transforming_dates(date)
        df = pd.DataFrame()
        df["int_dates"] = np.arange(date_as_int+1)
        df[self.case] = df["int_dates"].map(self._predict)
        df["date"] = df["int_dates"].map(self._transforming_integers)
        return df[["date",self.case]]
         
    def predict_given_a_date(self, date: str) -> int:  
        try:
            datetime.strptime(date, DATE_FORMAT)
        except ValueError:
            raise ValueError("Incorrect data format, it should be "+ DATE_FORMAT)
        
        if self.logistic_params_case["a"] == None:
            print("Fit method must be used to predict last day")
            return None
        
        date_as_int = self._transforming_dates(date)
        return self._predict(date_as_int)
