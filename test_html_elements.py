from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import unittest
import time

class TestContacts(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Firefox(options=firefox_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://10.48.10.147"  # Base URL for the application
        self.test_contacts = [f'Test Name {i}' for i in range(10)]  # Test data

    def test_contact_presence(self):
        """Test that all test contacts are present on the page"""
        driver = self.driver
        driver.get(self.base_url)
        
        # Wait for page to load
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # Check for each test contact
        for name in self.test_contacts:
            try:
                contact = driver.find_element(By.XPATH, f"//td[contains(text(), '{name}')]")
                self.assertTrue(contact.is_displayed(), f"Contact {name} is not displayed")
            except NoSuchElementException:
                self.fail(f"Test contact {name} not found in page source")
        
        print("Test completed successfully. All 10 test contacts were verified.")

    def test_add_new_contact(self):
        """Test adding a new contact through the UI"""
        driver = self.driver
        driver.get(self.base_url)
        
        # Generate unique test data
        test_name = "Selenium Test User"
        test_phone = f"555-{int(time.time()) % 10000:04d}"
        test_email = f"test{int(time.time())}@example.com"
        test_address = "123 Test Street"
        
        # Fill out the form
        driver.find_element(By.ID, "name").send_keys(test_name)
        driver.find_element(By.ID, "phone").send_keys(test_phone)
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "address").send_keys(test_address)
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Add Contact']").click()
        
        # Wait for the page to reload and check for success message
        try:
            message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "message"))
            self.assertIn("successfully", message.text.lower())
        except TimeoutException:
            self.fail("Success message not displayed after adding contact")
        
        # Verify the new contact appears in the table
        try:
            new_contact = driver.find_element(By.XPATH, f"//td[contains(text(), '{test_name}')]")
            self.assertTrue(new_contact.is_displayed())
        except NoSuchElementException:
            self.fail("Newly added contact not found in the table")

    def test_delete_contact(self):
        """Test deleting a contact through the UI"""
        driver = self.driver
        driver.get(self.base_url)
        
        # First add a contact to delete
        test_name = "Contact to Delete"
        driver.find_element(By.ID, "name").send_keys(test_name)
        driver.find_element(By.ID, "phone").send_keys("555-0000")
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Add Contact']").click()
        
        # Wait for the contact to appear
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//td[contains(text(), '{test_name}')]")))
        
        # Find and click the delete button for this contact
        delete_btn = driver.find_element(By.XPATH, 
            f"//td[contains(text(), '{test_name}')]/following-sibling::td//button[contains(text(), 'Delete')]")
        delete_btn.click()
        
        # Wait for success message
        try:
            message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "message")))
            self.assertIn("successfully", message.text.lower())
        except TimeoutException:
            self.fail("Success message not displayed after deleting contact")
        
        # Verify the contact is no longer in the table
        with self.assertRaises(NoSuchElementException):
            driver.find_element(By.XPATH, f"//td[contains(text(), '{test_name}')]")

    def test_search_functionality(self):
        """Test the search functionality"""
        driver = self.driver
        driver.get(self.base_url)
        
        # Search for a specific contact
        search_term = "Test Name 5"
        search_box = driver.find_element(By.NAME, "query")
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # Verify only the searched contact appears
        contacts = driver.find_elements(By.XPATH, "//tbody/tr")
        self.assertEqual(len(contacts), 1, "Should only find one contact matching search term")
        
        found_name = driver.find_element(By.XPATH, "//tbody/tr/td[1]").text
        self.assertEqual(found_name, search_term, "Found contact name doesn't match search term")

    def test_edit_contact(self):
        """Test editing an existing contact"""
        driver = self.driver
        driver.get(self.base_url)
        
        # Find and click the edit button for the first test contact
        edit_btn = driver.find_element(By.XPATH, 
            "//td[contains(text(), 'Test Name 0')]/following-sibling::td//button[contains(text(), 'Edit')]")
        edit_btn.click()
        
        # Wait for edit page to load
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        
        # Update the contact information
        new_name = "Updated Test Name"
        name_field = driver.find_element(By.NAME, "name")
        name_field.clear()
        name_field.send_keys(new_name)
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Update Contact']").click()
        
        # Wait for redirect back to main page
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # Verify the contact was updated
        try:
            updated_contact = driver.find_element(By.XPATH, f"//td[contains(text(), '{new_name}')]")
            self.assertTrue(updated_contact.is_displayed())
        except NoSuchElementException:
            self.fail("Updated contact not found in the table")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
