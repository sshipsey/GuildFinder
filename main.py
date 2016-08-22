from lxml import html, etree
import requests
from itertools import chain

server = 'thrall'
numGuilds = 100
xpath = '//a[@class="guild horde"]/nobr'

baseURL = 'http://www.wowprogress.com/pve/us/' + server
numPages = int(numGuilds / 20) + 1

# Returns a list of guild names
def getguilds(u, n):
    # Get page 1 (different URL parameters) and chain it to the subsequent pages
    return chain(getpage1(u), getnextpages(u, n))

# Get first page of guild names
def getpage1(url):
    return (child.text_content() for child in html.fromstring(requests.get(url + '?faction=horde&raids_week=&lang=en&class=&spec=').content).xpath(xpath))

# Get subsequent pages as a generator
def getnextpages(url, numPages):
    return chain.from_iterable((child.text_content() for child in html.fromstring(requests.get(baseURL + '/rating/next/' + str(page) + '/rating./raids_week./faction.horde/lang./class./spec.#rating290').content).xpath(xpath)) for page in range(0,numPages - 1))

# Function call
for g in getguilds(baseURL, numPages): print(g)
