from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


def extract_contact_info(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    contact_info = {}
    # You need to adjust these selectors based on the actual page structure
    email_section = soup.find('div', attrs={'data-cy': 'emailSection'})
    contact_info['Work Email'] = email_section.text.strip() if email_section else 'Not available'

    office_number_section = soup.find('div', attrs={'data-cy': 'officeNumberSection'})
    contact_info['Office Number'] = office_number_section.text.strip() if office_number_section else 'Not available'

    mobile_number_section = soup.find('div', attrs={'data-cy': 'mobileNumberSection'})
    contact_info['Mobile Number'] = mobile_number_section.text.strip() if mobile_number_section else 'Not available'

    # work_location_section = soup.find('div', attrs={'data-cy': 'workLocationSection'})
    # contact_info['Work Location'] = work_location_section.text.strip() if work_location_section else 'Not available'

    return contact_info