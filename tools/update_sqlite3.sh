#!/bin/sh
# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Sqlite3 update steps credits http://www.tohoho-web.com/django/tutorial.html
current_version=$(sqlite3 --version | cut -d. -f1,2)
  if [ $? == 1 ] ||  [ "$current_version" != "3.29" ]; then
  echo "Install sqlite3"
  cd /home/$@/
  wget https://www.sqlite.org/2019/sqlite-autoconf-3290000.tar.gz
  tar zxvf ./sqlite-autoconf-3290000.tar.gz
  cd ./sqlite-autoconf-3290000
  ./configure --prefix=/home/$@/opt/sqlite
  make
  make install
  cd ..
  rm -rf ./sqlite-autoconf-3290000 ./sqlite-autoconf-3290000.tar.gz
  sudo mv /usr/bin/sqlite3 /usr/bin/sqlite3_old
  echo "export PATH='/home/$@/opt/sqlite/bin:$PATH'" >> /home/$@/.bashrc
  echo "export LD_LIBRARY_PATH='/home/$@/opt/sqlite/lib'"  >> /home/$@/.bashrc
  echo "export LD_RUN_PATH='/home/$@/opt/sqlite/lib'" >> /home/$@/.bashrc
  
  source /home/$@/.bashrc
  new_version=$(sqlite3 --version | cut -d. -f1,2)
  if [ $? == 1] ||  [ "$new_version" != "3.29" ]; then
    echo $new_version
    exit 1
  fi
else
  echo "Do nothing"
fi
