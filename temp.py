import inotify.adapters
import os
import datetime
import logging
import yaml
import sys

arg = sys.argv
yaml_file = arg[1]
with open(yaml_file, 'r') as file:
  try:
    yaml_content = yaml.safe_load(file)
  except OSError:
    print ("Error loading tenant yaml file")

misc_content = yaml_content["MISC"]
log_enable = misc_content[0]["LOG_ENABLE"]
print(log_enable)
