from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from app.schemas import LastDayPredictionRequest, DatePredictionRequest, QueryRequest
from app.task import get_last_day_coditions, get_case_given_a_date, run_query

app = FastAPI()
app.title = "Platzi Test API"

@app.get("/")
async def index():
    return RedirectResponse("https://platzi.com")

@app.post("/predict/last-day")
async def predict_last_day_status(request: LastDayPredictionRequest, response: Response):
    return get_last_day_coditions(request, response)

@app.post("/predict/given-date")
async def predict_case_given_a_date(request: DatePredictionRequest,response: Response):
    return get_case_given_a_date(request, response)

@app.post("/query")
async def carry_out_a_query(request: QueryRequest, response: Response):
    return run_query(request, response)