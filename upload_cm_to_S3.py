#!/bin/python
# This script will upload a file prvided as a second argument to an object
# store bucket whose name is provided as the first argument.
#
# Usage: python uplaod_cm_to_S3.py <bucket name> <file name> [<cloud alias>]
#
# If used with AWS EC2, the script requires `~/.boto` file to contain your
# AWS keys, as such:
# [Credentials]
# aws_access_key_id = <your access key>
# aws_secret_access_key = <your secret key>
#
# If used with non EC2 cloud, you need to edit provide the access and secret
# keys for `A_KEY` and `S_KEY` variables below (you probably want to use a
# more descriptive alias for the given cloud than `cloud2` as well). In the
# case of using a clustom cloud, it is necessary to provide a the cloud alias
# as an additional argument when invoking the script.
#
# Required libraries: `boto`

import boto
import boto.s3.connection
from boto.s3.key import Key
# import subprocess
import sys
# import os


# Tailored for NeCTAR cloud; adjust as necessary
s3_host = 'swift.rc.nectar.org.au'
s3_port = 8888
s3_conn_path = '/'

try:
    bucket_name = sys.argv[1]
    file_name = sys.argv[2]
    cloud = 'ec2'
    if len(sys.argv) == 4:
        cloud = sys.argv[3]
        if cloud not in ['ec2', 'cloud2', 'aws_acct2']:
            raise
        elif cloud == 'cloud2':
            A_KEY = "your access key for cloud2"
            S_KEY = "your secret key for cloud2"
        elif cloud == 'aws_acct2':
            A_KEY = "your AWS access key for account 2"
            S_KEY = "your AWS secret key for account 2"
except IndexError:
    print "Usage: python upload_cm_to_S3.py <bucket name> <file name> [<cloud alias>]"
    print "Valid values for account are: ec2, cloud2"
    sys.exit(2)


def connect_s3():
    """
    Return a boto S3Connection object.
    """
    if cloud == 'ec2':
        s3c = boto.connect_s3()
    elif cloud == 'aws_acct2':
        s3c = boto.connect_s3(A_KEY, S_KEY)
    else:
        calling_format = boto.s3.connection.OrdinaryCallingFormat()
        s3c = boto.connect_s3(aws_access_key_id=A_KEY,
                              aws_secret_access_key=S_KEY,
                              is_secure=True,
                              host=s3_host,
                              port=s3_port,
                              calling_format=calling_format,
                              path=s3_conn_path)
    return s3c

print "Getting S3 connection"
s3_conn = connect_s3()
print "Got S3 connection for {0} cloud".format(cloud)
print "Getting bucket '%s'" % bucket_name
b = s3_conn.get_bucket(bucket_name)
k = Key(b, file_name)
# m_key = 'revision'
# cmd = "cd /Users/afgane/projects/pprojects/cloudman/cm_app; hg tip | grep changeset | cut -d':' -f2"
# process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# os.waitpid(process.pid, 0)
# rev = process.stdout.read().strip()
# print "Metadata '%s':'%s' on file '%s'" % (m_key, rev, file_name)
# # Metadata must be set before writing the file!
# k.set_metadata(m_key, rev)
print "Saving file '%s' to bucket '%s'" % (file_name, bucket_name)
k.set_contents_from_filename(file_name, reduced_redundancy=True)
# Set ACL on the file and bucket
if cloud == 'ec2':
    k.make_public()
print "DONE updating file '{0}' in bucket '{1}'".format(file_name, bucket_name)
