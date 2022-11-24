from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()  

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



class BaseCrawler:

    def __init__(self, main_wrapper_locator, browser="chrome_headless"):
        self.main_wrapper_locator = main_wrapper_locator
        if browser == "chrome_headless":
            main_wrapper_locator = main_wrapper_locator
        
            chrome_options = self.__set_chrome_options()
            self.driver = webdriver.Chrome(options=chrome_options,
                                           )

    def __set_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--ignore-certificate-errors")
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage') ##heroku
        chrome_options.add_argument('--verbose')
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        })
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')

        return chrome_options

    def close_connection(self):
        self.driver.close()

    def access_url(self, articleUrl):
        self.driver.get(articleUrl)

    def get_main_wrapper(self):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

class OrgExtractor(BaseCrawler):
    def __init__(self, main_wrapper_locator, browser="chrome_headless"):
        super().__init__(main_wrapper_locator, browser)

    def access_profile(self,playerHandle):
        super().access_url("https://robertsspaceindustries.com/citizens/" + playerHandle + "/organizations")

    def wait_element_visibility_and_return_it(self,expected_location, element_locator):
        myElem = WebDriverWait(expected_location, 20).until(EC.visibility_of_element_located(element_locator))
        return myElem

    def wait_elements_visibility_and_return_them(self,expected_location, element_locator):
        myElem = WebDriverWait(expected_location, 20).until(EC.presence_of_all_elements_located(element_locator))
        return myElem

    def has_no_org(self):
        noOrgElement = self.wait_element_visibility_and_return_it(self.currentWrapper, (By.XPATH, '//div[contains(@class,"profile-content")]'))
        if "NO ORG MEMBERSHIP FOUND" in noOrgElement.text:
            return True
        else:
            return False
    def handle_doesnt_exist(self):
        title = self.driver.title
        if "404 - Rob" in title:
            print("HANDLE NÃO EXISTE VIA 404")
            return True
        else:
            return False

    def get_org_name(self, playerHandle):
        self.access_profile(playerHandle)
        if(self.handle_doesnt_exist()):
            raise Exception("ERROR FINDING HANDLE")
        try:
            _ = self.wait_element_visibility_and_return_it(self.driver, self.main_wrapper_locator)
        except Exception as e:
            print(f"Couldn't find handle {playerHandle}")
            raise Exception("ERROR FINDING HANDLE")
        super().get_main_wrapper()
        if(self.has_no_org()):
            return ["NO ORG"]
        else:
            try:
                orgNameElement = self.wait_elements_visibility_and_return_them(self.currentWrapper, (By.XPATH, '//a[contains(@href,"/orgs/") and contains(@class,"value")]'))
            except Exception as e:
                print(f"Couldn't get orgs for handle {playerHandle}")
                raise Exception("ERROR FINDING ORGS FOR HANDLE")

            return([a.text for a in orgNameElement])

    def get_possible_handles(self, handle):
        return [handle.replace(" ", "_") , handle.replace(" ", "")]




