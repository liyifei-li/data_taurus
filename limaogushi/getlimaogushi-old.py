# -- coding: utf-8 --

import os
import re
import requests
from bs4 import BeautifulSoup
import time

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 设置列表页的URL和页数范围
data = {  
        "https://m.limaogushi.com/pd/shuiqian": 542,  
        "https://m.limaogushi.com/pd/youer": 3,  
        "https://m.limaogushi.com/pd/zheli": 92,  
        "https://m.limaogushi.com/pd/yizhi": 219,  
        "https://m.limaogushi.com/pd/gaoxiao": 9,  
        "https://m.limaogushi.com/pd/zhihui": 27,  
        "https://m.limaogushi.com/pd/chengyu": 83,  
        "https://m.limaogushi.com/pd/youmo": 112  
    }

error_file = 'error.txt'

for url_list, page in data.items():      
	print(f"{url_list}: {page}")   

	#url_list = 'https://m.limaogushi.com/pd/shuiqian'
	start_page = 1
	end_page = page

	# 创建存储文件的目录
	if not os.path.exists('data'):
	    os.mkdir('data')

	# 循环遍历列表页的每一页
	for page in range(start_page, end_page+1):
	    # 构造当前页的URL
	    if page == 1:
	        url = url_list
	    else:
	        url = f"{url_list}/page/{page}"

	    # 发送请求并解析HTML
	    response = requests.get(url, headers=headers)
	    soup = BeautifulSoup(response.content, 'html.parser')

	    # 查找所有详情页链接
	    links = soup.find_all('a', href=re.compile(r'/g/\d+\.html'))

	    # 循环遍历每个详情页链接，并抓取文本内容并存储为文件
	    for link in links:
	        detail_url = link['href']
	        print(detail_url)
	        response = requests.get(detail_url, headers=headers)

	        detail_soup = BeautifulSoup(response.content, 'html.parser')
	        title = detail_soup.find('h1').get_text(strip=True)
	        content_element = detail_soup.find('div', {'class': 'infoText'})

	        # 如果正文内容为空，则报错并记录文件名到错误文档中
	        if content_element is None:
	            with open(error_file, 'a', encoding='utf-8') as f:
        	        f.write(f"{title} {url}\n")

	        if content_element is not None:
	            #content = content_element.get_text(strip=True)
	            # 去掉 <div class="story-labels"> 里面的内容
	            labels_element = content_element.find('div', {'class': 'story-labels'})
	            if labels_element is not None:
	                labels_element.extract()

	            # 获取正文文本内容
	            content = content_element.get_text(strip=True)
	            #print(content)
	            # 生成文件名，并写入文件
	            file_name = f"data/{detail_url.split('/')[-1]}.txt"
	            with open(file_name, 'w', encoding='utf-8') as f:
	                result = content.split('上一篇', 1)[0]
	                f.write(f"{title}\n\n{result}")
	        time.sleep(1)


	    print(f"Page {page} finished.")


	print("All pages finished.")