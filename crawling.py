import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import traceback
from selenium.webdriver.support import expected_conditions as EC
import requests
def get_text(soup):
    title = soup.find('th').text
    tbody = soup.find('tbody')
    tr_list = tbody.findAll('tr')
    phone = tr_list[2].findAll('td')[1].text
    attached = tr_list[4].findAll('td')[0]
    content = tr_list[6].findAll('td')[0].text.strip()
    return title, phone, content

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
def crwal_sealife():
    driver = webdriver.Firefox()#('./chromedriver')
    delay = 10
    try:
        # 구글에 접속
        driver.get('https://www.sealife.go.kr/subject/support/list.do')

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
                print('title:', title)
                print('phone:', phone)
                print('content:', content)
                driver.execute_script("window.history.go(-1)")
    except:
        print("An exception occurred!")
        traceback.print_exc()
    finally:
        driver.quit()

def crawl_fishgg():
    url = 'https://fish.gg.go.kr/noti/27'
    url_base = 'https://fish.gg.go.kr'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class':'board list'})
    tr_list = table.find('tbody').findAll('tr')
    data = {'data':[]}
    for tr in tr_list:
        title = tr.find('td',{'class':'title'}).text.strip()
        link = tr.find('td',{'class':'title'}).a.attrs['href']
        date = tr.find('td', {'class':'date res-500-hidden'}).text.strip()
        full_link = url_base + link
        data['data'].append({'title': title, 'full_link': full_link, 'date': date})
    return data

def crawl_fipa():
    url = 'https://www.fipa.or.kr/sub3/?mn_idx=0003_0041_0043_&dp1=3&dp2=2&dp3=2'
    url_base = 'https://fish.gg.go.kr'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'board_st list tit'})
    tr_list = table.find('tbody').findAll('tr')
    data = {'data':[]}
    for tr in tr_list:
        title = tr.find('td', {'class': 'w_tit'}).text.strip()
        link = tr.find('td', {'class': 'w_tit'}).a.attrs['href']
        date = tr.find('td', {'class': 'w_date'}).text.strip()
        full_link = url_base + link
        data['data'].append({'title': title, 'full_link': full_link, 'date': date})
    return data

def crawl_nifs():
    url = 'https://www.nifs.go.kr/dokdo/bbs?id=notice'
    url_base = 'https://www.nifs.go.kr/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'summary': '공지사항 리스트 테이블'})
    tr_list = table.find('tbody').findAll('tr')
    data = {'data':[]}
    for tr in tr_list:
        title = tr.find('td', {'class': 'al'}).text.strip()
        link = tr.find('td', {'class': 'al'}).a.attrs['href']
        date = tr.findAll('td')[3].text
        full_link = url_base + link
        data['data'].append({'title': title, 'full_link': full_link, 'date': date})
    return data

def crawl_mof():
    url = 'https://www.mof.go.kr/article/list.do?menuKey=971&boardKey=10'
    url_base = 'https://www.mof.go.kr/article/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'boardBasic list'})
    tr_list = table.find('tbody').findAll('tr')
    data = {'data':[]}
    for tr in tr_list:
        title = tr.find('td', {'class': 'title'}).text.strip()
        link = tr.find('td', {'class': 'title'}).a.attrs['href']
        date = tr.find('td', {'class': 'date'}).text
        full_link = url_base + link
        data['data'].append({'title': title, 'full_link': full_link, 'date': date})
    return data

def crawl_jeonnam():
    url = 'https://www.jeonnam.go.kr/M7116/boardList.do?menuId=jeonnam0202000000'
    url_base = 'https://www.jeonnam.go.kr'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'bbs_table petition_table'})
    tr_list = table.find('tbody').findAll('tr')
    data = {'data':[]}
    for tr in tr_list:
        title = tr.find('td', {'class': 'title left petition'}).text.strip()
        link = tr.find('td', {'class': 'title left petition'}).a.attrs['href']
        date = tr.find('td', {'class': 'date'}).text
        full_link = url_base + link
        data['data'].append({'title': title, 'full_link': full_link, 'date': date})
    return data

def crawl_shinan():
    url = 'https://www.shinan.go.kr/home/www/openinfo/participation_07/participation_07_03'
    url_base = 'https://www.shinan.go.kr'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'list_table', 'id':'board_list_table'})
    tr_list = table.find('tbody').findAll('tr')
    data = {'data':[]}
    for tr in tr_list:
        title = tr.find('td', {'class': 'list_title'}).text.strip()
        link = tr.find('td', {'class': 'list_title'}).a.attrs['href']
        date = tr.find('td', {'class': 'list_reg_date'}).text
        full_link = url_base + link
        data['data'].append({'title': title, 'full_link': full_link, 'date': date})
    return data

if __name__ == '__main__':
    crawl_shinan()