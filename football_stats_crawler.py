# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 18:10:42 2022

@author: toddm
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time
import random
import os

# class Crawler:
    
#     def getPage(self, url):
#         try: 
#             req = requests.get(url)
#         except requests.exceptions.RequestException:
#             return None
#         return BeautifulSoup(req.text, 'hmtl.parser')
    
#     def safeGet(self, page)
    

#parse table

class fantasy_crawler:
    
    def __init__(self, domain = 'https://www.fantasypros.com'):
        self.domain = domain
    
    def req_url(self, url, show_urls = True):
        if show_urls:
            print(url)
        req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        self.bs = BeautifulSoup(webpage, 'html.parser')
        #self.bs
        
        
    def parse_table(self)->pd.core.frame.DataFrame:
        #print(self.bs)
        table = self.bs.find('table', {'id':'data'})
        rows = table.findAll('tr')
        player_stats = []
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            player_stats.append([ele for ele in cols if ele])
            
        table_headers = table.findAll('th')
        labels = [label.text.strip() for label in table_headers]

        roster_stats = pd.DataFrame(player_stats, columns=labels)        
        roster_stats.dropna(axis=0, inplace=True)
        
        return roster_stats
        

    
    def get_years(self):
        selection_tab = self.bs.find('select', {'class', 'select-links'})
        options = selection_tab.findAll('option')
        years_value = [years.text for years in options]
        years_path = [years['value'] for years in options]
        return {'years':years_value, 'years_path': years_path}
    
    def get_categories(self):
        categories = []
        categories_path = []
        options_bar = self.bs.find('ul', {'class', 'pills pills--horizontal desktop-pills'})
        options = options_bar.findAll('a')
        for option in options:
            path = option['href']
            categories.append(option.text)
            categories_path.append(self.domain +  path)
            
        return {'categories':categories, 'categories_path':categories_path}
        
    
    def random_delay(self, min_time:float = 1, max_possible:float=5):
        """Used to confuse site AI bots as to whether
        this is a bot or not."""
        sleep_time = min_time + random.random()*(max_possible-min_time)
        print(f'Waiting for: {sleep_time}')
        time.sleep(sleep_time)
    
    def crawl_years(self):
        years = self.get_years()
        links = [self.domain + path for path in years['years_path']]
        
        years_rosters = []
        for i in range(len(links)):
            link = links[i] #link to query
            year = years['years'][i] #years of the queried table
            self.req_url(link) #query link
            table = self.parse_table() #parse stats table

            #insert indicator for the year for this data for the player
            table.insert(1, 'year', [year]*len(table)) 
            # self.random_delay()
            years_rosters.append(table)
            
        self.data = {'years':years['years'], 'years_rosters':years_rosters}
        
    def get_all_players_names(self)->list:
        # years = self.data['years']
        dfs = self.data['years_rosters'] #get the rosters from every year
        non_unique_players = np.concatenate([df['Player'] for df in dfs]) #concatenate all the rosters
        all_players = np.unique(non_unique_players) #identify only unique players in the roster
        
        return all_players
    
    def group_player_history(self)->list:
        
        data_concat = pd.concat(self.data['years_rosters'],ignore_index=True)
        
        
        players_stats_grouped = list(data_concat.groupby('Player'))
        
        #produces packets of [{player name}, {df}]
        return players_stats_grouped
        
        
    def store_data(self, file_name = 'NFL'):
        #store data by: {sport}/{position} -> df by {player}/{year}
        grouped_history = self.group_player_history()
        
        # group_name = r'qb' ###################################################CHANGE THIS IN FINAL RUN
        group_name = self.bs.find('li', {'class', 'active'}).text
        
        
        #Build folder to store data in
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, group_name)
        if not os.path.exists(final_directory):
           os.makedirs(final_directory)
        
        #put files into folder
        for packet in grouped_history:
            player_name = packet[0]
            player_stats = packet[1]
            file_name = f'{player_name}.csv'
            
            path = os.path.join(final_directory,file_name)
            player_stats.to_csv(path,index=False)
            
        
    
#%%         
        
qb = fantasy_crawler()
qb.req_url('https://www.fantasypros.com/nfl/stats/qb.php')
qb.crawl_years()
qb.store_data()
#%%
dfs = qb.data['years_rosters']

df = qb.data['years_rosters'][0]

rb = fantasy_crawler()
rb.req_url('https://www.fantasypros.com/nfl/stats/rb.php')
rb.crawl_years()
rb.store_data()

wr = fantasy_crawler()
wr.req_url('https://www.fantasypros.com/nfl/stats/wr.php')
wr.crawl_years()
wr.store_data()

te = fantasy_crawler()
te.req_url('https://www.fantasypros.com/nfl/stats/te.php')
te.crawl_years()
te.store_data()

k = fantasy_crawler()
k.req_url('https://www.fantasypros.com/nfl/stats/k.php')
k.crawl_years()
k.store_data()

dst = fantasy_crawler()
dst.req_url('https://www.fantasypros.com/nfl/stats/dst.php')
dst.crawl_years()
dst.store_data()

dl = fantasy_crawler()
dl.req_url('https://www.fantasypros.com/nfl/stats/dl.php')
dl.crawl_years()
dl.store_data()

lb = fantasy_crawler()
lb.req_url('https://www.fantasypros.com/nfl/stats/lb.php')
lb.crawl_years()
lb.store_data()

db = fantasy_crawler()
db.req_url('https://www.fantasypros.com/nfl/stats/db.php')
db.crawl_years()
db.store_data()
#%%



"""
Referances:
https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
https://stackoverflow.com/questions/21185585/pandas-concatenating-conditioned-on-unique-values
https://stackoverflow.com/questions/51004029/create-a-new-dataframe-based-on-rows-with-a-certain-value
https://thispointer.com/python-how-to-create-a-list-and-initialize-with-same-values/
https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/





"""