FROM ubuntu:12.04
MAINTAINER Richard Bramley (richard.bramley@gmail.co.uk)

# install dependencies
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		apache2 \
	&& rm -r /var/lib/apt/lists/*

# Default command	
CMD ["apachectl", "-D", "FOREGROUND"]

# Ports
EXPOSE 80