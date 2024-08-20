FROM python:3.11.9

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR ./webpage

CMD python main.py

EXPOSE 8001
