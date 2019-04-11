#!/bin/bash
set -x
wget -qO - https://research.cs.wisc.edu/htcondor/ubuntu/HTCondor-Release.gpg.key | sudo apt-key add -
# Do this as root
echo "deb http://research.cs.wisc.edu/htcondor/ubuntu/8.8/xenial xenial contrib" >> /etc/apt/sources.list
echo "deb-src http://research.cs.wisc.edu/htcondor/ubuntu/8.8/xenial xenial contrib" >> /etc/apt/sources.list
apt-get update -y
apt-get install -y htcondor
systemctl start condor
systemctl enable condor