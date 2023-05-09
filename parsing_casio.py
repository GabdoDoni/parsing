import requests
from bs4 import BeautifulSoup
import lxml
import os
import json
from datetime import datetime
import csv

watch = []

def get_all_pages():
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    # req = requests.get(url='https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/', headers=headers, verify=False)
    #
    # if not os.path.exists('data_casio'):
    #     os.mkdir('data_casio')
    #
    # with open('data_casio/page_1.html', 'w') as file:
    #     file.write(req.text)

    with open('data_casio/page_1.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    watches = soup.find_all(class_='product-item__link')

    cur_date = datetime.now().strftime('%d_%m_%Y')

    with open(f'casio_{cur_date}.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Коллекция',
                'Артикул',
                'Адрес'
            )
        )

    for item in watches:

        watches_cat = item.find(class_='product-item__brand-img').attrs['alt'].strip()
        watches_name = item.find(class_='product-item__articul').text.strip()
        watches_url = 'https://shop.casio.ru' + item.get('href')

        # print(watches_cat)
        # print(watches_name)
        # print(watches_url)
        # print('*'*20)
        watch.append(
            {
                'Watch collection' : watches_cat,
                'Watch article' : watches_name,
                'Watch url' : watches_url
            }
        )

        with open(f'casio_{cur_date}.csv', 'a') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    watches_cat,
                    watches_name,
                    watches_url
                )
            )

    with open(f'casio_{cur_date}.json', 'a', encoding='utf=8') as file:
        json.dump(watch, file, indent=4, ensure_ascii=False)

def main():
    get_all_pages()


if __name__ == '__main__':
    main()