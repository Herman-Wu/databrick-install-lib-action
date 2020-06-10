FROM python:slim

RUN mkdir -p /app
COPY ./*.py requirements.txt entrypoint.sh /app/
RUN pip3 install -r /app/requirements.txt

RUN chmod u+x /app/entrypoint.sh
EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]