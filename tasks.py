import json
import requests
import xmltodict
from celery import Celery
from bs4 import BeautifulSoup



URL_XML ='https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber='
URL_FZ_44 ='https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber='
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }



app = Celery('task', broker='redis://localhost:6379/0')
app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.broker_connection_retry_on_startup = True




@app.task(bind=True)
def fetch_tender(self, page_number:int)->list:
    url = f'{URL_FZ_44}{page_number}'
    print("Constructed URL:", url)
    s = requests.Session()
    response = s.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tender_numbers = []

    # Находим все ссылки на печатные формы
    for link in soup.select('a[href*="notice/printForm/view.html"]'):
        print("Found link:", link['href'])  # Для отладки
        reg_number = link['href'].split('=')[-1]
        tender_numbers.append(reg_number)
    return tender_numbers


@app.task(bind=True)
def parse_xml(self, *reg_number):
    nums = parsing_list(reg_number)
    date = []
    for num in nums:
        xml_url = f'{URL_XML}{num}'
        s = requests.Session()
        response = s.get(xml_url, headers=HEADERS).text
        try:
            data = find_key('publishDTInEIS',json.loads(json.dumps(xmltodict.parse(response))))
            publish_date = next(data)
            result = f"{URL_XML}{num} - {publish_date}"
            date.append(result)
        except Exception as e:
            print(f"Error parsing XML for {num}: {e}")
            continue
    return date


def find_key(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find_key(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find_key(key, d):
                    yield result


def parsing_list(numbers):
    result = []
    date = numbers
    page = 0
    while  len(date)<3:
        for num in date:
            result.extend(num)
        date = result
        result=[]
        if page==100:
            break
        page+=1  
    return date