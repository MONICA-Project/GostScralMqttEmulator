#!/bin/sh

# NOTE: this command must be called with 

set -x

if [ -z "$1" ]; then
  echo "Missing Environment Choice. It must be local, prod or dev"
else
  echo "Environment Variable passed: $1"
  CONF="$1"
fi

source ${PWD}/repo_paths.sh

FOLDER_DOCKER_LOGS="$PATH_CODE"/logs
FILE_SETTINGS="$PATH_CODE_SETTINGS"/settings.py

if [ -f "$PATH_REPO"/docker-compose.override.yml ]; then rm "$PATH_REPO"/docker-compose.override.yml; fi
if [ -f "$PATH_REPO"/.env ]; then rm "$PATH_REPO"/.env; fi
if [ -f "$FILE_SETTINGS" ]; then rm "$FILE_SETTINGS"; fi
if [ ! -d "$FOLDER_DOCKER_LOGS" ]; then mkdir -p "$FOLDER_DOCKER_LOGS"; fi

ln -s "$PATH_REPO"/.env."$CONF" "$PATH_REPO"/.env
ln -s "$FILE_SETTINGS"."$CONF" "$FILE_SETTINGS"
if [ -f "$PATH_REPO"/docker-compose.override.yml."$CONF" ]; then ln -s "$PATH_REPO"/docker-compose.override.yml."$CONF" "$PATH_REPO"/docker-compose.override.yml; fi


