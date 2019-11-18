############################################################################################################################
# Event Handler  script that watches the main directory: "/root/Migration-as-a-Service/ansible/config_files/infrastructure"
# It watches for 3 main events: Create, Modify and Delete
# Based on the event occured, respective ansible playbooks will be invoked
# This script is only used for infrastructure requirements
############################################################################################################################

import inotify.adapters
import os
import datetime
import logging

# Migration directories
MIG_ANSIBLE = "/root/Migration-as-a-Service/ansible/"
MIG_PYTHON = "/root/Migration-as-a-Service/python/"
MIG_INFRA_LOG = "/root/Migration-as-a-Service/logs/infrastructure.log"

# Create log file
logging.basicConfig(filename="/root/Migration-as-a-Service/logs/event_handler.log", level=logging.INFO)

# Create event handlers for infrastructure and migration
notifier_infra = inotify.adapters.Inotify()
#notifier_mig = inotify.adapters.Inotify()

# Initialize directory to watch for events
notifier_infra.add_watch('/root/Migration-as-a-Service/ansible/config_files/infrastructure')
#notifier_mig.add_watch('/root/Migration-as-a-Service/ansible/config_files/migration')

# Error checking flag
continue_flag = True

# Event handling
for event in notifier_infra.event_gen():
    if event is not None:
        # If a new tenant is created
        if 'IN_CREATE' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' created in '{1}'".format(event[3], event[2]))
             tenant = '{0}'.format(event[3], event[2])
             dir_name = tenant.split(".")
             dir_exists=os.path.exists("/root/Migration-as-a-Service/" + str(dir_name[0]))
             if not dir_exists:
                os.system("mkdir /root/Migration-as-a-Service/" + str(dir_name[0]))
                os.system("mkdir /root/Migration-as-a-Service/" + str(dir_name[0]) + "/VM_templates")
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Created ' + str(dir_name[0]) + '/VM_templates directory for tenant ' + str(tenant))
                         
             # Validate tenant input
             exit_status = os.system("python3 " + str(MIG_PYTHON) + "validate_subnet.py " + str(tenant))
             #print exit_status
             if exit_status!= 0:
                continue_flag = False
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')

             # Create the required files for building infrastructure
             if continue_flag:
                exit_status = os.system("python3 " + str(MIG_PYTHON) + "parse_tenant.py " + str(tenant))
                #print exit_status
                if exit_status!= 0:
                   continue_flag = False
                   logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')

#            # Create infrastructure on cloud 1
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_infra_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                #print exit_status
                if exit_status!= 0:
                  continue_flag = False
                  logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')
             

             # Create infrastructure on cloud 2
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_infra_C2.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status!= 0:
                  continue_flag = False
                  logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')

             # Add routes in cloud 1
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "routes_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status!= 0:
                  continue_flag = False
                  logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')

             # Add routes in cloud 2
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "routes_C2.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')

             # Create VM templates on cloud 1
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_vm_C1_templates.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')

             # Create VM templates on cloud 2
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_vm_C2_templates.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  logging.error(' ' + str(datetime.datetime.now().time() + ' ' + 'FAILED to create infrastructure')

             # Create VMs in cloud 1
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_vm_C1.yml -i " + str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')

             # Create VMs in cloud 2
             if continue_flag:
                exit_status = os.system("ansible-playbook " + str(MIG_ANSIBLE) + "create_vm_C2.yml -i " +  str(MIG_ANSIBLE) + "inventory --extra-vars 'tenant_name=" + str(dir_name[0]) + "' -v >> " + str(MIG_INFRA_LOG))
                if exit_status != 0:
                  continue_flag = False
                  logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'FAILED to create infrastructure')
        
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'SUCCESSFULLY completed creating the required infrastructure')
  
             # Watch migration requests once the infrastructure is created
             # Event handling
#             for event in notifier_mig.event_gen():
#                 if event is not None:
                     # If a new tenant is created
#                     if 'IN_CREATE' in event[1]:
#                          logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' created in '{1}'".format(event[3], event[2]))
                          #print "file '{0}' created".format(event[3], event[2])
#                          tenant = '{0}'.format(event[3], event[2])
       
        #if 'IN_MODIFY' in event[1]:
        #     logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' modified in '{1}'".format(event[3], event[2]))
        #     print "file '{0}' modified".format(event[3], event[2])
             #os.system("your_python_script_here.py")
        #if 'IN_DELETE' in event[1]:
        #     logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' deleted in '{1}'".format(event[3], event[2]))
        #     print "file '{0}' deleted".format(event[3], event[2])
             #os.system("your_python_script_here.py")
