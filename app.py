from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
from job_details import parse_job_page  # Ensure this is correctly defined
from recruiter import extract_contact_info  # Ensure this is correctly defined

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# Uncomment the next line to run Chrome in headless mode for faster execution
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")

webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

driver.get('https://www.dice.com/jobs')
driver.maximize_window()
driver.delete_all_cookies()
time.sleep(20)

# Perform search
driver.find_element(By.ID, "typeaheadInput").send_keys("Data Analyst")
driver.find_element(By.ID, "google-location-search").send_keys("United States")
driver.find_element(By.ID, "submitSearch-button").click()
time.sleep(10)

# Filter search results
posted_date_section = driver.find_element(By.CSS_SELECTOR, 'dhi-accordion[data-cy="accordion-postedDate"]')
date_button = posted_date_section.find_element(By.CSS_SELECTOR, 'button[data-cy-index="1"]').click()

employment_type_section = driver.find_element(By.CSS_SELECTOR, 'dhi-accordion[data-cy="accordion-employmentType"]')
driver.execute_script("arguments[0].scrollIntoView();", employment_type_section)
employment_type_button = employment_type_section.find_element(By.CSS_SELECTOR, 'li[data-cy-value="CONTRACTS"] button').click()

driver.execute_script("window.scrollTo(0, 0);")

jobs_data = []
while True:
    job_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.card-title-link'))
    )
    main_window_handle = driver.current_window_handle

    for i, job_card in enumerate(job_cards):
        try:
            driver.execute_script("arguments[0].click();", job_cards[i])
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            driver.switch_to.window([handle for handle in driver.window_handles if handle != main_window_handle][0])
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_data = parse_job_page(soup)  # Ensure your parsing logic is correctly defined in the function

            # Attempt to click the "View Profile" button and extract recruiter info
            try:
                view_profile_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "dhi-seds-core-button.hydrated"))
                )
                view_profile_button.click()
                time.sleep(5)  # Adjust as needed

                recruiter_info = extract_contact_info(driver)  # Ensure this function is correctly defined
                job_data.update(recruiter_info)
            except Exception as e:
                print(f"No recruiter info")

            driver.close()
            driver.switch_to.window(main_window_handle)
            time.sleep(5)

            job_cards = driver.find_elements(By.CSS_SELECTOR, 'a.card-title-link')  # Re-fetch the job cards to avoid stale elements
            driver.execute_script("arguments[0].scrollIntoView();", job_cards[i+1])
            jobs_data.append(job_data)

            jobs_df = pd.DataFrame(jobs_data)
            jobs_df.to_csv('dice_listings.csv', index=False)
       
        except Exception as e:
            # print(f"Error processing job card: {e}")
            driver.switch_to.window(driver.window_handles[0])
            continue

    try:
        next_page_button = driver.find_element(By.CSS_SELECTOR, 'li.pagination-next.page-item.ng-star-inserted a')
        if "disabled" in next_page_button.get_attribute("class"):
            print("Reached the last page.")
            break
        next_page_button.click()
        print("Moving to the next page.")
        time.sleep(5)  # Adjust based on page load times
    except NoSuchElementException:
        print("No 'Next' button found. End of pages.")
        break
    except TimeoutException:
        print("Timed out waiting for the 'Next' button. End of pages.")
        break

driver.quit()