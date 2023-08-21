# -- coding: utf-8 --

import os
import re
import requests
from bs4 import BeautifulSoup
import time
import random


# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 定义正则表达式模式
pattern = r'[(（][^）)]*[)）]'

sitename = 'limaogushi'
siteurl = 'https://www.limaogushi.com'
log_file = sitename + '_log.txt'


# 将文件内容转换为字典   
data = []

# 打开需要抓取的文件，遍历文件内容，将 URL 和页面数转换为元组    
with open(sitename + "-todolist.txt", 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        url, start_page, end_page, standard_category = line.split()
        data.append((url, start_page, end_page, standard_category))


# 创建存储文件的目录
if not os.path.exists(sitename):
	    os.mkdir(sitename)


for url_list, start_page, end_page, standard_category in data:      
	print(f"{url_list}: {end_page}")   


	# 循环遍历列表页的每一页
	for page in range(int(start_page), int(end_page)+1):
	    # 构造当前页的URL
	    if page == 1:
	        url = url_list
	    else:
	        url = f"{url_list}/page/{page}"
	  
	    response = requests.get(url)
	    soup = BeautifulSoup(response.content, 'html.parser')

	    # 查找所有详情页链接
	    #links = soup.find_all('a', href=re.compile(r'/info/\d+\.html'))

	    links_div = soup.find('div',{'class': 'story-today clearfix'})

	    #没解析到，记录报错信息
	    if links_div is None:
	        formatted_log = f'Fail,,,,,来源URL：{url},\n'
	        print('No links')
            #写抓取日志
	        with open(log_file, 'a') as f:
	            f.write(formatted_log)
	        continue

	    links = []

	    for link in links_div.find_all('a', href=True):
	        href = link.get('href')
	        links.append(href)

	    #print(links)

	    # 查找所有详情页链接
	    #detaillinks = links.find_all('a', href=re.compile(r'/g/\d+\.html'))

	    #links  = soup.find_all('h2', class_='entry-title', href=re.compile(r'/info/\d+\.html'))
	    #print(links)

	    seen = set()


	    # 循环遍历每个详情页链接，并提取文本内容,然后存储为文件，写日志
	    for detail_link in links:
	        #detail_link = link.find('a')['href']
	        #print(detail_link)

            #去掉重复链接
	        if detail_link in seen:
	           print(f"Skipping duplicate link: {detail_link}")
	           continue
	        # 当前在处理的链接

	        # 将当前链接添加到set中
	        seen.add(detail_link)

	        detail_url = detail_link.replace('m.', 'www.')
	        print(f"Processing link: {detail_link}")

	        session = requests.Session()
	        response = session.get(detail_url)
	        response.encoding = 'utf-8'
	        #print(detail_url)
	        
	        # 解析页面内容，提取标题和内容  
	        soup = BeautifulSoup(response.text, "html.parser")
	        title_tag = soup.find('h1', {'class': 'infoTit'})
	        if title_tag:
	            story_name = title_tag.text.strip()
	            print(story_name)

	            #title = soup.select_one("h1.entry-title").text.strip()  
	            content = soup.find('div', {'class': 'infoWen'})
	            #print(content)
	            if content:
	                story_text = content.text.strip()
	            #print(story_text)

	            link_div = soup.find('div', class_='fLink white')
	            #print(link_div)
	            
	            #没解析到，记录报错信息，退出循环
	            if link_div is None:
	                formatted_log = f'Fail,,,,,来源URL：{url},\n'
	                #写抓取日志
	                with open(log_file, 'a') as f:
	                    f.write(formatted_log)
	                continue
	        
	            link_div = soup.find('div', class_='fLink white')
	            categorylinks = link_div.find_all('a')

	            raw_category1 = categorylinks[1].text
	            raw_category2 = categorylinks[2].text

	            #print(f'{raw_category1}/{raw_category2}')
	            # 生成文件名，如果文件名存在，则换一个名字
	            file_name = f'{sitename}/{story_name}.txt'
	            while os.path.exists(file_name):
	                random_num = random.randint(1, 100)
	                file_name = f'{sitename}/{story_name}_{random_num}.txt'

	            #先把格式化文本存储到文件中  
	            with open(file_name, 'w', encoding='utf-8') as f:
	            	# 对内容进行格式化，去除“上一篇”后面的文字 
	                story_text = story_text.split('上一篇', 1)[0]
	                # 对内容进行格式化，去除带括号的拼音或英文 ，如小兔子(rabbit)
	                story_content = re.sub(r'\([^)]*\)', '', story_text)

	                formatted_text = f'故事名称：{story_name}\n标准分类：{standard_category}\n原始分类1：{raw_category1}\n原始分类2：{raw_category2}\n来源URL：{detail_url}\n故事正文：{story_content}\n'
	                f.write(formatted_text)

	            #生成抓取成功的记录
	            formatted_log = f'Success,故事名称：{story_name},标准分类：{standard_category},原始分类1：{raw_category1},原始分类2：{raw_category2},来源URL：{detail_url},文件名：{file_name}\n'


            #错误处理：如果提取不到内容，则存储文件名到Log文档中 
	        else:
	            print("No title tag found")
	            #生成抓取失败的记录
	            formatted_log = f'Fail,,,,,来源URL：{detail_url},\n'

            #再写抓取日志
	        with open(log_file, 'a') as f:
	            f.write(formatted_log)

	        time.sleep(1)

	    print(f"Page {page} finished.")


	print("All pages finished.")