FROM python:3.9

WORKDIR /app

COPY . .

RUN cd ./src

RUN pip install -r requirements.txt

EXPOSE 8000
