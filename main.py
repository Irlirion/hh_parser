import requests
from bs4 import BeautifulSoup as bs

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
}

base_url = 'https://kazan.hh.ru/search/vacancy?area=88&st=searchVacancy&text=Python+junior&page=0'


def hh_parse(base_url, headers):
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    assert request.status_code == 200
    soup = bs(request.content, 'html.parser')
    divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
    for div in divs:
        title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
        href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
        company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
        responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
        requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
        content = responsibility + ' ' + requirement
        jobs.append({
            'title': title,
            'href': href,
            'company': company,
            'content': content,
        })
    print(jobs)

if __name__ == '__main__':
    hh_parse(base_url, headers)
