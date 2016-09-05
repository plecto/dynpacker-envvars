#!/usr/bin/env python
import urllib2
import yaml
import re
import boto
import os

CREDENTIALS_DIR = "/credentials"

conn = boto.connect_s3()

user_data_string = urllib2.urlopen("http://169.254.169.254/2012-01-12/user-data/").read()
user_data = dict(re.findall("\s?export (\w+)+\=\"?([\w\- \.\,\/]+)+\"?", user_data_string))

# Must have validate false, because of strict IAM rules
bucket = conn.get_bucket('ls-%(CLOUD_ENVIRONMENT)s-credentials' % user_data, validate=False)
user_files = list(bucket.list("%(CLOUD_DEV_PHASE)s/%(CLOUD_APP)s/" % user_data))

if not os.path.exists(CREDENTIALS_DIR):
    os.makedirs(CREDENTIALS_DIR)

for f in user_files:
    if not f.name.endswith("/"):  # Is a file
        local_file = f.name.split("/")[-1]
        f.get_contents_to_filename("%s/%s" % (CREDENTIALS_DIR, local_file))

with open("%s/settings.yml" % CREDENTIALS_DIR) as settings_file:
    user_env_vars = yaml.safe_load(settings_file)
    if user_env_vars:
        user_data.update(user_env_vars)

with open("/tmp/envvars", "w") as envvar_file:
    envvar_file.write("\n".join(["export %s=\"%s\"" % itm for itm in user_data.items()]))
