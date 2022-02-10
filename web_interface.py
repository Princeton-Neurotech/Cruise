from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class selenium():
    #options = webdriver.ChromeOptions()
    #options.binary_location = "/Applications/Google Chrome 2.app"
    #chrome_driver_binary = "/Users/leilahudson/Documents/GitHub/Roadblocks/chromedriver"
    #driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver = webdriver.Chrome(executable_path="/Users/nickolascasalinuovo/PycharmProjects/Roadblocks/chromedriver")
    driver.get("http://docs.google.com")
    
    injected_js = False
    while(driver):
        if driver.current_url:
            if driver.current_url.startswith("https://docs.google.com/document/d/"):
                # Inject JS 
                if not injected_js:
                    UID = driver.current_url[35:]
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
                    injected_js = True

    #assert "Python" in driver.title
    #elem = driver.find_element("q")
    #elem.clear()
    #elem.send_keys("pycon")
    #elem.send_keys(Keys.RETURN)
    #assert "No results found." not in driver.page_source
    driver.close()

    

"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

class selenium():
    # options = webdriver.ChromeOptions()
    # options.binary_location = "/Applications/Google Chrome 2.app"
    # chrome_driver_binary = "/Users/leilahudson/Documents/GitHub/Roadblocks/chromedriver"
    # driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver = webdriver.Chrome(executable_path="/Users/leilahudson/Documents/GitHub/Roadblocks/chromedriver.exe")
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()
"""