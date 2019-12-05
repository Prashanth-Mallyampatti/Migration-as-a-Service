#!/bin/bash

GUI_DIR="/Users/prashanthm/Migration-as-a-Service/src/northbound/gui"
INFRA_DIR="/Users/prashanthm/Migration-as-a-Service/src/northbound/config_files/infrastructure/"
MIG_DIR="/Users/prashanthm/Migration-as-a-Service/src/northbound/config_files/migration/"
GUI_INFRA_DIR="/Users/prashanthm/Migration-as-a-Service/src/northbound/gui/output/infra/*"
GUI_MIG_DIR="/Users/prashanthm/Migration-as-a-Service/src/northbound/gui/output/migrate/*"

cp $GUI_INFRA_DIR $INFRA_DIR
cp $GUI_MIG_DIR $MIG_DIR
