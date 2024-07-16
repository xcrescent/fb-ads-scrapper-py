import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from flask import Flask, jsonify, request


def extract_json_from_string(data_string):
    start_index = data_string.find('{')  # Find the start of JSON object
    end_index = data_string.rfind('}') + 1  # Find the end of JSON object
    json_data = data_string[start_index:end_index]  # Extract JSON string
    return json_data


def scrape_website( url):
    """Scrapes a website for specific content.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        list: A list of the scraped content (e.g., article titles).
    """
    # Initialize the Chrome web driver in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    # Extract data
    driver.implicitly_wait(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    for script in soup.find('body').find_all('script'):
        if script.get_text().find("props") != -1:
            data_string = script.get_text(strip=True).split('"props":')[1]
            print(data_string)
            # Extract JSON data from the string
            json_string = extract_json_from_string(data_string)
            print(json_string)
            # Parse JSON data into a Python dictionary
            # data_dict = json.loads(json_string)
            #
            # # Print the parsed dictionary
            # # print(json.dumps(data_dict, indent=4))  # Pretty-print the dictionary
            # for key, value in data_dict.items():
            #     print(key, ":", value)
            #     if isinstance(value, dict):
            #         for k, v in value.items():
            #             print("  ", k, ":", v)
            # return data_dict

    time.sleep(3)


page_id = 105642525462731
# Get the website URL to scrape (replace with the actual URL)
target_url = 'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=IN&search_type=page&media_type=all&view_all_page_id=' + str(page_id)
scraped_data = scrape_website(target_url)
if scraped_data is None:
    print("No data scraped.")
else:
    print("Data scraped successfully.")
    print(scraped_data)
