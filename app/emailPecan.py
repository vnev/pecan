"""
import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("peacanpete@gmail.com", "FreeZone")
 
msg = "Yo waassup!"
server.sendmail("peacanpete@gmail.com", "abirshukla@gmail.com", msg)
server.quit()
"""
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
def sendEmail(subject,emailBody,emailR):
	try:
		fromaddr = "peacanpete@gmail.com"
		toaddr = emailR
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = subject
		 
		body = emailBody
		msg.attach(MIMEText(body, 'plain'))
		 
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "FreeZone")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
	except:
		pass
#sendEmail("Pecan Email Subject","Pecan Email Body")