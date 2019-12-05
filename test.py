import inotify.adapters
import os
import datetime
import logging
import yaml

with open(yaml_file, 'r') as file:
  try:
     yaml_content = yaml.safe_load(file)
  except OSError:
    print ("Error loading tenant yaml file")

#misc_content = yaml_content["MISC"]
print (yaml_content["MISC"])
