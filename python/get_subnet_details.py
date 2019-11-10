# Writes the IP addresses in the format
# write to a file : /home/ece792/LN_PROJECT/<TENANT-NAME>/<name>.yaml
# dhcp_start: <ip-address> ip[2]
# dhcp_stop: <ip-address> ip[n-1]
# bridge_ip: <ip-address> ip[1]
# bridge_name: <name>
# net_mask: <net-mask>

import ipaddress
import yaml
import os
import sys
import logging

# Create log file
logging.basicConfig(filename="/var/migration/log/setup.log", level=logging.INFO)


def range_of_ips(ip, ns, br, file_name):
    try:
        ip_range = []
        #print(type(ipaddress.IPv4Network(ip)))
        network_mask = ipaddress.IPv4Network(ip)
        mask = (str(network_mask.with_netmask)).split("/")
        #print(mask[1])
        logging.info(' ' + str(datetime.datetime.now().time()) + 'Dumping to YAML file')
        for addr in ipaddress.IPv4Network(ip):
            ip_range.append(str(addr))
        length = len(ip_range)
        
        ip_range_hosts = ""
        for i in range(2,length-1,1):
            ip_range_hosts = str(ip_range_hosts) + str(ip_range[i]) + ","
            
        data = {'dhcp_start':ip_range[2], 'dhcp_end':ip_range[length-2],'bridge_ip': ip_range[1],'net_mask': mask[1],'ip_range_hosts': ip_range_hosts, 'ns_name': ns, 'bridge_name': br}
        logging.info(' ' + str(datetime.datetime.now().time()) + ' Network ' + str(mask[1]) + ' with mask' + mask + ' is created' + ' with DHCP start as ' + str(ip_range[2]) + ' with DHCP end as ' + str(ip_range[length-2]) + 'of bridge having an IP ' + str(ip_range[1]) + 'is created')
        
        file_name1 = file_name 
        with open(file_name1, 'w') as file:
            documents = yaml.dump(data, file, default_flow_style=False)
        return True 
    except ValueError:
        print("Not a valid IP range: " + str(ip_range))
        logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'IP address' + str(ip_range) + 'is not valid')
        return False

arg = sys.argv
tenant_name = arg[1].split('.')[0]
logging.info(' ' + str(datetime.datetime.now().time()) + ' Reading from YAML file ')
Yaml_file = "/root/Migration-as-a-Service/ansible/config_files/" + str(arg[1])
ns_counter = 0
br_counter = 0
with open(Yaml_file,'r') as stream:
    try:
        yaml_content = yaml.safe_load(stream)
        Cloud_Number = []
        for each in yaml_content:
            i = 0
            for item in yaml_content[each]:
                if len(item) > 0:
                    i = i + 1
            Cloud_Number.append(i)

        # For Cloud C1
        for x in range(0,Cloud_Number[0],1):
            subnet = yaml_content['C1'][x]['subnet_addr']
            logging.info(' ' + str(datetime.datetime.now().time()) + ' Reading from YAML file for subnet ' + subnet + ' in cloud C1 ')
            ns_counter += 1
            br_counter += 1
            ns_name = str(tenant_name) + "ns" + str(ns_counter)
            logging.info(' ' + str(datetime.datetime.now().time()) + ' Namespace for tenant in cloud 1' + ns_name + ' is created ')
            bridge_name = str(tenant_name) + "br" + str(br_counter)
            logging.info(' ' + str(datetime.datetime.now().time()) + ' Bridge for tenant in cloud 1' + bridge_name + ' is created ')
            # Creation of File
            path = "/root/Migration-as-a-Service/t1"
            file_name = "/root/Migration-as-a-Service/t1/t1c1.yaml"
            logging.info(' ' + str(datetime.datetime.now().time()) + ' YAML file ' + file_name + ' with details of tenant in cloud 1 is created')
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
                else:
                    print("The file path already exists: "+ str(path))
                    logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + ' File path ' +  str(path) + ' already exists ')
        
            except OSError:
                print ("Creation of the directory %s failed" % path)
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + ' Creation of directory ' +  path + ' failed ')
            ip_range = range_of_ips(subnet, ns_name, bridge_name, file_name)

        # For Cloud C2
        for x in range(0,Cloud_Number[1],1):
            subnet = yaml_content['C2'][x]['subnet_addr']
            logging.info(' ' + str(datetime.datetime.now().time()) + ' Reading from YAML file for subnet ' + subnet + ' in cloud C2 ')
            ns_counter += 1
            br_counter += 1
            ns_name = str(tenant_name) + "ns" + str(ns_counter)
            logging.info(' ' + str(datetime.datetime.now().time()) + ' Namespace for tenant in cloud 1' + ns_name + ' is created ')
            bridge_name = str(tenant_name) + "br" + str(br_counter)
            logging.info(' ' + str(datetime.datetime.now().time()) + ' Bridge for tenant in cloud 2' + bridge_name + ' is created ')
            # Creation of File
            path = "/root/Migration-as-a-Service/t1"
            file_name = "/root/Migration-as-a-Service/t1/t1c2.yaml"
            logging.info(' ' + str(datetime.datetime.now().time()) + ' YAML file ' + file_name + ' with details of tenant in cloud 2 is created')

            try:
                if not os.path.exists(path):
                    os.makedirs(path)
                else:
                    print("The file path already exists: "+ str(path))
                    logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + ' File path ' +  str(path) + ' already exists ')

            except OSError:
                print ("Creation of the directory %s failed" % path)
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + ' Creation of directory ' +  path + ' failed ')

            ip_range = range_of_ips(subnet, ns_name, bridge_name, file_name)

    except yaml.YAMLError as exc:
        print(exc)        
