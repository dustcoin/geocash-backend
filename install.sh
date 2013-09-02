#!/bin/sh
sudo mkdir -p /var/www/pool
sudo chown -R www-data:www-data /var/www
sudo rm -rf /var/www/pool/static
sudo cp -r ./static /var/www/pool/

sudo cp config/.htpasswd /var/www/pool
sudo cp config/pool /etc/nginx/sites-available
sudo rm /etc/nginx/sites-enabled/*
sudo ln -s /etc/nginx/sites-available/pool /etc/nginx/sites-enabled/pool

sudo service nginx reload
