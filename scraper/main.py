from bs4 import BeautifulSoup, NavigableString, Tag, Comment
from typing import List
import requests

urls = [
    "https://en.wikipedia.org/wiki/Microsoft_Azure",
    "https://en.wikipedia.org/wiki/Linux",
]

r = requests.get(urls[1])

text = r.text

soup = BeautifulSoup(text, "html.parser")

l = soup.body.contents

document_name = l[4].h1.string

bodyContent = l[4]

content = bodyContent.find(id="mw-content-text").div


def replace_tag(tag: str):
    links = content.find_all(tag)

    for i in links:
        newString = i.string
        if not newString:
            newString = ""
        i.replace_with(newString)


replace_tag("b")
replace_tag("a")

toc = content.find("div", "toclimit-3")
toc.decompose()
photos = content.find_all("div", attrs={"class": ["thumb"]})
refferences = content.find_all(attrs={"class": ["reference"]})
reflists = content.find_all(attrs={"class": ["reflist"]})
galleries = content.find_all("ul", "gallery")
tables = content.find_all("table")
styles = content.find_all("style")
spans = content.find_all("span", "mw-editsection")
photos = content.find_all("img")
comments = content.findAll(text=lambda text: isinstance(text, Comment))


ref = content.find(id="See_also")
ref_par = ref.parent
footer = [ref_par]
footer.extend(ref_par.find_all_next("div"))
footer.extend(ref_par.find_all_next("h2"))
footer.extend(ref_par.find_all_next("ul"))

junk = []
junk.extend(footer)
junk.extend(photos)
junk.extend(refferences)
junk.extend(reflists)
junk.extend(galleries)
junk.extend(tables)
junk.extend(styles)
junk.extend(spans)
junk.extend(photos)

for i in junk:
    print(i.attrs)
    i.decompose()

for i in comments:
    i.replace_with("")

content.smooth()

with open("output_ref.html", "w", encoding="utf-8") as f:
    f.write(str(content))
