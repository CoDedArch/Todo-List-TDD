from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
#needs a unittest which is a module in the standard library
import time


class NewVisitorTest(LiveServerTestCase):
    
    
    def setUp(self) -> None:
        self.options = Options()
        self.options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.browser = webdriver.Firefox(executable_path=r'C:\Users\hp\Downloads\geckodriver.exe', options = self.options)

    def tearDown(self) -> None:
        self.browser.quit()  

    def wait_for_row_in_list_table(self, row_text: list ) -> None:
        MAX_WAIT = 10
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_for_only_one_user(self) -> None:
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)
        
        # she notices the page title and header mention To-Do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME ,'h1').text
        self.assertIn('To-Do', header_text)
        
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),'Enter a to-do item'
        )


        # She types "Buy peacock feathers" into a text box(Edith's hobby
        #  is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        #when she hits enter, the page updates, and now the page lists
        # '1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # there is still a text box inviting her to ad another item. She
        # enters "Use peacock feathers to make a fly"( Edith is very methodical)
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        # The page updates again, and now shows both items on her list

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        #She is satisfied and she goes back to sleep
        
    def test_multiple_users_can_start_list_at_different_urls(self) -> None:
        #Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #Now a new user, Francis, comes along to the site.
        ## we use a new browser session to make sure that no information
        ## of edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path=r'C:\Users\hp\Downloads\geckodriver.exe', options = self.options)

        # Framcis visit the home page. There is no sign of Edith's
        #list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Eidth...
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis get hs own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list 
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
        

        self.fail('Finish the test!')

        # Edith wonders whether the site will remember her list. Then she sees
        # That the site has generated a unique URL for her -- there is some 
        # expalanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep