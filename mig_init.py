############################################################################################################################
# Event Handler  script that watches the main directory: "/root/Migration-as-a-Service/src/northbound/config_files/migration"
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
MIG_LOG = "/root/Migration-as-a-Service/var/logs/migration.log"

# Create log file
logging.basicConfig(filename="/root/Migration-as-a-Service/var/logs/event_handler.log", level=logging.INFO)

# Create event handlers for migration
notifier_mig = inotify.adapters.Inotify()

# Initialize directory to watch for events
notifier_mig.add_watch('/root/Migration-as-a-Service/src/northbound/config_files/migration')

# Error checking flag
continue_flag = True

# Event handling
for event in notifier_mig.event_gen():
    if event is not None:
        # If a new tenant is created
        if 'IN_CREATE' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' created in '{1}'".format(event[3], event[2]))
             tenant = '{0}'.format(event[3], event[2])
             dir_name = tenant.split(".")
             print dir_name[0]
             name = dir_name[0].split("_")
             print name[0] 
             print name[0]+".yml"
             dir_exists=os.path.exists("/root/Migration-as-a-Service/etc/" + str(dir_name[0]))
             if not dir_exists:
                os.system("mkdir /root/Migration-as-a-Service/etc/" + str(dir_name[0]))
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Created ' + str(dir_name[0]) + ' directory for tenant ' + str(tenant))
                        
             yaml_file = "/root/Migration-as-a-Service/src/northbound/config_files/migration/" + str(tenant)

             with open(yaml_file, 'r') as file:
                try:
                    yaml_content = yaml.safe_load(file)
                except OSError:
                    print ("Error loading tenant migration file")

             misc_content = yaml_content["MISC"]
             log_enable = misc_content[0]["LOG_ENABLE"]
 
             # Validate tenant input
             exit_status = os.system("python3 " + str(MIG_INPUT_PYTHON) + "validate_migration.py " + str(name[0]) + ".yml" + " " + str(tenant))
             #print exit_status
             if exit_status!= 0:
                continue_flag = False
                if log_enable:
                   logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to migrate for tenant ' + str(dir_name[0]))

             # Check if destination subnet is present or not
             # Create the subnet if not present
             if continue_flag:
                exit_status = os.system("python3 " + str(MIG_LOGIC_PYTHON) + "migration_check.py " + str(name[0]) + ".yml" + " " + str(name[0]) + "_mig.yml")
                #print exit_status
                if exit_status!= 0:
                   continue_flag = False
                   if log_enable:
                      logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to migrate for tenant ' + str(dir_name[0]))

             # Create the required files for building infrastructure
             if continue_flag:
                exit_status = os.system("python3 " + str(MIG_LOGIC_PYTHON) + "parse_migration.py " + str(tenant))
                #print exit_status
                if exit_status!= 0:
                   continue_flag = False
                   if log_enable:
                      logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to migrate for tenant ' + str(dir_name[0]))
              
             # Create the required files for building infrastructure
             if continue_flag:
                exit_status = os.system("python3 " + str(MIG_LOGIC_PYTHON) + "parse_tenant.py " + str(name[0]) + ".yml")
                #print exit_status
                if exit_status!= 0:
                   continue_flag = False
                   if log_enable:
                      logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to migrate for tenant ' + str(dir_name[0]))

             # Create migration infrastructure on cloud 1
             if continue_flag:
                if os.path.exists("/root/Migration-as-a-Service/etc/" + str(name[0]) + "/" + str(name[0]) + "c1.yml"):
                  exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_infra_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(name[0]) + "' -v >> " + str(MIG_LOG))
                  if exit_status!= 0:
                    continue_flag = False
                    if log_enable:
                       logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create migration infrastructure for tenant ' + str(name[0]))

             # Create migration infrastructure on cloud 2
             if continue_flag:
                if os.path.exists("/root/Migration-as-a-Service/etc/" + str(name[0]) + "/" + str(name[0]) + "c1.yml"):
                  exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_infra_C2.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(name[0]) + "' -v >> " + str(MIG_LOG))
                  if exit_status!= 0:
                    continue_flag = False
                    if log_enable:
                       logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create migration infrastructure for tenant ' + str(name[0]))
             # Create migration infrastructure routes on cloud 1
             if continue_flag:
                if os.path.exists("/root/Migration-as-a-Service/etc/" + str(name[0]) + "/" + str(name[0]) + "c1.yml"):
                  exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "routes_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(name[0]) + "' -v >> " + str(MIG_LOG))
                  if exit_status!= 0:
                    continue_flag = False
                    if log_enable:
                       logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create migration infrastructure routes for tenant ' + str(name[0]))
             # Create migration infrastructure routes on cloud 2
             if continue_flag:
                if os.path.exists("/root/Migration-as-a-Service/etc/" + str(name[0]) + "/" + str(name[0]) + "c1.yml"):
                  exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "routes_C2.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(name[0]) + "' -v >> " + str(MIG_LOG))
                  if exit_status!= 0:
                    continue_flag = False
                    if log_enable:
                       logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create migration infrastructure routes for tenant ' + str(name[0]))
             # Create infrastructure on cloud 1
             if continue_flag:
                if os.path.exists("/root/Migration-as-a-Service/etc/" + str(dir_name[0]) + "/" + str(dir_name[0]) + "C1.yml"):
                  exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "copy_vm_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_LOG))
                  if exit_status!= 0:
                    continue_flag = False
                    if log_enable:
                       logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to migrate for tenant ' + str(dir_name[0]))
             
             # Create infrastructure on cloud 2
             if continue_flag:
                if os.path.exists("/root/Migration-as-a-Service/etc/" + str(dir_name[0]) + "/" + str(dir_name[0]) + "C2.yml"):
                  exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "copy_vm_C2.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_LOG))
                  if exit_status!= 0:
                    continue_flag = False
                    if log_enable:
                       logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to migrate for tenant ' + str(dir_name[0]))
              
             if log_enable:
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'SUCCESSFULLY migrated for tenant ' + str(dir_name[0]))

       
        if 'IN_MODIFY' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' modified in '{1}'".format(event[3], event[2]))
             print "file '{0}' modified".format(event[3], event[2])
             #os.system("your_python_script_here.py")

        if 'IN_DELETE' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' deleted in '{1}'".format(event[3], event[2]))
             print "file '{0}' deleted".format(event[3], event[2])
             #os.system("your_python_script_here.py")
