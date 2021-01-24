import yaml
from gensim.models.doc2vec import Doc2Vec



def simgine( article_title, model_path='doc2vec.model' ):

    print( f'\n=========================== {article_title} ===========================\n' )
    try:
        with open(f"../scraper/scraped/{article_title}.yaml", "r", encoding="utf-8") as yaml_file:
            parsed = yaml.load(yaml_file, Loader=yaml.FullLoader)
            cats = set( parsed['Categories'] )
    except:
        print( f'No YAML file for {article_title}' )
        cats = None


    model = Doc2Vec.load( model_path )
    # print( f'\nSuccesfully loaded {model_path}' )


    # print( model.docvecs.distance( 'GameCube', 'Honda' ) )
    # return

    acc = 0
    TOP = 20
    row = '\t{:<40}{:<13}{}'
    wiki_prefix = 'https://en.wikipedia.org/wiki/'
    
    
    similar_doc = model.docvecs.most_similar( article_title, topn=TOP )

    print( f'Original link: {wiki_prefix}{article_title.replace(" ", "_")}' )
    if cats:
        print( f'Article has {len(cats)} Categories:' )
        for c in cats:
            print( f'\t* {c}' )
    print( f'\nTop {TOP} Wikipedia articles most similar to {article_title}:\n' )
    print( row.format( 'Article', 'Cosine Sim', 'Mutual Categories' ), '\n' )

    for i, pair in enumerate(similar_doc[0:TOP]):
        other_title = pair[0]
        # url = wiki_prefix + other_title.replace(' ', '_')
        # print(other_title)
        if cats:
            q = mutual_cats( cats, other_title )
            acc += int( q>0 )
        print( f'{i+1}.' + row.format( other_title, str(round(pair[1], 2)), q if q else 0) )
        



def mutual_cats( cats, other ):

    try:
        with open(f"../scraper/scraped/{other}.yaml", "r", encoding="utf-8") as yaml_file:
            parsed = yaml.load(yaml_file, Loader=yaml.FullLoader)
            other_cats = set( parsed['Categories'] )
            # other_cats = set( parsed['Categories'] ).union( set( parsed['Hidden Categories'] ))
    except:
        print( f'No YAML file for {other}' )
        return 0
    q = len( cats.intersection( other_cats ) )
    return q


if __name__ == "__main__":


    # simgine( 'Jaguar' )
    # simgine( 'Black panther' )
    # simgine( 'Buick' )


    '''
    #       Lem     Stop        Vec     Ep      Time, min (cleaning + training)
    1       -        +          100    250      0+11
    2       +        -          100    250      3+22
    3       +        +          100    250      1+8
    4       -        -          100    250      0+18
    5       +        +          100    250      1+9
    
    Best: 3?
    '''


    for i in range(1, 6):
        simgine( 'Nintendo Switch', model_path=f'{i}_doc2vec.model' )
    
    # simgine( 'Nintendo Switch', model_path=f'3_doc2vec.model' )
    # simgine( 'Nintendo Switch', model_path=f'doc2vec.model' )

'''
    # PLAYGROUND
    import os, random
    articles = os.listdir( '../scraper/scraped' )
    random.shuffle( articles )

    i = 0
    # for fn in 
    # articles:
    while i < 3:
        fn = articles.pop()
        # break
        # print(fn)
        if fn.endswith('.txt'):
            simgine( fn[:-4] )
            i+=1


'''