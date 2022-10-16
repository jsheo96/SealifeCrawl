import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import traceback
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
from utils import is_date
import url_list
def get_text(soup):
    title = soup.find('th').text
    tbody = soup.find('tbody')
    tr_list = tbody.findAll('tr')
    phone = tr_list[2].findAll('td')[1].text
    attached = tr_list[4].findAll('td')[0]
    content = tr_list[6].findAll('td')[0].text.strip()
    return title, phone, content

# javascript necessray
def do_crawl():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Firefox()#'./chromedriver')
    data = {'data':[]}
    delay = 5
    try:
        # 구글에 접속
        driver.get('https://www.sealife.go.kr/subject/support/list.do')
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tab = soup.find("table",{"class":"t_typelA listTypeA"})
        tbody = tab.find('tbody')
        tr_list = tbody.findAll('tr')#.find('td').find('td')
        for tr in tr_list:
            td = tr.find('td',{'class':'txt_left'})
            class_type = td.a.span.attrs['class'][0] # n1 or n2
            if class_type == 'n1':
                href = td.a.attrs['href']
                driver.execute_script(href)
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'contents')))
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                title, phone, content = get_text(soup)
                data['data'].append({'title':title,'phone':phone,'content':content})
                driver.execute_script("window.history.go(-1)")

    except:
        data = -1
        print("An exception occurred!")
        traceback.print_exc()
    finally:
        driver.quit()
        return data


def crawl_table_by_selenium(url):
    """
    Crawl table rows from url.
    It detects salient table and returns data from it.
    :param url: URL of page where the table exists.
    :return: Dict[List[Dict[title, full_link, date]]]
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    delay = 5
    # driver.get('https://www.sealife.go.kr/subject/support/list.do')
    driver.get(url)
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tbody_list = soup.findAll('tbody') # choose
    # finds tbody with maximum number of tr's
    assert len(tbody_list) >= 1, 'No tbody found in the response'

    max_index = max(enumerate([len(tbody.findAll('tr')) for tbody in tbody_list]), key=lambda x:x[1])[0]
    tbody = tbody_list[max_index]
    tr_list = tbody.findAll('tr')
    assert len(tr_list) >= 1, 'The table has no row'
    data = {'data': []}
    prev_td_list = None
    for tr in tr_list:
        td_list = tr.findAll('td')
        td_texts = [td.text.strip().split('\n')[0] for td in td_list]
        href = tr.find('a').attrs['href']
        # Case 1: Absolute path
        if href.startswith('/'): # link is absolute path
            link = '/'.join(url.split('/')[:3]) + href
        # Case 2: Relative path
        else:
            link = url.rsplit('/',1)[0] + '/' + href
        date = next(filter(lambda x: is_date(x), td_texts), None)
        assert date is not None, 'Cannot find the string for date'
        title = max(td_texts, key=lambda x:len(x))
        data['data'].append({'title': title, 'date': date, 'full_link': link})
        assert prev_td_list == None or len(td_list) == len(prev_td_list), 'The table has inconsistent number of columns'
        prev_td_list = td_list
    print(data)
    driver.quit()

    return data

def crawl_table(url):
    """
    Crawl table rows from url.
    It detects salient table and returns data from it.
    :param url: URL of page where the table exists.
    :return: Dict[List[Dict[title, full_link, date]]]
    """
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    tbody_list = soup.findAll('tbody') # choose
    # finds tbody with maximum number of tr's
    assert len(tbody_list) >= 1, 'No tbody found in the response'

    max_index = max(enumerate([len(tbody.findAll('tr')) for tbody in tbody_list]), key=lambda x:x[1])[0]
    tbody = tbody_list[max_index]
    tr_list = tbody.findAll('tr')
    assert len(tr_list) >= 1, 'The table has no row'
    data = {'data': []}
    prev_td_list = None
    for tr in tr_list:
        td_list = tr.findAll('td')
        td_texts = [td.text.strip().split('\n')[0] for td in td_list]
        href = tr.find('a').attrs['href']
        # Case 1: Absolute path
        if href.startswith('/'): # link is absolute path
            link = '/'.join(url.split('/')[:3]) + href
        # Case 2: Relative path
        else:
            link = url.rsplit('/',1)[0] + '/' + href
        date = next(filter(lambda x: is_date(x), td_texts), None)
        assert date is not None, 'Cannot find the string for date'
        title = max(td_texts, key=lambda x:len(x))
        data['data'].append({'title': title, 'date': date, 'full_link': link})
        assert prev_td_list == None or len(td_list) == len(prev_td_list), 'The table has inconsistent number of columns'
        prev_td_list = td_list
    return data

def crawl_url_list():
    total_data = {'data': []}
    for url in url_list.url_list:
        data = crawl_table(url)
        total_data['data'] = total_data['data'] + data['data']
    return total_data

if __name__ == '__main__':
    for url in url_list.url_list:
        crawl_table(url)
