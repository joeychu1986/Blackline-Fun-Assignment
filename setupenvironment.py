#!/usr/bin/env python

import time
from fabric.colors import red as _red,green as _green, yellow as _yellow
import boto
import boto.ec2



ec2_key='asdasdasdasd'
ec2_secret='asdasdasdasdasdasdasdasd'
ec2_region='us-west-2'
ec2_key_pair='test'
ec2_instancetype='t2.micro'
ec2_amis='ami-5189a661'
user_data_script="""#!/bin/bash

ec2_key='asdasdasdasd'
ec2_secret='asdasdasdasdasdasdasdasd'
BUCKET_PUPPET='BLACKLINEpuppet'
sudo apt-get update

sudo apt-get --yes --force-yes install puppet s3cmd
S3CMD="/etc/.s3mcf"
wget --output-document=$S3CMD http://s3-us-west-2.amazonaws.com/$BUCKET_PUPPET/.s3mcfg
sed -i -e "s#__AWS_ACCESS_KEY__#$ec2_key#" \
    -e "s#__AWS_SECRET_KEY__#$ec2_secret#" $S3CMD
chmod 400 $S3CMD
 
until \
    s3cmd -c $S3CMD sync --no-progress --delete-removed \
    s3://$BUCKET_PUPPET/ /etc/puppet/ && \
    sudo /usr/bin/puppet apply /etc/puppet/manifests/BLhello.pp ; \
do sleep 5 ; done
"""


print(_green('--------Fun to create EC2------------'))
Name=raw_input('give ec2 a name:')
Key=raw_input('give it a keyname:')
Tag=raw_input('give it a tag:')



def create_server():
    """
    Creates EC2 Instance
    """
    print(_green("Started..."))
    print(_red("...Creating Funnnnn EC2 instance..."))
    
    conn = boto.ec2.connect_to_region(ec2_region, aws_access_key_id=ec2_key, aws_secret_access_key=ec2_secret)
         
						
    image = conn.get_all_images(ec2_amis)
 
    reservation = image[0].run(1, 1, key_name=ec2_key_pair,instance_type=ec2_instancetype,user_data=user_data_script)

    instance = reservation.instances[0]
    conn.create_tags([instance.id], {Key:Tag})
    conn.create_tags([instance.id], {'Name':Name})
    while instance.state == u'pending':
        print(_yellow("Instance state: %s" % instance.state))
        time.sleep(10)
        instance.update()

    print(_green("Instance state: %s" % instance.state))
    print(_green("Public dns: %s" % instance.public_dns_name))

    return instance.public_dns_name

create_server()
