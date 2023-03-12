from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


phone_number = 'Your Num with country code'
contact_names = ["your contacts"]

email_from = 'mail send the email'
email_password = 'password the sending mail  '
email_to = 'mail reciving one'

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get('https://web.whatsapp.com/')
wait = WebDriverWait(driver, 30)

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._2_1wd[data-tab='3']")))

last_profile_pictures = {}
for contact_name in contact_names:
    search_box = driver.find_element(By.CSS_SELECTOR, "div._2_1wd[data-tab='3']")
    search_box.click()
    search_box.send_keys(contact_name)
    search_box.send_keys(Keys.RETURN)

    profile_picture = driver.find_element(By.CSS_SELECTOR, "img._2goTk")
    last_profile_pictures[contact_name] = profile_picture.get_attribute('src')

while True:
    for contact_name in contact_names:
        profile_picture = driver.find_element(By.CSS_SELECTOR, "img._2goTk")
        current_profile_picture = profile_picture.get_attribute('src')

        if current_profile_picture != last_profile_pictures[contact_name]:
            message = f"{contact_name} changed their profile picture!"
            print(message)

            email_subject = "WhatsApp Profile Picture Changed"
            email_body = message
            message = MIMEMultipart()
            message['From'] = email_from
            message['To'] = email_to
            message['Subject'] = email_subject
            message.attach(MIMEText(email_body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_from, email_password)
            server.sendmail(email_from, email_to, message.as_string())
            server.quit()

            response = urllib.request.urlopen(current_profile_picture)
            new_profile_picture = response.read()

            filename = f"{contact_name}.jpg"
            with open(filename, 'wb') as f:
                f.write(new_profile_picture)

            last_profile_pictures[contact_name] = current_profile_picture

    time.sleep(5)
