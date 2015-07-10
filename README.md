## CloudMan update scripts

Use the scripts provided here to update the source code for the [CloudMan
application][1] in the desired bucket/container. This is intended to be used
during application development or if you would like to customize CloudMan.

To use, simply place both scripts in the CloudMan source root directory,
give the scritps execute permissions, set the desired target bucket name in
`update_cm.sh` script and run with `sh update_cm.sh`.

Before the first run, you may need to define you `~/.boto` file with your
AWS credentials or provide appropriate credentials in `upload_cm_to_S3.py`
file (along with specifying the desired cloud alias). See the individual
scripts for more details.

[1]: https://github.com/galaxyproject/cloudman
