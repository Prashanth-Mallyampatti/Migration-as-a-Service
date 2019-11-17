##############################################
# Script to create mainBR, a connectivity to 
# hypervisor and provider ns pns
##############################################

#!/bin/bash

# Create mainBR network and bridge
sudo cp /root/networks/mainBR.xml /etc/libvirt/qemu/networks/
cd /etc/libvirt/qemu/networks
sudo virsh net-define mainBR.xml
sudo virsh net-start mainBR
sudo virsh net-autostart mainBR

# Create pns
sudo ip netns add pns

# Create veth pair
sudo ip link add p1 type veth peer name br
ip link set dev br up
brctl addif mainBR br

# Attach veth pair to pns
ip link set p1 netns pns
ip netns exec pns ip link set dev p1 up
ip netns exec pns dhclient p1

ip link set dev mainBR up

# Rules to take care
rule_num_1=`sudo iptables -t filter -L FORWARD -nv --line-numbers | grep testBR | grep REJECT | awk -c '{print $1}' | awk 'NR==1'`
rule_num_2=`sudo iptables -t filter -L FORWARD -nv --line-numbers | grep testBR | grep REJECT | awk -c '{print $1}' | awk 'NR==2'`
#echo "$rule_num_1"
#echo "$rule_num_2"

sudo iptables -t filter -D FORWARD $rule_num_1
sudo iptables -t filter -D FORWARD $rule_num_1
