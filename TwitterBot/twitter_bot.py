#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import sys, getopt
import csv
from datetime import date 



# # Stats & Graphs
# Max chances created


# In[2]:


def get_array(n,x,y):
    list = []
    rows_player = n.find_all('tr')
    tds = rows_player[0].find_all('td')
    for i in range(x,y):
        list.append(tds[i].get('data-stat'))
    return list 


# In[3]:


def get_tables(url,text,table):
    res = requests.get(url)
    ## The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("",res.text),'lxml')
    all_tables = soup.findAll("tbody")
    
    team_table = all_tables[0]
    team_vs_table = all_tables[1]
    
    player_table = all_tables[2]
    return team_table


# In[4]:


def get_frame(features_array, table):
    pre_df_player = dict()
    features_wanted_player = features_array
    rows_player = table.find_all('tr')
#     print(features_wanted_player)
    for row in rows_player:
        if(row.find('th',{"scope":"row"}) != None):
            for f in features_wanted_player:
                if f != "player":
#                     print(f)
                    cell = row.find("td",{"data-stat": f})
#                     print(cell)
                    text = cell.renderContents().strip().decode("utf-8")
#                     print(text)
                    if(text == ''):
                        text = '0'
                    if((f!='player')&(f!='club')&(f!='position')&(f!='squad')&(f!='age')&(f!='birth_year')):
                        text = float(text.replace(',',''))
                    if f in pre_df_player:
                        pre_df_player[f].append(text)
                    else:
                        pre_df_player[f] = [text]
                else: 
                        cell = row.find("th",{"data-stat": f})
                        text = cell.text
                        if(text == ''):
                            text = '0'
                        if((f!='player')&(f!='club')&(f!='position')&(f!='squad')&(f!='age')&(f!='birth_year')):
                            text = float(text.replace(',',''))
                        if f in pre_df_player:
                            pre_df_player[f].append(text)
                        else:
                            pre_df_player[f] = [text]
               
                    
    df_player = pd.DataFrame.from_dict(pre_df_player)
    return df_player


# In[5]:


def frame_for_category(url,features_array,table):

    df_player = get_frame(features_array, table)
    return df_player


# In[6]:


def get_data(url,features_array,table):
    df1 = frame_for_category(url,features_array,table)
    return df1


# In[7]:


def make_table(a,url,features_array,table):
    x = get_data(url,features_array,table)
    x.to_csv(a,index=False)
    return x


# In[8]:


# Get player name 
def get_name(table):
    pre_df_player = {}
    pre_df_player["player"] = []
    rows_player = table.find_all('tr')
#     print(features_wanted_player)
    for row in rows_player:
#         a = row.find('th',{"scope":"row"})
#         print(a)
        b = row.find("th",{"data-stat": "player"})
        
        c = b.find("a").text
        pre_df_player["player"].append(c)
        
    return pre_df_player


# In[9]:


res1 = requests.get(r"https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures")
## The next two lines get around the issue with comments breaking the parsing.
comm = re.compile("<!--|-->")
soup = BeautifulSoup(res1.text,'html.parser')
all_tables = soup.findAll("tbody")
all_tables
matches = all_tables[0]

rows = matches.find_all('td', {'data-stat': 'date'})


# In[10]:


matches = []
for i in rows: 
    
    a = i.find_all("a", text=str(date.today()))
    if a:
        matches.append(i.parent())
        


# In[11]:


big_teams = ["Liverpool","Chelsea","Manchester Utd","Manchester City","Newcastle Utd","Arsenal","Tottenham"]
home_list = []
away_list = []


for i in matches:
    i = str(i)
    soup1 = BeautifulSoup(i,'html.parser')
    
    
#     k =.find_all("td")
#     print(k)
    
    home = soup1.find('td',{'data-stat':'home_team'})
    away = soup1.find('td',{'data-stat':'away_team'})
#     print(away.find('a'))
#     print(home.find('a'))
    if home.find('a').text in big_teams:
        home_list.append(home.parent)
    if away.find('a').text in big_teams:
        away_list.append(away.parent)

req_matches = list(set(home_list + away_list))
 

    


# In[12]:


# Get Match Link

match_links = []

for m in req_matches:
    tag = m.find_all('td',{'data-stat':'score'})
    tag = str(tag)
    tag = BeautifulSoup(tag,'html.parser')
    
    f = tag.a['href']
    final_link = "https://fbref.com" + f
    match_links.append(final_link)


# In[ ]:





# In[ ]:


res = requests.get(match_links[0])
url = requests.get(match_links[0])

    ## The next two lines get around the issue with comments breaking the parsing.
comm = re.compile("<!--|-->")
soup = BeautifulSoup(comm.sub("",res.text),'lxml')
all_tables = soup.findAll("tbody")
t1 = all_tables[0]

