FROM python:3.9-slim-bullseye
WORKDIR /sim

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3-dev default-libmysqlclient-dev build-essential

COPY sim ./
COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]