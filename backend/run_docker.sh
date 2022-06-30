#!/bin/bash
source variables.sh

echo "Run Docker"
sudo docker compose -p $DOCKER_NAME up
