import requests
from itertools import chain
from bs4 import BeautifulSoup

server = 'thrall'
numGuilds = 100
params = '?faction=horde'
parser = "lxml"

baseURL = 'http://www.wowprogress.com/pve/us/' + server
numPages = int(numGuilds / 20) + 1

# Fetch page 1 of guild list from URL
def fetchpage1(params):
    return requests.get(baseURL + params).content

# Fetch a subsequent page of guild list from URL
def fetchnextpage(p):
    return requests.get(baseURL + '/rating/next/' + str(p)).content

# Create a Soup that takes an HTML object as a parameter and returns
# al list of Tag objects meeting our criteria
def CreateSoup(v):
    return BeautifulSoup(v, parser).find_all("a", {"class":"guild horde"})
    
# Returns a list of guild names
def getguilds(u, n):
    # Get page 1 (different URL parameters) and chain it to the subsequent pages
    return chain(getpage1(u), getnextpages(u, n))

# Get first page of guild names
def getpage1(url):
    return (tag.nobr.string for tag in CreateSoup(fetchpage1(params)))

# Get subsequent pages as a generator
def getnextpages(url, numPages):
    return chain.from_iterable((tag.nobr.string for tag in CreateSoup(fetchnextpage(page))) for page in range(0, numPages - 1))
    
# Function call
for g in getguilds(baseURL, numPages): print(g)
