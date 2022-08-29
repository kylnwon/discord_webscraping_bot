from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class webscraping:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.first_part = "https://www.bestbuy.com/site/searchpage.jsp?st="
        self.second_part = "&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys"

    def get_keywords(self, user_message): 
        words = user_message.split()[1:]
        keywords = '+'.join(words)
        return keywords

    def send_url(self, keywords):
        return (self.first_part+keywords+self.second_part)

    # class with button 
    class_="c-button c-button-disabled c-button-sm c-button-block add-to-cart-button"
