from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import json

# Test data (email + password pairs)
credentials = [
    ("test1@example.com", "Password123"),
    ("rith22080.it@rmkec.ac.in", "12345678Rr@"),
    ("test2@example.com", "MySecret789"),
    ("test3@example.com", "12345678Rr@"),
]

# Backend API endpoint (Agent A)
BACKEND_URL = "http://127.0.0.1:8000/login-with-email"

# Frontend URL
FRONTEND_URL = "http://localhost:5173"

# Chrome options
options = Options()
options.add_argument("--start-maximized")

# Setup ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

try:
    while True:  # 🔄 run continuously until stopped
        for email, password in credentials:
            # Open frontend login page
            driver.get(FRONTEND_URL)

            # Wait for email input
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            email_input.clear()
            email_input.send_keys(email)

            # Wait for password input
            password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
            password_input.clear()
            password_input.send_keys(password)

            # Find and click submit button
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            submit_button.click()

            # Small wait to simulate UI
            time.sleep(2)

            # Call backend (Agent A) to validate login
            payload = {
                "email": email,
                "password": password,
                "request_type": "login"
            }
            try:
                response = requests.post(BACKEND_URL, json=payload)
                backend_data = response.json()
            except Exception as e:
                backend_data = {"status": "failure", "error": str(e)}

            # Print frontend + backend result
            print("=" * 60)
            print(f"Frontend tested: {email} / {password}")
            print("Backend Response:", json.dumps(backend_data, indent=2))
            print("=" * 60)

            # Small delay between users
            time.sleep(3)

finally:
    driver.quit()
