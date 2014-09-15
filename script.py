import urllib2
import yaml
import re
import boto
import os

CREDENTIALS_DIR = "/credentials"

conn = boto.connect_s3()


user_data_string = urllib2.urlopen("http://169.254.169.254/2012-01-12/user-data/").read()
user_data = dict([s.replace("export ", "").split("=") for s in re.findall("(?:\s)?(export \w+\=[\w_]+)+", user_data_string)])

# Must have validate false, because of strict IAM rules
bucket = conn.get_bucket('ls-%(CLOUD_ENVIRONMENT)s-credentials' % user_data, validate=False)
user_files = list(bucket.list("%(CLOUD_DEV_PHASE)s/%(CLOUD_APP)s/" % user_data))

for f in user_files:
    local_file = f.name.split("/")[-1]
    f.get_contents_to_filename("%s/%s" % (CREDENTIALS_DIR, local_file))

if not os.path.exists(CREDENTIALS_DIR):
    os.makedirs(CREDENTIALS_DIR)

with open("%/settings.yml" % CREDENTIALS_DIR) as settings_file:
    user_data.update(yaml.safe_load(settings_file))

with open("/tmp/envvars", "w") as envvar_file:
    envvar_file.write("\n".join(["export %s=\"%s\"" % itm for itm in user_data.items()]))
