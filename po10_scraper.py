import requests
import time
from bs4 import BeautifulSoup
import random
import csv
import pickle
import pandas as pd
import sys


def fetch(year, sex, event):
    URL = 'https://thepowerof10.info/rankings/rankinglist.aspx?'
    args = {'event': event, 'agegroup': 'ALL', 'sex': sex, 'year': year}
    r = requests.get(URL, params=args)
    html_text = r.text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


def scrape(year, sex, event):

    rankings = []

    print(f'Scraping {event}{sex} from {year}...')
    year = int(float(year))
    soup = fetch(year, sex, event)
    for item in soup.findAll('tr', {'class': ['rlr', 'rlra']}):
        # todo fix scraper so doesn't mess up badly formatted dates via regex
        ranking = item.select('td')[0].text
        time = item.select('td')[1].text
        club = item.select('td')[10].text
        date = item.select('td')[12].text
        if date[1] == ' ':
            date = '0' + date
        date = date[:7] + '20' + date[7:9]
        namerow = item.select('td')[6]
        if namerow.find('a') is None:
            continue
        else:
            name = namerow.find('a').text

        rankings.append({'sex': sex, 'event': event, 'ranking': ranking, 'time': time, 'name': name,
                         'club': club, 'date': date})

    return rankings


if __name__ == '__main__':
    years = range(2006, 2019)
    # years = range(2018, 2019)
    events = ['800', '1500', '3000', '5000', '10000']
    # events = ['1500']
    sexes = ['M', 'W']
    # sexes = ['M']
    data = []
    for sex in sexes:
        for event in events:
            for year in years:
                rankings = scrape(year, sex, event)
                for entry in rankings:
                    data.append(entry)
    keys = data[0].keys()
    with open('data.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writerows(data)
