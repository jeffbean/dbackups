Database Backups
================

Overview
--------
The purpose of this tool is to make backing up databases in bulk easy to do. This service runs database actions based on a config file. No implementation details are needed to backup you common databases.

Currently supports the following Databases for backup:

* PostGreSQL
* MySQL

Installation
------------
Supported Platforms:

* Linux

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

    vim ~/.dbackups/databases.ini

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

## dbackupscron

Currently the one way to run the job of backing up the configured Databases from the config file is to run the
command

    dbackupscron

This will try to dump and upload all enabled databases in the config file. This is meant as a first step towards having
 python schedule its own cron and run as a systemd/init service.


## dbackups_cli

This command that is configured to be in your runtime path will allow for some extensible actions.

To run just an on demand backup of a database in the configuration file run the following:

    dbackups_cli backup example-db

To clone from one database to another you can use the clone command:

    dbackups_cli clone dev-host dev_port dev_user new_db_name example-db

You can also specify a password with this command.

As of today the DB that you want to clone from needs to be in the ```database config``` file!

### Cron Script

Create a similar cron script in `/etc/cron.daily/`

    sudo vim /etc/cron.daily/dbackups.cron
    sudo chmod +x /etc/cron.daily/dbackups.cron

Contents:

    #!/usr/bash
    source ~/.venvs/dbackups/bin/activate && dbackupscron


## Logging


Logging for this application today is done by a config file. this can be found in the `config` directory under the
project root.
This file gets used by all of the binaries distributed by this application.

By default the logs can be found in the program directory:

    ~/.dbackups/logs/

The `dbackupscron` script has its own log allowing easy triage of the cron script

    ~/.dbackups/logs/database_backup_cron.log

## Futures

* Windows support
* Script to enter new configuration entries to the database.ini
* Add cleanup for the dump files. (relying on temp dir cleanup today)
* A simple UI to see uploaded backups, and configure database entries.


## DataBase Troubleshooting

* [MySQL](docs/mysql.md)
* [PostGreSQL](docs/postgres.md)

## Reporting issues

As a start please log issues or they might never be fixed!

As a guild the following is a checklist of things to check and provide in your issue.

* What OS are you running?
* Please attach the [logs](##Logging)
* Can you reproduce?
* What steps did you take to get the issue?


## Documentation Issues

For issues with the documentation or enhancements desired please log an issue with what page the issue is on and all the details about why it is not correct or clarification needed in any part of the docs.