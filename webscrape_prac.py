import requests
from bs4 import BeautifulSoup as bs
import argparse
from random import choice

parser = argparse.ArgumentParser()
parser.add_argument("-q", help="for search term")
parser.add_argument("-r", help="if you want one random quote")

args = parser.parse_args()

url = f"https://quotes.toscrape.com/"


r = requests.get(url)
print(r)
soup = bs(r.content, "html.parser")

anchor1 = soup.find_all('span',{"class": "text"})
anchor2 = soup.find_all('small', {"class": "author"})

print(anchor1)

if args.r != None :
    scraped_quote = choice([f"{quote.get_text.strip()} - {author.get_text.strip()}" for quote,author in zip(anchor1,anchor2)])
    print(scraped_quote)
else:
    for i,(quote,author) in enumerate(zip(anchor1, anchor2)):
       quote = quote.get_text()
       author = author.get_text()

       print(f"[{i}] : {quote} - {author}")

