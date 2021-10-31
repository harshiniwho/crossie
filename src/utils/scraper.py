import urllib.request
import re
import requests
from bs4 import BeautifulSoup


ANAGRIND_SOURCE = "https://www.crosswordunclued.com/2008/09/anagram-indicators.html"
BASE_LINK = "https://cryptics.fandom.com/wiki"
ANAGRIND_LINK = "/List_of_anagram_indicators"
CONTAINERS_LINK = "/List_of_container_and_contents_indicators"
LINKING_LINK = "/List_of_linking_words_and_phrases"
CHARADES_LINK = "/List_of_juxtaposition_indicators"


def fetch_anagrinds():
    anagrind_source = requests.get(ANAGRIND_SOURCE, verify=False)
    anagrind_soup = BeautifulSoup(anagrind_source.content, "html.parser")

    tds = anagrind_soup.find_all("td")
    i = 0
    anagrinds = []
    for td in tds:
        td_str = str(td)
        if "<br/>" in td_str:
            td_str = td_str.replace('<td valign="top" width="180">', '').replace('</td>', '').replace('<td valign="top" width="170">', '').replace('<td valign="top" width="175">', '')
            td_str = td_str.replace('<br/>', '')
            l = td_str.split('          ')
            anagrinds.extend(l)
    return anagrinds


def scrape_base(keyword, end_url):
    source = requests.get(BASE_LINK + end_url, verify=False)
    soup = BeautifulSoup(source.content, "html.parser")
    uls = soup.find_all("ul")
    for ul in uls:
        if keyword in str(ul):
            ul_str = str(ul)
            break
    ul_str = ul_str.replace('<ul>', '').replace('<li>', '').replace('</li>', '').replace('</ul>', '')
    return ul_str.split('\n')


def scrape_containers():
    return scrape_base("absorbing", CONTAINERS_LINK)


def scrape_linking_words():
    return scrape_base("disguising", LINKING_LINK)


def scrape_charades():
    return scrape_base("abutting", CHARADES_LINK)


def scrape_anagrams():
    anagrinds = []
    anagrinds.extend(scrape_base("absurd", ANAGRIND_LINK))
    anagrinds.extend(scrape_base("baffled", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("circulated", ANAGRIND_LINK))
    anagrinds.extend(scrape_base("defective", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("eccentric", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("fiddled", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("gambol", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("haphazard", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("inordinate", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("jaunty", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("knead", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("liberally", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("madness", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("naughty", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("obstreperous", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("paranormal", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("queer", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("ragged", ANAGRIND_LINK)) 
    anagrinds.extend(scrape_base("sabotage", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("tailor", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("uncontrolled", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("vacillating", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("wacky", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("yielding", ANAGRIND_LINK))    
    anagrinds.extend(scrape_base("zany", ANAGRIND_LINK))    
    return anagrinds


def write_list_to_file(filename, list_data):
    with open("data/" + filename, 'w') as f:
        for d in list_data:
            f.write(d + "\n")


def main():
    # anagrinds = scrape_anagrams()
    # write_list_to_file("anagrinds", anagrinds)
    charades = scrape_charades()
    write_list_to_file("charades", charades)
    linkers = scrape_linking_words()
    write_list_to_file("linking-words", linkers)
    containers = scrape_containers()
    write_list_to_file("containers", containers)
    # anagrinds = fetch_anagrinds()
    # print(anagrinds)

if __name__ == "__main__":
    main()
