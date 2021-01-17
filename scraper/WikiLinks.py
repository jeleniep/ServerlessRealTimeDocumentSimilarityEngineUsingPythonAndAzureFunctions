
import requests
from tqdm import tqdm
import time


'''
PARAMETERS
'''

'''
Category names from this page:
https://en.wikipedia.org/wiki/Wikipedia:Contents/Categories
or any other subcategory link which starts with Category:

Car Brands + Big Cats = Jaguar overlapping
'''
cat_list = [
    #'Computer Science',
    'Car Brands',
    'Fender electric guitars',
    # 'Natural Resources',
    # 'New Wave of British Heavy Metal musical groups', # doesnt work?
    'Home video game consoles',
    'Big Cats'
]

'''how many times we will enter the subcategory level'''
DEPTH = 1

'''desired output format'''
format = 'YML' #'TXT'



# Preprocessing
categories = []
for cat in cat_list:
    cat = cat.replace(' ', '_').lower()
    cat = cat[0].upper() + cat[1:]
    categories.append(cat)

print('List of categories:', categories)



S = requests.Session()
WikiPrefix = 'https://en.wikipedia.org/wiki/'
URL = "https://en.wikipedia.org/w/api.php"



# request
def fetch_pages( cmtitle ):

    PARAMS = {
        "action": "query",
        "cmtitle": cmtitle,
        "cmlimit": "1000",
        "list": "categorymembers",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA['query']['categorymembers']
    return PAGES



output = {}
replacements = 0



start = time.time()
for category in categories:


    # entry point
    start_platform = {
        'level': 0,
        'origin': f"Category:{category}",
        'pages': fetch_pages( f"Category:{category}" )
    }

    print('Starting point has', len(start_platform['pages']), 'links.')

    queue = [ start_platform ]
    links_in_category = 0


    # BFS using list queue
    while len(queue) != 0:

        platform = queue.pop(0)
        level = platform['level']
        pages = platform['pages']
        origin = platform['origin']

        print('\n=========================')
        print( 'QUEUE LENGTH =', len(queue) )
        print( f'Rendering: {origin}')
        print('=========================\n')

        
        print(f'Platform has level {level} and {len(pages)} links.\n')
        direct_links = 0
        cat_links = 0

        for page in tqdm(pages):
            
            title = page['title']
            pageid = page['pageid']

            if title.startswith('Category:'):
                if level < DEPTH:
                    new_platform = {
                        'level': level + 1,
                        'origin': title,
                        'pages': fetch_pages( title )
                    }
                    queue.append( new_platform )
                    cat_links += 1
                    
            else:
                direct_links += 1
                links_in_category += 1
                if output.get( pageid ):
                    replacements += 1
                output[ pageid ] = WikiPrefix + title.replace(' ', '_')
        
        print(f'\nAdded {direct_links} direct page links to output; {cat_links} categories added to the queue.')
        print('Total number of direct links :', len(output))
        if ( len(pages) == (direct_links+cat_links) ):
            print('Nothing lost.')
    

    print(f'Direct links fetch for Category:{category} : {links_in_category}')
    print('Total number of direct links :', len(output))
    # input()


finish = round(time.time()-start, 1)
print(f'\nElapsed time: {finish} s')
print(f'Fetched links for categories: {categories}')
print(f'The same page met more than once: {replacements}')
print(f'Total number of wiki page links fetched: {len(output)}')


if format == 'TXT':

    print('Writing it to urls.txt')
    with open('urls.txt', 'w') as f:
        for link in output.values():
            f.write("%s\n" % link)

elif format == 'YML':
    print('Writing it to urls.yml')
    with open('urls.yml', 'w') as f:
        f.write('---\n')
        f.write('# urls:')
        for link in output.values():
            f.write( f'\n- {link}')


# stats for nerds
with open('records.txt', 'a') as f:
    f.write(f'DEPTH: {DEPTH}\tTIME: {finish}\tFETCHED:{len(output)}\t\tREPL: {replacements}\tCAT_LIST: {categories}\n')
