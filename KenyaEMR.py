import schedule
import time
import nmap, socket
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# in order to use the service, we need adminEmail, hostname, services(array of services)
adminEmail= 'emmanueljan80@gmail.com'
hostname = 'www.mwandishi.co.ke'
services_open = [
    {"port": "80",
     "description":"Notifiy service"
     },
    {"port": "8080",
     "description":"Database service"
     },
    {"port": "8041",
     "description":"Messaging service"
     },
    {"port": "8082",
     "description":"Triage service"
     },
    {"port": "8083",
     "description":"Reports service"
     },
    {"port": "8084",
     "description":"Lab service"
     },
]

services_closed = [
    {"port": "80",
     "description":"Notifiy service"
     },
    {"port": "8080",
     "description":"Database service"
     },
    {"port": "8041",
     "description":"Messaging service"
     },
    {"port": "8082",
     "description":"Triage service"
     },
    {"port": "8083",
     "description":"Reports service"
     },
    {"port": "8084",
     "description":"Lab service"
     },
]

timeInterval = 0.05

port = [sub['port']for sub in services_open]
description = [sub['description']for sub in services_open]

ports_closed = [sub['port']for sub in services_open]
description_of_ports = [sub['description']for sub in services_open]

# This function sends emails to the system admin: it accepts the message content as a parameter
def mail(message):
    mail_content = message
    #The mail addresses and password
    sender_address = 'blinxcorporation@gmail.com'
    sender_pass = 'Katumo@4211'
    receiver_address = adminEmail
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Alert! Service Notification'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    
  
def func():
    response = os.system("ping " + hostname)
        # and then check the response...
    if response == 0:
    
        pingstatus = "Network Active"
        print(pingstatus)
            
    else:
        pingstatus = "Network Error"
        print(pingstatus)
        mail( hostname + ' server is down')

#open ports
    for element in port:
        new_element = int(element)
        ind = port.index(element)
        des = description[ind]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((hostname, new_element))
        if result == 0:
            print(des + ' port is working')
            
        else:
            mail(des + ' not working' + ' in ' + hostname )
            print(des + ' not working' + ' in ' + hostname)
#closed ports
    for port_element in ports_closed:
        new_port_element = int(port_element)
        indx = port.index(port_element)
        desc = description_of_ports[indx]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((hostname, new_port_element))
        if result == 0:
            mail(des + ' working' + ' in ' + hostname + " on port "+ port_element +" (Should be closed)" )
            print(des + ' port is working')
            
        else:
            
            print(des + ' not working' + ' in ' + hostname)
  
schedule.every(timeInterval).minutes.do(func)
  
while True:
    schedule.run_pending()
    time.sleep(timeInterval)