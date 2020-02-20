#!/bin/sh
set -x

source ${PWD}/repo_paths.sh

declare -a array_file_enhancepermission=($PATH_IMAGES/redis/redis_run.sh $PATH_IMAGES/worker_celery/celery_entrypoint.sh $PATH_CODE/shared/settings/appglobalconf.py)

for file_permission in "${array_file_enhancepermission[@]}"
	do
		if [ ! -f "$file_permission" ]; then
			echo "$file_permission Does not exists!"
		else
				chmod 777 $file_permission
		fi
	done
