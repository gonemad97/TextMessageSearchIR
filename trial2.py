# import pickle
#
# pickle_in = open("dict.pickle","rb")
# example_dict = pickle.load(pickle_in)
#
# print(example_dict)
# print(type(example_dict))

import requests,re
from bs4 import BeautifulSoup as bs


main_url = "https://justenglish.me/2014/04/18/synonyms-for-the-96-most-commonly-used-words-in-english/"
try:
    requestSource = requests.get(main_url) # or "html.parser"
except:
    print ("Failed to establish connection. Check your internet.")
beautifiedSource = bs(requestSource.content, "html.parser")

div_tag = beautifiedSource.find("div", {"class": "entry clearfix"})
ptag = div_tag.findAll("p")
# for i in list(ptag):
#     if i.strong:
#         print(i.strong.text)
for i in list(ptag):
    print(i.text)