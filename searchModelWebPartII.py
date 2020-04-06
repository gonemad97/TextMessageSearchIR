from elasticsearch import Elasticsearch
import pickle,heapq

es = Elasticsearch()
global res
def create_index():
    res = None
    pickle_in = open("movie_list_paras.pickle","rb")
    movies = pickle.load(pickle_in)

    count = 1

    if es.indices.exists(index="movie_dialogue"):
        return res

    print(len(movies))
    for movie in movies:
        res = es.index(index="movie_dialogue", id=count, body=movie)
        count += 1

    print("finished indexing")
    es.indices.refresh(index="movie_dialogue")

    return res

def abbreviations(user_query):

    words = user_query.split()
    abbreviations = {
        "ily":"i love you",
        "ofc":"of course",
        "ikr":"i know right",
        "nvm":"never mind",
        "lmk":"let me know",
        "brb":"be right back",
        "lol":"laughing out loud",
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


def search_query(user_query):
    create_index()
    res = es.search(index="movie_dialogue",
                    size = 50, body={"query":{
            "match_phrase":{
                "script":user_query
            }
        },
            "highlight":{
                "fragment_size":100,
                "fields":{
                    "script":{ "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] }
                }
            }
        })
    #print(res)
    scores = {}
    convo = {}
    # print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        convo[hit["_source"]["title"]] = hit["highlight"]["script"]
        #scores[hit["_source"]["title"]] = hit["_score"]
        scores[hit["_score"]] = hit["_source"]["title"]
        # print(hit["_source"]["title"])
        # print(hit["highlight"]["script"])
        # print(hit["_score"])

    return scores,convo

def retieve_top_convos(user_query):
    scores,convo = search_query(user_query)
    heap = [(-key, value) for key,value in scores.items()]
    largest = heapq.nsmallest(10, heap)
    largest = [key for value, key in largest]
    result = {}
    for i in largest:
        result[i] = convo[i]

    #print(result)
    # return result

    #for updating results if a single worded query with less than 10 results
    if len(user_query.split()) == 1 and len(result) < 10:
        count = 10 - len(result)



def delete_index():
    es.indices.delete(index='movie_dialogue')
    print("Existing index, 'movie_dialogue' has been deleted. Indexing again...")
    search_query()

# delete_index()
# # search_query()