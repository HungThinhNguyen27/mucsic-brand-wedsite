FROM python:3.9.16-slim

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat

ENV APP=/app

# Change the workdir.
WORKDIR $APP

# Install the requirements
COPY requirements.txt $APP

RUN pip3 install -r requirements.txt

# Copy the rest of the files
COPY . $APP

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker build -t my_django_app:latest .  
# docker run -d --name djangoserver -p 8080:8000 my_django_app:latest
# docker network connect my_network djangoserver
# docker network connect my_network songs-service-mongodb-1
# docker network connect my_network songs-service-flask_app-1
# docker network connect my_network pictures-services-server-2
# docker inspect network my_network 
