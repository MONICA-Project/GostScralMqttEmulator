#!/bin/sh
set -x

CONFIGURE_SCRIPT=$(realpath ${PWD}/configure_docker_environment.sh)
COMPLETE_STARTUP_LINUX=$(realpath ${PWD}/complete_startup_oslinux.sh)

eval $CONFIGURE_SCRIPT prod
eval $COMPLETE_STARTUP_LINUX