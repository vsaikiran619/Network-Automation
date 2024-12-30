import smtplib

def send_mail(output_file):
    from_address = 'bskiran@corp.untd.com'
    to_address = 'dsandeep@corp.untd.com'
    subject = 'Test Script'
    body = "Hello"
    subject = 'Test'
    msg = f"subject : {subject} n \n {body} \n \n"

    server = smtplib.SMTP("10.103.32.62", 25)
    server.sendmail(from_address, to_address, msg)
    server.quit()


send_mail("hello")
