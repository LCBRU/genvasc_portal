FROM tutum/nginx
MAINTAINER Richard Bramley <rabramley@gmail.com>

ARG deployment_environment

RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/genvasc_portal.$deployment_environment /etc/nginx/sites-enabled/genvasc_portal
ADD cert /cert
