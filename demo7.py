#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


def canoo_data():
    competitors_size = requests.get('https://www.globaldata.com/company-profile/canoo-inc/').text
    soup_competitors = BeautifulSoup(competitors_size, 'lxml')
    
    trends=requests.get('https://www.greenlancer.com/post/ev-market-trends').text
    soup_trends=BeautifulSoup(trends, 'lxml')
    
    price_strategies=requests.get('https://www.marketsandmarkets.com/Market-Reports/electric-vehicle-market-209371461.html').text
    soup_price_strategies=BeautifulSoup(price_strategies, 'lxml')
    
    keyPlayers=requests.get('https://www.linkedin.com/pulse/electric-vehicles-market-insights-players-forecast-till/').text
    soup_keyPlayers=BeautifulSoup(keyPlayers, 'lxml')
    
    
    
    return soup_competitors, soup_trends, soup_price_strategies, soup_keyPlayers


# In[3]:


soup_competitors, soup_trends, soup_price_strategies, soup_keyPlayers = canoo_data()


# In[4]:


def gather_competitors_data(soup_competitors):
    competitors_list = []
    for i in soup_competitors.find_all('thead', class_='table-light'):
        competitors_data = i.text
        competitors_list.extend(competitors_data.strip().split('\n'))
    return competitors_list[1:6]


# In[5]:


def gather_trends_data(soup_trends):
    trends_list = []
    for i in soup_trends.find_all('h2'):
        trends_data = i.text.strip()
        trends_list.append(trends_data)
    return trends_list


# In[6]:


def gather_strategies_data(soup_price_strategies):
    strategies_list = []
    for i in soup_price_strategies.find_all('h2'):
        strategies_data = i.text.strip()
        strategies_list.append(strategies_data)
    return strategies_list


# In[7]:


def gather_key_players_data(soup_keyPlayers):
    key_players_list = []
    for i in soup_keyPlayers.find_all('p'):
        keyPlayers_data = i.text.strip()
        key_players_list.append(keyPlayers_data)
    return key_players_list


# In[8]:


def scrape_canoo_financial_data():
    yahoo_finance_url = 'https://finance.yahoo.com/quote/GOEV/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAFiI9m9Wd0J3vMCdI6YNr5CZGS6xAK_I-2Gcv_fr1a8tTQUpMjoe4dSS5DhhU-sVL_mU0n6ek6TQhrUE_Rje05NHK30N2erPPcITy_0mwIce5_5fBAoQhz0yCbQlC2NHcQB1o6qO12sd5hozrlhOe_riA6Qi0zNfoEoprPTq_agX'
    webpage = requests.get(yahoo_finance_url).text
    soup = BeautifulSoup(webpage, 'html.parser')

    revenue = soup.find('td', {'data-test': 'OPEN-value'}).text.strip()
    profit_margin = soup.find('td', {'data-test': 'OPEN-value'}).text.strip()

    return {
        'Revenue': revenue,
        'Profit Margin': profit_margin,
    }


# In[9]:


def gather_canoo_data():
    
    financial_data = scrape_canoo_financial_data()
    

    canoo_data = {}
    
    if financial_data:
        canoo_data.update(financial_data)
    

    return canoo_data


# In[10]:


competitors_list = gather_competitors_data(soup_competitors)
trends_list = gather_trends_data(soup_trends)
strategies_list=gather_strategies_data(soup_price_strategies)
key_players_list=gather_key_players_data(soup_keyPlayers)


# In[11]:


#df = pd.DataFrame({'Competitors': competitors_list, 'Trends': trends_list}).T
df = pd.DataFrame([competitors_list, trends_list, strategies_list, key_players_list])


# In[12]:


canoo_data = gather_canoo_data()
df_finance = pd.DataFrame({
    'Revenue': [canoo_data['Revenue']],
    'Profit Margin': [canoo_data['Profit Margin']]
})

# Concatenate the two DataFrames


# In[13]:


df


# In[14]:


df = df.T


# In[15]:


df.columns = ['Competitors', 'Trends', 'Strategies', 'Key Players']


# In[ ]:





# In[16]:


df = pd.concat([df, df_finance], axis=1)


# In[17]:


df


# In[19]:


df.to_csv('canoo_dataFrame.csv', index=False)


# In[ ]:




