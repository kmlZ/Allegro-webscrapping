import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from product import Product
import requests
from bs4 import BeautifulSoup
import html.parser
import json

SEARCH_ITEM = input("Wpisz nazwę produktu\n")
# SEARCH_ITEM = "asd"
JSNON_FILE_NAME = "search_output/"+SEARCH_ITEM.replace(" ","_") + ".json"
PAGES_TO_SEARCH = input("Wpisz liczbę stron do przeszukania\n")
print("Pages to search: " + PAGES_TO_SEARCH)
PAGES_TO_SEARCH = int(PAGES_TO_SEARCH)
page = PAGES_TO_SEARCH
print(JSNON_FILE_NAME)

options = Options()
options.headless = False
browser = webdriver.Firefox(executable_path="drivers/geckodriver.exe",options=options)
browser.get("https://allegro.pl")

headers = {
   "User-agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3'
    }

products = []



    
close = WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button._qdoeh:nth-child(1)")))
close.click()
browser.find_element_by_css_selector("._d25db_3K7x6").send_keys(SEARCH_ITEM)
browser.find_element_by_xpath("/html/body/div[2]/div[3]/header/div/div/div/div/form/button").click()
soup = BeautifulSoup(requests.get(browser.current_url, headers = headers).content, "html.parser")
current_url = browser.current_url
while True:
    if page != 0:
        try:
            r = requests.get(browser.current_url + "&p=" + str(page), headers=headers)
            soup = BeautifulSoup(r.content, "html.parser")
            r_url = r.url
        except:
            break
    for element in soup.find_all('div', class_="_9c44d_2H7Kt"):
        
        name = ''
        price = ''
        link = ''
        main_link = ''
        try:
            name = element.find('h2', class_="_9c44d_LUA1k").findChild().text
            price_wrapper = element.find('span', class_="_9c44d_1zemI").text       
            link = element.find('h2', class_="_9c44d_LUA1k").findChild().get("href")
            main_link = r_url
        except:
            print("Exception")
        product = Product(name,price_wrapper,link, main_link)
        products.append(product)
       # print("Name: " + name)
       # print("Price: " + price_wrapper)
       # print("Link: " + link)
        #print()
    print("Page: " + str(page))
    page = page - 1
    if page == 0:
        break

    #print("Link do strony allegro: "+r.url)
    
        
run = 0        
      
# browser.quit()    
print("Browser closed!")

with open(JSNON_FILE_NAME, 'w', encoding='utf8') as json_file:
    data = {}
    data["Products"] = []
    for prod in products:
        data["Products"].append(prod.serialize())
    json.dump(data,json_file,sort_keys=True, indent=4,ensure_ascii=False)

