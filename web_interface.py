from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class selenium():
    #options = webdriver.ChromeOptions()
    #options.binary_location = "/Applications/Google Chrome 2.app"
    #chrome_driver_binary = "/Users/leilahudson/Documents/GitHub/Roadblocks/chromedriver"
    #driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver = webdriver.Chrome(executable_path="/Users/leilahudson/Documents/GitHub/Roadblocks/chromedriver.exe")
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()