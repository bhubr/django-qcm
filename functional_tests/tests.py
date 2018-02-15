from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
import unittest

MAX_WAIT = 3

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('movie-table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.2)

    def test_can_register_a_user(self):
        self.browser.get(self.live_server_url + '/register')
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Register', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('input-username')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your username'
        )

        # She types "Inception" into a text box
        inputbox.send_keys('foobar')

        inputbox = self.browser.find_element_by_id('input-email')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your email'
        )

        # She types "Inception" into a text box
        inputbox.send_keys('foobar@example.com')

        inputbox = self.browser.find_element_by_id('input-password')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your password'
        )

        # She types "Inception" into a text box
        inputbox.send_keys('foobar')

        # When she hits enter, the page updates, and now the page lists
        # "1: Inception" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)

        time.sleep(0.5)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/libraries/foobar/')


    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('MovieLib', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your Movie list', header_text)

        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Not logged-in', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('input-new-movie')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a movie title'
        )

        # She types "Inception" into a text box
        inputbox.send_keys('Inception')

        # When she hits enter, the page updates, and now the page lists
        # "1: Inception" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Inception')

        inputbox = self.browser.find_element_by_id('input-new-movie')
        inputbox.send_keys('The Sixth Sense')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Inception')
        self.wait_for_row_in_list_table('2: The Sixth Sense')

        # There is still a text box inviting her to add another item. She
        # enters "Armageddon"
        # self.fail('Finish the test!')
        # She is invited to enter a to-do item straight away

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('input-new-movie')
        inputbox.send_keys('Avatar')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Avatar')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/libraries/.+')

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Avatar', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('input-new-movie')
        inputbox.send_keys('X-Men')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: X-Men')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/libraries/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Avatar', page_text)
        self.assertIn('X-Men', page_text)

        # Satisfied, they both go back to sleep