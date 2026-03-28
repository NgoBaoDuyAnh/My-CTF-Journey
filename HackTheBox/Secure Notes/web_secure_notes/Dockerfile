FROM node:21-bullseye

RUN apt-get update && apt-get install -y gnupg curl supervisor

RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
      gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
       --dearmor

RUN echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/7.0 main" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list

RUN apt-get update && apt-get install -y mongodb-org

COPY challenge/conf/supervisord.conf /etc/supervisord.conf

RUN mkdir -p /app
WORKDIR /app
COPY challenge/src .
RUN npm i

ENV FLAG=HTB{f4k3_fl4g_f0r_t3st1ng}

EXPOSE 3000

RUN mkdir -p /data/db

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]


