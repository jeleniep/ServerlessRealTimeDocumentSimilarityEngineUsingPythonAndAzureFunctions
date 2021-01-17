from bs4 import BeautifulSoup, NavigableString, Tag, Comment
from typing import List
import requests
import yaml
from tqdm import tqdm

import os, sys

folderpath = "scraped/"
if not os.path.exists(folderpath):
    os.makedirs(folderpath)


def unwrap_all(content: Tag, tag: str):
    links = content.find_all(tag)

    for i in links:
        i.unwrap()


def sanitize(content: Tag):
    # @pietkap
    try:
        toc = content.find("div", "toclimit-3")
    except AttributeError as err:
        print(err)
        return -1

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
    # print(len(l))
    # print(l[4])
    # sys.exit()
    # TODO: replace spaces with underscores
    document_name = l[4].h1.string
    bodyContent = l[4]

    # print(type(bodyContent))

    content = bodyContent.find(id="mw-content-text").div

    # @pietkap
    try:
        abstract: Tag = content.find("p", attrs={"class": None})
    except AttributeError as err:
        print(err)
        print(document_name)
        return -1

    resp = sanitize(abstract)
    # print(resp)
    if resp == -1:
        return -1
    unwrap_all(abstract, "b")
    unwrap_all(abstract, "a")
    unwrap_all(abstract, "i")
    unwrap_all(abstract, "span")

    abstract_text = abstract.get_text()

    with open(f"{folderpath}{document_name}.txt", "w", encoding="utf-8") as f:
        # print( f'Saved to {folderpath}{document_name}.txt' )
        f.write(abstract_text)


def main():
    with open("urls.yml", "r", encoding="utf-8") as file:
        urls = yaml.safe_load(file)

    already = os.listdir(folderpath)
    errors = 0
    for url in tqdm(urls):

        fn = url.split("/")[-1] + ".txt"
        if fn in already:
            print(f"{fn} already exists")
            continue

        r = requests.get(url)
        if r.status_code == 200:
            text = r.text

            if scrap(text) == -1:
                print(f"Error writing {url}")
                errors += 1
        else:
            print(f"Error fetching url: {url}")

    print(f"Brought {len(urls)-errors}/{len(urls)} articles.")


if __name__ == "__main__":
    main()
