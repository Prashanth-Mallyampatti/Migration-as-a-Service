##############################################################################################################
# Event Handler  script that watches the main directory: "/root/Migration-as-a-Service/ansible/config_files"
# It watches for 3 main events: Create, Modify and Delete
# Based on the event occured, respective ansible playbooks will be invoked
##############################################################################################################

import inotify.adapters
import os
import datetime
import logging

# Create log file
logging.basicConfig(filename="/root/Migration-as-a-Service/logs/event_handler.log", level=logging.INFO)

# Create event handler
notifier = inotify.adapters.Inotify()

# Initialize directory to watch for events
notifier.add_watch('/root/Migration-as-a-Service/ansible/config_files')

# Event handling
for event in notifier.event_gen():
    if event is not None:
        if 'IN_CREATE' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' created in '{1}'".format(event[3], event[2]))
             print "file '{0}' created".format(event[3], event[2])
             os.system("validate.py")
        if 'IN_MODIFY' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' modified in '{1}'".format(event[3], event[2]))
             print "file '{0}' modified".format(event[3], event[2])
             #os.system("your_python_script_here.py")
        if 'IN_DELETE' in event[1]:
             logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "file '{0}' deleted in '{1}'".format(event[3], event[2]))
             print "file '{0}' deleted".format(event[3], event[2])
             #os.system("your_python_script_here.py")
