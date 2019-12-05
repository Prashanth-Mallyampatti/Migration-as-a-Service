############################################################################################################################
# Event Handler  script that watches the main directory: "/root/Migration-as-a-Service/src/northbound/config_files/infrastructure"
# It watches for 3 main events: Create, Modify and Delete
# Based on the event occured, respective ansible playbooks will be invoked
# This script is only used for infrastructure requirements
############################################################################################################################

import inotify.adapters
import os
import datetime
import logging
import yaml

# Migration directories
MIG_ANSIBLE = "/root/Migration-as-a-Service/src/southbound/ansible/"
MIG_INPUT_PYTHON = "/root/Migration-as-a-Service/src/northbound/validation_scripts/"
MIG_LOGIC_PYTHON = "/root/Migration-as-a-Service/src/logiclayer/parser_scripts/"
MIG_INFRA_LOG = "/root/Migration-as-a-Service/var/logs/infrastructure.log"

dir_exists = os.path.exists(MIG_INFRA_LOG)
if not dir_exists:
  os.system("touch " + str(MIG_INFRA_LOG))

dir_exists = os.path.exists("/root/Migration-as-a-Service/var/logs/event_handler.log")
if not dir_exists:
  os.system("touch /root/Migration-as-a-Service/var/logs/event_handler.log")

# Create log file
logging.basicConfig(filename="/root/Migration-as-a-Service/var/logs/event_handler.log", level=logging.INFO)

# Create event handlers for infrastructure and migration
notifier_infra = inotify.adapters.Inotify()

# Initialize directory to watch for events
notifier_infra.add_watch('/root/Migration-as-a-Service/src/northbound/config_files/infrastructure')

# Error checking flag
continue_flag = True

# Event handling
for event in notifier_infra.event_gen():
    if event is not None:
        # If a new tenant is created
        ############# Create a new infrastructure ##############

        if 'IN_CREATE' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' created in '{1}'".format(event[3], event[2]))
             tenant = '{0}'.format(event[3], event[2])
             dir_name = tenant.split(".")
             print (dir_name[0])
             dir_exists=os.path.exists("/root/Migration-as-a-Service/etc/" + str(dir_name[0]))
             if not dir_exists:
                os.system("mkdir /root/Migration-as-a-Service/etc/" + str(dir_name[0]))
                os.system("mkdir /root/Migration-as-a-Service/etc/" + str(dir_name[0]) + "/VM_templates")
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Created ' + str(dir_name[0]) + '/VM_templates directory for tenant ' + str(tenant))
             print (str(tenant))
             # Check if logging feature is enabled or not
             yaml_file = "/root/Migration-as-a-Service/src/northbound/config_files/infrastructure/" + str(tenant)

             with open(yaml_file, 'r') as file:
                try:
                    yaml_content = yaml.safe_load(file)
                except OSError:
                    print ("Error loading tenant yaml file")

             misc_content = yaml_content["MISC"] 
             log_enable = misc_content[0]["LOG_ENABLE"]
             print (log_enable)
             # Validate tenant input
             exit_status = os.system("python3 " + str(MIG_INPUT_PYTHON) + "validate_subnet.py " + str(tenant))
             #print exit_status
             if exit_status!= 0:
                continue_flag = False
                if log_enable:
                    logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))

             # Create the required files for building infrastructure
             if continue_flag:
                exit_status = os.system("python3 " + str(MIG_LOGIC_PYTHON) + "parse_tenant.py " + str(tenant))
                #print exit_status
                if exit_status!= 0:
                   continue_flag = False
                   if log_enable:
                      logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))

#            # Create infrastructure on cloud 1
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_infra_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                #print exit_status
                if exit_status!= 0:
                  continue_flag = False
                  if log_enable:
                     logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))
             

             # Create infrastructure on cloud 2
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_infra_C2.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status!= 0:
                  continue_flag = False
                  if log_enable:
                     logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))

             # Add routes in cloud 1
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "routes_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status!= 0:
                  continue_flag = False
                  if log_enable:
                     logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))

             # Add routes in cloud 2
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "routes_C2.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  if log_enable:
                     logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant' + str(dir_name[0]))

             # Create VM templates on cloud 1
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_vm_C1_templates.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  if log_enable:
                     logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))

             # Create VM templates on cloud 2
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_vm_C2_templates.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  if log_enable:
                     logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant' + str(dir_name[0]))

             # Create VMs in cloud 1
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_vm_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  if log_enable:
                     logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))

             # Create VMs in cloud 2
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_vm_C2.yml -i " +  str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  if log_enable:
                      logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))

             if continue_flag:
                if log_enable:
                    logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'SUCCESSFULLY completed creating the required infrastructure for tenant ' + str(dir_name[0]))
             else:
                if log_enable:
                    logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure for tenant ' + str(dir_name[0]))
  
      
        ############# Modify infrastructure ##############
 
        if 'IN_MODIFY' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' modified in '{1}'".format(event[3], event[2]))
             print "file '{0}' modified".format(event[3], event[2])
             #os.system("your_python_script_here.py")


        ################# Delete infrastructure(not supported) #####################

        if 'IN_DELETE' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' deleted in '{1}'".format(event[3], event[2]))
             print "file '{0}' deleted".format(event[3], event[2])
             #os.system("your_python_script_here.py")
