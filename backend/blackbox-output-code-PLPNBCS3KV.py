from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Test data (email + password pairs)
credentials = [
    ("test1@example.com", "Password123"),
    ("rith22080.it@rmkec.ac.in", "12345678Rr@"),
    ("test2@example.com", "MySecret789"),
    ("test3@example.com", "12345678Rr@"),
]

# Chrome options
options = Options()
options.add_argument("--start-maximized")

# Setup ChromeDriver (auto install correct version)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

try:
    for email, password in credentials:
        driver.get("http://localhost:5173/auth")  # your login page

        # Wait for email input
        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.clear()
        email_input.send_keys(email)

        # Wait for password input
        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.clear()
        password_input.send_keys(password)

        # Find and click submit button
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        submit_button.click()

        # Optional: wait for some result (dashboard, alert, URL change etc.)
        time.sleep(3)  # adjust as per app response time

        # Output test info
        print(f"Tested: {email} / {password}")
        print("Current URL:", driver.current_url)
        print("-" * 50)

finally:
    driver.quit()
