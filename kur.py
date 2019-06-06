#!/usr/bin/env python
# coding: utf-8

# In[120]:


import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[121]:


url = 'https://m.doviz.com/kur/serbest-piyasa/sterlin'
response = requests.get(url)


# In[122]:


soup = BeautifulSoup(response.text, 'html.parser')


# In[123]:


r = soup.find("div", attrs={"class":"table"})


# In[124]:


df1 = pd.read_html(str(r), thousands=', ')[0]
df1


# In[125]:


df2 = pd.read_html(str(r), thousands=', ')[1]
df2


# In[126]:


frames = [df1, df2]
result = pd.concat(frames, ignore_index=True) #tablo information index düzeltimi
result


# In[160]:


df = pd.DataFrame({
'x': result['Alış'],
'y': result['Satış'],
'group': result['Banka']
})
 
p = sns.regplot(data=df, x="x", y="y", fit_reg=False, marker="^", color="purple")

for line in range(0,df.shape[0]):
     p.text(df.x[line], df.y[line], df.group[line], horizontalalignment='left', size='medium', color='black', weight='semibold')

