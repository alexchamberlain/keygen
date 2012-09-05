#!/bin/bash

if [ ! -f server.crt ];
then
  openssl genrsa -des3 -out server.key.bak 2048
  openssl req -new -key server.key.bak -out server.csr
  openssl rsa -in server.key.bak -out server.key
  openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
fi

rm -rf nginx-1.2.3
if [ ! -f nginx-1.2.3.tar.gz ];
then
  wget http://nginx.org/download/nginx-1.2.3.tar.gz
fi

tar -xzf nginx-1.2.3.tar.gz

pwdir="$(pwd)"

cd nginx-1.2.3
./configure --prefix="$pwdir" --sbin-path=nginx --conf-path=nginx.conf \
            --with-http_ssl_module
make
make install
