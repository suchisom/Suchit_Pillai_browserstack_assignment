from dotenv import load_dotenv
import string
from collections import Counter
import time
import os
import requests
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor   
#firefox
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#excluding firefox
#from webdriver_manager.firefox import GeckoDriverManager

load_dotenv()

BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

class ElpaisScrapper:
    def __init__(self,driver,thread_name):
        self.driver = driver
        self.wait = WebDriverWait(self.driver,15)   #witch to 10 ->> 15
        self.thread_name = thread_name
        
    def visit_site(self):
        print("Navigating site")
        self.driver.get("https://elpais.com/")
        
        #cookie handling
        #resorting to default id for cookie banners
        try:
            accept_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
            accept_btn.click()
            print(f"[{self.thread_name}]Cookie accepted")
        except Exception as e:
            print(f"[{self.thread_name}]already accepted or not found:", e)
        
    def go_to_opinion(self):
        print(f"[{self.thread_name}]navigate to opinion section")
        try:
            #look for link that containes opinion text
            #trying direct url
            self.driver.get("https://elpais.com/opinion/")
        #    opinion_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"Opinion")))
        #    opinion_link.click()
            self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,"body")))
        except Exception as e:
            print(f"[{self.thread_name}]error navigating: {e}")
            
    
    def get_articles(self):
        print("fetching articles")
        
        articles = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
        
        first_five = articles[:5]
        data = []
        
        for index,article in enumerate(first_five):
            try:
                #get content
                title_element = article.find_element(By.TAG_NAME,"h2")
                title_text = title_element.text
                
                #get content(summary)
                try:
                    content_text = article.find_element(By.TAG_NAME,"p").text
                except:
                    content_text = "Non content found"
                
                img_url = None
                try:
                    img_element = article.find_element(By.TAG_NAME,"img")
                    img_url = img_element.get_attribute("src")
                except:
                    print("no image found")
                
                
                data.append(
                    {
                        "title" : title_text,
                        "content" : content_text,
                        "image_url" : img_url 
                    }
                )
                
                #download image (with threads)
                if img_url:
                    safe_name = self.thread_name.replace(" ","_").replace("/","-")
                    filename = f"article_{index+1}_{safe_name}.jpg"
                    self.download_image(img_url,filename)
                
            except Exception as e:
                print(f"[{self.thread_name}]error scrapping article{index} : {e}")
            
        return data
    
    def download_image(self,url,filename):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, 'wb')as f:
                    f.write(response.content)
                #print(f"Saved {filename}")
        except Exception as e:
            pass #silent pass to continue thread
    
    def translate_titles(self,articles_data):
        print("\n----------translating--------------")
        translated_titles = []
        
        url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
        
        #headers
        headers = {
        "content-type"    :  "application/json",
        "X-RapidAPI-Key" : os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host" :  "rapid-translate-multi-traduction.p.rapidapi.com"
        }
        for i,art in enumerate(articles_data):
            spanish_title = art['title']
            print(f"translating: {spanish_title}")
            
            #data to send to API
            payload = {
                "from" : "es",
                "to"   : "en",
                "q"    : spanish_title
            }
            
            try:
                #sleep time to avoid hitting api limits
                time.sleep(0.5)
                #send request
                response = requests.post(url,json = payload, headers = headers)
                
                #check if it worked
                if response.status_code == 200:
                    #checking for a list sent by api
                    translation = response.json()[0]
                    #print(f"-> Result : {translation}")
                    
                    #store store
                    translated_titles.append(translation)
                    art['translation_title'] = translation
                else:
                    #print(f"-> API error{response.status_code}: {response.text}")
                    translated_titles.append(spanish_title)
            except Exception as e:
                #print(f"-> failed connection : {e}")
                translated_titles.append(spanish_title)
            #time.sleep(1)
        return translated_titles
    
    def analyze_headers(self,translated_titles_list):
        print("\n------analysing headers---------")
        
        #joining titles
        full_text = " ".join(translated_titles_list)
        #clean punctuation and stuff
        #
        clean_text = full_text.translate(str.maketrans('','',string.punctuation))
        
        words = clean_text.lower().split()
        
        #count
        word_counts = Counter(words)
        
        print(f"\n--words repeated more than twice[{self.thread_name}]--")
        found = False
        for word,count in word_counts.items():
          if count > 2:
            print(f"-> '{word} : {count} times")
            found = True
        if not found:
            print("-> no words appeared twice or more ")

                    
    def close(self):
        self.driver.quit()


def run_session(cap_index_tuple):
    index,caps = cap_index_tuple
    
    #giving thread a nice name
    device_name = caps.get('bstack:options', {}).get('deviceName',caps.get('browserName','Unknown'))
    thread_name = f"{device_name}"
    
    print(f"--> starting thread {index + 1}: {thread_name}")
    
    #driver setup
    options  = webdriver.ChromeOptions()
    for key,value in caps.items():
        options.set_capability(key,value)
    
    driver = None
    try:
        driver = webdriver.Remote(command_executor=URL,options = options)
        
        bot = ElpaisScrapper(driver,thread_name)
        
        
        bot.visit_site()
        bot.go_to_opinion()
        data = bot.get_articles()
        
        #print spanish titles
        print(f"[{thread_name}] Scraped {len(data)} articles.")
        for d in data:
            print(f"   [{thread_name}] ES Title: {d['title']}")
        
        translated = bot.translate_titles(data)
        
        # Print English Titles 
        for t in translated:
            print(f"   [{thread_name}] EN Title: {t}")
            
        bot.analyze_headers(translated)
        
        #mark test as passed
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Full Flow Completed"}}')
        
    except Exception as e:
        print(f"[{thread_name}] CRITICAL ERROR: {e}")
        if driver:
            driver.execute_script(f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed", "reason": "Error: {str(e)}"}} }}')
    
    finally:
        if driver:
            driver.quit()
            print(f"finished thread{index + 1} : {thread_name}")

if __name__ == "__main__":
    caps_list = [
        { 'bstack:options': {'os': 'Windows', 'osVersion': '11'}, 'browserName': 'Chrome', 'browserVersion': 'latest' },
        { 'bstack:options': {'os': 'OS X', 'osVersion': 'Ventura'}, 'browserName': 'Firefox', 'browserVersion': 'latest' },
        { 'bstack:options': {'os': 'Windows', 'osVersion': '10'}, 'browserName': 'Edge', 'browserVersion': 'latest' },
        { 'bstack:options': {'deviceName': 'Samsung Galaxy S22', 'osVersion': '12.0'}, 'browserName': 'chrome' },
        { 'bstack:options': {'deviceName': 'iPhone 14 Pro', 'osVersion': '16'}, 'browserName': 'safari' }
    ]

    print("--- STARTING 5 PARALLEL SESSIONS ---")
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_session, enumerate(caps_list))
    print("--- ALL DONE ---")
    
        
        
        
    
        
    
    

            
            
                    
                