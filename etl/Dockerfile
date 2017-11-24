FROM ubuntu:14.04

MAINTAINER Richard bramley <rabramley@gmail.com>

RUN apt-get update && \
    apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install cron mysql-client gettext ssmtp && \
    apt-get clean

ADD scripts /scripts

# Setup Mailing Config
RUN echo 'root=richard.a.bramley@uhl-tr.nhs.uk' > /etc/ssmtp/ssmtp.conf
RUN echo 'mailhub=smtp.xuhl-tr.nhs.uk' >> /etc/ssmtp/ssmtp.conf

RUN echo 'alias ggppdb="mysql -h $GGPP_DB_HOST -u $GGPP_DB_USER -p$GGPP_DB_PASSWORD $GGPP_DB_NAME"' >> ~/.bashrc

RUN { crontab -l ; echo "* * * * * bash /scripts/etl_redcapToPortal_practiceDetails.sh >> /cron.log 2>&1"; } | crontab -
RUN { crontab -l ; echo "* * * * * bash /scripts/etl_redcapToPortal_userDetails.sh >> /cron.log 2>&1"; } | crontab -
RUN { crontab -l ; echo "* * * * * bash /scripts/etl_civicrmToPortal_recruitStatus.sh >> /cron.log 2>&1"; } | crontab -

CMD ["/scripts/startup.sh"]