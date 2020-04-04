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
import html5lib

# SEARCH_ITEM = input("Wpisz nazwę produktu\n")
SEARCH_ITEM = "asd"

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
browser.get("https://allegro.pl")

headers = {
   "User-agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3'
    }



def search():
    close = WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[8]/div/div[2]/div/button")))
    close.click()
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/header/div/div/div/div/form/input").send_keys(SEARCH_ITEM)
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/header/div/div/div/div/form/button").click()
    soup = BeautifulSoup(requests.get(browser.current_url, headers = headers).content, "html5lib")
    soup.findChildren()
    for element in soup.find_all('div', class_="_9c44d_2H7Kt"):
        name = element.find('h2', class_="_9c44d_LUA1k").findChild().text
        price_wrapper = element.find('span', class_="_9c44d_1zemI").text       
        link = element.find('h2', class_="_9c44d_LUA1k").findChild().get("href")
        print("Name: " + name)
        print("Price: " + price_wrapper)
        print("Link: " + link)
        print()
        
    print("Link do strony allegro: "+browser.current_url)
    time.sleep(5)       
    browser.quit()    
    print("Browser closed!")    
search()


