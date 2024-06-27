from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup

positive_keywords = {
    'software developer': 10,
    'frontend developer': 8,
    'backend developer': 8,
    'ios developer': 9,
}

negative_keywords = {
    'senior': -10,
    'lead': -8,
    'cloud': -5,
}

experience_filter = {
    "3+ years": True,
    "more than three years": True,
    "over 3 years": True,
    "three to five years": True,
    "3-5 years": True,
    "3 to 5 years": True,
    "4+ years": True,
    "4-6 years": True,
    "5+ years": True,
    "5-7 years": True,
    "5 to 7 years": True,
    "six years": True,
    "more than 3 years": True,
    "several years": True,
    "senior": True,
    "advanced experience": True,
}

exclude_cities = {
    "queensland": True,
    "sydney": True,
    "canberra": True,
    "perth": True,
    "brisbane": True,
    "adelaide": True,
    "darwin": True,
    "hobart": True
}

include_keywords = {
    "melbourne": True,
    "remote": True,
    "work from home": True,
    "telecommute": True,
    "virtual position": True,
    "flexible location": True,
    "nationwide": True,
    "work anywhere": True,
    "location flexible": True,
    "location independent": True,
    "distributed team": True,
    "global team": True,
    "remote option": True,
    "anywhere in australia": True
}

def scrape_linkedin(job_title, location):
    options = Options()
    options.headless = True  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
    driver.get(url)
    
    # Wait for the job listings to load
    time.sleep(5)
    
    jobs = []
    job_cards = driver.find_elements(By.CSS_SELECTOR, '.jobs-search__results-list li')
    
    if not job_cards:
        print("No job cards found on LinkedIn")
    
    for job_card in job_cards:
        try:
            title = job_card.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title').text.strip()
            company = job_card.find_element(By.CSS_SELECTOR, 'h4.base-search-card__subtitle').text.strip()
            location = job_card.find_element(By.CSS_SELECTOR, 'span.job-search-card__location').text.strip()
            link = job_card.find_element(By.CSS_SELECTOR, 'a.base-card__full-link').get_attribute('href')
            
            # Navigate to the job detail page to get the job description
            driver.get(link)
            time.sleep(3)  # Wait for the job description to load
            
            job_description = driver.find_element(By.CSS_SELECTOR, 'div.jobs-description__content').text.strip()
            
            jobs.append({'title': title, 'company': company, 'location': location, 'link': link, 'description': job_description})
            
            # Navigate back to the job listings page
            driver.back()
            time.sleep(3)
        except Exception as e:
            print(f"Error parsing job card on LinkedIn: {e}")
            continue
    
    driver.quit()
    return jobs

def scrape_seek(job_title, location):
    url = f"https://www.seek.com.au/{job_title}-jobs/in-{location}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from Seek: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = []
    job_cards = soup.find_all('div', {'data-automation': 'jobCard'})

    if not job_cards:
        print("No job cards found on Seek")

    for job_card in job_cards:
        try:
            title = job_card.find('a', {'data-automation': 'jobTitle'}).get_text(strip=True)
            company = job_card.find('span', {'class': 'job-company'}).get_text(strip=True)
            location = job_card.find('div', {'data-automation': 'jobCard-location'}).get_text(strip=True)
            link = 'https://www.seek.com.au' + job_card.find('a', {'data-automation': 'jobTitle'})['href']
            job_description = job_card.find('div', {'data-automation': 'jobShortDescription'}).get_text(strip=True)
            jobs.append({'title': title, 'company': company, 'location': location, 'link': link, 'description': job_description})
        except Exception as e:
            print(f"Error parsing job card on Seek: {e}")
            continue
    
    return jobs

def scrape_jora(job_title, location):
    url = f"https://au.jora.com/j?q={job_title}&l={location}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from Jora: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = []
    job_cards = soup.find_all('div', class_='job-card')

    if not job_cards:
        print("No job cards found on Jora")

    for job_card in job_cards:
        try:
            title = job_card.find('a', class_='job-link').get_text(strip=True)
            company = job_card.find('span', class_='job-company').get_text(strip=True)
            location = job_card.find('a', class_='job-location').get_text(strip=True)
            link = 'https://au.jora.com' + job_card.find('a', class_='job-link')['href']
            job_description = job_card.find('div', class_='job-abstract').get_text(strip=True)
            jobs.append({'title': title, 'company': company, 'location': location, 'link': link, 'description': job_description})
        except Exception as e:
            print(f"Error parsing job card on Jora: {e}")
            continue
    
    return jobs

def score_job(title):
    score = 0
    for word, points in positive_keywords.items():
        if word.lower() in title.lower():
            score += points
    for word, points in negative_keywords.items():
        if word.lower() in title.lower():
            score += points
    return score

def filter_jobs(jobs):
    filtered_jobs = []

    for job in jobs:
        description = job['description'].lower()
        location = job['location'].lower()
        
        # Exclude based on experience
        exclude = any(term.lower() in description for term in experience_filter)
        
        # Check for exclusion cities unless remote
        exclude_city = any(city.lower() in location for city in exclude_cities)
        include = any(keyword.lower() in description for keyword in include_keywords)
        
        if exclude and not include:
            continue
        
        if exclude_city and not include:
            continue

        filtered_jobs.append(job)

    return filtered_jobs

def filter_and_score_jobs(jobs):
    filtered_jobs = filter_jobs(jobs)
    scored_jobs = []
    for job in filtered_jobs:
        score = score_job(job['title'])
        if score > 0:
            job['score'] = score
            scored_jobs.append(job)
    scored_jobs.sort(key=lambda x: x['score'], reverse=True)
    return scored_jobs

def main():
    job_title = 'software developer'
    location = 'Melbourne'
    
    linkedin_jobs = scrape_linkedin(job_title, location)
    seek_jobs = scrape_seek(job_title, location)
    jora_jobs = scrape_jora(job_title, location)
    
    all_jobs = linkedin_jobs + seek_jobs + jora_jobs
    
    if not all_jobs:
        print("No jobs were scraped")
        return
    
    scored_jobs = filter_and_score_jobs(all_jobs)
    
    if not scored_jobs:
        print("No jobs were scored")
        return
    
    df = pd.DataFrame(scored_jobs)
    df.to_csv('jobs_scored.csv', index=False)

if __name__ == "__main__":
    main()
