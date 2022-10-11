import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import traceback

def get_text(soup):
    title = soup.find('th').text
    tbody = soup.find('tbody')
    tr_list = tbody.findAll('tr')
    phone = tr_list[2].findAll('td')[1].text
    attached = tr_list[4].findAll('td')[0]
    content = tr_list[6].findAll('td')[0].text.strip()
    return title, phone, content
    

driver = webdriver.Chrome('./chromedriver')
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
