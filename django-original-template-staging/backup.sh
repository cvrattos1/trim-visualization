#!/bin/bash
# Deployment script for template-app
# Purpose: copies the correct docker-compose, requirements.txt, and .env file to
#          the correct locations and then runs the docker commands and initialization
#          scripts.
# Command: ./deploy.sh [environment]] -[destroy] -[restart]  > deployment.log
# Options: environment = development, staging, or production
#          -destroy = delete all containers and images before Building
#          -restart = restart docker-machine before building Containers
#          > deployment.log = write starttup messages to a file 'deployment.log'
#

echo "-----------------------------------------------------"
echo "Starting backup:  $(date)"
echo "-----------------------------------------------------"
SECONDS=0

# Create DB Backup
echo "-----------------------------------------------------"
echo "Export database"
echo "-----------------------------------------------------"
docker exec -i -t db_server bash ./scripts/export_mysql_backup.sh


minutes=$((SECONDS/60))
seconds=$((SECONDS%60))

echo "-----------------------------------------------------"
echo "Ending backup:  $(date)"
echo "Backup took $minutes minutes and $seconds seconds."
echo "-----------------------------------------------------"