t2 = all_tables[1]
t3 = all_tables[2]
t4 = all_tables[3]
t5 = all_tables[4]
t6 = all_tables[5]
t7 = all_tables[6]
t8 = all_tables[7]
t9 = all_tables[8]
t10 = all_tables[9]
t11 = all_tables[10]
t12 = all_tables[11]
t13 = all_tables[12]
t14 = all_tables[13]


passing = get_array(t2,4,26)
passing_types = get_array(t3,4,19)
def_actions = get_array(t4,4,20)
poss = get_array(t5,4,18)
misc = get_array(t6,4,20)
summary = ['goals','assists','shots','shots_on_target','xg','npxg','xg_assist']
keeper = get_array(t14,1,23)


# In[ ]:


h_names = pd.DataFrame.from_dict(get_name(t1))
a_names = pd.DataFrame.from_dict(get_name(t11))


# In[ ]:


x = get_data(url,summary,t1)
Summary = get_data(url,summary,t1)
A_passing = get_data(url,passing,t2)
A_passing_types = get_data(url,passing_types,t3)
A_def_actions = get_data(url,def_actions,t4)
A_poss = get_data(url,poss,t5)
A_misc = get_data(url,misc,t6)
A_keeper = get_data(url,keeper,t7)

B_Summary = get_data(url,summary,t8)
B_passing = get_data(url,passing,t9)
B_passing_types = get_data(url,passing_types,t10)
B_def_actions = get_data(url,def_actions,t11)
B_poss = get_data(url,poss,t12)
B_misc = get_data(url,misc,t13)
B_keeper = get_data(url,keeper,t14)


Summary = pd.DataFrame.from_dict(Summary)
A_passing = pd.DataFrame.from_dict(A_passing)
A_passing_types = pd.DataFrame.from_dict(A_passing_types)
A_def_actions = pd.DataFrame.from_dict(A_def_actions)
A_poss = pd.DataFrame.from_dict(A_poss)
A_misc = pd.DataFrame.from_dict(A_misc )
A_keeper = pd.DataFrame.from_dict(A_keeper)

B_Summary = pd.DataFrame.from_dict(B_Summary)
B_passing = pd.DataFrame.from_dict(B_passing)
B_passing_types = pd.DataFrame.from_dict(B_passing_types)
B_def_actions = pd.DataFrame.from_dict(B_def_actions)
B_poss = pd.DataFrame.from_dict(B_poss)
B_misc = pd.DataFrame.from_dict(B_misc)
B_keeper = pd.DataFrame.from_dict(B_keeper)


# In[ ]:


A_Summary = pd.concat([h_names, Summary],axis = 1)
A_passing = pd.concat([h_names, A_passing],axis = 1)
A_passing_types = pd.concat([h_names, A_passing_types],axis = 1)
A_def_actions = pd.concat([h_names, A_def_actions],axis = 1)
A_poss = pd.concat([h_names, A_poss],axis = 1)
A_misc = pd.concat([h_names, A_misc],axis = 1)
A_keeper = pd.concat([h_names, A_keeper],axis = 1)
B_Summary = pd.concat([a_names, B_Summary],axis = 1)
B_passing = pd.concat([a_names, B_passing],axis = 1)
B_passing_types = pd.concat([a_names, B_passing_types],axis = 1)
B_def_actions = pd.concat([a_names, B_def_actions],axis = 1)
B_poss = pd.concat([a_names, B_poss],axis = 1)
B_misc = pd.concat([a_names, B_misc],axis = 1)
B_keeper = pd.concat([a_names, B_keeper],axis = 1)


# In[ ]:





# Graphs Required 
# 
# 1. npxg with number of goals scored
# 2. short long medium passes
# 3. passes into final third 
# 4. def actions 
# 5. most overall gifted player

# In[ ]:


import matplotlib.pyplot as plt 

# Most goals with npxg 
def post(n):
    a= n['npxg'].idxmax()
    x = n['npxg'].max()
    
    

# Get the name of the person at that index
    name = n.loc[a, 'player']
    goals = n.loc[a, 'goals']
#      c = x.iloc[6]
#      print(x)
    return name,goals,x
    


a,b,c = post(A_Summary)


# In[ ]:


prim = f"{a} had the highest non-penalty xg of {c}, scoring {int(b)} goals "


# In[ ]:


from twython import Twython

consumer_key = "IHUm2jJFQ2139miHpK8QrjbNR"
consumer_secret = "DDIMEUusBqYpRew0QcOeRmkbFR6XFJH7yxaAhZNxJcDdZUfN7j"
access_key = "1600888525955948545-5QSSIU4nl7xhugO3AHxxS0Kt9wS7c7"
access_secret = "lZZ6bBE7vPIa390RvIORmffnRiRoPyL69yl1fjvludddT"
api = Twython(consumer_key, consumer_secret,access_key, access_secret)
api.update_status(status=prim)


# In[ ]:


#Count missing variable
data.isnull().sum().sort_values(ascending=False)

