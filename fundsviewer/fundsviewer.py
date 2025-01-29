#!/usr/bin/env python
#-*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import sys
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set different logging for this file
# see: https://stackoverflow.com/questions/8269294/python-logging-only-log-from-script
#logging = logging.getLogger(__name__)

##formatter = logging.Formatter(
    ##fmt="%(asctime)s %(levelname)s: %(message)s", 
    ##datefmt="%Y-%m-%d - %H:%M:%S"
##)
#console_handler = logging.StreamHandler(sys.stdout)
#console_handler.setLevel(logging.DEBUG)
##console_handler.setFormatter(formatter)

#logging.setLevel(logging.DEBUG)
#logging.addHandler(console_handler)



#import fundsviewer.fundsviewer_urls
URL_TEST = 'test'
URL_GENERALI = 'https://generali-investments.pl/contents/pl/klient-indywidualny/wyceny-funduszy-otwartych'


def webpage_driver(page_url: str):
    """
    Runs browser in headless mode and downloads
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.get(page_url)
    
    return driver


class FundWebsite(ABC):
    def __init__(self):
        self.web_url = None
        self.web_driver = None
        
    @abstractmethod
    def get_data(self):
        pass
    
    @property
    def page_source(self) -> str:
        return self.web_driver.page_source
    
    @staticmethod
    def webpage_driver(page_url: str):
        """
        Runs browser in headless mode and downloads
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        #options.headless = True  # NOTE: not working, see www.selenium.dev/blog/2023/headless-is-going-away/
        #options.add_argument('user-agent=')
        #options.add_argument('--disable-blink-features=AutomationControlled')
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.get(page_url)
        
        return driver


class GeneraliFundWebsite(FundWebsite):
    def __init__(self, page_url: str=URL_GENERALI):
        self.web_url = page_url
        self.web_driver = webpage_driver(self.web_url)
        self.fund_names = []
        self.data_urls = []
        self.dataframe = None
        
        try:
            logging.debug(f'Loading webpage {self.web_url}')
            WebDriverWait(self.web_driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME,"even"))
            )
        except Exception as e:
            raise e
            #logging.critical(e, exc_info=True)
            #logging.debug('Cannot load page')
    
    def get_data(self) -> pd.DataFrame:
        print(f'page status: {EC.presence_of_element_located((By.CLASS_NAME,"even"))}\n')
        logging.debug(f'page status: {EC.presence_of_element_located((By.CLASS_NAME,"even"))}\n')
        
        val_table = self.web_driver.find_elements(By.ID,"funds-valuations")[0]
        dummy_tx = val_table.text
        elements = val_table.find_elements(By.CLASS_NAME,"even")
        elements += val_table.find_elements(By.CLASS_NAME,"odd")

        
        # find link to 
        dfs = []
        for element in elements:
            dummy_tx = element.text
            
            # check if one can find link text and otherwise ignore element
            try:
                self.data_urls.append(
                    element.find_element(By.LINK_TEXT, "Pobierz wycenę").get_attribute("href")
                )
                if 'null' in self.data_urls[-1]:
                    raise ValueError
            except:
                continue
            
            # while link found put it to the list of links
            self.fund_names.append( element.text.split('\n')[0] )
            dfs.append( pd.read_csv(self.data_urls[-1], encoding='iso-8859-15', sep=';', decimal=',') )
            logging.debug(self.data_urls[-1], self.fund_names[-1])

        for df in dfs:
            df['Dzieñ wyceny'] = pd.to_datetime(df['Dzieñ wyceny'])

        self.dataframe = dfs[0]
        self.dataframe = self.dataframe.rename(columns={'Wycena' : self.fund_names[0]})
        for df, fdname in zip(dfs[1:], self.fund_names[1:]):
            self.dataframe = self.dataframe.merge(
                df.rename(columns={'Wycena' : fdname}),
                how='left',
                on='Dzieñ wyceny'
            )
        self.dataframe.rename(columns={'Dzieñ wyceny': 'Day'}, inplace=True)
        self.dataframe.set_index('Day', inplace=True)
        logging.debug('\nData loaded.')
        
        return self.dataframe
    
    def to_csv(self, path: str='.'):
        path += '/generali.csv'
        
        if self.dataframe is None:
            self.get_data()
        self.dataframe.to_csv(path)
    










# webpage structure?

#import networkx as nx
#from networkx.drawing.nx_pydot import graphviz_layout

"""
def bfs(t):
    # create graph and base node
    graph = nx.DiGraph()
    graph.add_node(1,tag=t.name)
    
    # create queue of tags to visit
    queue = [(t,1)]   # (tag, node id)
    while len(queue) > 0:
        cur_node = queue.pop(0)
        
        cnt = 1
        for tag in cur_node[0].find_all(recursive=False):
            queue.append( (tag,cur_node[1]+cnt) )
            graph.add_node(cur_node[1]+cnt,tag=tag.name)
            graph.add_edge(cur_node[1],cur_node[1]+cnt)
            cnt += 1
    return graph



def traverse(t, graph, current_path=None,current_node=1):
    if current_path is None:
        current_path = [t.name]
    
    graph.add_node(current_node)
    
    for tag in t.find_all(recursive=False):
        if not tag.find():
            print( " -> ".join(current_path + 
                               [tag.name, tag.find(text=True).strip()]) )
        else:
            traverse(tag, current_path + [tag.name],current_node=current_node+1)
    return graph
"""
