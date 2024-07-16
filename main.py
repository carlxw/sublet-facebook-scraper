from selenium import webdriver
from FacebookScraper import *
from bs4 import BeautifulSoup
import json
config = json.load(open("config.json"))

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
# options.add_argument(f"--user-data-dir={config["chrome_userdata_dir"]["macos"]}")
options.add_argument(f"--user-data-dir={config["chrome_userdata_dir"]["windows"]}")
options.add_argument("--profile-directory=Default")
options.add_argument("--remote-debugging-pipe")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

FB_GROUP_URLS = config["urls_to_scrape"]

CHART_DATA = {
    "name": [],
    "profile_url": [],
    "group_name": [],
    "source": [],
    "content": [],
}

FEED_CLASS = config["classes"]["feed_class"]
NUMBER_OF_SCROLLS = 5
FOUND_POSTS = set([])


# https://medium.com/elnkart/facebook-login-using-selenium-python-bd28d2cb3740
def main():  
    for url_entry in FB_GROUP_URLS:
        for group_name, link in url_entry.items():
            for url in link.values():
                isBuyAndSell = False if "buy_sell_discussion" in url else True
                change_url(driver, f"{url}?sorting_setting=CHRONOLOGICAL_LISTINGS" if isBuyAndSell else f"{url}?sorting_setting=RECENT_ACTIVITY")
                scroll_to_bottom(driver, 1, scroll_value=2)

                for _ in range(NUMBER_OF_SCROLLS):
                    names, contents, profiles, new_posts = [], [], [], []
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    posts = soup.findAll("div", {"class": FEED_CLASS})

                    # Filter out the bad posts
                    try:
                        for _, post in enumerate(posts):
                            # print(f"Post number {index} ==============")
                            # print(post.find_all(string=True, recursive=False))
                            # print(post.find_all(string=True, recursive=True))
                            if post not in FOUND_POSTS:
                                new_posts.append(post)
                                FOUND_POSTS.add(post)
                    except:
                        print("Posts cannot find_all()")
                    
                    # Add new posts to data
                    for post in new_posts:
                        scrape(post, names, contents, profiles)

                    category = "Buy and Sell" if isBuyAndSell else "Discussion"
                    add_to_data(names, contents, profiles, CHART_DATA, category, group_name)
                    scroll_to_bottom(driver, 1, scroll_value=1.1)

    # Write the data to an Excel Spreadsheet
    generate_excel_file(["Seller Name", "Group", "Category", "Post Contents"], CHART_DATA)


if __name__ == "__main__":
    main()
    driver.close()
