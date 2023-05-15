import json
import json
import time
from bs4 import BeautifulSoup
import datetime
import csv
import asyncio
import aiohttp

books_data = []

async def get_page_data(session, page):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    url = f'https://www.labirint.ru/genres/2308/?available=1&display=table&page={page}'

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'lxml')

        books = soup.find('tbody', class_='products-table__body').find_all('tr')

        for bo in books:
            books_info = bo.find_all('td')
            try:
                book_name = books_info[0].find('a').text.strip()
            except:
                book_name = 'Нет название книги'
            try:
                book_avtor = books_info[1].text.strip()
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
                book_discount = round((int(book_price_old.replace(' ', '')) - int(book_price.replace(' ', ''))) / int(
                    book_price_old.replace(' ', '')) * 100)
            except:
                book_discount = 'Нету скидки'

            books_data.append(
                {
                    'book_name': book_name,
                    'book_avtor': book_avtor,
                    'book_publishining': book_izda,
                    'book_price': book_price,
                    'book_price_old': book_price_old,
                    'book_discount': book_discount
                }
            )
        print(f"[INFO] Обработал страницу {page}")




async def gather_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    url = 'https://www.labirint.ru/genres/2308/?available=1&display=table'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        pages_count = int(soup.find('div', class_='pagination-number').find_all('a')[-1].text)
        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(f'labirint_{cur_time}_async.json', 'w') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)

    with open(f'labirint_{cur_time}_async.csv', 'w') as file:
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

    for book in books_data:

        with open(f'labirint_{cur_time}_async.csv', 'a') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    book['book_name'],
                    book['book_avtor'],
                    book['book_izda'],
                    book['book_price'],
                    book['book_price_old'],
                    book['book_discount']
                )
            )


if __name__ == '__main__':
    main()