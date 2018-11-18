FROM python:3.7

COPY dev-requirements.txt /var/botarang/dev-requirements.txt
RUN pip install -r /var/botarang/dev-requirements.txt
WORKDIR /var/botarang
ENV PYTHONPATH "${PYTHONPATH}:/var/botarang/botarang"
