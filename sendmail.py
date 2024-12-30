import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define the email sender and receiver
sender_email = "bskiran@corp.untd.com"
receiver_email = "logs-routing-hyd@corp.untd.com"
def getpassword():
    password = getpass.getpass("Enter your outlook password: ")
    return password

password = getpassword()

# Create the MIMEMultipart object
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Script mail"

# Create the body of the email
body = "This is a test email sent from Python."
msg.attach(MIMEText(body, 'plain'))

# Set up the SMTP server
try:
    # Connect to the server
    server = smtplib.SMTP('mailrelay01.hyd.int.untd.com', 25)  # Change smtp.example.com to your email provider's SMTP server
    server.starttls()  # Use TLS (Transport Layer Security)
    
    # Login to the server
    server.login(sender_email, password)
    
    # Send the email
    server.send_message(msg)
    
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
#finally:
    # Terminate the SMTP session and close the connection
 #   server.quit()

