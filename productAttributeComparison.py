import pandas as pd
from fuzzywuzzy import fuzz
import pickle

dfASOS = pd.read_pickle("webScrapeASOS.pkl")[:]
dfASOS = dfASOS.add_prefix('ASOS_') 

dfHnM = pd.read_pickle("webScrapeHM.pkl")
dfHnM = dfHnM.add_prefix('HnM_') 


dfASOScopy = dfASOS.copy(deep = True)
dfHnMcopy = dfHnM.copy(deep = True)

pairedNames = []

for ASOSName in dfASOS['ASOS_Name']:
    matchName = []
    matchScore = 0
    for HnMName in dfHnM['HnM_Name']:
        stringCompareScore = fuzz.token_set_ratio(ASOSName, HnMName)
        if stringCompareScore >= matchScore:
            matchScore = stringCompareScore
            matchName = HnMName
            
    pairedNames.append([ASOSName,matchName,matchScore])

with open('pairedNamesListPKL.pkl', 'wb') as f:
    pickle.dump(pairedNames, f)
    
#------------------------------------------------------------------------------
groupDF = pd.DataFrame([])
listArb = []
for namePair in pairedNames:
    ASOSNamePair = namePair[0]
    HnMNamePair = namePair[1]
    pairScore = namePair[2]
    
    ASOSslice = dfASOS[dfASOS['ASOS_Name'] == ASOSNamePair].copy(deep=True)
    HnMslice = dfHnM[dfHnM['HnM_Name'] == HnMNamePair].copy(deep=True)
    
    for index, dfRow in HnMslice.iterrows():
        
        ASOSseries = ASOSslice.iloc[0].squeeze()
        HnMseries = dfRow.squeeze()
                
        newSeries02 = pd.concat([ASOSseries, HnMseries])
        
        tester = newSeries02.to_frame().T
        groupDF = groupDF.append(tester)
        
groupDF.to_pickle('productCompareASOSHM.pkl')
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

