FROM node@sha256:b375b98d1dcd56f5783efdd80a4d6ff5a0d6f3ce7921ec99c17851db6cba2a93

RUN apk update && apk add nginx
ENV SECRET_ALLEY=REDACTED


COPY config/default.conf /etc/nginx/http.d/

WORKDIR /app
COPY ./challenge/package.json ./package.json
RUN npm install
COPY challenge/index.js ./index.js
COPY ./challenge/public ./public
COPY ./challenge/routes ./routes
COPY ./challenge/views ./views
RUN sed -i "s/\$SECRET_ALLEY/$SECRET_ALLEY/g" /etc/nginx/http.d/default.conf
COPY ./config/index.html /var/www/html/index.html
COPY ./config/evil-robot.jpg /var/www/html/evil-robot.jpg



EXPOSE 80
ENV FLAG=HTB{REDACTED}

CMD nginx && node index.js
