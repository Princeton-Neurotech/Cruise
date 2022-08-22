from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import keyboard_features
import extract_text
import logging
logging.basicConfig()

class selenium():
    kb = keyboard_features.keyboard()
    extractor = extract_text.textExtractor()
    docs_service = extractor.get_credentials()
        
    def connectSelenium(self, url):
        in_docs = False
        while not in_docs:
            if url:
                if url.startswith("https://docs.google.com/document/d/"):
                    print("found document")
                    if not in_docs:
                        UID = url[35:-5]
                        sleep(1)
                        in_docs = True
        
        # document ID obtained from Google Doc
        return UID
    
    def processSelenium(self, UID):               
        text = self.extractor.retrieveText(UID, self.docs_service)
        return self.kb.realtime(text)

    def closeSelenium(self, driver):
        driver.close()