#PistonHeads_df_make_model = pd.read_pickle("PistonHeads_dataMakeAndModelPickle.pkl")
#
#PistonHeads_into_AutoTrader = PistonHeads_df_make_model.copy(deep = True)
#PistonHeads_into_AutoTrader = PistonHeads_into_AutoTrader.add_prefix('PH_')
#PistonHeads_into_AutoTrader["Associated_AT_Make"] = 'Unmatched'
#PistonHeads_into_AutoTrader["Associated_AT_Model"] = 'Unmatched'
#
#PistonHeads_into_AutoTrader_Original = PistonHeads_into_AutoTrader.copy(deep=True)
## =============================================================================
## Matching Makes
## =============================================================================
#AT_Makes = pd.Series(AutoTrader_df_make_model['Make'].unique())
#PH_Makes = pd.Series(PistonHeads_df_make_model['Make'].unique())
#
#
#makeMatchList = []
#makeMatchListName = []
#makeMultiList = []
#makeNoMatchList = []
#makeIssueList = []
#for PHmake in PH_Makes:
#    print(PHmake)
#    makeStringCompare = AT_Makes[AT_Makes == PHmake]
#
#    if len(makeStringCompare)==1:
#        print('Found One Match')
#        matchPH = PHmake
#        matchAT = makeStringCompare.iloc[0]
#        makeMatchList.append([matchPH,matchAT])
#        makeMatchListName.append(matchPH)
#    elif len(makeStringCompare)>1:
#        print('Found Multiple Matches')
#        makeMultiList.append([PHmake,makeStringCompare.iloc[:]])
#    elif len(makeStringCompare)==0:
#        print('No Match Found')
#        makeNoMatchList.append(PHmake)
#    else: # i.e. less than one match... Fail
#        print('Error: Matching Failed...')
#        makeIssueList.append(PHmake)
#
#makeMatchSeries= pd.Series(makeMatchListName)
#
#for matchedMake in makeMatchSeries:
#    matchingMakes = PistonHeads_df_make_model[PistonHeads_df_make_model['Make'] == matchedMake]
#    indexNum = matchingMakes.index.tolist()
#    columnNum = PistonHeads_into_AutoTrader.columns.get_loc('Associated_AT_Make')
#    name = matchedMake
#    
#    for index in indexNum:
#        PistonHeads_into_AutoTrader.iat[int(index),columnNum] = name
#
## =============================================================================
## Matching Models
## =============================================================================
#AT_Models = pd.Series(AutoTrader_df_make_model['Model'].unique())
#PH_Models = pd.Series(PistonHeads_df_make_model['Model'].unique())
#
#modelMatchList = []
#modelMatchListName = []
#modelMultiList = []
#modelNoMatchList = []
#modelIssueList = []
#for PHmodel in PH_Models:
#    print(PHmodel)
#    modelStringCompare = AT_Models[AT_Models == PHmodel]
#
#    if len(modelStringCompare)==1:
#        print('Found One Match')
#        matchPH = PHmodel
#        matchAT = modelStringCompare.iloc[0]
#        modelMatchList.append([matchPH,matchAT])
#        modelMatchListName.append(matchPH)
#    elif len(modelStringCompare)>1:
#        print('Found Multiple Matches')
#        modelMultiList.append([PHmodel,modelStringCompare.iloc[:]])
#    elif len(modelStringCompare)==0:
#        print('No Match Found')
#        modelNoMatchList.append(PHmodel)
#    else: # i.e. less than one match... Fail
#        print('Error: Matching Failed...')
#        modelIssueList.append(PHmodel)
#
#modelMatchSeries= pd.Series(modelMatchListName)
#
#for matchedModel in modelMatchSeries:
#    matchingModels = PistonHeads_df_make_model[PistonHeads_df_make_model['Model'] == matchedModel]
#    indexNum = matchingModels.index.tolist()
#    columnNum = PistonHeads_into_AutoTrader.columns.get_loc('Associated_AT_Model')
#    name = matchedModel
#    
#    for index in indexNum:
#        PistonHeads_into_AutoTrader.iat[int(index),columnNum] = name
## =============================================================================
##
## =============================================================================
#PistonHeads_into_AutoTrader_SimpleMatch = PistonHeads_into_AutoTrader.copy(deep=True)
#
#PistonHeads_into_AutoTrader_SimpleMatch = PistonHeads_into_AutoTrader_SimpleMatch[PistonHeads_into_AutoTrader_SimpleMatch['Associated_AT_Make'] != "Unmatched"]
#PistonHeads_into_AutoTrader_SimpleMatch = PistonHeads_into_AutoTrader_SimpleMatch[PistonHeads_into_AutoTrader_SimpleMatch['Associated_AT_Model'] != "Unmatched"]
#
#percentMatched = 100 * len(PistonHeads_into_AutoTrader_SimpleMatch)/len(PistonHeads_into_AutoTrader)
#
##print("You have successfully matched: " + str(100-percentUnmatched) + " % of all Makes and Models Through Simple Compare")
#print("You have successfully matched: " + '{0:.2f}'.format(percentMatched) + " % of all Makes and Models Through Simple Compare")
## =============================================================================
## 
## =============================================================================
#PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch = PistonHeads_into_AutoTrader.copy(deep=True)
#
#PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch = PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch[PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch['Associated_AT_Make'] != "Unmatched"]
#PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch = PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch[PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch['Associated_AT_Model'] == "Unmatched"]
#
#PistonHeads_into_AutoTrader_SentimentMatch = PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch.copy(deep=True)
#PistonHeads_into_AutoTrader_SentimentMatch["Association_Score"] = int(0)
#
#for i, row in enumerate(PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch.iterrows()):
#    PH_Make = row[1][0]
#    PH_Model = row[1][2]
#    AT_Make = row[1][4] # not needed really...
#    
#    modelCompareSlice = AutoTrader_df_make_model[AutoTrader_df_make_model['Make'] == PH_Make]
#    
#    bestScore = 0
#    bestMatch = 'AAA'
#    for j, slicedRow in enumerate(modelCompareSlice.iterrows()):
#        AT_Model = slicedRow[1][1]
#        stringCompareScore = fuzz.token_set_ratio(PH_Model, AT_Model)
#        if stringCompareScore>bestScore:
#            bestScore = stringCompareScore
#            bestMatch = AT_Model
#    
#    if bestScore>=78:
#        indexNum = row[0]
#        columnNum = PistonHeads_into_AutoTrader_MakeMatch_NoModelmatch.columns.get_loc('Associated_AT_Model')
#        if (PistonHeads_into_AutoTrader_SentimentMatch.at[indexNum,'Associated_AT_Model'] == "Unmatched"):
#            PistonHeads_into_AutoTrader_SentimentMatch.at[indexNum,'Associated_AT_Model'] = bestMatch
#            PistonHeads_into_AutoTrader_SentimentMatch.at[indexNum,'Association_Score'] = bestScore
#
#PistonHeads_into_AutoTrader.update(PistonHeads_into_AutoTrader_SentimentMatch)
#
#
## =============================================================================
## 
## =============================================================================
#PistonHeads_into_AutoTrader_SimpleNSentimentMatch = PistonHeads_into_AutoTrader.copy(deep=True)
#
#PistonHeads_into_AutoTrader_SimpleNSentimentMatch = PistonHeads_into_AutoTrader_SimpleNSentimentMatch[PistonHeads_into_AutoTrader_SimpleNSentimentMatch['Associated_AT_Make'] != "Unmatched"]
#PistonHeads_into_AutoTrader_SimpleNSentimentMatch = PistonHeads_into_AutoTrader_SimpleNSentimentMatch[PistonHeads_into_AutoTrader_SimpleNSentimentMatch['Associated_AT_Model'] != "Unmatched"]
#
#percentMatched = 100 * len(PistonHeads_into_AutoTrader_SimpleNSentimentMatch)/len(PistonHeads_into_AutoTrader_Original)
#
##print("You have successfully matched: " + str(100-percentUnmatched) + " % of all Makes and Models Through Simple Compare")
#print("You have successfully matched: " + '{0:.2f}'.format(percentMatched) + " % of all Makes and Models Through Simple Compare And Sentiment Analysis")
#
#
#
#
#
#
#
#
#
#





