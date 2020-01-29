import json
import smtplib
import email.utils
from email.mime.text import MIMEText
from fabric import Connection

user="centos@"
path_to_properties="/home/bgants/projects/disk-alerts/properties.json"
path_to_key="/home/bgants/projects/disk-alerts/keys/"
sender = 'someone@somewhere.com'
receivers = ['you-1@somewhere.com','you-2@somewhere.com']
subject = "Disk Space Alert"

def sendAlert(nodeName, deviceThreshold, percentAvail):
    verbiage = ("""
                The node %s had its disk size threshold of %s%% execeeded, it was found to be %s
                """
        % (nodeName, deviceThreshold, percentAvail))
    msg=MIMEText(verbiage)
    msg['Subject'] = subject

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, msg.as_string())         
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")
     

with open(path_to_properties) as f:
  data = json.load(f)

for x in data:
  for y in data[x]:
    print("Checking disk space for node %s" % y["name"])
    for z in y["devices"]:
        result = Connection(user+y["name"], connect_kwargs={"key_filename": path_to_key+y["name"]+'.pem'}).run('df -kh '+ z["device"],  hide=True)
        out_line = result.stdout.splitlines()
        out_space = out_line[1].split()
        if(int(out_space[4].replace('%','')) > z['deviceThreshold']):
            sendAlert(y["name"],z['deviceThreshold'],out_space[4])
