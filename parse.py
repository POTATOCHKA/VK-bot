import requests
from lxml import html
import re
headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def google(q):
    s = requests.Session()
    q =  '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&tbm=isch' + \
          '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)
    pattern = r"(https.{10,90}\.jpg)"
    x = re.findall(pattern, r.text)
    req = s.get(x[0], headers=headers_Get)
    with open("google.jpg", "wb") as f:
        f.write(req.content)


def kinopoisk(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.kinopoisk.ru/index.php?kp_query=' + q
    r = s.get(url, headers=headers_Get)
    tree = html.fromstring(r.text)
    pattern = r"(film\/([0-9]{1,10})\/)"
    x = re.findall(pattern, r.text)
    id = x[1][1]
    url = 'https://st.kp.yandex.net/images/film_big/' + id + '.jpg'
    print(url)
    req = s.get(url, headers=headers_Get)
    with open("kinopoisk.jpg", "wb") as f:
        f.write(req.content)
