import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

DIN_EPOST = ''  # The email you setup to send the email using app password
DITT_EPOST_PASSORD = ''  # The app password you generated

def send_epost(filnavn):
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(DIN_EPOST, DITT_EPOST_PASSORD)

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = DIN_EPOST
    msg['To'] = ""
    msg['Subject'] = 'Forsøkt opplåsing'

    # Add message body
    body = 'En opplåsing ble forsøkt. Vedlagt er bilde som ble tatt.'
    msg.attach(MIMEText(body, 'plain'))

    # Attach an image file
    filnavn = filnavn
    attachment = open(filnavn, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= ' + filnavn)
    msg.attach(part)

    # Convert message to string
    text = msg.as_string()

    # Send the email
    smtpserver.sendmail(DIN_EPOST, DIN_EPOST, text)

    # Close the connection
    smtpserver.close()

