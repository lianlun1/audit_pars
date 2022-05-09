import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time
import csv


start_time = time.time()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'accept': '*/*'
}

audit_urls = []

def get_audits():

    with open('auditors.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow(
            (
                'Фамилия Имя Отчество',
                'Фамилия Имя Отчество на иностранном языке',
                'Субъект Российской Федерации',
                'ОРНЗ',
                'ОГРНИП',
                'Саморегулируемая организация аудиторов',
                'Дата и номер решения о приеме в члены саморегулируемой организации аудиторов',
                'Дата вступления в силу решения о приеме в члены саморегулируемой организации аудиторов',
                'Номер аттестата',
                'Вид аудита',
                'Номер и дата решения о выдаче',
                'Орган, выдавший аттестат',
                'Номер и дата приказа об аннулировании',
                'Орган, аннулировавший аттестат',
                'Основания аннулирования'
            )
        )

    url = 'https://t24.io/auditory?page=1'
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    pages = soup.find('div', class_='table-responsive').find('ul').find_all('li')
    page_count = pages[-2].text

    for i in range(1, int(page_count) + 1):
        print(f'Страница {i} в работе')
        url=f'https://t24.io/auditory?page={i}'
        req = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(req.text, 'lxml')
        audits_urls = soup.find('div', class_='col-md-8').find_all('h4', class_='h4-responsive')

        for item in audits_urls:
            try:
                audit_url = item.find('a').get('href').strip()
            except Exception as ex:
                print(ex)
            
            try:
                get_datas(url=audit_url)
            except Exception as ex:
                print(ex)
            

def get_datas(url):
    
    audits_data = []
    
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    audit_items = soup.find('div', class_='col-md-9').find_all('dd')

    try:
        audit_full_name = audit_items[0].text.strip()
    except:
        audit_full_name = '-'

    try:
        audit_foreign_full_name = audit_items[1].text.strip()
    except:
        audit_foreign_full_name = '-'

    try:
        subject = audit_items[2].text.strip()
    except:
        subject = '-'

    try:
        ORNZ = audit_items[3].text.strip()
    except:
        ORNZ = '-'

    try:
        OGRNIP = audit_items[4].text.strip()
    except:
        OGRNIP = '-'

    try:
        audit_organization = audit_items[5].text.strip()
    except:
        audit_organization = '-'

    try:
        date_and_number_of_the_decision = audit_items[6].text.strip()
    except:
        date_and_number_of_the_decision = '-'

    try:
        date_of_entry_into_force = audit_items[7].text.strip()
    except:
        date_of_entry_into_force = '-'

    certificate_items = soup.find('div', class_='table-responsive').find('table').find('tbody').find('tr').find_all('td')

    try:
        certificate_number = certificate_items[0].text.strip()
    except:
        certificate_number = ''

    try:
        audit_view = certificate_items[1].text.strip()
    except:
        audit_view = ''

    try:
        number_and_date_of_the_extradition = certificate_items[2].text.strip()
    except:
        number_and_date_of_the_extradition = ''

    try:
        authority = certificate_items[3].text.strip()
    except:
        authority = ''

    try:
        number_and_date_of_the_cancellation = certificate_items[4].text.strip()
    except:
        number_and_date_of_the_cancellation = ''

    try:
        authority_that_annuled = certificate_items[5].text.strip()
    except:
        authority_that_annuled = ''

    try:
        grounds = certificate_items[6].text.strip()
    except:
        grounds = ''

    audits_data.append(
        {
            'Фамилия Имя Отчество': audit_full_name,
            'Фамилия Имя Отчество на иностранном языке': audit_foreign_full_name,
            'Субъект Российской Федерации': subject,
            'ОРНЗ': ORNZ,
            'ОГРНИП': OGRNIP,
            'Саморегулируемая организация аудиторов': audit_organization,
            'Дата и номер решения о приеме в члены саморегулируемой организации аудиторов': date_and_number_of_the_decision,
            'Дата вступления в силу решения о приеме в члены саморегулируемой организации аудиторов': date_of_entry_into_force,
            'Номер аттестата': certificate_number,
            'Вид аудита': audit_view,
            'Номер и дата решения о выдаче': number_and_date_of_the_extradition,
            'Орган, выдавший аттестат': authority,
            'Номер и дата приказа об аннулировании': number_and_date_of_the_cancellation,
            'Орган, аннулировавший аттестат': authority_that_annuled,
            'Основания аннулирования': grounds
        }
    )

    with open('auditors.csv', 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                audit_full_name,
                audit_foreign_full_name,
                subject,
                ORNZ,
                OGRNIP,
                audit_organization,
                date_and_number_of_the_decision,
                date_of_entry_into_force,
                certificate_number,
                audit_view,
                number_and_date_of_the_extradition,
                authority,
                number_and_date_of_the_cancellation,
                authority_that_annuled,
                grounds
            )
        )

def main():
    get_audits()
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")

if __name__ == '__main__':
    main()