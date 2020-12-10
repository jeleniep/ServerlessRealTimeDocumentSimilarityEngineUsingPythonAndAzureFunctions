from bs4 import BeautifulSoup, NavigableString, Tag, Comment
from typing import List
import requests
import yaml

import os

folderpath = 'scraped/'
if not os.path.exists(folderpath):
    os.makedirs(folderpath)



def unwrap_all(content: Tag, tag: str):
    links = content.find_all(tag)

    for i in links:
        i.unwrap()


def sanitize(content: Tag):
    toc = content.find("div", "toclimit-3")
    if toc:
        toc.decompose()
    photos = content.find_all("div", attrs={"class": ["thumb"]})
    references = content.find_all(attrs={"class": ["reference"]})
    reflists = content.find_all(attrs={"class": ["reflist"]})
    galleries = content.find_all("ul", "gallery")
    tables = content.find_all("table")
    styles = content.find_all("style")
    spans = content.find_all("span", "mw-editsection")
    photos = content.find_all("img")
    pronunciation = content.find_all("span", "rt-commentedText")
    comments = content.findAll(text=lambda text: isinstance(text, Comment))

    footer: List[Tag] = []
    ref = content.find(id="See_also")
    if ref:
        ref_par = ref.parent
        if ref_par:
            footer.append(ref_par)
            footer.extend(ref_par.find_all_next("div"))
            footer.extend(ref_par.find_all_next("h2"))
            footer.extend(ref_par.find_all_next("ul"))

    junk = []
    junk.extend(footer)
    junk.extend(photos)
    junk.extend(pronunciation)
    junk.extend(references)
    junk.extend(reflists)
    junk.extend(galleries)
    junk.extend(tables)
    junk.extend(styles)
    junk.extend(spans)
    junk.extend(photos)

    for i in junk:
        i.decompose()

    for i in comments:
        i.replace_with("")

    content.smooth()


def scrap(text: str):
    soup = BeautifulSoup(text, "lxml")
    l = soup.body.contents
    document_name = l[4].h1.string
    bodyContent = l[4]

    content = bodyContent.find(id="mw-content-text").div

    abstract: Tag = content.find("p").find_next_sibling("p")

    sanitize(abstract)
    unwrap_all(abstract, "b")
    unwrap_all(abstract, "a")
    unwrap_all(abstract, "i")
    unwrap_all(abstract, "span")

    abstract_text = abstract.get_text()

    with open(f"{folderpath}{document_name}.txt", "w", encoding="utf-8") as f:
        f.write( abstract_text )


def main():
    with open("urls.yaml") as file:
        urls = yaml.safe_load(file)

    for url in urls:
        r = requests.get(url)
        text = r.text
        scrap(text)


if __name__ == "__main__":
    main()
