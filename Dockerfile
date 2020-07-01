FROM python:3.7.5-slim

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh
COPY installWhlLibrary.py /installWhlLibrary.py

ENTRYPOINT ["/entrypoint.sh"]