# (C) Copyright 2019 Hewlett Packard Enterprise Development LP
FROM python:3.7-alpine
LABEL MAINTAINER="nithya.ganesan@hpe.com"

# Install required system packages
RUN apk add --update curl gcc g++ bash \
    && rm -rf /var/cache/apk/* && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h

ENV PYTHONPATH=/usr/local/lib/python3.6/site-packages

# Create volume mount points for data set, word patterns and output
VOLUME /data
VOLUME /pattern
VOLUME /output

# Build WordStock
ADD wordstock /wordstock
ADD README.md /wordstock

#RUN pip install --prefix /usr/local --no-cache-dir /wordstock
RUN pip install --prefix /usr/local /wordstock \
    && pip install --prefix /usr/local -r /wordstock/test-requirements.txt

ADD bin /wordstock
RUN  chmod 755 /wordstock/*.sh

# Run WordStock
ENTRYPOINT ["/wordstock/entrypoint.sh"]

