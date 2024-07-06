import time
from time import gmtime, strftime
import xlsxwriter


def change_url(driver, link, delay_time = 3):
    """Change the URL with a timer to suspend the thread"""
    driver.get(link)
    time.sleep(delay_time)


def scroll_to_bottom(driver, num_scrolls, delay_time = 3, scroll_value = 1.175):
    """Scroll to the bottom of the page 'n' times"""
    for _ in range(num_scrolls):
        driver.execute_script(f"window.scrollTo(0, (document.body.scrollHeight)/{scroll_value})")
        time.sleep(delay_time)


def add_to_data(names, contents, profiles, data, category, group_name):
    """After receiving scrapped data, process it"""
    for i in range(len(names)):
        content_text = ""
        for entry in contents[i]:
            content_text += entry + " \\ "
        data_entry = {
            "name": names[i][0],
            "profile_url": f"https://www.facebook.com{profiles[i]}",
            "group_name": group_name,
            "source": category,
            "content": content_text
        }
        for key, val in data_entry.items():
            data[key].append(val)
    names.clear()
    contents.clear()


def generate_excel_file(headers, data):
    """Generate an Excel file using xlsxwriter API"""
    wb = xlsxwriter.Workbook(f"FACEBOOK_SCRAPED_DATA_{strftime("%Y.%m.%d_%H-%M-%S", gmtime())}.xlsx")
    ws = wb.add_worksheet("Sheet 1")

    # Write the headers
    for i in range(len(headers)):
        ws.write(0, i, headers[i])

    # Populate the data - asserting data arrays all have equal row numbers
    for i in range(len(data["name"])):
        ws.write_url(i + 1, 0, data["profile_url"][i], string=data["name"][i])
        ws.write(i + 1, 1, data["group_name"][i])
        ws.write(i + 1, 2, data["source"][i])
        ws.write(i + 1, 3, data["content"][i])

    wb.close()


NAME_CLASS = "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"
CONTENT_CLASS = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"
FACEBOOK_PROFILE_CLASS = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"


def scrape(post, names, contents, profiles):
    """Scrape a post for it's OP, content, and OP URL"""
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