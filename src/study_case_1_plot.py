from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

plt.style.use("seaborn-darkgrid")
FONT_SIZE = 22
plt.rcParams.update({'font.size': FONT_SIZE})
LOCATION_OF_STUDY = "CO"
DATE_FORMAT = "%Y-%m-%d"
MAIN_KEYWORD = "covid-19"
SECONDARY_KEYWORD = os.environ.get("SECONDARY_KEYWORD","cursos online")

def get_interest_overtime_given_a_keyword_and_location(keyword: str, 
                        location: str = LOCATION_OF_STUDY) -> pd.DataFrame:
    try:
        trend_request = TrendReq()
        trend_request.build_payload(kw_list=[keyword],geo=location)
        return trend_request.interest_over_time()
    except Exception as error:
        print(f"Error {error} has happened, please check the arguments")

def get_slice_of_df_given_years(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    return df.loc[(df.index > start) & (df.index < end)]


covid_19_interest = get_interest_overtime_given_a_keyword_and_location(MAIN_KEYWORD)
secondary_interest = get_interest_overtime_given_a_keyword_and_location(SECONDARY_KEYWORD)

covid_19_interest_2020 = get_slice_of_df_given_years(covid_19_interest,"2020", "2021")
secondary_interest_2020 = get_slice_of_df_given_years(secondary_interest,"2020", "2021")

covid_19_interest_2020 = covid_19_interest_2020[covid_19_interest_2020.index != "2020-08-02"]
secondary_interest_2020 = secondary_interest_2020[secondary_interest_2020.index != "2020-08-02"]

fig, (ax1, ax2) = plt.subplots(1,2)
fig.set_figheight(10)
fig.set_figwidth(15)
ax1.plot(covid_19_interest_2020.index, covid_19_interest_2020[MAIN_KEYWORD])
ax1.set_xlabel("date", fontsize = FONT_SIZE)
ax1.set_ylabel("keyword: '" + MAIN_KEYWORD + "' interest", fontsize = FONT_SIZE)
fig.autofmt_xdate()
sns.regplot(x = covid_19_interest_2020[MAIN_KEYWORD], 
            y = secondary_interest_2020[SECONDARY_KEYWORD], 
            ax = ax2)
ax2.set_xlabel("keyword: '" + MAIN_KEYWORD + "' interest", fontsize = FONT_SIZE)
ax2.set_ylabel("keyword: '" + SECONDARY_KEYWORD + "' interest", fontsize = FONT_SIZE)
plt.tight_layout()
plt.savefig("impact.png",dpi=120)
plt.close()


