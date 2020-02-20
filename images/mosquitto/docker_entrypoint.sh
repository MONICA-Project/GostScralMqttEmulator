#!/bin/ash
set -e

if ( [ -z "${MOSQUITTO_USERNAME_VALUE}" ] || [ -z "${MOSQUITTO_PASSWORD_VALUE}" ] ); then
  echo "MOSQUITTO_USERNAME_VALUE or MOSQUITTO_PASSWORD_VALUE not defined"
  exit 1
fi

echo "START MOSQUITTO PWD GENERATION"

# create mosquitto passwordfile
touch /etc/mosquitto/auth/mosquitto_pwd
mosquitto_passwd -b /etc/mosquitto/auth/mosquitto_pwd ${MOSQUITTO_USERNAME_VALUE} ${MOSQUITTO_PASSWORD_VALUE}

echo "CREATION MOSQUITTO PWD DONE!"

exec mosquitto "$@"