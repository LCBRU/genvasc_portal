#!/usr/bin/env bash

mysqldump -h civicrmdb -u civiuser -pcivipass civicrm PracticeDetails | sed 's/PracticeDetails/etl_PracticeDetails/g' | mysql -h mysql -u gpuser -pgppass gp
