import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# === CONFIG ===
SAZEN_PRODUCT_URL = 'https://www.sazentea.com/en/products/c21-matcha'
EMAIL_FROM = os.environ['EMAIL_FROM']
EMAIL_TO = os.environ['EMAIL_TO']  # Can be same as sender
EMAIL_SUBJECT = '🍵 Matcha In Stock Alert!'
GMAIL_APP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']  # NOT your normal Gmail password

# === CHECK AVAILABILITY ===
def is_matcha_available():
    try:
        response = requests.get(SAZEN_PRODUCT_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup.text)
        content = str(soup.find(id="content"))
        #print ("content: " , content)
        #print("is matcha available? " , "Marukyu Koyamaen" in str(content))
        #print("is matcha available? " , "Kanbayashi Shunsho" in str(content))
        return ("Marukyu Koyamaen" in content) or ("Yamamasa Koyamaen" in content) or ("Kanbayashi Shunsho" in content)
    except Exception as e:
        print("Error checking stock:", e)
        return False

# === SEND EMAIL ===
def send_email():
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = EMAIL_SUBJECT
    print ("email from: ", EMAIL_FROM)
    print ("email to: " , EMAIL_TO)

    body = "Good news! 🍵 Marukyu Koyamaen/Yamamasa Koyamaen/Kanbayashi Shunsho in stock on Sazen:\n" + SAZEN_PRODUCT_URL
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

# === MAIN LOGIC ===
if __name__ == "__main__":
    if is_matcha_available():
        send_email()
