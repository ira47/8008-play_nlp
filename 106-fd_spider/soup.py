import requests
import csv
# import beautifulsoup4 as bs4
import random
import time

def get_douban_id():
    books = []
    with open('fd_booklist.csv','r',encoding='gbk') as f:
        lines = csv.reader(f)
        for line in lines:
            a = line[0].split('《')
            b = a[1].split('》')
            books.append(b[0])

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    website_prefix = 'https://book.douban.com/j/subject_suggest?q='

    min_stop_time = 2000
    max_stop_time = 5000
    max_retry = 2
    with open('douban_without_rank.csv', 'w', newline='', encoding='utf-8') as ff:
        f = csv.writer(ff)
        for index,book in enumerate(books):
            retry = max_retry
            while retry > 0:
                sleep = random.randint(min_stop_time,max_stop_time)
                time.sleep(sleep/1000.0)
                book = books[index]
                r = requests.get(website_prefix+book,headers=headers)
                if r.status_code != 200:
                    print(index,book)
                    exit(1)
                j = r.json()
                if len(j)==0:
                    retry -= 1
                    continue
                j = j[0]
                if 'title' not in j or 'author_name' not in j or 'id' not in j:
                    retry -= 1
                    continue
                title = j['title']
                author = j['author_name']
                id_ = j['id']
                print(book,title, author,id_)
                f.writerow([title, author,id_])
                break
            if retry <= 0:
                f.writerow([book,'',''])



get_douban_id()