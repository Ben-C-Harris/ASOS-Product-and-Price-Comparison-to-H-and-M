import pandas as pd
import pickle

dfASOS = pd.read_pickle("webScrapeASOS.pkl")[:]
dfASOS = dfASOS.add_prefix('ASOS_') 

dfHnM = pd.read_pickle("webScrapeHM.pkl")
dfHnM = dfHnM.add_prefix('HnM_') 

dfComparison = pd.read_pickle('productCompareASOSHM.pkl')
dfComparison.to_csv('productCompareASOSHM.csv')
    
with open('productPairsASOSHM.pkl', 'rb') as f:
    pairedNamesASOStoHnM = pickle.load(f)
