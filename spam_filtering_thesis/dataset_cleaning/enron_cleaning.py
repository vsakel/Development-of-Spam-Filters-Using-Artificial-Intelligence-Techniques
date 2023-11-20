# try to data clean enron dataset

import re
import pandas as pd
import contractions

# prokyptei to enron_pre_translate.csv
def data_clean(text):

    new_txt = re.sub(r"\n+", " ", text) # replace \n (new line character) with space
    new_txt = re.sub(r"- - - -.*?forwarded.*?subject :",".",new_txt) # clean the email attachments
    new_txt = re.sub(r"- - - -.*?original.*?subject :",".",new_txt) # clean the email attachments
    new_txt= re.sub(r"[^a-zA-Z.,'\d\s]", " ", new_txt ) # Remove all symbols except letters, numbers
    #dots ".", comma ","  "'" apostrophe "'"
    new_txt = re.sub(r"\s'\s","'",new_txt) # replace "can ' t" to "can't" so we use below function
    new_txt = contractions.fix(new_txt) # fix words like 'can't' to 'can not' to decrease the size of vocab
    new_txt= re.sub(r"\s+", " ", new_txt)  # Replacing all gaps with spaces 
    new_txt = new_txt.strip()

    # an einai none to email meta to katharismo den mou prosferei kati kai to diwxnw
    if new_txt == " ":
        return 'none'
    

    return new_txt


dataset = pd.read_csv("enron_spam_data.csv",encoding='ISO-8859-1')
dataset = dataset.dropna() # remove rows with Null/NaN values
dataset.rename(columns = {'Spam/Ham':'Category'}, inplace = True)
dataset = dataset.loc[:,['Message','Category']]
dataset.drop_duplicates(inplace=True) # remove duplicates
dataset.Message = dataset.Message.apply(data_clean)
# drop emails that have none content after cleaning
dataset = dataset.loc[dataset.Message != 'none']
dataset.drop_duplicates(inplace=True)
# Category will turn into 1- >spam, 0-> ham
dataset.Category = dataset.Category.map({ "ham": 0, "spam": 1 })
dataset.to_csv('enron_pre_translate.csv', index = False) # save dataframe into csv, enron spam csv has only message and category



