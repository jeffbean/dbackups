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
* requests

Install using `pip`.

    pip install git+ssh://git@git.mcp.com/jbean/dbackups.git

Configure
---------
The purpose of this package is that now backing up multiple databases within an infrastructure. You can also specify
where to upload the backups.

Config File:

This uses python ```os.path.expanduser('~')``` and translates to the following:

Windows

    %HOMEPATH%/.dbackups/databases.ini

Linux

    HOME/.dbackups/databases.ini

Add each or your databases as a section of the config file. Defining the connection and upload options.

### Example
    [example-db]
    # if you want to enable the backup for this database
    enabled = True
    # the type of database
    db_type = postgresql
    # connection parameters for the DB
    db_host = host_of_database
    db_name = user
    db_user = postgres
    db_pass = password123
    db_port = 5432

    # these are passed into a requests.put method (futures will improve this section)
    upload_url = https://backups.example.com/backups/
    upload_user = backupuser
    upload_pass = password543


##Logging

Logging for this application today is done by a config file. this can be found in the `config` directory under the
project root.
This file gets used by all of the binaries distributed by this application.

By default the logs can be found in the program directory:


    ~/.dbackups/logs/

The `dbackupscron` script has its own log allowing easy triage of the cron script

    ~/.dbackups/logs/database_backup_cron.log

Test install
------------

To test that the package installed correctly with the python path setup run the following:

    dbackuptest

This will do nothing but exercise importing the modules going to be used with the cron script. This also verifies
that the entry points are working properly.