from dotenv import load_dotenv
import string
from collections import Counter
import time
import os
import requests
from selenium import webdriver 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager


class ElpaisScrapper:
    def __init__(self):
        self.driver = webdriver.Firefox(service = Service (GeckoDriverManager().install()))
        self.wait = WebDriverWait(self.driver,10)
        
    def visit_site(self):
        print("Navigating site")
        self.driver.get("https://elpais.com/")
        
        #cookie handling
        #resorting to default id for cookie banners
        try:
            accept_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
            accept_btn.click()
            print("Cookie accepted")
        except Exception as e:
            print("already accepted or not found:", e)
        
    def go_to_opinion(self):
        print("navigate to opinion section")
        try:
            #look for link that containes opinion text
            opinion_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"Opinion")))
            opinion_link.click()
        except:
            self.driver.get("https://elpais.com/opinion/")
    
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
                
                #download image locally
                if img_url:
                    self.download_image(img_url, f"article_{index + 1}.jpg")
                
            except Exception as e:
                print(f"error scrapping article{index} : {e}")
            
        return data
    
    def download_image(self,url,filename):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, 'wb')as f:
                    f.write(response.content)
                print(f"Saved {filename}")
        except Exception as e:
            print(f"failed to download{filename}: {e}")
    
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
                #send request
                response = requests.post(url,json = payload, headers = headers)
                
                #check if it worked
                if response.status_code == 200:
                    #checking for a list sent by api
                    translation = response.json()[0]
                    print(f"-> Result : {translation}")
                    
                    #store store
                    translated_titles.append(translation)
                    art['translation_title'] = translation
                else:
                    print(f"-> API error{response.status_code}: {response.text}")
                    translated_titles.append(spanish_title)
            except Exception as e:
                print(f"-> failed connection : {e}")
                translated_titles.append(spanish_title)
            time.sleep(1)
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
        
        print("words repeated more than twice:")
        found = False
        for word,count in word_counts.items():
          if count > 2:
            print(f"-> '{word} : {count} times")
            found = True
        if not found:
            print("-> no words appeared twice or more ")

                    
    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    bot = ElpaisScrapper()
    try:
        #scrape
        bot.visit_site()
        bot.go_to_opinion()
        articles_data = bot.get_articles()
    
    #print what we found
        for art in articles_data:
            print(f"Title : {art['title']}")
        
        translated_headers = bot.translate_titles(articles_data)
        bot.analyze_headers(translated_headers)
#for art in articles_data:
#print(f"\nTitle : {art["title"]}")
#print(f"\nContent : {art["content"]}")

    
    finally:
        bot.close()
        
    
        
    
    

            
            
                    
                