import os, time
# import facebook_scraper as fs
from selenium import webdriver
from dotenv import load_dotenv
from FacebookScraper import *
from bs4 import BeautifulSoup

load_dotenv()
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
# prefs = {"profile.default_content_setting_values.notifications": 2}
# options.add_experimental_option("prefs", prefs)
# options.add_argument("--user-data-dir=C:\\Users\\carlw\\AppData\\Local\\Google\\Chrome\\User Data")
# options.add_argument(r"--profile-directory=Default")

driver = webdriver.Chrome(options=options)
driver.maximize_window()
FACEBOOK_USERNAME = os.getenv("FACEBOOK_USERNAME")
FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")


FB_GROUP_URLS = [
    "https://www.facebook.com/groups/3428997217345482/",
    "https://www.facebook.com/groups/1998166543836067/",
    "https://www.facebook.com/groups/855632539122696/",
    "https://www.facebook.com/groups/664699027351008/",
    "https://www.facebook.com/groups/WaterlooSublet/",
]


# https://medium.com/elnkart/facebook-login-using-selenium-python-bd28d2cb3740
def main():
    driver.get("https://www.facebook.com/")
    login(FACEBOOK_USERNAME, FACEBOOK_PASSWORD, driver)
    
    # TODO: Set up proper wait times
    for link in FB_GROUP_URLS:
        change_url(driver, link)
        sort_by_newest(driver)
        scroll_to_bottom(driver, 5)

        feed = driver.find_element(By.CSS_SELECTOR, '''div[role="feed"]''').get_attribute("innerHTML")
        soup = BeautifulSoup(feed, "html.parser")
        texts = soup.findAll(string=True)
        texts = filter_bs4_texts(texts)
        print(texts)
        print("======================")


if __name__ == "__main__":
    main()
    driver.close()
