from elasticsearch import Elasticsearch
import pickle,heapq

"""
Methods mentioned below are used for the Flask application.
"""
es = Elasticsearch()
global res

"""
Uses the pickle object containing the dictionary of movie titles and their scripts, to insert into
a new Elasticsearch index, one record at a time. The resulting index is returned.
"""
def create_index():
    res = None
    pickle_in = open("movie_list_paras_full.pickle","rb")
    movies = pickle.load(pickle_in)

    count = 1

    if es.indices.exists(index="movie_dialogue"):
        return res

    print(len(movies))
    for movie in movies:
        res = es.index(index="movie_dialogue", id=count, body=movie)
        count += 1

    print("Finished indexing")
    es.indices.refresh(index="movie_dialogue")

    return res

"""
Holds a list of text abbreviations and their full forms. When a user enters a search query with 
these abbreviations, they will be converted to their full forms, for the ease of getting better
search results. The newly formed search query is returned.
"""
def abbreviations(user_query):

    words = user_query.split()
    abbreviations = {
        "ily":"i love you",
        "ofc":"of course",
        "ikr":"i know right",
        "nvm":"never mind",
        "lmk":"let me know",
        "brb":"be right back",
        "lol":"laugh out loud",
        "ur":"you're",
        "u":"you",
        "thr":"there",
        "r":"are",
        "urs":"yours",
        "tht":"that",
        "k":"okay",
        "thnks":"thanks",
        "thanx":"thanks",
        "thnx":"thanks",
        "pic":"picture",
        "pics":"pictures",
        "gn":"good night",
        "gm":"good morning"}

    words = [abbreviations.get(n, n) for n in words]
    q = ' '.join(words)

    return q


"""
The user's search query is processed and a match phrase process is conducted using the ES search API.
Highlighting, also a part of the ES API, is performed as well on the words directly matching the
search query. A dictionary with the movie titles and their scores as well as a dictionary with the
resulting movie titles and their highlighted scripts are returned.
"""
def search_query(user_query):
    create_index()
    res = es.search(index="movie_dialogue",
                    size = 50, body={"query":{
            "match_phrase":{
                "script":user_query
            }
        },
            "highlight":{
                "type":"unified",
                "fragment_size":100,
                "fields":{
                    "script":{ "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] }
                }
            }
        })
    #print(res)
    scores = {}
    convo = {}
    for hit in res['hits']['hits']:
        convo[hit["_source"]["title"]] = hit["highlight"]["script"]
        #scores[hit["_source"]["title"]] = hit["_score"]
        scores[hit["_score"]] = hit["_source"]["title"]
        # print(hit["_source"]["title"])
        # print(hit["highlight"]["script"])
        # print(hit["_score"])

    return scores,convo


"""
Using the score and conversation(movie script) dictionaries, a heap is used to create a descendingly
ordered list of movies and their scripts based on the Lucene Practical Scoring Function.
If the user's search query is a single word, and if it fits a word in the list of synonyms in the 
pickle file, this algorithm will use the reults from the query's synonym word, if in case the total
results from the original query word, do not make it to 10.
"""
def retieve_top_convos(user_query):
    #lucene practical score based heap-top 10 results
    scores,convo = search_query(user_query)
    heap = [(-key, value) for key,value in scores.items()]
    largest = heapq.nsmallest(10, heap)
    largest = [key for value, key in largest]
    result = {}
    for i in largest:
        convo[i] = [" ".join(convo[i])]
        result[i] = convo[i]

    #print(result)
    # return result

    #for updating results if a single worded query with less than 10 results
    if len(user_query.split()) == 1 and len(result) < 10:
        count = 10 - len(result)
        pickle_in = open("synonyms.pickle","rb")
        synonyms = pickle.load(pickle_in)
        if user_query in synonyms:
            new_user_query = synonyms[user_query]

            scores,convo = search_query(new_user_query)
            heap = [(-key, value) for key,value in scores.items()]
            largest = heapq.nsmallest(count, heap)
            largest = [key for value, key in largest]


            #uppercase to highlight new synonyms
            for i in largest:
                for j in convo[i]:
                    for k in j.split():
                        k = k.replace("<mark>","")
                        k = k.replace("</mark>","")
                        if k.lower() == synonyms[user_query]:
                            x = k.upper()
                            j = j.replace(k,x)
                            convo[i] = [j]

                result[i] = convo[i]

            #print(result)
            return result
        else:
            #print(result)
            return result
    else:
        #print(result)
        return result



"""
Solely for testing and presentation purposes and not for the user's use. Deletes the index.
"""
def delete_index():
    es.indices.delete(index='movie_dialogue')
    print("Existing index, 'movie_dialogue' has been deleted. Index again.")
    # search_query()

# delete_index()
create_index()
# # search_query()
# retieve_top_convos("awful")