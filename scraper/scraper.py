import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_indeed_jobs(keyword="python developer", pages=2):
    base_url = "https://pk.indeed.com/jobs?l=karachi&from=mobRdr&utm_source=%2Fm%2F&utm_medium=redir&utm_campaign=dt&vjk=507726b3a828652f"
    job_list = []

    for page in range(0, pages * 10, 10):
        params = {
            "q": keyword,
            "start": page
        }
        response = requests.get(base_url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="job_seen_beacon")

        for job in results:
            title = job.find("h2").text.strip() if job.find("h2") else None
            company = job.find("span", class_="companyName").text.strip() if job.find("span", class_="companyName") else None
            location = job.find("div", class_="companyLocation").text.strip() if job.find("div", class_="companyLocation") else None
            date_posted = job.find("span", class_="date").text.strip() if job.find("span", class_="date") else None

            job_list.append({
                "title": title,
                "company": company,
                "location": location,
                "date_posted": date_posted,
                "source": "Indeed"
            })

        time.sleep(2)  # polite scraping

    df = pd.DataFrame(job_list)
    df.to_csv("jobs.csv", index=False)
    return df
