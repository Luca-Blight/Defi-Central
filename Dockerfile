FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /defi-central

COPY requirements.txt /defi-central/

RUN apt update

RUN pip install -r requirements.txt

COPY . /ecom-db/

ENV PYTHONPATH="/db/app"

CMD python app/account_reports/main.py
