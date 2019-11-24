import requests
from bs4 import BeautifulSoup
import pandas as pd


names = []
features = []
colors = []
cats = []
links = []

namePriceColor = []

itemNums = 2000
url = 'https://www2.hm.com/en_gb/men/shop-by-product/view-all.html?sort=stock&image-size=small&image=model&offset=0&page-size=' + str(itemNums)

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

page = requests.get(url, headers=agent)
soup = BeautifulSoup(page.text, 'html.parser')


categories = soup.find_all("article", class_="hm-product-item")
for cat in categories:
    cats.append(cat.get('data-category'))
    
urlLink = soup.find_all("a", class_="item-link")
for link in urlLink:
    fullLink = 'https://www2.hm.com' + link.get('href')
    links.append(fullLink)    
        
for line in soup.find_all(class_="item-details"):
    for subSearch in line.find_all(class_="item-heading"):
        name = line.find('a')
    for subSubSearch in line.find_all(class_="item-price"):
        feature = line.find('span')
    for subSubSubSearch in line.find_all(class_="list-swatches"):
        color = line.find('li')
        
    names.append(name.text)
    features.append(feature.text)
    colors.append(color.text.strip())
    
    namePriceColor.append([name.text,feature.text,color.text.strip()])


data_transposed = zip(names,features,colors,cats,links)
df = pd.DataFrame(data_transposed, columns=["Name","Price (£)","Color","Category","URL_Link"])

df['Price (£)'] = df['Price (£)'].str[1:]
df['Price (£)'] = pd.to_numeric(df['Price (£)'], errors='coerce')

df.to_pickle('webScrapeHM.pkl')





















