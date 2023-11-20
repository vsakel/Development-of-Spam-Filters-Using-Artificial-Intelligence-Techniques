# combine csv files of youtube, to construct the youtube dataset
# then apply some text cleaning before translation

import pandas as pd
import re
import contractions

def data_clean(text):
    
    text = re.sub(r'<.*>',' ',text) # remove html tags
    text = re.sub(r'http\S+', 'Link',text) # replace links with keyword Link, there is a problem that some 
    # spam emails contains only urls, what can i do in preprocessing? delete it?
    text = re.sub(r'\n+', ' ', text) # replace \n (new line character) with space
    text  = re.sub(r"[^a-zA-Z.,'\d\s]", ' ', text) # Remove all symbols except letters, numbers
    # #dots ".", comma ","  "'" apostrophe "'"
    text = contractions.fix(text) # fix words like 'can't' to 'can not' so we decrease vocabulary
    text= re.sub(r'\s+', ' ', text)  # Replacing all gaps with space 
    text = text.strip()

    # an einai none to email meta to katharismo den mou prosferei kati kai to diwxnw
    if text == ' ' or text == '':
        return 'none'
    

    return text

yt1 = pd.read_csv('Youtube01-Psy.csv',encoding='ISO-8859-1') 
yt2 = pd.read_csv('Youtube02-KatyPerry.csv',encoding='ISO-8859-1') 
yt3 = pd.read_csv('Youtube03-LMFAO.csv',encoding='ISO-8859-1') 
yt4 = pd.read_csv('Youtube04-Eminem.csv',encoding='ISO-8859-1') 
yt5 = pd.read_csv('Youtube05-Shakira.csv',encoding='ISO-8859-1') 

data = pd.concat([yt1,yt2,yt3,yt4,yt5],ignore_index=True) # youtube dataset 
data.rename(columns = {'CLASS':'Category','CONTENT':'Message'}, inplace = True)
data = data.loc[:,['Message','Category']]
data = data.dropna()
data.drop_duplicates(inplace=True)
data.Message = data.Message.apply(data_clean)
data = data.loc[data.Message != 'none']
data.drop_duplicates(inplace=True)

spam = len(data.loc[data.Category==1])
ham = len(data.loc[data.Category==0])

print("total ham :",ham) # num of ham 
print("\ntotal spam :",spam) # num of spam 
data.to_csv('youtube_datav2.csv', index = False)
