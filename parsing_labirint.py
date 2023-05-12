import json
from os.path import join

import requests
from bs4 import BeautifulSoup
import lxml
import datetime
import csv

def get_data():
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(f'labirint_{cur_time}.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Название книги',
                'Имя автора',
                'Издательство',
                'Цена',
                'Старая цена',
                'Скидка',
            )
        )


    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    url = 'https://www.labirint.ru/genres/2308/?available=1&display=table'

    req = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(req.text, 'lxml')

    pages_count = int(soup.find('div', class_='pagination-number').find_all('a')[-1].text)
    # print(pages_count)
    books_data = []

    for page in range(1, pages_count):
        url = f'https://www.labirint.ru/genres/2308/?available=1&display=table&page={page}'

        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')

        books = soup.find('tbody', class_='products-table__body').find_all('tr')

        for bo in books:
            books_info = bo.find_all('td')
            try:
                book_name = books_info[0].find('a').text.strip()
            except:
                book_name ='Нет название книги'
            try:
                book_avtor =books_info[1].text.strip()
            except:
                book_avtor = 'Нету автора книги'
            try:
                book_izda = books_info[2].find_all('a')
                book_izda = ':'.join([bp.text.strip() for bp in book_izda])
            except:
                book_izda = 'Нету издательства книги'
            try:
                book_price = books_info[3].find(class_='price-val').find('span').text.strip()
            except:
                book_price = 'Нету цен'
            try:
                book_price_old = books_info[3].find(class_='price-old').text.strip()
            except:
                book_price_old = 'Нету старой цены'
            try:
                book_discount = round((int(book_price_old.replace(' ', '')) - int(book_price.replace(' ', '')))/int(book_price_old.replace(' ', ''))*100)
            except:
                book_discount = 'Нету скидки'


            # print(book_name)
            # print(book_avtor)
            # print(book_price)
            # print(book_price_old)
            # print(f'Скидка {book_discount} %')
            # print(book_izda)
            # print("*"*10)

            books_data.append(
                {
                    'book_name': book_name,
                    'book_avtor': book_avtor,
                    'book_publishining': book_izda,
                    'book_price': book_price,
                    'book_price_old' : book_price_old,
                    'book_discount': book_discount
                }
            )

            with open(f'labirint_{cur_time}.csv', 'a') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_name,
                        book_avtor,
                        book_izda,
                        book_price,
                        book_price_old,
                        book_discount,
                    )
                )

        print(f'Обработано {page}/{pages_count}')

    with open(f'labirint_{cur_time}.json', 'w') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)







def main():
    get_data()


if __name__ == '__main__':
    main()