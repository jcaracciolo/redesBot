#!/bin/bash
echo "Installing dependencies"
sudo apt-get install python python-pip
pip install -r requirements.txt >> /dev/null

echo "Installing Redis"
wget http://download.redis.io/redis-stable.tar.gz >> /dev/null
tar xvzf redis-stable.tar.gz
cd redis-stable
sudo make install >> /dev/null
cd ..

echo "Running Redis"
redis-server --daemonize yes >> /dev/null

echo "Getting py-redis from github since pip one is outdated"
git clone https://github.com/andymccurdy/redis-py.git
cd redis-py/
sudo python setup.py install >> /dev/null
cd ..


sudo rm -rf redis-*
