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


FEED_CLASS = "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"
NAME_CLASS = "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"
CONTENT_CLASS = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"
EMPTY_POST_CLASS = "xod5an3 xq8finb x14vqqas"
UNAVILABLE_CONTENT_CLASS = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h"
FACEBOOK_PROFILE_CLASS = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"


CHART_DATA = {
    "name": [],
    "profile_url": [],
    "group_name": [],
    "source": [],
    "content": [],
}


NUMBER_OF_SCROLLS = 3


def scrape(post, names, contents, profiles):
    filter_list = [None, " ", "No Content found"]
    name = post.find("span", {"class": NAME_CLASS}, recursive=True)
    if name is not None:
        name = name.find_all(string=True)
    content = post.find("span", {"class": CONTENT_CLASS}, recursive=True)
    if content is not None:
        content = content.find_all(string=True)
    if content not in filter_list and name not in filter_list: 
        names.append(name)
        contents.append(content)
        profile = post.find("a", {"class": FACEBOOK_PROFILE_CLASS}, recursive=True)
        if profile is not None:
            profile = profile.get("href")
            profiles.append(profile)
        else:
            profiles.append("")
    else:
        if content not in filter_list and name in filter_list:
            names.append("UNKNOWN")
            contents.append(content)
            profiles.append("")


# https://medium.com/elnkart/facebook-login-using-selenium-python-bd28d2cb3740
def main():  
    for url_entry in FB_GROUP_URLS:
        for group_name, link in url_entry.items():
            for url in link.values():
                isBuyAndSell = False if "buy_sell_discussion" in url else True
                change_url(driver, f"{url}?sorting_setting=CHRONOLOGICAL_LISTINGS" if isBuyAndSell else f"{url}?sorting_setting=RECENT_ACTIVITY")

                for _ in range(NUMBER_OF_SCROLLS):
                    names, contents, profiles = [], [], []
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    posts = soup.findAll("div", {"class": FEED_CLASS})
                    
                    for post in posts:
                        print(post.find_all(string=True, recursive=False))
                        print("========================")
                        print(post.find_all(string=True, recursive=True))
                        scrape(post, names, contents, profiles)
                        scroll_to_bottom(driver, 2)

                    category = "Buy and Sell" if isBuyAndSell else "Discussion"
                    add_to_data(names, contents, profiles, CHART_DATA, category, group_name)

    # Write the data to an Excel Spreadsheet
    generate_excel_file(["Seller Name", "Group", "Category", "Post Contents"], CHART_DATA)


if __name__ == "__main__":
    main()
    driver.close()
