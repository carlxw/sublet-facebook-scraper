from selenium import webdriver
from time import gmtime, strftime
from FacebookScraper import *
from bs4 import BeautifulSoup
from pandas import DataFrame


options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--user-data-dir=C:\\Users\\carlw\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--profile-directory=Default")
options.add_argument("--remote-debugging-pipe")
driver = webdriver.Chrome(options=options)
driver.maximize_window()


FB_GROUP_URLS = [
    {"Rez One/ICON - Student Housing In Waterloo": "https://www.facebook.com/groups/3428997217345482/"},
    {"Student Housing in Waterloo": "https://www.facebook.com/groups/1998166543836067/"},
    {"Rez-One sublets - Student Housing Waterloo": "https://www.facebook.com/groups/855632539122696/"},
    {"Waterloo Student Housing": "https://www.facebook.com/groups/664699027351008/"},
    {"UW/WLU 4 Month Subletting": "https://www.facebook.com/groups/WaterlooSublet/"},
]


FEED_CLASS = "x1n2onr6 x1ja2u2z"
NAME_CLASS = "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"
CONTENT_CLASS = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"


CHART_DATA = {
    "name": [],
    "group_name": [],
    "source": [],
    "content": [],
}


NUMBER_OF_SCROLLS = 10


# https://medium.com/elnkart/facebook-login-using-selenium-python-bd28d2cb3740
def main():
    driver.get("https://www.facebook.com/")
    
    for url_entry in FB_GROUP_URLS:
        for group_name, link in url_entry.items():
            # Process Buy and Sell Page
            change_url(driver, link)
            sort_by_newest(driver)
            scroll_to_bottom(driver, NUMBER_OF_SCROLLS)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            posts = soup.findAll("div", {"class": FEED_CLASS})
            names, contents = [], []
            for post in posts:
                name = post.find("span", {"class": NAME_CLASS})
                content = post.find("span", {"class": CONTENT_CLASS})
                if content is not None and name is not None: 
                    names.append(name.findAll(string=True))
                    contents.append(content.findAll(string=True))

            if len(names) != len(contents):
                delta = len(names) - len(contents)
                if abs(delta) == 1:
                    if delta > 0:
                        names.pop()
                    else:
                        contents.pop()
                else:
                    raise Exception("A mismatch occured")

            add_to_data(names, contents, CHART_DATA, "Buy and Sell", group_name)
            
            # Process Discussions
            change_url(driver, f"{link}buy_sell_discussion/")
            sort_by_newest(driver)
            scroll_to_bottom(driver, NUMBER_OF_SCROLLS)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            posts = soup.findAll("div", {"class": FEED_CLASS})
            names, contents = [], []
            for post in posts:
                name = post.find("span", {"class": NAME_CLASS})
                content = post.find("span", {"class": CONTENT_CLASS})
                if content is not None and name is not None: 
                    names.append(name.findAll(string=True))
                    contents.append(content.findAll(string=True))

            if len(names) != len(contents):
                delta = len(names) - len(contents)
                if abs(delta) == 1:
                    if delta > 0:
                        names.pop()
                    else:
                        contents.pop()
                else:
                    raise Exception("A mismatch occured")

        add_to_data(names, contents, CHART_DATA, "Discussions", group_name)

    # Write the data to an Excel Spreadsheet
    # https://stackoverflow.com/questions/13437727/how-to-write-to-an-excel-spreadsheet-using-python
    df = DataFrame({
        "Seller Name": CHART_DATA["name"],
        "Group Name": CHART_DATA["group_name"],
        "Source": CHART_DATA["source"],
        "Post Content": CHART_DATA["content"]
    })

    df.to_excel(f"FACEBOOK_SCRAPED_DATA_{strftime("%Y.%m.%d_%H-%M-%S", gmtime())}.xlsx", sheet_name="Sheet1", index=False)


if __name__ == "__main__":
    main()
    driver.close()
