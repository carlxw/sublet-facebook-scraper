import time
from selenium.webdriver.common.by import By


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


def add_to_data(names, contents, data, category, group_name):
    """After receiving scrapped data, process it"""
    for i in range(len(names)):
        content_text = ""
        for entry in contents[i]:
            content_text += entry + "\n"
        data_entry = {
            "name": names[i][0],
            "group_name": group_name,
            "source": category,
            "content": content_text
        }
        for key, val in data_entry.items():
            data[key].append(val)
    names.clear()
    contents.clear()
