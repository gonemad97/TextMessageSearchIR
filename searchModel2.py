from elasticsearch import Elasticsearch
import crawler
import pickle

class QuerySearch(object):
    es = Elasticsearch()
    pickle_in = open("movie_list_paras.pickle","rb")
    movies = pickle.load(pickle_in)
    count = 1
    try:
        es.indices.delete(index='movie_dialogue')
        print("deleted")

    except:
        for movie in movies:
            res = es.index(index="movie_dialogue", id=count, body=movie)
            res = es.get(index="movie_dialogue", id=count)
            print(res['_source'])
            count += 1

        print("finished indexing")
        es.indices.refresh(index="movie_dialogue")

        res = es.search(index="movie_dialogue", body={"query": {"match_phrase": {
            "script":"told you"
        }}})

        print("Got %d Hits:" % res['hits']['total']['value'])
        for hit in res['hits']['hits']:
            print(hit["_source"])
            print(hit["_score"])

