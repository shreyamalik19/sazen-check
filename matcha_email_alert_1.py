import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIG ===
SAZEN_PRODUCT_URL = 'https://www.sazentea.com/en/products/c21-matcha'
EMAIL_FROM = ''
EMAIL_TO = ''  # Can be same as sender
EMAIL_SUBJECT = '🍵 Matcha In Stock Alert!'
GMAIL_APP_PASSWORD = ''  # NOT your normal Gmail password

# === CHECK AVAILABILITY ===
def is_matcha_available():
    try:
        response = requests.get(SAZEN_PRODUCT_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.text)
        return "Marukyu Koyamaen" in soup.text
    except Exception as e:
        print("Error checking stock:", e)
        return False

# === SEND EMAIL ===
def send_email():
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = EMAIL_SUBJECT

    body = "Good news! 🍵 Marukyu Koyamaen matcha is in stock on Sazen:\n" + SAZEN_PRODUCT_URL
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
