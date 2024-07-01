import os, time
# import facebook_scraper as fs
from selenium import webdriver
from dotenv import load_dotenv
from FacebookScraper import *
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
# options.add_argument("--user-data-dir=C:\\Users\\carlw\\AppData\\Local\\Google\\Chrome\\User Data")
# options.add_argument(r"--profile-directory=Default")

driver = webdriver.Chrome(options=options)
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
    print(1)
    driver.get("https://www.facebook.com/")
    login(FACEBOOK_USERNAME, FACEBOOK_PASSWORD, driver, 5)
    
    # TODO: Set up proper wait times
    for link in FB_GROUP_URLS:
        driver.get(link)
        driver.find_elements(By.XPATH, '''//div[contains(@class, 'xu06os2 x1ok221b')]''')[2].click()
        driver.find_elements(By.XPATH, '''//div[contains(@class, 'x78zum5 xdt5ytf xz62fqu x16ldp7u')]''')[-2].click()
        time.sleep(120)


if __name__ == "__main__":
    main()
    driver.close()
