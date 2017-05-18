#! /usr/bin/ python

#Python script to get opinion polls dataset

import requests
import bs4 as bs
import pandas as pd


def main(full_path='.', return_df=False):
    '''
    Function to scrape and download or return as data frame of the opinion pools data for
    2017 uk general election

    variables:
    ----------
    full_path: Enter the full path for directory you wish to download to defult is current directory
    return_df: Boolean value, set true to return the dataset.

    '''
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
    assert rows_2015 + rows_2016 + rows_2017 == len(df_opinion), print('Data inconsistent!')
    print('Download Successful!')

    # Get rid of special characters
    for i in df_opinion.columns[3:-1]:
        df_opinion[i] = ([_.split('%')[0] for _ in df_opinion[i]])

    df_opinion['Sample size'] = [int("".join(_.split(','))) for _ in df_opinion['Sample size']]


    #Remove NA substitutes
    def test_apply(x):
        try:
            return float(x)
        except ValueError:
            return None

    for i in df_opinion.columns[3:-1]:
        df_opinion[i] = df_opinion[i].apply(test_apply)

    if return_df:
        return df_opinion
    else:
        df_opinion.to_csv("/".join([full_path, 'opinion_polls.csv']), index=False)


if __name__ == '__main__':
    main()
