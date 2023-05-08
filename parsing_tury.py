import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    # req = requests.get(url=url, headers=headers)
    # src = req.text

    # with open('tury.html', 'w') as file:
    #     file.write(src)
    #
    # soup = BeautifulSoup(src, 'lxml')
    #
    # hotels_info = soup.find_all(class_='reviews-travel__info')
    #
    # for hotels in hotels_info:
    #     hotels_name = hotels.find(class_="h4").text.strip()
    #     hotels_url = soup.find('a').get('href')
    #     print(hotels_name)
    #     print(hotels_url)
    #     print('*'*20)


hotels_list = []


def get_data_with_selenium(url):
    options = Options()
    # options.preferences = {'general.useragent.override': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    options.page_load_strategy = 'normal'

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url=url)
        time.sleep(5)

        with open('selenium-tury.html', 'w') as file:
            file.write(driver.page_source)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    with open('selenium-tury.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    hotels_info = soup.find_all(class_='reviews-travel__info')

    for hotels in hotels_info:
        hotels_name = hotels.find(class_="h4").text.strip()
        hotels_url = hotels.find('a').get('href')
        # print(hotels_name)
        # print(hotels_url)
        # print('*' * 20)

        hotels_list.append(
            {
                'Hotel name': hotels_name,
                'Hotel url': hotels_url
            }
        )


    with open('tury.json', 'a', encoding='utf=8') as file:
        json.dump(hotels_list, file, indent=4, ensure_ascii=False)


def main():
    # get_data('https://tury.ru/hotel/?cat=1317')
    get_data_with_selenium('https://tury.ru/hotel/?cat=1317')


if __name__ == '__main__':
    main()

