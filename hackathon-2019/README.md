# Introduction

## Building the Docker Images

1.  When you first start or everytime you make a change, run the buildall.sh.  This will rebuilt any docker images.
2.  Starting the containers docker-compose up
3.  Stopping the containers (cntrl c) docker-compose down
4.  Once the containers are up, you can seed the data:  curl -X POST http://127.0.0.1:5000/api/v1.0/contacts/seed
5.  To see some data you can issue the following commands:
    curl http://127.0.0.1:5000/api/v1.0/contacts
    curl http://127.0.0.1:5000/api/v1.0/groups