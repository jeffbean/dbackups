## Linux

### MySQL Setup

Make sure you have `mysqldump` installed

    sudo yum install mysqldump -y

#### User Permissions

In order to the required dumps the user specified needs some GRANTED permissions.

The implimnetation has ```mysqldump --single-transaction``` so all you need is select to perform the action.
Future is to have this as a configuration option.

    GRANT SELECT
    ON <tablename>.*
    TO  '<dump_user>'@'<hostname>'
    IDENTIFIED BY '<password>';