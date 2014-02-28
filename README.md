Database Backup Tool
====================

Overview
--------
The purpose of this tool is to make backing up databases in bulk easy to do. This service runs database actions based on a config file. No implementation details are needed to backup you common databases.

Installation
------------
Setup Requirements:

* setuptools_git

Requirements:

* Python 2.7
* Fabric
* requests

Install using `pip`.

    pip install dbackups

or

    pip install git@git.mcp.com:jbean/dbackups.git

Configure
---------
The purpose of this package is that now backing up multiple databases within an infrastructure. You can also specify
where to upload the backups.

Config Files:

* config/backup_database.ini
* config/config_example.ini

### Example

    [example-db]
    # if you want to enable the backup for this database
    enabled = True
    # the type of database
    db_type = postgresql
    # connection paramiters for the DB
    db_host = host_of_database
    db_name = user
    db_user = postgres
    db_pass = password123
    db_port = 5432

    # these are passed into a requests.put method (futures will improve this section)
    upload_url = https://backups.example.com/backups/
    upload_user = backupuser
    upload_pass = password543

Test install
------------
To test that the package installed correctly with the python path setup run the following:

    dbackuptest

This will do nothing but exercise importing the modules going to be used with the cron script. This also verifies
that the entry points are working properly.