#pip install beautifulsoup4

from bs4 import BeautifulSoup
from lxml import html
import requests

url = "https://www.gumtree.com/for-sale/Northumberland"
page = requests.get(url)
tree = html.fromstring(page.content)
soup = BeautifulSoup(page.content, 'html.parser')

#print (soup.prettify())

for article in soup.find_all('article'):
#	print(article.find_all('a').find_all(attrs={"itemprop" : "url"})
    for link in  article.find_all(attrs={"itemprop" : "url"}):
        #print(url + link.get('href'));
        for content in link.find_all(attrs={"class" : "listing-content"}):
            for title in content.find_all(attrs={"class" : "listing-title", "itemprop" : "name"}):
                if 'size' in str(title): #size = thing to find
                    print('found')
                    print(title)
            #    else:
            #        print(title)
			#for description in content.find_all(attrs={"itemprop" : "description"}):
				#print (description.string)
			#for price in content.find_all(attrs={"itemprop" : "price"}):
				#print (price.string)
#			print(content.prettify())
			#print '--------------------'
