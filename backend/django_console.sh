source variables.sh

echo "Run Docker Django bash"

sudo docker compose -p $DOCKER_NAME exec $DJANGO_SERVICE_NAME bash
