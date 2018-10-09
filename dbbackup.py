#!/usr/bin/python

###########################################################
#
# This python script is used for mysql database backup
# using mysqldump utility with mysql_config_editor and 
# --login-path implementation for added security.
#  This will work on MySQL 5.6+. 
#
# If using MySQL 5.5 and below, uncomment 
# DB_USER & DB_USER_PASSWORD and fill in user credentials (not ideal).
# 
# This will automatically delete database backup folders 
# in the specified directory that are older than 30 days.
# 
# Author : Joseph 'JB' Bernadas
# Created on : May 11, 2016
# # Python version : 2.7x
#
##########################################################

# Import required python libraries
import os
import time
import datetime
import shutil

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup. 
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databses names one on each line and assignd to DB_NAME variable.

DB_HOST = 'localhost'

### UNCOMMENT THE TWO LINES BELOW IF YOU WOULD LIKE TO USE VISIBLE MYSQL CREDENTIALS, WHICH IS HIGHLY NOT RECOMMENDED
# DB_USER = 'YOUR_MYSQL_USERNAME' 
# DB_USER_PASSWORD = 'YOUR_MYSQL_PASSWORD'

### IT IS BETTER TO USE --login-path TO STORE CREDENTIALS (WILL ONLY WORK WITH MYSQL 5.6 AND ABOVE)
### IF YOU ARE NOT FAMILIAR WITH --login-path PLEASE LOOK INTO 'mysql_config_editor' DOCUMENTATION FOR IMPLEMENTATION
### IN LOCAL MYSQL TO CREATE THE MORE SECURE '--login-path'. YOU HAVE TO CHANGE
### THE BELOW VARIABLE TO THE ONE REGISTERED IN YOUR 'mysql_config_editor
### --login-path= '.
DB_USER_ALIAS = 'PUT_LOGIN_PATH_VALUE_HERE'

# Below is path to text file that holds all the names of target databases
# You may need to escape forward slash characters if using on Windows.
DB_NAME = '/PATH/TO/WHERE/YOU/INSTALLED/db_backup/dbnames.txt'

# Below is path to where the backup folders will be placed, this is 
# also the path that this program will use in deleting older folders. 
# You may need to escape forward slash characters if using on Windows.
# BE VERY CAREFUL WHEN CHANGING THE BELOW PATH, WILL DELETE DIRECTORIES!!!
BACKUP_PATH = '/PATH/TO/WHERE/YOU/INSTALLED/db_backup/database_backups/'
days_backup = 30 # Change this to tell program how many days to keep backups

# Getting current datetime to create separate backup folder like "12012013-071334".
DATETIME = time.strftime('%Y%m%d-%H%M%S')

# Takes the date/time, concatenate with BACKUP_PATH to form the path
TODAYBACKUPPATH = BACKUP_PATH + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
print "creating backup folder"
if not os.path.exists(TODAYBACKUPPATH):
    os.makedirs(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assigned multiple backups in DB_NAME.
print "Checking for database names file."
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print "Databases file found..."
    print "Starting backup of all databases listed in file " + DB_NAME
    time.sleep(3)
else:
    print "Database file not found..."
    print "Starting backup of database " + DB_NAME
    multi = 0
    time.sleep(3)

# Starting actual database backup process.
if multi:
    in_file = open(DB_NAME,"r")
    flength = len(in_file.readlines())
    in_file.close()
    p = 1
    dbfile = open(DB_NAME,"r")

    while p <= flength:
        db = dbfile.readline()  # reading database name from file
        ### Uncomment the below if using Windows
        #db = db[:-1]            # deletes extra line
        
        ### Uncomment the below if using Linux
        db = db[:-2]            # deletes extra line

        ### IF YOU ARE USING THE NON-SECURE VISIBLE CREDENTIALS IN LINE 35, 36 UNCOMMENT THE BELOW LINE.
        #dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"

        ### IF YOU ARE USING THE RECOMMENDED --login-path MYSQL AUTHENTICATION AS PREVIOUSLY SET
        ### IN SHELL BY USING THE 'mysql_config_editor' COMMAND LINE UTILITY, 
        ### COMMENT OUT THE BELOW LINE (ONLY IF YOU ARE NOT USING VISIBLE CREDENTIALS IN LINE 35, 36).
        dumpcmd = "mysqldump --login-path=" + DB_USER_ALIAS  + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
        os.system(dumpcmd)
        p = p + 1
    dbfile.close()
else:
    db = DB_NAME

    ### IF YOU ARE USING THE NON-SECURE VISIBLE CREDENTIALS IN LINE 35, 36 UNCOMMENT THE BELOW LINE.
    #dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"

    ### IF YOU ARE USING THE RECOMMENDED --login-path MYSQL AUTHENTICATION AS PREVIOUSLY SET
    ### IN SHELL BY USING THE 'mysql_config_editor' COMMAND LINE UTILITY, 
    ### COMMENT OUT THE BELOW LINE (ONLY IF YOU ARE NOT USING VISIBLE CREDENTIALS IN LINE 35, 36).
    dumpcmd = "mysqldump --login-path=" + DB_USER_ALIAS + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
    os.system(dumpcmd)

### Reports back to console if backup has finished
print "Backup script completed."
### Waits for a couple seconds
time.sleep(2.50)
### Reports back to console where backkups where placed
print "Your backups has been created in '" + TODAYBACKUPPATH + "' directory."
### Waits a few more minutes
time.sleep(4)
### Reports the next task to be done, delete old backups
print "We will now delete backups older than %s days." % (days_backup)
time.sleep(3)

##### The below code deletes entire directories older than #####
##### n days in the directory specified by BACKUP_PATH.   #####
numdays = 86400*days_backup
now = time.time()
for r,d,f in os.walk(BACKUP_PATH):
    for dir in d:
        timestamp = os.path.getmtime(os.path.join(r,dir))
        if now-numdays > timestamp:
            try:
                print "removing ",os.path.join(r,dir)
                shutil.rmtree(os.path.join(r,dir))
            except Exception,e:
                print e
                pass
            else: 
                print "folder older than %s days deleted." % (days_backup)

raw_input("All tasks completed. Please press enter to close this terminal.")
