FROM httpd:2.4

RUN apt-get update && \
    apt-get install -y bash coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/storage/files/uploads/public && \
    mkdir -p /opt/storage/files/uploads/private && \
    mkdir -p /opt/vault/confidential && \
    mkdir -p /opt/share/bin && \
    mkdir -p /opt/share/config

COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY index.html /usr/local/apache2/htdocs/index.html
COPY generate.html /usr/local/apache2/htdocs/generate.html
COPY validator.sh /opt/share/bin/validator.sh
COPY salt-keys.txt /opt/share/config/salt-keys.txt
COPY sample1.pdf /opt/storage/files/uploads/public/8f3a9b2c-4d1e-4a5f-9c8b-7e6d5a4b3c2d.pdf
COPY sample2.zip /opt/storage/files/uploads/public/1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d.zip
COPY secret.txt /opt/vault/confidential/secret.txt

RUN chmod +x /opt/share/bin/validator.sh && \
    chmod 644 /opt/vault/confidential/secret.txt && \
    echo "production_salt_key_$RANDOM$RANDOM" > /opt/share/config/salt-keys.txt && \
    echo "testing_salt_key_$RANDOM$RANDOM" >> /opt/share/config/salt-keys.txt && \                                                       
    echo "demo_salt_key_$RANDOM$RANDOM" >> /opt/share/config/salt-keys.txt \
    chown -R www-data:www-data /opt/storage && \
    ln -s /opt /usr/local/apache2/htdocs/opt

EXPOSE 80
