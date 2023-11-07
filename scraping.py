from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
from bs4 import BeautifulSoup

# Set up the Selenium WebDriver.
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Optional: Run in headless mode, without a UI.
driver = webdriver.Chrome(options=options)

def get_description(book_id: str) -> str:
    """Returns the description of the book with book id == book_id
    Args:
        book_id: Goodreads unique identifier for a book
    Returns:
        Description of that book
    """

    url = 'https://www.goodreads.com/book/show/' + book_id

    # Perform an HTTP GET request to the given URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content with Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <div> element with class "BookPageMetadataSection"
        div_content = soup.find('div', class_='BookPageMetadataSection')
        if div_content:
            
            # Find all <span> elements within div_content
            spans = div_content.find_all('span', class_='Formatted')
            return spans[0].text
        else:
            return None
    else:
        return None

def apply_language_filter():
    # Click the 'Filters' button, identified by its class name
    filters_button = driver.find_element(By.CSS_SELECTOR, ".Button--secondary")
    # apply_button = driver.find_element(By.XPATH, "//button[.//span[text()='Apply']]")
    driver.execute_script("arguments[0].click();", filters_button)
    # filters_button.click()

   
    # Wait until the 'English' radio button is clickable, and then click it
    time.sleep(2)
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "en"))).click()
    english_button = driver.find_element(By.ID, "en")
    driver.execute_script("arguments[0].click();", english_button)

    
    # Click the 'Apply' button, which is the button containing the text "Apply"
    print("hello")
    apply_button = driver.find_element(By.XPATH, "//button[.//span[text()='Apply']]")
    apply_button.click()

def get_reviews(url, max_reviews=100):
    driver.get(url)
    apply_language_filter()

    reviews = []
    reviews_collected = 0

    while reviews_collected < max_reviews:
        print(reviews_collected)
        # Wait for the reviews to load
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reviewText")))
        time.sleep(2)
        # Get all review containers
        review_containers = driver.find_elements(By.CSS_SELECTOR, ".ReviewText")
        
        for container in review_containers:
            # Find the element with the class 'Formatted' which contains the review text
            review_elements = container.find_elements(By.CSS_SELECTOR, ".Formatted")
            review_text = ' '.join([element.text for element in review_elements])
            
            reviews.append(review_text)
            reviews_collected += 1
            if reviews_collected >= max_reviews:
                break

        try:
            # Click the 'Show more reviews' button
            # Note: Replace 'show_more_reviews_button_selector' with the actual selector for the 'Show more reviews' button
            # more_reviews_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'Button--transparent')))
            more_reviews_button = driver.find_element(By.CSS_SELECTOR, ".Button--transparent")
            # apply_button = driver.find_element(By.XPATH, "//button[.//span[text()='Apply']]")
            # driver.execute_script("arguments[0].click();", filters_button)        

            driver.execute_script("arguments[0].scrollIntoView(true);", more_reviews_button)
            driver.execute_script("arguments[0].click();", more_reviews_button)
        except (NoSuchElementException, TimeoutException):
            # No more reviews to load
            break

        # It's a good idea to sleep for a short interval to avoid being rate-limited.
        time.sleep(5)

    return reviews
driver.quit()
