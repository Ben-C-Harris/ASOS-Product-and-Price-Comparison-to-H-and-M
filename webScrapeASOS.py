import requests
from bs4 import BeautifulSoup
import pandas as pd



links = []
names = []
prices = []


itemNums = 1

while itemNums <=30:
    url = 'https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new%20in|new%20products&page=' + str(itemNums)
    
    
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    
    
    page = requests.get(url, headers=agent)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    itemPrices = soup.find_all("span", class_="_342BXW_")
    for itemPrice in itemPrices:
    #    print(itemPrice.text)
        prices.append(itemPrice.text)
           
    for line in soup.find_all(class_="_2oHs74P"):
        for subSearch in line.find_all(class_="_10-bVn6"):
            name = line.find('p')
            names.append(name.text)
            
    itemLinks = soup.find_all("a", class_="_3x-5VWa")
    for itemLink in itemLinks:
        links.append(itemLink.get('href'))        
       
    itemNums +=1


data_transposed = zip(names,prices,links)        
df = pd.DataFrame(data_transposed, columns=["Name","Price (£)","URL_Link"])

df['Price (£)'] = df['Price (£)'].str[1:]
df['Price (£)'] = pd.to_numeric(df['Price (£)'], errors='coerce')

df.to_pickle('webScrapeASOS.pkl')

















