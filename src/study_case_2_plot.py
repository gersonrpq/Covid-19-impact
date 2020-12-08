from model import CaseLogisticModel
from google.oauth2 import service_account
from google.cloud import bigquery
from matplotlib import pyplot as plt
import os

plt.style.use("seaborn-darkgrid")
FONT_SIZE = 22
plt.rcParams.update({'font.size': FONT_SIZE})
# Caso de estudio y pais de estudio 
COUNTRY_OF_STUDY = os.environ.get("COUNTRY_OF_STUDY","Colombia")
CASE_OF_STUDY = os.environ.get("CASE_OF_STUDY","cumulative_confirmed")


# Credencials para bigquery
credentials_dict = {
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

credentials = service_account.Credentials.from_service_account_info(credentials_dict)

# Cliene bigquery
client = client = bigquery.Client(credentials=credentials, 
                        project=credentials_dict["project_id"])

# query string para hacer la prediccion en funcion de los datos
query = f'''
SELECT date, {CASE_OF_STUDY}
FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
WHERE country_name = "{COUNTRY_OF_STUDY}" AND aggregation_level = 0
'''

try:
    samples = client.query(query).result().to_dataframe()
except Exception as error:
    raise ValueError(f"Error {error} has happened please check the arguments")

# Eliminando datos Nan 
samples = samples[samples["cumulative_confirmed"] != 0].dropna()

# Instanciando modelo
model = CaseLogisticModel(COUNTRY_OF_STUDY, CASE_OF_STUDY)

# Ajustando modelo
model.fit(samples, printing = False)

# Variables de interes
predicted_last_day_of_case = model.predict_last_day()
amount_of_case_at_last_day = model.predict_last_day_amount_case()

with open("text.txt","w") as outfile:
    outfile.write(f"Model predicted last day: {predicted_last_day_of_case} \n")
    outfile.write(f"Model predicted amount of afected at last day: {amount_of_case_at_last_day} \n")
    outfile.write("\n")
    outfile.write("Model params and erros:")
    a = int(model.logistic_params_case["a"])
    a_error = round(model.logistic_params_error_case["a_error"],4)
    b = int(model.logistic_params_case["b"])
    b_error = round(model.logistic_params_error_case["b_error"],4)
    c = int(model.logistic_params_case["c"])
    c_error = round(model.logistic_params_error_case["c_error"],4)
    outfile.write(f"a = {a} +/- {a_error} \n")
    outfile.write(f"b = {b} +/- {b_error} \n")
    outfile.write(f"c = {c} +/- {c_error} \n")
    outfile.write("\n")

model_prediction_day = "2021-01-01"
model_samples = model.get_behavior_until_a_date(model_prediction_day)
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)
ax.plot(samples["date"], 
        samples["cumulative_confirmed"],
        c = "salmon", label =  f"{CASE_OF_STUDY} cases", marker = '.')
ax.plot(model_samples["date"],
       model_samples["cumulative_confirmed"], 
        c = "orangered",label = f"{CASE_OF_STUDY} prediction")
fig.autofmt_xdate()
ax.set_xlabel("Date")
ax.set_ylabel(f"{CASE_OF_STUDY} cases")
fig.legend()
plt.tight_layout()
plt.savefig("prediction.png",dpi=120)
plt.close()