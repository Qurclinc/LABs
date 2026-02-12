FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod 755 start.sh

ENTRYPOINT [ "./start.sh" ]