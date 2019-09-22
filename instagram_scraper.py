import os
import time
import platform
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from constants import *


class Instagram_scrapper():
    def __init__(self):
        self.add_executable_to_path()
        self.driver = None

    def add_executable_to_path(self): # To avoid install browsers drivers 
        # Add exec in SO path
        if not os.getcwd() in os.get_exec_path():
            os.environ["PATH"] = os.environ["PATH"] + ";" if platform.system() == "Windows" else os.environ["PATH"] + ":" 
    
    def wait_for_load(self, by=By.ID, name='react-root', timeout=10):
        element_present = EC.presence_of_element_located((by, name))
        WebDriverWait(self.driver, timeout).until(element_present)
    
    def scrapping(self, query, limit=50):
        self.driver = webdriver.Chrome()
        self.query_tag(query, limit)
    
    def query_tag(self, query, limit, timeout=4):
        self.driver.get(SEARCH_TAG_URL.format(query['value']))
        div_with_imgs = None        
        # Wait for the page to load completely.
        try:
            self.wait_for_load(By.ID, 'react-root')
            div_with_imgs = self.driver.find_elements_by_class_name("_bz0w")
        except TimeoutException:
            try:
                self.driver.find_element_by_css_selector(".p-error.dialog-404")
            except:
                print("Some error occurred while loading the page")

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.SPACE).perform()
        actions.send_keys(Keys.SPACE).perform()
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(5)

        num_scrolls = math.ceil((limit - len(div_with_imgs))/ IMGS_PER_SCROLL)
        scroll = 0
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")     

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2.5)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            bso = BeautifulSoup(self.driver.page_source)
            print(len(bso.findAll('div',{'class':'_bz0w'})))
            if new_height == last_height or num_scrolls == scroll:
                break

            last_height = new_height
            scroll = scroll + 1
        
        div_with_imgs = self.driver.find_elements_by_class_name("_bz0w")
    

query = {
    "value":"disney"
}
instagram = Instagram_scrapper()
instagram.scrapping(query)

    