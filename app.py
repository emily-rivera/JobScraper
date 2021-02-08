from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Scraping from Indeed.com
# gets the url string from the user input
def get_url(position, location, level):
    # url template for the job search
    url_template = 'https://www.indeed.com/jobs?q={}&l={}&explvl={}'
    # formats the url with the information
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = url_template.format(position, location, level)
    return url


def get_record(card):
    # get the job title
    if (card.find('h2', 'title')):
        job_title = card.h2.a.get('title')
    else:
        job_title = "No Job Title Found"
    # get the company name
    if (card.find('span', 'company')):
        company_title = (card.find('span', 'company').text.strip())
    else:
        company_title = "No Company Title Found"
    # get the job location
    if (card.find('div', 'recJobLoc')):
        job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    else:
        job_location = "No Job Location Found"
    # get the salary
    if (card.find('span', 'salaryText')):
        job_salary = card.find('span', 'salaryText').text.strip()
    else:
        job_salary = "No Salary Found"
    # get the job summary
    if (card.find('div', 'summary')):
        job_summary = card.find('div', 'summary').text.strip().replace('\n', ' ')
    else: 
        job_summary = "No Job Summary Found"

    record = (job_title, company_title, job_location, job_salary, job_summary)

    return record

def main(position, location, level):
    records = []
    url = get_url(position, location, level)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', 'jobsearch-SerpJobCard')

    for card in cards:
        record = get_record(card)
        records.append(record)

    return records

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        search_title = request.form["title"]
        search_location = request.form["location"]
        search_level = request.form["level"]

        url = get_url(search_title, search_location, search_level)

        records = main(search_title, search_location, search_level)

        return render_template("search_results.html", url=url, records=records)
    else:
        return render_template("index.html")

if __name__ == "__name__":
    app.run(debug=True)
