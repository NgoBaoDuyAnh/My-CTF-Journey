#!/bin/bash
NAME="secure_notes"
docker rm -f web_$NAME
docker build --tag=web_$NAME .
docker run -p 1337:3000 --rm --name=web_$NAME --detach web_$NAME