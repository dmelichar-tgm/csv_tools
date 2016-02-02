#!/usr/bin/env bash

sudo apt-get update

sudo apt-get -y --force-yes install git-core python3 python3-pip python-mock python-nose python-coverage pylint

sudo sh -c 'echo "APT::Cache-Limit "100000000";" >> /etc/apt/apt.conf.d/70debconf'

wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update

sudo apt-get -y --force-yes install jenkins

sudo apt-get -y --force-yes install apache2
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod vhost_alias
sudo a2dissite default
sudo echo '
    ServerAdmin webmaster@localhost
    #ServerName ci.company.com
    #ServerAlias ci
    ProxyRequests Off
        #Order deny,allow
        #Allow from all
    ProxyPreserveHost on
    ProxyPass / http://localhost:8080/
' >> /etc/apache2/sites-available/jenkins.conf

sudo a2ensite jenkins.conf

sudo sh -c 'echo "ServerName JenkinsCI" >> /etc/apache2/conf.d/jenkins.conf' && sudo service apache2 restart
sudo apache2ctl restart

CSV_TOOLS_PATH='/home/vagrant/CSV-Tools'
if [ -d "$CSV_TOOLS_PATH" ]; then 
    cd "$CSV_TOOLS_PATH"
    sudo python3 setup.py install
    sudo pip3 install -r requirements.txt
else 
    echo 'The required shared folder to the project root has not been established. Check in the Vagrantfile if the right path is set'
fi