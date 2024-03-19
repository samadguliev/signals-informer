FROM python:3.10-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY . .
CMD ["python3", "main.py"]