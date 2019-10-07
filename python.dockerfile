FROM python:3.7-buster


RUN pip3 install isodate==0.6.0 \
                numpy==1.16.3 \
                pandas==0.24.2 \
                pyxlsb==1.0.5 \
                rdflib==4.2.2

COPY ./scripts /scripts
RUN mkdir /data
VOLUME /data

CMD ["python3"]


