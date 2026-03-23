docker build --tag=web-dustyalleys . && \
docker run -p 1337:80 --rm --name=web-dustyalleys -it web-dustyalleys
