import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

USERNAME = "landegutt@hotmail.com"
PASSWORD = "mBalkong1i"

msg = MIMEText(
"Hei Ove! Dette er en test fra XPS-vaktmesteren."
)

msg["Subject"] = "Test fra XPS-vaktmesteren"
msg["From"] = USERNAME
msg["To"] = "ove.lande@oceangeoloop.no"

server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()

server.login(USERNAME, PASSWORD)

server.send_message(msg)

server.quit()

print("E-post sendt!")

