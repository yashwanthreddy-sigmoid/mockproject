docker-compose -f kafka.yaml up -d
docker-compose -f elasticsearch.yaml up -d
#docker-compose build # for airflow
docker-compose up -d # for airflow

