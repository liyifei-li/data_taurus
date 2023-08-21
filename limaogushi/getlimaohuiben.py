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

# 打开文件    
with open("todo.txt", "r") as f:    
    # 读取文件内容    
    content = f.readlines()

# 将文件内容转换为字典   
data = {}

# 遍历文件内容，将 URL 和页面数转换为字典键值对    
for line in content:    
    url, page_num = line.strip().split(" ")    
    data[url] = int(page_num)

# 创建存储文件的目录
if not os.path.exists('huiben'):
	    os.mkdir('huiben')

error_file = 'huiben_error.txt'
finished_file = 'huiben_success.txt'


for url_list, page in data.items():      
	print(f"{url_list}: {page}")   

	#url_list = 'https://m.limaogushi.com/pd/shuiqian'
	start_page = 1
	end_page = page


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
	    links = soup.find_all('a', href=re.compile(r'/huiben/\d+\.html'))

	    # 循环遍历每个详情页链接，并抓取文本内容并存储为文件
	    for link in links:
	        detail_url = link['href']
	        print(detail_url)
	        response = requests.get(detail_url, headers=headers)

	        # 解析页面
	        soup = BeautifulSoup(response.text, 'html.parser')
	        title = soup.h1.string
	        audio_src = soup.find('source', {'type': 'audio/mp3'}).get('src')
	        print(audio_src)

	        # 下载音频文件
	        try:
	            response = requests.get(audio_src, headers=headers)
	            if response.status_code == 200:
        	        #filename = 'huiben/' + title + '.mp3'
        	        last_slash = audio_src.rfind("/")
        	        filename = 'huiben/' + audio_src[last_slash+1:]
        	        print(filename)
        	        with open(filename, 'wb') as f:
	                    f.write(response.content)
        	        print('下载成功')
        	        with open(finished_file, 'a') as f:
        	            f.write(title + '  ' + filename + '\n')
	            else:
        	        raise requests.exceptions.RequestException
	        except requests.exceptions.RequestException:
	            print('下载失败')
	            if not os.path.exists(error_file):
	                with open(error_file, 'w') as f:
	                    pass
	            with open(error_file, 'a') as f:
	                f.write(title + ' 下载失败')


	    print(f"Page {page} finished.")


	print("All pages finished.")