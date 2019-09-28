Credits http://www.tohoho-web.com/django/tutorial.html
```
# yum install -y wget gcc make
# wget https://www.sqlite.org/2019/sqlite-autoconf-3290000.tar.gz
# tar zxvf ./sqlite-autoconf-3290000.tar.gz
# cd ./sqlite-autoconf-3290000
# ./configure --prefix=/usr/local
# make
# make install
# cd ..
# rm -rf ./sqlite-autoconf-3290000 ./sqlite-autoconf-3290000.tar.gz
# mv /usr/bin/sqlite3 /usr/bin/sqlite3_old
# ln -s /usr/local/bin/sqlite3 /usr/bin/sqlite3
# echo 'export LD_LIBRARY_PATH="/usr/local/lib"' >> ~/.bashrc
# source ~/.bashrc
```