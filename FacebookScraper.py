from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def login(username, password, driver, wait_time = 2):
    """Logs into Facebook using .env creds"""
    email_elem = driver.find_element(By.ID, "email") 
    email_elem.send_keys(username)
    password_elem = driver.find_element(By.ID, "pass") 
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.RETURN)
    driver.implicitly_wait(wait_time)


def change_url(driver, url):
    """Changes the URL and waits for the page to properly load"""
    driver.get(url)
    page_title = driver.find_element(By.XPATH, '''//a[@href="'+url+'"]''')

    wait = WebDriverWait(driver, timeout=2)
    wait.until(lambda d : page_title.is_displayed())