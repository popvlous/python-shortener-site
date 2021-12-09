FROM python:3.9

ENV FLASK_APP run.py

RUN mkdir -p temp
RUN mkdir -p logs
COPY run.py gunicorn-cfg.py requirements.txt config.py .env ./
COPY app app

RUN pip install -r requirements.txt
#python -m pip install --upgrade pip'
EXPOSE 5005
#CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]