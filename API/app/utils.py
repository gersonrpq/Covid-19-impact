from datetime import datetime
import pandas as pd

def date_validation(date: str) -> bool:
    try:
        datetime.strptime(date)
        return True
    except:
        return False

def data_frame_to_dict(df: pd.DataFrame) -> dict:
    return df.to_dict("list")