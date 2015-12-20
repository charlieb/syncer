# Syncer
Downloads only new media file from specific server directory.
Used to download files from, for example, a seedbox. Keeps track of all the
files that have been downloaded so that even if the local copy is removed it
won't be downloaded again.

Add to crontab to regularly sync local to remote.

    */3 * * * * python syncer.py

It will automatically read it's configuration information from a json formatted file named
config in the current directory.

The settings are as follows you can copy and paste the below:


    {
    "notify_smtp_login": "my.name@gmail.com", 
    "notify_from_email": "my.name@gmail.com",
    "notify_smtp_server": "smtp.gmail.com",
    "notify_to_email": "my.name@gmail.com",
    "synced_filename": "already_synced",
    "local_directory": "/srv/media_player",
    "notify_smtp_pword": "mygmailapppassword",
    "notify_smtp_port": 465,
    "remote_host": "my.server.org",
    "remote_directory": "/downloads/complete" 
     }

