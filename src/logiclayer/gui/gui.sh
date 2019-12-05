#!/bin/bash

INFRA_DIR="/root/Migration-as-a-Service/src/northbound/config_files/infrastructure/"
MIG_DIR="/root/Migration-as-a-Service/src/northbound/config_files/migration/"
GUI_INFRA_DIR="/root/Migration-as-a-Service/src/northbound/gui/output/infra/*"
GUI_MIG_DIR="/root/Migration-as-a-Service/src/northbound/gui/output/migrate/*"

cp $GUI_INFRA_DIR $INFRA_DIR
cp $GUI_MIG_DIR $MIG_DIR

cd /root/Migration-as-a-Service/src/northbound/config_files
git add .
git commit -m "Adding tenant files"
git push origin master
