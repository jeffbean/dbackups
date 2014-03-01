Database Backups
================

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

Install using `virtualenv` and `pip`.

    mkdir -p ~/.venvs
    virtualenv ~/.venvs/dbackups
    source ~/.venvs/dbackups/bin/activate
    pip install dbackups

Install using `pip`.

    pip install dbackups

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

Running
-------

Currently the one way to run the job of backing up the configured Databases from the config file is to run the
command

    dbackupscron

This will try to dump and upload all enabled databases in the config file. This is meant as a first step towards having
 python schedule its own cron and run as a systemd/init/windows service.

### Cron Script
Create a similar cron script in `/etc/cron.daily/`

    sudo vim /etc/cron.daily/dbackups.cron
    sudo chmod +x /etc/cron.daily/dbackups.cron

Contents:

    #!/usr/bash
    source ~/.venvs/dbackups/bin/activate && dbackupscron


Logging
-------

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

Windows
-------

Some more work is involved in getting this to run in windows. And I have not fully tested the happy path for Windows
as it is `low priority`.

### Binaries

For the postgres server you need to make sure that the Postgresql binaries are in your system path.

To add the directory to your user path run in `Powershell`:

    [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files (x86)\PostgreSQL\<version>\bin", [System.EnvironmentVariableTarget]::User)