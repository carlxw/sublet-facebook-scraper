import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.wait import WebDriverWait


def login(username, password, driver, wait_time = 3):
    """Logs into Facebook using .env creds"""
    email_elem = driver.find_element(By.ID, "email") 
    email_elem.send_keys(username)
    password_elem = driver.find_element(By.ID, "pass") 
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.RETURN)
    time.sleep(wait_time)


def change_url(driver, link, delay_time = 3):
    """Change the URL with a timer to suspend the thread"""
    driver.get(link)
    time.sleep(delay_time)


def sort_by_newest(driver, delay_time = 1):
    driver.find_elements(By.XPATH, '''//div[contains(@class, 'xu06os2 x1ok221b')]''')[2].click()
    time.sleep(delay_time)
    driver.find_elements(By.XPATH, '''//div[contains(@class, 'x78zum5 xdt5ytf xz62fqu x16ldp7u')]''')[-2].click()
    time.sleep(delay_time)


def scroll_to_bottom(driver, num_scrolls, delay_time = 3):
    """Scroll to the bottom of the page 'n' times"""
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(delay_time)


def filter_bs4_texts(list: list[str]):
    common_keywords = [
        "Facebook",
        "All reactions:",
        "Comment",
        "Like",
        "View more comments",
        " ",
        " · ",
        "\xa0",
        "Like",
        "See more",
        "Write a public comment…",
        "New listings",
        "sort group feed by",
        "Shared with Public group",
        "Shared with Private group",
        "Message",
        "Reply",
        "Write a comment…",
        "Moderator",
        "Top contributor",
    ]

    # Get a sample output copied and manually process that
    filtered_list = [text for text in list if text not in common_keywords]

    return filtered_list