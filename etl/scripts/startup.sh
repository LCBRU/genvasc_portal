#!/usr/bin/env bash

sleep 3m

envsubst < /scripts/sql/etl_civicrm_recruitStatus.template > /scripts/sql/etl_civicrm_recruitStatus.sql

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_redcapToPortal_practiceDetails.template > /scripts/etl_redcapToPortal_practiceDetails.sh
chmod 744 /scripts/etl_redcapToPortal_practiceDetails.sh
touch /cron.log

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_civicrmToPortal_recruitStatus.template > /scripts/etl_civicrmToPortal_recruitStatus.sh
chmod 744 /scripts/etl_civicrmToPortal_recruitStatus.sh
touch /cron.log

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_redcapToPortal_userDetails.template > /scripts/etl_redcapToPortal_userDetails.sh
chmod 744 /scripts/etl_redcapToPortal_userDetails.sh
touch /cron.log

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_redcapToPortal_delegationLog.template > /scripts/etl_redcapToPortal_delegationLog.sh
chmod 744 /scripts/etl_redcapToPortal_delegationLog.sh
touch /cron.log

# Run cron deamon
# -m off : sending mail is off 
# tail makes the output to cron.log viewable with the $(docker logs container_id) command
cron && tail -f /cron.log