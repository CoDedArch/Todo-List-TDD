from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#needs a unittest which is a module in the standard library
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.options = Options()
        self.options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.browser = webdriver.Firefox(executable_path=r'C:\Users\hp\Downloads\geckodriver.exe', options = self.options)

    def tearDown(self) -> None:
        self.browser.quit()  

    def test_can_start_a_list_and_retrieve_it_later(self) -> None:
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')
        
        # she notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')
        
        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feathers" into a text box(Edith's hobby
        #  is tying fly-fishing lures)

        #when she hits enter, the page updates, and now the page lists
        # '1: Buy peacock feathers" as an item in a to-do list

        # there is still a text box inviting her to ad another item. She
        # enters "Use peacock feathers to make a fly"( Edith is very methodical)

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees
        # That the site has generated a unique URL for her -- there is some 
        # expalanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')