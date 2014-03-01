Windows
-------

Not really supported as I have seen some random behavior.

Some more work is involved in getting this to run in windows. And I have not fully tested the happy path for Windows
as it is `low priority`.

### Postgres Setup

Install the postgres package for windows from the PostgreSQL [here](http://www.postgresql.org/download/windows/)

For the postgres server you need to make sure that the PostgreSQL binaries are in your system path.

To add the directory to your user path run in `Powershell`:

    [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\PostgreSQL\9.3\bin", [System.EnvironmentVariableTarget]::User)

### MySQL Setup

Install MySQL to get the necessary binaries to perform a `mysqldump` from MySQL [here](http://dev.mysql.com/downloads/)

    [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\MySQL\MySQL Server 5.6\bin", [System.EnvironmentVariableTarget]::User)

#### User Permissions

In order to the required dumps the user specified needs some GRANTED permissions.

The implimnetation has ```mysqldump --single-transaction``` so all you need is select to perform the action.
Future is to have this as a configuration option.

    GRANT SELECT
    ON <tablename>.*
    TO  '<dump_user>'@'<hostname>'
    IDENTIFIED BY '<password>';

