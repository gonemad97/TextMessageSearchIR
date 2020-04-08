import requests
from bs4 import BeautifulSoup as bs
import re,pickle


'''
This class crawls required movie script information from a website and stores it into a pickle file 
to be used later.
'''
class Crawler(object):

    """
    Crawls a website that holds movie scripts. It curls through every link alphabetically
    in the website and it crawls each and every movie under every alphabet. A list of all these links
    is returned here.
    """
    def crawl_movie_links(self):
        links = []
        alphabet = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        print("Fetching all movie links...")
        for letter in alphabet:

            main_url = "https://www.scripts.com/scripts/" + letter + "/99999"
            try:
                requestSource = requests.get(main_url) # or "html.parser"
            except:
                print ("Failed to establish connection. Check your internet.")
            beautifiedSource = bs(requestSource.content, "html.parser")

            td_tag = beautifiedSource.findAll("td", {"class": "tal qx"})

            for i in list(td_tag):
                links.append("https://www.scripts.com" + i.a["href"])

            print("Got " + letter)

        return links


    """
    Crawls a website containing some English words and their synomyms. A dictionary with the word
    and its appropriate synonym is returned.
    """
    def find_synonyms(self):
        main_url = "https://justenglish.me/2014/04/18/synonyms-for-the-96-most-commonly-used-words-in-english/"
        try:
            requestSource = requests.get(main_url) # or "html.parser"
        except:
            print ("Failed to establish connection. Check your internet.")
        beautifiedSource = bs(requestSource.content, "html.parser")

        div_tag = beautifiedSource.find("div", {"class": "entry clearfix"})
        ptag = div_tag.findAll("p")

        synonyms = {}
        for i in list(ptag):
            x = i.text.replace(" —","")
            val = x[x.find(" "):][1:].split(',')[0]
            key = x[:x.find(" ")].lower()
            if key == "ask–":
                key = key.replace('ask–',"ask")
            if key:
                synonyms[key] = val

        pickle_out = open("synonyms.pickle","wb")
        pickle.dump(synonyms, pickle_out)
        pickle_out.close()


    """
    Each link that was returned as a total list will be parsed here. A dictionary containing the 
    movie title and the script of the first scene of each movie is stored. The script is further
    processed to remove unnecessary punctuation and it converted to lower case to better search 
    results.
    """
    def crawl_dialogues(self): #multiple dictionaries with one sentence and movie title EACH
        movie_list = []
        links = self.crawl_movie_links()
        print(len(links))
        # text_file = open("OutputMovies1.txt", "a")
        print("Crawling all links...stay tuned.")
        for link in links:

            print(link)
            requestSource = requests.get(link)

            if requestSource.status_code == 200:

                beautifiedSource = bs(requestSource.content, "html.parser")
                block = beautifiedSource.blockquote.findAll("p")

                try:
                    h1_tag = beautifiedSource.find("h1", {"id": "disp-script-title"})
                    title = h1_tag.a.text
                    print(title)
                except:
                    title = "Unknown"

                movie = {"title":title,"script":''}
                for j in list(block):
                    x = re.sub("[^\w\d'\s]+",'',j.text).lower()
                    # x = j.text
                    if x != '':
                        movie["script"] += " " +x.strip(' ')
                    else:
                        continue
                movie_list.append(movie)
                print(movie)
                # text_file.write(json.dumps(movie,indent=3, sort_keys=True))

            else:
                continue

        pickle_out = open("movie_list_paras_full.pickle","wb")
        pickle.dump(movie_list, pickle_out)
        pickle_out.close()

        return None




x = Crawler()
print(x.crawl_dialogues())
# print(x.find_synonyms())