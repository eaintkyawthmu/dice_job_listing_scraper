from bs4 import BeautifulSoup

def parse_job_page(soup):
    # Basic Job Information Extraction
    job_title_element = soup.find('h1', {'data-cy': 'jobTitle'})
    job_title = job_title_element.text.strip() if job_title_element else 'Not Available'

    company_name_element = soup.find('a', {'data-cy': 'companyNameLink'})
    company_name = company_name_element.text.strip() if company_name_element else 'Not Available'
    company_link = company_name_element['href'].strip() if company_name_element else 'Not Available'

    location_element = soup.find('li', {'data-cy': 'location'})
    location = location_element.text.strip() if location_element else 'Not Available'

    posted_date_element = soup.find('li', {'data-cy': 'postedDate'})
    posted_date = posted_date_element.text.split('|')[0].strip() if posted_date_element else 'Not Available'

    # Overview Extraction
    overview_details = get_job_overview(soup)
    recruiter_info = recruiter_details(soup)

    # Combine basic info and overview details
    job_data = {
        'Job Title': job_title,
        'Company Name': company_name,
        'Company Link': company_link,
        'Location': location,
        'Posted Date': posted_date,
    }
    job_data.update(overview_details)  # Merge overview details into the job data dictionary
    job_data.update(recruiter_info)  # Merge recruiter info into the job data dictionary

    return job_data

def get_job_overview(soup):
    detail_containers = soup.find_all('div', {'class': 'job-overview_detailContainer__TpXMD'})
    details = {}

    for container in detail_containers:
        chips = container.find_all('div', {'class': 'chip_chip__cYJs6'})
        for chip in chips:
            text = chip.text.strip()
            if 'Contract' in text:
                details['Employment Type'] = text
            elif '$' in text:
                details['Pay'] = text
            elif 'Hybrid' in text or 'days' in text:
                details['Work Arrangement'] = text  # Changed to 'Work Arrangement' for clarity
            elif 'Travel' in text:
                details['Travel Requirements'] = text

    skills_section = soup.find('div', {'class': 'Skills_chipContainer__mlLa7'})
    if skills_section:
        skills_chips = skills_section.find_all('div', {'class': 'chip_chip__cYJs6'})
        details['Primary Skill Set'] = [chip.text.strip() for chip in skills_chips] if skills_chips else 'Not Available'

    job_details_section = soup.find('div', {'class': 'job-description'})
    if job_details_section:
        details['Job Description'] = job_details_section.text.strip()
    else:
        details['Job Description'] = 'Not Available'

    return details


def recruiter_details(soup):
    recruiter_section = soup.find('div', {'data-cy': 'recruiterProfileWidget'})
    if recruiter_section:
        recruiter_name = recruiter_section.find('p', {'data-cy': 'recruiterName'}).text.strip()
        recruiter_company = recruiter_section.find('p', {'data-cy': 'recruiterCompany'}).text.strip()
        recruiter_data = {
            'Recruiter Name': recruiter_name,
            'Recruiter Company': recruiter_company,
        }
    else:
        recruiter_data = {
            'Recruiter Name': 'Not Available',
            'Recruiter Company': 'Not Available',
        }
    return recruiter_data
