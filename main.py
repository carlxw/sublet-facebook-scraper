from selenium import webdriver
from time import gmtime, strftime
from FacebookScraper import *
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--user-data-dir=C:\\Users\\carlw\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--profile-directory=Default")
options.add_argument("--remote-debugging-pipe")
driver = webdriver.Chrome(options=options)
driver.maximize_window()


FB_GROUP_URLS = [
    {"Rez One/ICON - Student Housing In Waterloo": {
        "buy_and_sell": "https://www.facebook.com/groups/3428997217345482/",
        "discussion": "https://www.facebook.com/groups/3428997217345482/buy_sell_discussion"
    }},
    {"Student Housing in Waterloo": {
        "buy_and_sell": "https://www.facebook.com/groups/1998166543836067/",
        "discussion": "https://www.facebook.com/groups/1998166543836067/buy_sell_discussion"
    }},
    {"Rez-One sublets - Student Housing Waterloo": {
        "buy_and_sell": "https://www.facebook.com/groups/855632539122696/",
        "discussion": "https://www.facebook.com/groups/855632539122696/buy_sell_discussion"
    }},
    {"Waterloo Student Housing": {
        "discussion": "https://www.facebook.com/groups/664699027351008/"
    }},
    {"UW/WLU 4 Month Subletting": {
        "buy_and_sell": "https://www.facebook.com/groups/WaterlooSublet/",
        "discussion": "https://www.facebook.com/groups/WaterlooSublet/buy_sell_discussion"
    }},
]


CHART_DATA = {
    "name": [],
    "profile_url": [],
    "group_name": [],
    "source": [],
    "content": [],
}


FEED_CLASS = "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"
NUMBER_OF_SCROLLS = 5
FOUND_POSTS = set()


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
