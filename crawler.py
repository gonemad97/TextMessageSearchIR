import requests
from bs4 import BeautifulSoup as bs
import re,json,pickle

def crawl_movie_links(self):
    links = []
    alphabet = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
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

    return links


def crawl_dialogues(self):
    movie_list = []
    links = self.crawl_movie_links()
    text_file = open("OutputMovies1.txt", "a")
    for link in links:
        movie = {}
        requestSource = requests.get(link)

        if requestSource.status_code == 200:

            beautifiedSource = bs(requestSource.content, "html.parser")
            block = beautifiedSource.blockquote.findAll("p")

            h1_tag = beautifiedSource.find("h1", {"id": "disp-script-title"})
            title = h1_tag.a.text

            movie[title] = []

            for j in list(block):
                x = re.sub("[^\w\d'\s]+",'',j.text).lower()
                print(x)
                movie[title].append(x.strip(' '))
            text_file.write(json.dumps(movie,indent=3, sort_keys=True))
            movie_list.append(movie)

        else:
            continue

    pickle_out = open("movielist.pickle","wb")
    pickle.dump(movie_list, pickle_out)
    pickle_out.close()

    return None