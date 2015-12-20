import subprocess 
import smtplib
import json

class Syncer(object):
    def __init__(self):
        self.synced_filename = ''
        self.remote_host = ''
        self.last_get = []
        self.remote_directory= ''
        self.local_directory = ''

        self.notify_from_email = ''
        self.notify_to_email = ''
        self.notify_smtp_server = ''
        self.notify_smtp_port = 0
        self.notify_smtp_login = ''
        self.notify_smtp_pword = ''

    def read_config(self, config_filename):
        self.read_json(config_filename)
        self.read_synced()

    def read_synced(self):
        self.synced = set([line.strip() for line in open(self.synced_filename)])

    def write_synced(self):
        open(self.synced_filename, 'w').write('\n'.join(self.synced))

    def to_json(self):
        config = self.__dict__.copy()
        del config['last_get']
        del config['synced']
        return json.dumps(config)

    def read_json(self, config_filename):
        config = json.load(open(config_filename))
        for k in config: self.__dict__[k] = config[k] 

    def get_media_filenames(self): 
        media_extensions = ['avi','mkv','mpg','mp4','m4v']
        command = '''ssh %s "find %s -iregex '.*\.\(%s\)'"'''%(self.remote_host, self.remote_directory, '\|'.join(media_extensions))
        process = subprocess.Popen(command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        output,stderr = process.communicate()
        status = process.poll()
        print status
        return output.split('\n') 
        
    def get(self, filename):
        print "Getting " + filename
        process = subprocess.Popen("scp %s:%s %s"%(self.remote_host, filename, self.local_directory),
            shell=True)
        status = process.poll()

    def notify(self):
        if self.last_get:
            content = "\r\n".join(
                    ["From: " + self.notify_from_email,
                    "To: " + self.notify_to_email,
                    "Subject: Download Notification",
                    ""] + list(self.last_get))
            if self.notify_smtp_port == 857:
                mail = smtplib.SMTP(self.notify_smtp_server, self.notify_smtp_port)
                mail.ehlo()
                mail.starttls()
            elif self.notify_smtp_port == 465:
                mail = smtplib.SMTP_SSL(self.notify_smtp_server, self.notify_smtp_port)
                mail.ehlo()
            mail.login(self.notify_smtp_login, self.notify_smtp_pword)
            mail.sendmail(self.notify_from_email, self.notify_to_email, content)
            mail.close()

    def sync(self, update_synced_only = False):
        all_media = set(self.get_media_filenames()) 
        self.last_get = all_media - self.synced
        print self.last_get
        if not update_synced_only:
            for f in self.last_get: self.get(f)
        self.synced = all_media
        self.write_synced()

def test():
    s = Syncer()
    s.read_config('config')
    #s.sync(True)
    s.sync()
    s.notify()

if __name__ == "__main__":
    test()

