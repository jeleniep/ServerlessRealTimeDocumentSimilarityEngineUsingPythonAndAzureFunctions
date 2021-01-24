from tqdm import tqdm
import os, re


datafolder = "../scraper/scraped/"
os.listdir(datafolder)


def read_wiki(v=True):
    fns = []
    content = []
    for fn in os.listdir(datafolder):
        if fn.endswith('.txt'):
            with open( datafolder+fn ) as f:
                    
                c = "".join(f.readlines())
                if v:
                    print(fn, '\n', c, '\n')
                content.append(c)
                fns.append( fn[:-4] )
    print(f'\nRead {len(content)} files.')
    return content, fns

content, labels = read_wiki(v=False)


# # Cleaning

import nltk
from nltk.stem import WordNetLemmatizer
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

tokenizer = RegexpTokenizer(r'\w+')
stopword_set = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()

# print(len(stopword_set))


def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)



def clean( data ):

    new = []
    print('Cleaning:')
    for d in tqdm(data):
        
        # 1. Lowercase
        new_str = d.lower()
        
        # 2. Remove integers
        new_str = re.sub('\d', '', new_str)

        # 3. Split into list of words
        tokens = tokenizer.tokenize( new_str )
        # print( f'Length: {len(tokens)} -> ', end='' )

        # 4. Remove stop words (a, the, he, she, etc.)
        # porównanie ze stopwords i bez
        tokens = list(set(tokens).difference(stopword_set))
        
        # 5. Stemming: return to base form by part of speech
        # też sprawdzić!
        tokens = [wordnet_lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokens]
        tokens = [x for x in tokens if len(x) > 2]

        # print( f'{len(tokens)}' )
        new.append( tokens )

    return new



cleaned = clean( content )
# len(cleaned)


# Bigrams (not working?)
from gensim.models.phrases import Phrases
bigram = Phrases(cleaned)
cleaned = [bigram[doc] for doc in cleaned]


# print(len(cleaned[0]), cleaned[0])
# print([len(doc) for doc in cleaned])


# Dictionary
from gensim import corpora
dictionary = corpora.Dictionary(cleaned)
# print(dictionary)
# print(dictionary.token2id)


corpus = [dictionary.doc2bow(text) for text in cleaned]
# print(len(corpus))
# print([len(bow) for bow in corpus])




# # Doc2Vec Training
from gensim.models.doc2vec import Doc2Vec, TaggedDocument


# ## Tagging
tagged = [ TaggedDocument(doc, tags=[label]) for doc, label in zip(cleaned, labels) ]
tagged[0]



# Parameters
# bigger vectors? 300
VEC_SIZE = 200

# *.99?
LR = 0.025
EPOCHS = 100




model = Doc2Vec(
    vector_size = VEC_SIZE,
    alpha=LR,

    # context width
    window=2,

    # LR drops to this
    # automatycznie??
    min_alpha=0.00025,

    # ignore words with 2 or less occurrences
    min_count=2,

    # distributed memory alg
    dm=1 
 )




model.build_vocab( tagged )
# losses = []


print('Training:')
for epoch in tqdm( range(1, EPOCHS+1) ):
    
    # Forward pass
    model.train(
        tagged,
        total_examples=model.corpus_count,
        epochs=model.epochs
    )

    # doesn't exist???
    # losses.append( model.get_latest_training_loss() )

    # Decrease LR
    LR -= 0.002
    model.min_alpha = model.alpha


# print( losses )
similar_doc = model.docvecs.most_similar( 'Jaguar' )
print(similar_doc)



# # Saving

# fn = 'doc2vec.model'
fn = '5_doc2vec.model'
print(f'Saved {fn}')
model.save(fn)
# model = Doc2Vec.load(fname)
