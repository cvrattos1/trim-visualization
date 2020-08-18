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

while getopts "e:m:r:d:i:c:" option; do
  case $option in
    e ) environment=$OPTARG
    ;;
    m ) machine_name=$OPTARG
    ;;
    r ) restart=$OPTARG
    ;;
    d ) destroy=$OPTARG
    ;;
    i ) import=$OPTARG
    ;;
    c ) check=$OPTARG
    ;;
  esac
done

if [[ "$destroy" == "destroy" ]]
then
  destroy=1
else
  destroy=0
fi

if [[ "$restart" == "restart" ]]
then
  restart=1
else
  restart=0
fi

if [[ "$import" == "import" ]]
then
  import=1
else
  import=0
fi

if [[ "$check" == "check" ]]
then
  check=1
else
  check=0
fi

if [[ "$test" ]]
then
    test_input=$test
    test=1
else
    test=0
fi

echo "-----------------------------------------------------"
echo "Inputs from command"
echo "-----------------------------------------------------"
echo "environment: $environment"
echo "machine_name: $machine_name"
echo "restart: $restart"
echo "destroy: $destroy"
echo "test: $test"
echo "import: $import"

has_docker_machine=$(which docker-machine)

# Run tests
echo "-----------------------------------------------------"
echo "Run tests"
echo "-----------------------------------------------------"

if [ -z "$has_docker_machine" ]
then
  docker_machine=0
else
  docker_machine=1
fi

echo "has docker machine: $has_docker_machine"
echo "docker machine flag: $docker_machine"
echo "docker machine condition: (($docker_machine != 0 ))"


# check arguments
if [ -z "$environment" ]
then
  echo "No environment was passed. Specify development, staging, or production."
  exit 1 # terminate and indicate error
fi

if [ -z "$machine_name" ]
then
  echo "No machine_name was passed, using default as docker-machine."
  machine_name=default
fi

# Is docker machine running
echo "Check if Docker-machine is running..."
if (($docker_machine == 1 ))
then
  docker_running=$(docker-machine status $machine_name)
  echo "-----------------------------------------------------"
  echo "Docker-machine status for $machine_name: $docker_running"
  echo "-----------------------------------------------------"


  if [[ "$docker_running" == *"Running"* ]]
  then
    echo "-----------------------------------------------------"
    echo "Docker-machine is running...set environment variables."
    echo "-----------------------------------------------------"
    eval "$(docker-machine env $machine_name)"
  fi

  if [[ "$docker_running" == *"Stopped"* ]]
  then
    echo "-----------------------------------------------------"
    echo "Docker-machine is stopped...start machine."
    echo "-----------------------------------------------------"
    $(docker-machine start $machine_name)
    echo "-----------------------------------------------------"
    echo "Set environment variables."
    echo "-----------------------------------------------------"
    eval "$(docker-machine env $machine_name)"
  fi
  if [[ "$docker_running" == *"Saved"* ]]
    then
      echo "-----------------------------------------------------"
      echo "Docker-machine is Saved...start machine."
      echo "-----------------------------------------------------"
      $(docker-machine start $machine_name)
      echo "-----------------------------------------------------"
      echo "Set environment variables."
      echo "-----------------------------------------------------"
      eval "$(docker-machine env $machine_name)"
  fi

  echo "-----------------------------------------------------"
  echo "Checking if destroy command was passed"
  echo "-----------------------------------------------------"
  if (($destroy != 0 ))
    then
      echo "-------------------------------------------------------------------"
      echo "Destroy was passed -- clearing out existing containers and images."
      echo "-------------------------------------------------------------------"
      eval $(docker stop $(docker ps -a -q)  && docker rm $(docker ps -a -q) --force && docker rmi $(docker images -a -q) --force)
  else
    echo "-----------------------------------------------------"
    echo "Destroy was not passed -- using containers."
    echo "-----------------------------------------------------"
  fi

  echo "-----------------------------------------------------"
  echo "Checking if restart command was passed"
  echo "-----------------------------------------------------"
  if (($restart != 0 ))
    then
      echo "-------------------------------------------------------------------"
      echo "Restart was passed -- restart docker machine."
      echo "-------------------------------------------------------------------"
      eval $(docker-machine restart $machine_name)
  else
    echo "-----------------------------------------------------"
    echo "Restart was not passed -- using existing docker machine."
    echo "-----------------------------------------------------"
  fi
