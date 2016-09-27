FROM ubuntu:14.04

MAINTAINER Richard bramley <rabramley@gmail.com>

RUN apt-get update && \
    apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install cron mysql-client && \
    apt-get clean

RUN echo "* * * * * mysqldump -h civicrmdb -u civiuser -pcivipass civicrm PracticeDetails | mysql -h mysql -u gpuser -pgppass gp" | crontab -

CMD cron -f