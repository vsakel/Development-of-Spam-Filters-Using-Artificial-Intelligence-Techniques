# try text cleaning sms dataset

import pandas as pd
import re
import contractions


def data_clean(text):

    text = re.sub(r"\n+", " ", text) # replace \n (new line character) with space
    # replace links with keyword Link 
    text = re.sub(r'http.*\. \S+', ' Link',text,flags=re.IGNORECASE)
    # * means zero or more, \S+ means one or more non space char, \s+ means one or more spaces
    text = re.sub(r'http.*?\s', ' Link ',text,flags=re.IGNORECASE) # http links without space between
    text = re.sub(r'http.*', ' Link ',text, flags=re.IGNORECASE) # http links without space between and at the end of message
    text= re.sub(r"[^a-zA-Z.,'\d\s]", " ", text ) # Remove all symbols except letters, 
    # numbers, dots ".", comma ","  "'" apostrophe "'"
    text= re.sub(r"\s+", " ", text)  # Replacing all gaps with spaces 
    text = text.strip() # remove leading and last gap

    # an einai none to email meta to katharismo den mou prosferei kati kai to diwxnw
    if text == " " or text == "":
        return 'none'
    

    return text


dataset = pd.read_csv('sms.csv',encoding='ISO-8859-1')
dataset = dataset.dropna() # remove rows with Null/NaN values
# # peta tis diploeggrafes
dataset.drop_duplicates(inplace=True)
dataset.Message = dataset.Message.apply(data_clean)
# drop emails that have none content after cleaning

dataset = dataset.loc[dataset.Message != 'none']
dataset.drop_duplicates(inplace=True)
# Category will turn into 1- >spam, 0-> ham
dataset.Category = dataset.Category.map({ "ham": 0, "spam": 1 })

# save it to a csv file
dataset.to_csv('sms_pre_translate.csv', index = False)
