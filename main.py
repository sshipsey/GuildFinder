import requests
from tabulate import tabulate
from itertools import chain, zip_longest
from bs4 import BeautifulSoup

server = 'thrall'
numGuilds = 60
params = '?faction=horde'
parser = "lxml"

baseURL = 'http://www.wowprogress.com/pve/us/' + server
numPages = int(numGuilds / 20)

# Fetch page 1 of guild list from URL
def fetchpage1(params):
    return requests.get(baseURL + params).content

# Fetch a subsequent page of guild list from URL
def fetchnextpage(p):
    return requests.get(baseURL + '/rating/next/' + str(p)).content

# Create a Soup that takes an HTML object as a parameter and returns
# a list of Tag objects meeting our criteria
def CreateSoup(v):
    return zip_longest((tag.nobr.string for tag in BeautifulSoup(v, parser).find_all("a", {"class":"guild horde"})), (tag.b.string for tag in BeautifulSoup(v, parser).find_all("span", {"class":"innerLink ratingProgress"})))
    
# Returns a generator of guild names by chaining the first page to subsequent pages
def getguilds(u, n):
    return chain(getpage1(u), getnextpages(u, n))

# Get first page of guild names
def getpage1(url):
    return (CreateSoup(fetchpage1(params)))

# Get subsequent pages as a generator
def getnextpages(url, numPages):
    return chain.from_iterable((CreateSoup(fetchnextpage(page))) for page in range(0, numPages - 1))
    
# Function call
print(tabulate([guild for guild in getguilds(baseURL, numPages)], headers=['Guild Name', 'Progression']))