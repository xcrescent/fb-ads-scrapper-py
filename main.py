import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from flask import Flask, jsonify, request

# Create Flask application
app = Flask(__name__)


def extract_json_from_string(data_string):
    start_index = data_string.find('{')  # Find the start of JSON object
    end_index = data_string.rfind('}') + 1  # Find the end of JSON object
    json_data = data_string[start_index:end_index]  # Extract JSON string
    return json_data


def scrape_website(url):
    """Scrapes a website for specific content."""
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
        if script.get_text().find("publisherPlatform") != -1:
            data_string = script.get_text(strip=True).split('"adCard":')[1].split(';')[0].split(',"size')[0]
            # Extract JSON data from the string
            json_string = extract_json_from_string(data_string)
            # print(json_string)
            # Parse JSON data into a Python dictionary
            data_dict = json.loads(json_string)

            # Print the parsed dictionary
            # print(json.dumps(data_dict, indent=4))  # Pretty-print the dictionary
            # for key, value in data_dict.items():
                # print(key, ":", value)
                # if isinstance(value, dict):
                    # for k, v in value.items():
                        # print("  ", k, ":", v)
            return data_dict


access_token = 'EAAMoZBMPNLDABO13XPk75gjNUJTzoYHaXeXnrEg5AoN8pZA2XXO5FERZB3hU8PPXE1diPwmHgZAe7U9KjMKJfXDmoZA6AeD80dZARqru7cWTKnDkrgFEE6QEUrAaRPt3pDEqDNY8bnRn12oAOKh2TATRZBnvp9Ir0z2mVbPLAXhlLyXQ8xJ8y8Y0XRqS0HBa3bQq7QTO3ZCawNWw89TjOgZDZD'


# Define a route to serve JSON data using adArchiveID as parameter
@app.route('/api/data', methods=['GET'])
def get_data():
    ad_archive_id = request.args.get('ad_archive_id')
    # Get the website URL to scrape (replace with the actual URL)
    target_url = ('https://www.facebook.com/ads/archive/render_ad/?id=' + ad_archive_id + '&access_token=' + access_token)
    scraped_data = scrape_website(target_url)
    if scraped_data is None:
        return jsonify({"error": "No data found for the provided adArchiveID."})
    # Export the scraped data to a JSON file
    with open('scraped_data_'+ad_archive_id+'.json', 'w') as file:
        json.dump(scraped_data, file, indent=4)
    # Get the adArchiveID from the query parameters
    return jsonify(scraped_data)


if __name__ == '__main__':
    app.run(debug=True)
