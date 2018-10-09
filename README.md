#db_backup
<h1>DB_BACKUP</h1>

This is a Python 2.7 script that creates a copy of your MySQL databases. 

How it works is it executes the 'mysqldump' utility which in turn creates the .sql file copies of the database names listed in dbnames.txt.

1.) So, first step, we need to go into mysql and type in our credentials

    <pre>mysql -u root -p</pre>

2.) Manually copy all the databases we want to backup into the dbnames.txt file using a text editor, one database name per line (don't copy the mysql system names).

3.) The dbbackup.py script recommends using the --login-path for accessing the MySQL server, so you need to set up 

<pre>mysql_config_editor</pre>

4.) To use <pre>mysql_config_editor</pre> utility to register a --login-path alias into mysql (the purpose of this is so that we don't write the username and password into the dbbackup.py, instead we will be using an alias thats encrypted and known to mysql). So we need to type the below commands into command prompt:

<pre>shell>mysql_config_editor set --login-path=YOUR_CHOSEN_ALIAS_HERE --host=localhost --user=MYSQL_USER_NAME_HERE --password</pre>

5.) Once that is done, open dbbackup.py in a text editor and make sure the variable 'DB_USER_ALIAS' is set to our --login-path:

<pre>DB_USER_ALIAS = 'YOUR_CHOSEN_ALIAS_HERE'</pre>

6.) Still in dbbackup.py, we need to make sure the 'DB_NAME' and 'BACKUP_PATH' variable are pointed to the correct paths:

In Windows it should look like this:
<pre>
DB_NAME = 'v:\\vHost\\db_backup\\dbnames.txt'
BACKUP_PATH = 'v:\\vHost\\db_backup\\database_backups\\'
</pre>

In Linux it should look like this:
<pre>
DB_NAME = '/PATH/TO/WHERE/YOU/INSTALLED/db_backup/dbnames.txt'
BACKUP_PATH = '/PATH/TO/WHERE/YOU/INSTALLED/db_backup/'
</pre>

<hr>

<h3>To use this in Ubuntu Linux.</h3>

1.) Open cron job file

<pre>sudo crontab -e</pre>

2.) Choose the editor

3.) Type the below at the bottom of cron file if you want the backup to happen every 6 AM system time.

<pre>* 6 * * * sudo python /PATH/TO/WHERE/YOU/INSTALLED/db_backup/dbbackup.py</pre>

4.) Set the files and folder permissions to 660 so that root and you can access the files and folders.

<hr>

<h3>To use this in Windows</h3>

1.) Open up Windows Task Scheduler to let Windows run our python script once a day.

2.) Type in Start search bar Task Scheduler.

3.) On the rightmost column click Create Basic Task.

4.) Fill out the name of our task. Then provide description of what it does. Click next.

5.) Choose when you want the task to start. Click next.

6.) Choose time and frequency of task. Leave blank the Synchronize across time zones. Click next.

7.) We are now on the Action menu, choose the radio button to Start a program. Click next.

8.) We will be in the Start a Program menu. We now put the path to our python script, which is:

C:\PATH\TO\WHERE\YOU\INSTALLED\db_backup\dbnames.txt





  
