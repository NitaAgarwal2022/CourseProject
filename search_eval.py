import math
import sys
import time
import metapy
import pytoml
import sqlite3

results=list ([])

def preProcessQueries(query):
    updatedQuery = metapy.index.Document()
    updatedQuery=query
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LengthFilter(tok, min=3, max=30)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok.set_content(query.content())
    tokens = [token for token in tok]
    docString= " ".join(tokens)
    newDoc = metapy.index.Document()
    newDoc.content(docString)
    updatedQuery=newDoc
    
    return updatedQuery

def performSearch():
    
    connection = sqlite3.connect("C:/Users/nitaj/MS_work/sqlitedbFiles/TISProject.db")
    cursor = connection.cursor()
    
    cfg = "config.toml"
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)    
    ranker = metapy.index.OkapiBM25(k1=3.293,b=0.8,k3=2.6)
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    print("query_path",query_path)
    query = metapy.index.Document()

    mpList=("MP1","MP2.1","MP2.2","MP2.3","MP2.4","MP3")

    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())

            uQuery=preProcessQueries(query)            
            result = ranker.score(idx, uQuery, top_k)
            for i in result:
                
                mp_id = mpList[query_num]
                document_id=i[0]
                score=i[1]
                print(mp_id,document_id,score)
                cursor.execute("insert into search_results (mp_id, document_id, score) values (?, ?, ?)",
                (mp_id, document_id, score))
                               
            
    connection.commit()
    connection.close()
    
    return results   

if __name__ == '__main__':
    print("in main")
    performSearch()
    