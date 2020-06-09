FROM python:3.7.5-slim

COPY entrypoint.sh /entrypoint.sh
COPY installWhlLibrary.py /installWhlLibrary.py
COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

ENTRYPOINT ["/entrypoint.sh"]