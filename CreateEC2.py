#!/usr/bin/env python

import time
from fabric.colors import red as _red,green as _green, yellow as _yellow
import boto
import boto.ec2

#Below basic info of Ec2 need to be edited to fit

ec2_key='AKIAJF3N7V57LHOEBFZA'
ec2_secret='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'
ec2_region='us-west-2'
ec2_key_pair='blackline'
ec2_instancetype='t2.micro'
ec2_amis='ami-5189a661'

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
 
    reservation = image[0].run(1, 1, key_name=ec2_key_pair,instance_type=ec2_instancetype)

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
