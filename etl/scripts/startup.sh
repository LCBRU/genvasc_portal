#!/usr/bin/env bash

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_practice_details.template > /scripts/etl_practice_details.sh
chmod 744 /scripts/etl_practice_details.sh
touch /cron.log

# Run cron deamon
# -m off : sending mail is off 
# tail makes the output to cron.log viewable with the $(docker logs container_id) command
cron && tail -f /cron.log