# dynpacker-envvars
Assign EC2 instances environment variables from EC2 User Data and S3 buckets, such as db credentials or 3rd party login credentials.

Install the following way:

```bash
curl https://raw.githubusercontent.com/plecto/dynpacker-envvars/master/script.py > /etc/init.d/s3_settings.sh

chmod 755 /etc/init.d/s3_settings.sh
update-rc.d s3_settings.sh defaults

echo "#!/bin/sh
. /tmp/envvars" > /etc/profile.d/ec2_user_data.sh
chmod +x /etc/profile.d/ec2_user_data.sh
```

Now when logging in, you will have the environment variables from User Data as well as the related S3 bucket in your shell, just like ```heroku run```.

# How it finds credentials

Looks for the following S3 bucket: ```ls-%(CLOUD_ENVIRONMENT)s-credentials``` and for the following subkeys: ```%(CLOUD_DEV_PHASE)s/%(CLOUD_APP)s/``` wgere the variables should be in EC2 User Data as e.g. 'export CLOUD_ENVIRONMENT=dev'.
