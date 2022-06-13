docker-compose down # for airflow, can also use --remove-orphans
docker-compose -f kafka.yaml down
docker-compose -f elasticsearch.yaml down
#docker volume rm $(docker volume list -q)