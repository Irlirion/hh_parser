import csv
import requests
from bs4 import BeautifulSoup as bs

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
}

base_url = 'https://kazan.hh.ru/search/vacancy?area=88&st=searchVacancy&text=Python&page=0'


def hh_parse(base_url, headers):
    jobs = []
    urls = [base_url]
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    assert request.status_code == 200
    soup = bs(request.content, 'html.parser')
    try:
        pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
        count = int(pagination[-1].text)
        for i in range(count):
            url = f'https://kazan.hh.ru/search/vacancy?area=88&st=searchVacancy&text=Python+&page={i}'
            if url not in urls:
                urls.append(url)
    except:
        print('Only one page')
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
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
            except:
                print('Some error')
    return jobs

def write_to_csv(jobs):
    with open('parsed_jobs.csv', 'w', encoding='utf8', newline='') as file:
        a_pan = csv.writer(file, delimiter=',')
        a_pan.writerow(('Вакансии', 'URL', 'Компания', 'Описание'))
        for job in jobs:
            a_pan.writerow((job['title'], job['href'], job['company'], job['content']))


if __name__ == '__main__':
    write_to_csv(hh_parse(base_url, headers))

