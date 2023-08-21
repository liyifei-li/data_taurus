import re
from bs4 import BeautifulSoup

with open('gushidaquan-div.txt', 'r', encoding='utf-8') as f:
    html = f.read()
print(html)

soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('a', href=True)
print(links)

with open('gushidaquan-todolist.txt', 'w', encoding='utf-8') as f:
    for link in links:
        url = link['href']
        text = re.sub(r'\s+', ' ', link.get_text()).strip()
        print(f'{url} 1 x {text}\n')
        f.write(f'{url} 1 x {text}\n')