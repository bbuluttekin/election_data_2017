#! /usr/bin/ python

#Python script to get opinion polls dataset

import requests
import bs4 as bs
import pandas as pd

url = 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_United_Kingdom_general_election,_2017'
respond = requests.get(url)
soup = bs.BeautifulSoup(respond.text, 'lxml')

tables = soup.find_all('table')
table = tables[1]

df_opinion = pd.DataFrame()

#Getting year 2017
print('Getting year 2017')
rows_2017 = 0
for i, row in enumerate(tables[0].find_all('tr')):
    if len(row) != 23:
        
        continue
    if i == 0:
        df_opinion = pd.DataFrame(columns=[[_.text for _ in row.find_all('th')] + ['Year']])
        continue
    df_opinion.loc[i] = [_.text for _ in row.find_all('td')] + [int(2017)]
    rows_2017 += 1

#Getting year 2016
print('Getting year 2016')
rows_2016 = 0
for i, row in enumerate(tables[1].find_all('tr')):
    if len(row) != 23:
        continue
    if i == 0:
        continue
    df_opinion.loc[i + 1000] = [_.text for _ in row.find_all('td')] + [int(2016)]
    rows_2016 += 1


# Getting year 2015
print('Getting year 2015')
rows_2015 = 0
for i, row in enumerate(tables[2].find_all('tr')):
    if len(row) != 23:
        continue
    if i == 0:
        continue
    df_opinion.loc[i + 2000] = [_.text for _ in row.find_all('td')] + [int(2015)]
    rows_2015 += 1

    
# Logic Validation
if rows_2015 + rows_2016 + rows_2017 == len(df_opinion):
    print('Download Successful!')
else:
    print('Data inconsistent!')
    
    
# Get rid of special characters
for i in df_opinion.columns[3:-1]:
    df_opinion[i] = ([_.split('%')[0] for _ in df_opinion[i]])
    
df_opinion['Sample size'] = [int("".join([_.split(',')[0], _.split(',')[1]])) for _ in df_opinion['Sample size']]


#Remove NA substitutes
def test_apply(x):
    try:
        return float(x)
    except ValueError:
        return None

for i in df_opinion.columns[3:-1]:
    df_opinion[i] = df_opinion[i].apply(test_apply)


df_opinion.to_csv('opinion_polls.csv', index=False)