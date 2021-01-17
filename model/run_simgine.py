



def simgine( article_title ):

    from gensim.models.doc2vec import Doc2Vec

    fname = 'doc2vec.model'
    
    model = Doc2Vec.load( fname )
    print( f'\nSuccesfully loaded {fname}' )

    similar_doc = model.docvecs.most_similar( article_title )

    row = '\t\t{:<35}{}'
    print( f'\nTop 10 Wikipedia articles most similar to {article_title}:\n' )
    print( row.format( 'Article', 'Cosine Sim <-1; 1>' ), '\n' )

    for i, pair in enumerate(similar_doc[0:10]):
        print( f'{i+1}.' + row.format( pair[0], str(round(pair[1], 2)) ) )




if __name__ == "__main__":
    # simgine( 'Black panther' )
    # simgine( 'Jaguar' )


    import os, random
    articles = random.sample( os.listdir( '../scraper/scraped' ), 5 )

    for fn in articles:
        simgine( fn[:-4] )

    '''
    Top 10 Wikipedia articles most similar to Atari Jaguar:

                    Article                            Cosine Sim 

    1.              PlayStation (console)              0.59
    2.              Panthera onca augusta              0.59
    3.              TurboGrafx-16                      0.58
    4.              Sonic's Ultimate Genesis Collection0.57
    5.              Nintendo Entertainment System      0.57
    6.              History of the Nintendo Entertainment System0.56
    7.              TurboDuo                           0.55
    8.              Atari 5200                         0.53
    9.              North American jaguar              0.52
    10.             Amiga CD32                         0.51
    '''