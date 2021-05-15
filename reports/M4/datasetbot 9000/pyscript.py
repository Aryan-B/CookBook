import base64
import os
import requests
import time

from io import BytesIO
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def check_if_result_b64(source):
    possible_header = source.split(',')[0]
    if possible_header.startswith('data') and ';base64' in possible_header:
        image_type = possible_header.replace('data:image/', '').replace(';base64', '')
        return image_type
    return False

def get_driver():

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/80.0.3987.132 Safari/537.36'
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--allow-cross-origin-auth-prompt")

    new_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOCATION, options=options)
    new_driver.get(f"https://www.google.com/search?q={'+'.join(SEARCH_TERMS)}&source=lnms&tbm=isch&sa=X")
    return new_driver



CHROME_DRIVER_LOCATION = r'chromedriver.exe'
file1 = open('classes.txt', 'r')
Lines = file1.readlines()
SEARCH_TERMS = ['Apple']

for line in Lines:
    try:
        SEARCH_TERMS[0]=line.strip()
        TARGET_SAVE_LOCATION = os.path.join(os.getcwd(),'download', ' '.join([x.capitalize() for x in SEARCH_TERMS]),  r'{}.{}')
        if not os.path.isdir(os.path.dirname(TARGET_SAVE_LOCATION)):
            os.makedirs(os.path.dirname(TARGET_SAVE_LOCATION))
        driver = get_driver()

        first_search_result = driver.find_elements_by_xpath('//a/div/img')[0]
        first_search_result.click()

        right_panel_base = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'''//*[@data-query="{' '.join(SEARCH_TERMS)}"]''')))
        first_image = right_panel_base.find_elements_by_xpath('//*[@data-noaft="1"]')[0]
        magic_class = first_image.get_attribute('class')
        image_finder_xp = f'//*[@class="{magic_class}"]'


        time.sleep(3)

        thumbnail_src = driver.find_elements_by_xpath(image_finder_xp)[-1].get_attribute("src")

        for i in range(100):
            try:
                target = driver.find_elements_by_xpath(image_finder_xp)[-2]
                wait_time_start = time.time()
                while (target.get_attribute("src") == thumbnail_src) and time.time() < wait_time_start + 5:
                    time.sleep(0.2)
                thumbnail_src = driver.find_elements_by_xpath(image_finder_xp)[-1].get_attribute("src")
                attribute_value = target.get_attribute("src")
                print(attribute_value)
                is_b64 = check_if_result_b64(attribute_value)
                if is_b64:
                    image_format = is_b64
                    content = base64.b64decode(attribute_value.split(';base64')[1])
                else:
                    resp = requests.get(attribute_value, stream=True)
                    temp_for_image_extension = BytesIO(resp.content)
                    image = Image.open(temp_for_image_extension)
                    image_format = image.format
                    content = resp.content
                with open(TARGET_SAVE_LOCATION.format(i, image_format), 'wb') as f:
                    f.write(content)
                svg_arrows_xpath = '//div[@jscontroller]//a[contains(@jsaction, "click:trigger")]//*[@viewBox="0 0 24 24"]'
                next_arrow = driver.find_elements_by_xpath(svg_arrows_xpath)[-3]
                next_arrow.click()
            except Exception as e:
                next_arrow = driver.find_elements_by_xpath(svg_arrows_xpath)[-3]
                next_arrow.click()
                print("Error in image, skipped...")
    except Exception as e:
                print("Error in current query, starting next query...")