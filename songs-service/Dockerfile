FROM python:3.9.16-slim

ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# docker build -t songs_services:latest . 
# docker run -d --name songs_services-2 -p 5020:3010 songs_services:latest
# docker exec -it bd1eef19defe mongosh -u root -p root123 --authenticationDatabase admin
# mongosh -u admin -p root --authenticationDatabase admin
