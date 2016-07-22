# dynpacker-envvars
Assign EC2 instances environment variables from EC2 User Data and S3 buckets

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
