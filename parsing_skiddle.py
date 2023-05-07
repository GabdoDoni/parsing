import json

import requests
from bs4 import BeautifulSoup
import lxml
import json

url = 'https://www.skiddle.com/festivals/'

req = requests.get(url)
src = req.text
# print(src)

fests_url_list = []

with open('skiddle.html', 'w') as file:
    file.write(src)

with open('skiddle.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
all_festivals = soup.find_all('a', class_="card-details-link")

for item in all_festivals:
    fest_url = 'https://www.skiddle.com' + item.get("href")
    fests_url_list.append(fest_url)

# print(fests_url_list)
count = 0
fest_list_result = []
for url in fests_url_list:
    count += 1
    print(count)
    print(url)

    req = requests.get(url=url)

    try:
        soup = BeautifulSoup(req.text, 'lxml')

        fest_name = soup.find(class_="MuiTypography-root MuiTypography-body1 css-r2lffm").text.strip()
        fest_block = soup.find(class_='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-1ik2gjq')
        fest_date = fest_block.find(class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol').text.strip()

        # print(fest_name)
        # print(fest_date)
        # print('*'*20)

        fest_list_result.append(
            {
                'Fest name' : fest_name,
                'Fest date' : fest_date
            }
        )

    except Exception as ex:
        print(ex)
        print('Damn...')

with open('fest_list.json', 'a', encoding='utf=8') as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)




