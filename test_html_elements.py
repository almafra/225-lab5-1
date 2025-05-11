from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import unittest
import time

class TestContacts(unittest.TestCase):
    def setUp(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_contacts(self):
        driver = self.driver
        driver.get("http://10.48.10.147")

        for i in range(10):
            test_name = f'Test Name {i}'
            assert test_name in driver.page_source, f"Test contact {test_name} not found in page source"

    def test_page_title_and_heading(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        self.assertIn("Add Contacts", driver.page_source)

    def test_input_fields_exist(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        input_fields = driver.find_elements(By.TAG_NAME, "input")
        self.assertEqual(len(input_fields), 2)

    def test_table_headers(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        headers = driver.find_elements(By.TAG_NAME, "th")
        header_texts = [h.text.strip() for h in headers]
        for expected in ["Name", "Phone Number", "Delete"]:
            self.assertIn(expected, header_texts)

    def test_contact_ali_exists(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        self.assertIn("Ali", driver.page_source)

    def test_total_number_of_contacts(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        rows = driver.find_elements(By.XPATH, "//table//tr")[1:]
        self.assertEqual(len(rows), 11)

    # NEW TEST: Add a contact using the form
    def test_add_new_contact(self):
        driver = self.driver
        driver.get("http://10.48.10.147")

        input_fields = driver.find_elements(By.TAG_NAME, "input")
        self.assertEqual(len(input_fields), 2, "Expected two input fields")

        # Fill out the form
        input_fields[0].send_keys("Selenium Bot")
        input_fields[1].send_keys("555-555-5555")
        input_fields[1].send_keys(Keys.RETURN)  # Assuming this submits the form

        time.sleep(1)  # Wait for the page to update

        # Verify the contact is added
        self.assertIn("Selenium Bot", driver.page_source)
        self.assertIn("555-555-5555", driver.page_source)

    # NEW TEST: Delete a contact (if delete button/link exists)
    def test_delete_contact(self):
        driver = self.driver
        driver.get("http://10.48.10.147")

        # Add a contact to delete
        input_fields = driver.find_elements(By.TAG_NAME, "input")
        input_fields[0].send_keys("Delete Me")
        input_fields[1].send_keys("000-000-0000")
        input_fields[1].send_keys(Keys.RETURN)
        time.sleep(1)

        # Find and click the delete button for "Delete Me"
        rows = driver.find_elements(By.XPATH, "//table//tr")
        for row in rows:
            if "Delete Me" in row.text:
                delete_button = row.find_element(By.TAG_NAME, "button")  # Adjust if it's a link
                delete_button.click()
                break

        time.sleep(1)

        # Confirm contact is gone
        self.assertNotIn("Delete Me", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
