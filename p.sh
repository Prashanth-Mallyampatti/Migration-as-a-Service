#!/bin/bash

# Rules to take care
rule_num_1=`sudo iptables -t filter -L FORWARD -nv --line-numbers | grep testBR | grep REJECT | awk -c '{print $1}' | awk 'NR==1'`
rule_num_2=`sudo iptables -t filter -L FORWARD -nv --line-numbers | grep testBR | grep REJECT | awk -c '{print $1}' | awk 'NR==2'`
echo "$rule_num_1"
echo "$rule_num_2"

sudo iptables -t filter -D FORWARD $rule_num_1
sudo iptables -t filter -D FORWARD $rule_num_1
