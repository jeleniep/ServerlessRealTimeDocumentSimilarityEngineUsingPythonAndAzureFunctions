from gensim.models.doc2vec import Doc2Vec

def simgine( article_title, path ):
    # fname = 'doc2vec.model'    
    model = Doc2Vec.load( path )
    similar_doc = model.docvecs.most_similar( article_title )
    response = {}
    for i, pair in enumerate(similar_doc[0:10]):
        response[i+1] = {
            'Article': pair[0],
           ' Cosine Sim <-1; 1>': str(round(pair[1], 2))
        }
    return response
    





