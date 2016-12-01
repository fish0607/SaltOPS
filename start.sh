#!/bin/bash

mysql_port=3306
mysql_host=127.0.0.1
project_dir="/home/project/SaltOPS"

cd ${project_dir} || exit 0
python manage.py makemigrations && python manage.py migrate

nc -vzz ${mysql_host} ${mysql_port} || /etc/init.d/mysqld start 

python manage.py runserver 0.0.0.0:80

