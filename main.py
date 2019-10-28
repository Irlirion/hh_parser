import requests
from bs4 import BeautifulSoup

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
}

base_url = 'https://kazan.hh.ru/search/vacancy?area=88&st=searchVacancy&text=Python+junior&page=0'

def hh_parse(base_url):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    assert request.status_code == 200
    print('OK')

if __name__ == '__main__':
    hh_parse(base_url)