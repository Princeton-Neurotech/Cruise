from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import only_keyboard_features
import extract_text

class selenium():
        kb = only_keyboard_features.keyboard()
        extractor = extract_text.textExtractor()
        
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.get("https://drive.google.com/drive/u/1/my-drive")
        
        in_docs = False
        while(driver):
            if driver.current_url:
                if driver.current_url.startswith("https://docs.google.com/document/d/"):
                    # Inject JS 
                    if not in_docs:
                        UID = driver.current_url[35:-5]
                        sleep(1)
                        driver.execute_script("var bgl1;") 
                        driver.execute_script("parents = document.getElementsByClassName('kix-canvas-tile-content');")
                        driver.execute_script("""
                        window.fRed = function flashRed(){
                            Array.from(parents).forEach(
                                function(element,index,array){
                                        if(element.children.length == 1){
                                            element.children[0].style='border: 5px solid #ffcfcf;';
                                        }
                                });
                            setTimeout(window.fGrey,20);
                            return "red";
                        }
                        """) 
                        driver.execute_script("""
                        window.fGrey = function flashGrey(){
                            Array.from(parents).forEach(
                                function(element,index,array){
                                    if(element.children.length == 1){
                                        element.children[0].style='border: 5px solid #ffffff;';
                                    }
                                });
                            setTimeout(window.fRed, 20);
                            return "grey";
                        }
                        """) 
                        driver.execute_script("window.fRed();") 
                        in_docs = True
                        for i in range(1000):
                            text = extractor.retrieveText(UID)
                            kb.realtime(text)
                            kb.getData()
                            sleep(5)

        driver.close()

