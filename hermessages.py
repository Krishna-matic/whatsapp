from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

# Replace this with the name of the person or group you want to respond to
her_name = "Curious D"
reply_message = "Hi, I saw your message. I'm a python bot replying to you automatically(yeah he made me last night ). 😄"

# Set up Chrome options
options = Options()
options.add_argument('--user-data-dir=./User_Data')  # Keep session saved
options.add_argument('--profile-directory=Default')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')

# Path to your ChromeDriver (adjust if needed)
driver_path = 'chromedriver.exe'

# Open WhatsApp Web
driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.get('https://web.whatsapp.com')

input("Scan the QR code with your phone and press Enter here once done.\n")

print("Waiting for chat to load...")

# Open chat
try:
    chat = driver.find_element(By.XPATH, f'//span[@title="{her_name}"]')
    chat.click()
    print(f"Chat with {her_name} opened. Bot is now listening...")
except ElementClickInterceptedException:
    print(f"Could not click on chat with {her_name}. Another element is blocking it.")
    driver.quit()

# Listening for new messages
last_message = ""

while True:
    try:
        time.sleep(3)
        messages = driver.find_elements(By.CSS_SELECTOR, "div._21Ahp span.selectable-text")
        if messages:
            current_message = messages[-1].text
            if current_message != last_message:
                print(f"New message detected: {current_message}")
                last_message = current_message

                # Locate message box and send message
                try:
                    message_box = driver.find_element(By.XPATH, '//div[@title="Type a message"]')
                    message_box.click()
                    message_box.send_keys(reply_message)

                    send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                    send_button.click()
                    print("Replied successfully.")
                except NoSuchElementException:
                    print("Error: Could not find message box or send button.")
    except KeyboardInterrupt:
        print("Bot stopped by user.")
        break
