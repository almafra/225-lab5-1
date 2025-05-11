from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import unittest

class TestContacts(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Ensures the browser window does not open
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_contacts(self):
        driver = self.driver
        driver.get("http://10.48.10.147")  # Replace with your target website
        
        # Check for the presence of all 10 test contacts
        for i in range(10):
            test_name = f'Test Name {i}'
            assert test_name in driver.page_source, f"Test contact {test_name} not found in page source"
        print("Test completed successfully. All 10 test contacts were verified.")

    # NEW TEST: Check page title
    def test_title(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        self.assertIn("Contacts", driver.title)  # Adjust "Contacts" to your actual expected title

    # NEW TEST: Check if a search input exists
    def test_search_input_presence(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        search_elements = driver.find_elements(By.TAG_NAME, "input")
        self.assertTrue(len(search_elements) > 0, "No input elements found on the page")

    # NEW TEST: Try typing in the first input field (if available)
    def test_typing_in_input(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        try:
            search_box = driver.find_element(By.TAG_NAME, "input")
            search_box.send_keys("Test Name 1")
            search_box.send_keys(Keys.RETURN)
        except Exception as e:
            self.fail(f"Could not interact with the input field: {e}")

    # NEW TEST: Check for presence of footer or an element by ID/class
    def test_footer_presence(self):
        driver = self.driver
        driver.get("http://10.48.10.147")
        footer_elements = driver.find_elements(By.TAG_NAME, "footer")
        self.assertTrue(len(footer_elements) > 0, "Footer not found on the page")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
