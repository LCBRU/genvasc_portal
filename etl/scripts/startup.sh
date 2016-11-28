#!/usr/bin/env bash

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_redcapToPortal_practiceDetails.template > /scripts/etl_redcapToPortal_practiceDetails.sh
chmod 744 /scripts/etl_redcapToPortal_practiceDetails.sh
touch /cron.log

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_portalToCiviCrm_recruitDetails.template > /scripts/etl_portalToCiviCrm_recruitDetails.sh
chmod 744 /scripts/etl_portalToCiviCrm_recruitDetails.sh
touch /cron.log

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_civicrmToPortal_recruitStatus.template > /scripts/etl_civicrmToPortal_recruitStatus.sh
chmod 744 /scripts/etl_civicrmToPortal_recruitStatus.sh
touch /cron.log

# prepend application environment variables to crontab
env | sed 's/^/export /' | cat - /scripts/etl_civicrmToPortal_missingRecruits.template > /scripts/etl_civicrmToPortal_missingRecruits.sh
chmod 744 /scripts/etl_civicrmToPortal_missingRecruits.sh
touch /cron.log

# Run cron deamon
# -m off : sending mail is off 
# tail makes the output to cron.log viewable with the $(docker logs container_id) command
cron && tail -f /cron.log