FROM python:3.7-slim-stretch

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn","main:app","--host", "0.0.0.0","--port","80"]