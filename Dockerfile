#Start from a python image
FROM python:3.8-slim

ARG BASIC_AUTH_USERNAME_ARG
ARG BASIC_AUTH_PASSWORD_ARG

ENV BASIC_AUTH_USERNAME=$BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWORD=$BASIC_AUTH_PASSWORD_ARG

#Copy files to container
COPY ./requirements.txt /usr/requirements.txt

#Set CWD
WORKDIR /usr

#Install all dependencies on the container
RUN pip3 install -r requirements.txt

#Copy the following folders too
COPY ./src /usr/src
COPY ./models /usr/models
COPY ./data /usr/data

#execute this command
ENTRYPOINT [ "python3" ]

#on this path
CMD [ "src/app/main.py" ]

#Build nao pode ter espaços, é Dockerfile