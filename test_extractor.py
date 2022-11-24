
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()  


    




import unittest
from org_extractor import *
from lib2to3.pgen2 import driver
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#Tests
class TestOrgExtraction(unittest.TestCase):
    def setUp(self):
        main_wrapper_locator = (By.ID ,'public-profile')
        self.extractor = OrgExtractor(main_wrapper_locator=main_wrapper_locator)

    def tearDown(self):
        self.extractor.close_connection()

    def test_no_org_handle(self):
        result = self.extractor.get_org_name("Titan")
        self.assertIn("NO ORG", result)


    def test_one_org_handle(self):
        result = self.extractor.get_org_name("JoaoRaiden")
        self.assertIn("Shadow Moses", result)

    def test_multi_org_handle(self):
        result = self.extractor.get_org_name("AvengerOne")
        self.assertIn("Avenger Squadron", result)
        self.assertIn("Absolute Zero Syndicate", result)

    def test_possible_spaced_handles(self):
        possibleHandles = self.extractor.get_possible_handles("Moist Noodle")
        self.assertIn("MoistNoodle", possibleHandles)
        self.assertIn("Moist_Noodle", possibleHandles)





        


