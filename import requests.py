from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

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

def scrape_linkedin(job_title, location):
    options = Options()
    options.headless = True  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
    driver.get(url)
    
    # Wait for the job listings to load
    time.sleep(5)
    
    jobs = []
    job_cards = driver.find_elements(By.CLASS_NAME, 'result-card')
    
    if not job_cards:
        print("No job cards found")
    
    for job_card in job_cards:
        try:
            title = job_card.find_element(By.CLASS_NAME, 'result-card__title').text.strip()
            company = job_card.find_element(By.CLASS_NAME, 'result-card__subtitle').text.strip()
            location = job_card.find_element(By.CLASS_NAME, 'job-result-card__location').text.strip()
            link = job_card.find_element(By.CLASS_NAME, 'result-card__full-card-link').get_attribute('href')
            jobs.append({'title': title, 'company': company, 'location': location, 'link': link})
        except Exception as e:
            print(f"Error parsing job card: {e}")
            continue
    
    driver.quit()
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

def filter_and_score_jobs(jobs):
    scored_jobs = []
    for job in jobs:
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
    
    if not linkedin_jobs:
        print("No jobs were scraped")
        return
    
    scored_jobs = filter_and_score_jobs(linkedin_jobs)
    
    if not scored_jobs:
        print("No jobs were scored")
        return
    
    df = pd.DataFrame(scored_jobs)
    df.to_csv('linkedin_jobs_scored.csv', index=False)

if __name__ == "__main__":
    main()
