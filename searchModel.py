from elasticsearch import Elasticsearch
import pickle,heapq

es = Elasticsearch()
class QuerySearch(object):
    global res
    def create_index(self):
        res = None
        pickle_in = open("movie_list_paras.pickle","rb")
        movies = pickle.load(pickle_in)

        count = 1

        if es.indices.exists(index="movie_dialogue"):
            return res

        print(len(movies))
        for movie in movies:
            res = es.index(index="movie_dialogue", id=count, body=movie)
                # res = es.get(index="movie_dialogue", id=count)
                # print(res['_source'])
            count += 1

        print("finished indexing")
        es.indices.refresh(index="movie_dialogue")

        return res


    def search_query(self):
        self.create_index()
        user_query = input("Enter your query: ")
        res = es.search(index="movie_dialogue",
                        size = 50, body={"query": {"match_phrase": {
                "script":user_query
            }},
                "highlight":{
                    "type":"plain",
                    "fragment_size":100,
                    "fields":{
                        "script":{ "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] }
                    }
                }
            })
        #print(res)
        scores = {}
        convo = {}
        print("Got %d Hits:" % res['hits']['total']['value'])
        for hit in res['hits']['hits']:
            convo[hit["_source"]["title"]] = hit["highlight"]["script"]
            #scores[hit["_source"]["title"]] = hit["_score"]
            scores[hit["_score"]] = hit["_source"]["title"]
            print(hit["_source"]["title"])
            print(hit["highlight"]["script"])
            print(hit["_score"])
        heap = [(-key, value) for key,value in scores.items()]
        largest = heapq.nsmallest(20, heap)
        largest = [key for value, key in largest]
        result = {}
        for i in largest:
            result[i] = convo[i]
        return result

    def delete_index(self):
        es.indices.delete(index='movie_dialogue')
        print("deleted, existing index. Run again.")
        self.search_query()


x = QuerySearch()
#print(x.search_query())
print(x.delete_index())