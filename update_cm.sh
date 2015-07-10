#!/bin/bash
# This script is a convenience script for updating Galaxy CloudMan source code
# on S3/Swift. The script deletes the old tarball with CloudMan's source and
# creates a new one. Then, by calling a python script, the newly created file
# is uploaded to S3 in the specified bucket (see below). Both of these script
# should be placed in the CloudMan application root directory and given
# `execute` permissions.
#
# Usage: sh update_cm.sh [cloud]
# The single optinal argument indicates which cloud to use. Supported values
# are provided in the ``upload_cm_to_S3.py`` script. If no value is provided,
# AWS EC2 cloud is assumed.

cm_path=`pwd`
cm_filename="cm.tar.gz"
# cm_bucket_names[1]="cloudman-os"
# cm_bucket_names[2]="cloudman-test"
cm_bucket_names[3]="cloudman-dev"
# cm_bucket_names[4]="cm-5aed808b872c4e503054e592d5bc11c1"

for cm_bucket_name in "${cm_bucket_names[@]}"; do
  REPLY="y" # default to auto update
  if [ "$cm_bucket_name" == "cloudman" ]; then
      REPLY="n"
      read -p "This is going to the 'cloudman' bucket. Are you sure (y/n)?"
  fi
  if [ "$REPLY" == "y" ]; then
      echo ""
      echo "Uploading to bucket '$cm_bucket_name' to cloud '$1' at `date`"
      echo ""

      cd $cm_path
      if [ -f $cm_filename ]; then
          echo "Removing the old CM tarball $cm_filename"
          rm $cm_filename
      fi
      echo "Removing all *.pyc files"
      find . -name "*.pyc" -exec rm -rf {} \;
      echo "Removing all .orig files"
      find . -type f -name "*.orig" | xargs rm;
      echo "Creating a new CM tarball $cm_path/$cm_filename"
      tar -czf $cm_filename --exclude "paster.log" --exclude "ec2autorun.py" \
                            --exclude "update_cm.sh" --exclude "upload_cm_to_S3.py" \
                            --exclude "userData.txt" --exclude "userData.yaml" \
                            --exclude "persistent-volumes-latest.txt" --exclude "snaps.yaml"\
                            --exclude "cm_webapp.pid"\
                            --exclude "cm_boot.py" --exclude ".hgignore" --exclude ".git" *
      python upload_cm_to_S3.py $cm_bucket_name $cm_filename $1
      python upload_cm_to_S3.py $cm_bucket_name cm_boot.py $1
      # python upload_cm_to_S3.py $cm_bucket_name snaps.yaml $1
  fi
  echo ""
done
echo "Update complete at `date`"
