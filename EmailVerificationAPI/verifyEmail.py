import smtplib
from email.message import EmailMessage
import ssl
import random

hostEmail = "anprdetectionsystem@gmail.com"
hostPass = "xbhbduydivmdohhy"

reciever = "parthprajapati13@hotmail.com"

msg = EmailMessage()
msg['Subject'] = "Your Verification Code from ANPR System"
msg['From'] = hostEmail
msg['To'] = reciever

key = str(random.randint(111111,999999))

msg.add_alternative(f"""\n\n

<div class="c-email">
    <div class="c-email__header">
      <h1 class="c-email__header__title">Your Verification Code</h1>
    </div>
    <div class="c-email__content">
      <p class="c-email__content__text text-title">
        Enter this verification code in field:
      </p>
      <div class="c-email__code">
        <span class="c-email__code__text">"""+key+"""</span>
      </div>
      <p class="c-email__content__text text-italic opacity-30 text-title mb-0">Return to the ANPR System and enter the code.</p>
    </div>
    <div class="c-email__footer"></div>
  </div>

""", subtype="html")


context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(hostEmail, hostPass)
    smtp.sendmail(hostEmail, reciever, msg.as_string())