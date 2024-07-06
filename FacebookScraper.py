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