from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

doc2 = {
    'author': 'madhuri',
    'text': ["hello bitch","das right","yo girl got this"],
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", id=1, body=doc)
print(res['result'])

res = es.index(index="test-index", id=2, body=doc2)
print(res['result'])

res = es.get(index="test-index", id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

# res = es.search(index="test-index", body={"query": {"match_phrase": {"text":"bonsai cool"}}})
#res = es.search(index="test-index", body={"query": {"match_all": {}}})
res = es.search(index="test-index", body={"query": {"match_phrase": {}}})


print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
    # if "bonsai" in hit["_source"]["text"]:
    #     print("True")
    if type(hit["_source"]["text"]) == list:
        for i in hit["_source"]["text"]:
            if "das right" in i:
                print(True)
            else:
                continue