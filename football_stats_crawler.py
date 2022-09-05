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
    def req_url(self, url, show_urls = True):
        if show_urls:
            print(url)
        req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        self.bs = BeautifulSoup(webpage, 'html.parser')
        #self.bs
        
        
    def parse_table(self):
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

        return {'labels':labels, 'player_stats': player_stats}        
        # df = pd.DataFrame(players)
        # df.columns = labels
        # df.dropna(axis=0, inplace=True)
        

    
    def get_years(self):
        selection_tab = self.bs.find('select', {'class', 'select-links'})
        options = selection_tab.findAll('option')
        years_value = [years['value'] for years in options]
        years_path = [years['value'] for years in options]
        return {'years':years_value, 'years_path': years_path}
    
    def random_delay(self, min_time:float = 1, max_possible:float=5):
        """Used to confuse site AI bots as to whether
        this is a bot or not."""
        sleep_time = min_time + random.random()*(max_possible-min_time)
        print(f'Waiting for: {sleep_time}')
        time.sleep(sleep_time)
    
    def crawl_years(self):
        domain = 'https://www.fantasypros.com'
        years = self.get_years()
        links = [domain + path for path in years['years_path']]
        
        tables = []
        for link in links:
            # self.random_delay()
            self.req_url(link)
            tables.append(self.parse_table())
            
        self.data = {'years':self.get_years()['years'], 'data':tables}
        
        
qb = fantasy_crawler()
qb.req_url('https://www.fantasypros.com/nfl/stats/qb.php')
qb.crawl_years()

rb = fantasy_crawler()
rb.req_url('https://www.fantasypros.com/nfl/stats/rb.php')
rb.crawl_years()

wr = fantasy_crawler()
wr.req_url('https://www.fantasypros.com/nfl/stats/wr.php')
wr.crawl_years()

te = fantasy_crawler()
te.req_url('https://www.fantasypros.com/nfl/stats/te.php')
te.crawl_years()

k = fantasy_crawler()
k.req_url('https://www.fantasypros.com/nfl/stats/k.php')
k.crawl_years()

dst = fantasy_crawler()
dst.req_url('https://www.fantasypros.com/nfl/stats/dst.php')
dst.crawl_years()

dl = fantasy_crawler()
dl.req_url('https://www.fantasypros.com/nfl/stats/dl.php')
dl.crawl_years()

lb = fantasy_crawler()
lb.req_url('https://www.fantasypros.com/nfl/stats/lb.php')
lb.crawl_years()

db = fantasy_crawler()
db.req_url('https://www.fantasypros.com/nfl/stats/db.php')
db.crawl_years()

#%%



"""
Referances:
https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table




"""