else
  echo "-----------------------------------------------------"
  echo "Docker machine not installed - no restart is possible"
  echo "-----------------------------------------------------"
fi

# Set ENV variables
# Copy assets from deployment directories to execute directory
if [ ! -d "$environment" ]; then
  echo "/$environment directory does not exist."
  exit 1 # terminate and indicate error
fi

if [ ! -f "$environment/docker-compose.yml" ]; then
  echo "$environment directory or docker-compose.yml do not exist."
  exit 1 # terminate and indicate error
fi

echo "-----------------------------------------------------"
echo "copying nginx files for development"
echo "-----------------------------------------------------"

echo "Loading $environment scripts"
cp -fr ./$environment/nginx/sites-enabled ./nginx/
cp -fr ./$environment/nginx/nginx.conf ./nginx/nginx.conf
cp -fr ./$environment/nginx/Dockerfile ./nginx/Dockerfile
echo "-----------------------------------------------------"

echo "-----------------------------------------------------"
echo "Loading $environment scripts"
cp -fr ./$environment/.env ./.env
cp -fr ./$environment/docker-compose.yml ./docker-compose.yml
cp -fr ./$environment/requirements.txt ./requirements.txt
echo "-----------------------------------------------------"

if [ ! -f "./docker-compose.yml" ]; then
  echo "docker-compose.yml does not exist. Was it copied?"
  exit 1 # terminate and indicate error
fi


# exit 1 # terminate and indicate error


if [ -f "./docker-compose.yml" ]; then

  # Remove static files
  if [ -f "./WebApp/template_app/static/template_app/template_app/" ]; then
    echo "-----------------------------------------------------"
    echo "Remove static files before building"
    echo "-----------------------------------------------------"
    rm -rf WebApp/template_app/static/template_app/template_app/
  fi

  # Build Containers
  echo "-----------------------------------------------------"
  echo "Building containers"
  echo "-----------------------------------------------------"
  docker-compose build

  # Start Containers
  echo "-----------------------------------------------------"
  echo "Starting containers"
  echo "-----------------------------------------------------"
  docker-compose up -d --remove-orphans

  echo "-----------------------------------------------------"
  echo "Pause to allow things to come up"
  echo "-----------------------------------------------------"
  sleep 15

  # Initialize Application
  echo "-----------------------------------------------------"
  echo "Initialize application"
  echo "-----------------------------------------------------"
  docker exec -tt web_server bash WebApp/scripts/init_app.sh

  if (($import != 0 ))
    then
    # Create DB Structure
    echo "-----------------------------------------------------"
    echo "Create database"
    echo "-----------------------------------------------------"
    docker exec -tt db_server bash ./scripts/import_mysql_backup.sh
    else
      echo "-----------------------------------------------------"
      echo "No database created or updated because 'I' flag not passed"
      echo "-----------------------------------------------------"
  fi

  docker_ip=$(docker-machine ip $machine_name)

  echo "-----------------------------------------------------"
  echo "Containers are running on $docker_ip"
  echo "-----------------------------------------------------"
fi

if (($check != 0 ))
  then
  echo "-----------------------------------------------------"
  echo "Dependency checks"
  echo "Only works with versioned packages check"
  echo "-----------------------------------------------------"
  echo "Dependency Security check"
  echo "-----------------------------------------------------"
  docker exec -it web_server safety check --json -r requirements.txt
  echo "-----------------------------------------------------"
  echo "Version check"
  echo "-----------------------------------------------------"
  docker exec -it web_server pip-check -a -H

  # Any security issues should be mitagated or a description of why they are
  #     not relevant should be included below.
  echo "-----------------------------------------------------"
  echo "Django Security check"
  echo "-----------------------------------------------------"
  docker exec -it web_server python manage.py check --deploy

  echo "-----------------------------------------------------"
  echo "Bandit Security check"
  echo "-----------------------------------------------------"
  docker exec -it web_server bandit -r WebApp/

  echo "-----------------------------------------------------"
  echo "License check"
  echo "-----------------------------------------------------"
  docker exec -it web_server pip-licenses --with-system --with-urls --order=license
else
  echo "-----------------------------------------------------"
  echo "No security or version checks were done"
  echo "-----------------------------------------------------"

fi


minutes=$((SECONDS/60))
seconds=$((SECONDS%60))

echo "-----------------------------------------------------"
echo "Ending build:  $(date)"
echo "Build took $minutes minutes and $seconds seconds."
echo "-----------------------------------------------------"
