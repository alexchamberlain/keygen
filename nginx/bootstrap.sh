#!/bin/bash

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
