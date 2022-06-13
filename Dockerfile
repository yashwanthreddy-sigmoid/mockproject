FROM apache/airflow:2.3.1
COPY requirements.txt .
RUN pip install -r requirements.txt







