FROM python:3.7-alpine as py3.7-alpine
FROM py3.7-alpine as builder

RUN mkdir /dependancies
WORKDIR /dependancies

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/dependancies" -r /requirements.txt

FROM py3.7-alpine

COPY --from=builder /dependancies /usr/local

WORKDIR /home

COPY server.py boot.sh ./
# RUN chmod +x boot.sh

# EXPOSE 80
# ENTRYPOINT ["sh", "./boot.sh"]
CMD ["python3"]