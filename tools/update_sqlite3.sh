#!/bin/sh
# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Sqlite3 update steps credits http://www.tohoho-web.com/django/tutorial.html
current_version=$(sqlite3 --version | cut -d. -f2)
if [ $current_version == 7 ]; then
  cd /home/ec2-user/
  wget https://www.sqlite.org/2019/sqlite-autoconf-3290000.tar.gz
  tar zxvf ./sqlite-autoconf-3290000.tar.gz
  cd ./sqlite-autoconf-3290000
  # TODO remove this hardcoded path and make it dynamic
  ./configure --prefix=/home/ec2-user/opt/sqlite
  make
  make install
  cd ..
  rm -rf ./sqlite-autoconf-3290000 ./sqlite-autoconf-3290000.tar.gz
  sudo mv /usr/bin/sqlite3 /usr/bin/sqlite3_old
  # TODO remove these hardcoded path and make it dynamic
  echo 'export PATH=/home/ec2-user/opt/sqlite/bin:$PATH' >> /home/ec2-user/.bashrc
  echo 'export LD_LIBRARY_PATH="/home/ec2-user/opt/sqlite/lib"' >> /home/ec2-user/.bashrc
  echo 'export LD_RUN_PATH="/home/ec2-user/opt/sqlite/lib"' >> /home/ec2-user/.bashrc
else
  echo "Do nothing"
fi
