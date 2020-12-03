from bs4 import BeautifulSoup, NavigableString, Tag
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

photos = content.find_all("div", "thumb tright")
refferences = content.find_all(attrs={"class": "reference"})
reflists = content.find_all(attrs={"class": "reflist"})
galleries = content.find_all("ul", "gallery")
tables = content.find_all("table")
styles = content.find_all("style")
spans = content.find_all("span", "mw-editsection")

junk = []
junk.extend(photos)
junk.extend(refferences)
junk.extend(reflists)
junk.extend(galleries)
junk.extend(tables)
junk.extend(styles)
junk.extend(spans)

for i in junk:
    i.decompose()

ref = content.find(id="References")
ref_par = ref.parent

with open("output.html", "w", encoding="utf-8") as f:
    f.write(str(content))
