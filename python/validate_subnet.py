################################################################
# Script to validate the config files for the tenant.
# If this script fails, the infrastructure will not be created.
################################################################

import ipaddress
import yaml
import sys
import datetime
import logging
import os

# Logging file
logging.basicConfig(filename="/root/Migration-as-a-Service/logs/infrastructure.log", level=logging.INFO)

# Reads yaml config file provided as parameter
arg = sys.argv
#print(arg)
Yaml_file = os.path.join('/root/Migration-as-a-Service/ansible/config_files/infrastructure', arg[1])

# Check if subnet IP provided is valid in each case.
try:
    with open(Yaml_file,'r') as stream:    
      try:
        yaml_content = yaml.safe_load(stream)
        logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Printing the yaml input file')
        logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + str(yaml_content))
        
        Cloud_Number = []
        for each in yaml_content:
          i = 0
          for item in yaml_content[each]:
            if len(item) > 0:
              i = i + 1
        Cloud_Number.append(i)


        # list of subnet address in the first cloud
        C1S = []
        for x in range(0,Cloud_Number[0],1):
          subnet = str(yaml_content['C1'][x]['subnet_addr'])
          # Check whether the given subnet is valid
          try:
            ip_addr = ipaddress.ip_network(subnet)
            logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Provided subnet in C1: ' + subnet + ' is valid')
          except ValueError:
            logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'Provided subnet in C1: ' + subnet + ' is not valid')
            exit()
          
          C1S.append(subnet)
          if subnet in C1S:
            logging.error(' ' + str(datetime.datetime.now().time()) + 'Multiple subnet in the C1 are same')
            exit()



        C2S = []
        for x in range(0,Cloud_Number[1],1):
          subnet = str(yaml_content['C2'][x]['subnet_addr'])
          # Check whether the given subnets are valid
          try:
            ip_addr = ipaddress.ip_network(subnet)
            logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Provided subnet in C2: ' + subnet + ' is valid')
          except ValueError:
            logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'Provided subnet in C2: ' + subnet + ' is not valid')
            exit()
          
          C2S.append(subnet)
          if subnet in C2S:
            logging.error(' ' + str(datetime.datetime.now()) + 'Duplicate subnets in the C2')
            exit()

        print(C1S)
        print("\n")
        print(C2S)
     
      except yaml.YAMLError as exc:
        #print(exc)
        logging.error(' ' + str(datetime.datetime.time().now()) + ' ' + str(exc))
 
except ValueError:
  logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Unable to open user input yaml file')
  




