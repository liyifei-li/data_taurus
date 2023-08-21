# -- coding: utf-8 --

import os
import re
import requests
from bs4 import BeautifulSoup
import time
import random
import datetime

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 定义正则表达式模式
pattern = r'[(（][^）)]*[)）]'

sitename = 'tom61'
siteurl = 'http://www.tom61.com'
log_file = sitename + '_log.txt'
max_tries = 3
retry_count = 0


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
	#print(f"{url_list}: {page}")   


	# 循环遍历列表页的每一页
	for page in range(int(start_page), int(end_page)+1):
	    # 构造当前页的URL
	    if page == 1:
	        url = url_list
	    else:
	        url = f"{url_list}/index_{page}.html"
	    print(url)

	    response = requests.get(url)
	    soup = BeautifulSoup(response.content, 'html.parser')

	    # 查找所有详情页链接
	    linksdiv = soup.find('dl', class_='txt_box')
	    links = linksdiv.find_all('a')

	    #print(links)

	    seen = set()


	    # 循环遍历每个详情页链接，并提取文本内容,然后存储为文件，写日志
	    for link in links:
	        detail_link = link.get('href') 
	        print(detail_link)

            #去掉重复链接
	        if detail_link in seen:
	           print(f"Skipping duplicate link: {detail_link}")
	           continue
	        # 当前在处理的链接
	        print(f"Processing link: {detail_link}")

	        # 将当前链接添加到set中
	        seen.add(detail_link)

	        detail_url = siteurl + detail_link
	        session = requests.Session()
	        #response = session.get(detail_url)
	        #response.encoding = 'utf-8'
	        #print(detail_url)
	        

	        while retry_count < max_tries:
	            try:
	            	session = requests.Session()
	            	response = session.get(detail_url)
	            	response.encoding = 'utf-8'
	            	# 解析页面内容，提取标题和内容  
	            	soup = BeautifulSoup(response.text, "html.parser")
	            	title_tag = soup.find('div', id='thistitle')
	                
	            	story_name = title_tag.text.strip()
	            	print(story_name)

	            	content = soup.find('div', class_='t_news_txt').get_text()
	            	break  # 如果成功获取内容，跳出循环
	            except Exception as e:
	                print(f'抓取页面失败：{e}')
	                retry_count += 1
	        else:
	            print(f'无法获取页面 {detail_url} 的内容，已达到最大重试次数')
	            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	            formatted_log = f'Fail,,,,,来源URL：{detail_url},{current_time}\n'
	            continue

	        #story_content = soup.find('div', class_='t_news_txt')
	        #content = soup.find('div', class_='t_news_txt').get_text()
	        content = re.sub(r'<.*?>', '', content)  # 删除HTML标签
	        story_content = content.replace('</p>', '\n')  # 将</p>替换为换行符
	        #print(story_content)

	        raw_category1 = '儿童文学'
	        raw_category2 = standard_category


	        # 生成文件名，如果文件名存在，则换一个名字
	        file_name = sitename + '/' + story_name + '.txt'
	        while os.path.exists(file_name):
	            random_num = random.randint(1, 100)
	            file_name = f'{sitename}/{story_name}_{random_num}.txt'

	        #先把格式化文本存储到文件中  
	            
	        with open(file_name, 'w', encoding='utf-8') as f:
	            # 对内容进行格式化
	           
	            formatted_text = f'故事名称：{story_name}\n标准分类：{standard_category}\n原始分类1：{raw_category1}\n原始分类2：{raw_category2}\n来源URL：{detail_url}\n故事正文：{story_content}\n'
	              
	            f.write(formatted_text)

	        #生成抓取成功的记录
	        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	        formatted_log = f'Success,故事名称：{story_name},标准分类：{standard_category},原始分类1：{raw_category1},原始分类2：{raw_category2},来源URL：{detail_url},{current_time}\n'


            #再写抓取日志
	        with open(log_file, 'a') as f:
	            f.write(formatted_log)

	        time.sleep(1)

	    print(f"Page {page} finished.")


	print("All pages finished.")