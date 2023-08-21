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
standard_category = '民间故事'
page = 1

def get_detail_content(detail_url, Once):
    retry_count = 0
    nextdo = False
    while retry_count < max_tries:
        try:
            session = requests.Session()
            response = session.get(detail_url)
            response.encoding = 'utf-8'
            # 解析页面内容，提取标题和内容  
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.find('div', id='thistitle')
            story_name = title_tag.text.strip()
            content = soup.find('div', class_='t_news_txt').get_text()
            # 对内容进行格式化
            content = re.sub(r'<.*?>', '', content)  # 删除HTML标签
            story_content = content.replace('　　', '\n')  # 将</p>提取后的空白替换为换行符
            #print(story_content)

            if not Once:
            
                # 对第一次的页面，检查是否有下一页
                tags = soup.find_all('a', class_='c_page')
                urls = [tag['href'] for tag in tags]
                #print(urls)

                for next_url in urls:
                    #其他页面再调用，则不需要
                    story_name, next_content  = get_detail_content(siteurl + next_url, True)
                    if next_content is not None:
                        story_content += next_content
                        #print(story_content)
            break  # 如果成功获取内容，跳出循环
        except Exception as e:
            print(f'抓取页面失败：{e}')
            retry_count += 1
    else:
        print(f'无法获取页面 {detail_url} 的内容，已达到最大重试次数')
        return None, None

    return story_name, story_content


detail_url = 'http://www.tom61.com/ertongwenxue/tonghuagushi/2015-02-11/54803.html'

# 获取详情页的内容
story_name, story_content = get_detail_content(detail_url, False)
if story_content is None:
    # 如果获取详情页内容失败，则记录日志并跳过当前链接
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_log = f'Fail,,,,,来源URL：{detail_url},{current_time}\n'
    with open(log_file, 'a') as f:
        f.write(formatted_log)
else:
    # 解析详情页的内容
    #story_name, story_content = detail_content

    raw_category1 = '儿童文学'
    raw_category2 = standard_category

    # 生成文件名，如果文件名存在，则换一个名字
    file_name = sitename + '/' + story_name + '.txt'
    while os.path.exists(file_name):
        random_num = random.randint(1, 100)
        file_name = f'{sitename}/{story_name}_{random_num}.txt'

    # 将格式化后的内容存储到文件中
    with open(file_name, 'w', encoding='utf-8') as f:
        formatted_text = f'故事名称：{story_name}\n标准分类：{standard_category}\n原始分类1：{raw_category1}\n原始分类2：{raw_category2}\n来源URL：{detail_url}\n故事正文：{story_content}\n'
        f.write(formatted_text)

    # 生成抓取成功的记录
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_log = f'Success,故事名称：{story_name},标准分类：{standard_category},原始分类1：{raw_category1},原始分类2：{raw_category2},来源URL：{detail_url},{current_time}\n'

    # 写入抓取日志
    with open(log_file, 'a') as f:
        f.write(formatted_log)

print(f"Page {page} finished.")

