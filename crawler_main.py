import requests
from bs4 import BeautifulSoup as bs
import re,pickle


class Crawler(object):
    
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


    # def crawl_dialogue_singledict(self): #all movies into a SINGLE dictionary
    #     movies = {}
    #     links = self.crawl_movie_links()
    #     for link in links:
    #         print(link)
    #         requestSource = requests.get(link)
    #
    #         if requestSource.status_code == 200:
    #
    #             beautifiedSource = bs(requestSource.content, "html.parser")
    #             block = beautifiedSource.blockquote.findAll("p")
    #
    #             h1_tag = beautifiedSource.find("h1", {"id": "disp-script-title"})
    #             title = h1_tag.a.text
    #
    #             movies[title] = []
    #
    #             for j in list(block):
    #                 x = re.sub("[^\w\d'\s]+",'',j.text).lower()
    #                 print(x)
    #                 movies[title].append(x.strip(' '))
    #
    #         else:
    #             continue
    #
    #     return movies

    # def crawl_dialogues(self): #multiple dictionaries with list of all sentences
    #     movie_list = []
    #     links = self.crawl_movie_links()
    #     # text_file = open("OutputMovies1.txt", "a")
    #     print("Crawling all links...stay tuned.")
    #     for link in links:
    #         movie = {}
    #         print(link)
    #         requestSource = requests.get(link)
    #
    #         if requestSource.status_code == 200:
    #
    #             beautifiedSource = bs(requestSource.content, "html.parser")
    #             block = beautifiedSource.blockquote.findAll("p")
    #
    #             h1_tag = beautifiedSource.find("h1", {"id": "disp-script-title"})
    #             title = h1_tag.a.text
    #
    #             movie[title] = []
    #
    #             for j in list(block):
    #                 x = re.sub("[^\w\d'\s]+",'',j.text).lower()
    #                 movie[title].append(x.strip(' '))
    #             # text_file.write(json.dumps(movie,indent=3, sort_keys=True))
    #             movie_list.append(movie)
    #
    #         else:
    #             continue
    #
    #     pickle_out = open("movie_list.pickle","wb")
    #     pickle.dump(movie_list, pickle_out)
    #     pickle_out.close()
    #
    #     return None

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

                # for j in list(block):
                #     movie = {"title":title}
                #     x = re.sub("[^\w\d'\s]+",'',j.text).lower()
                #     if x != '':
                #         movie["script"] = x.strip(' ')
                #         movie_list.append(movie)
                #         print(movie)
                #     else:
                #         continue
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