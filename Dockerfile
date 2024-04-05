FROM python:3.9

WORKDIR /app

COPY . .

RUN cd ./src

RUN mkdir logs

RUN pip install -r requirements.txt

EXPOSE 8000
