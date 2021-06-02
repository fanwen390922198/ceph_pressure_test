#!/bin/bash

cd /root/fio/

tar -zxvf libdshconfig-0.20.9.tar.gz

cd libdshconfig-0.20.9

./configure

make && make install

cd ../

tar -zxvf dsh-0.25.9.tar.gz
cd dsh-0.25.9

./configure --prefix=/usr/local/

make && make install

ln -s /usr/local/lib/libdshconfig.so.1 /lib64/
