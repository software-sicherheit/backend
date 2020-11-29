FROM python:3.9-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /app/
ADD . /app
RUN pip3 install -r /app/django/requirements.txt
EXPOSE 8080
CMD ["/app/start-server.sh"]
