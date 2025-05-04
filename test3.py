import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-q", help="for search term")
parser.add_argument("-r", help="if you want one random quote")

args = parser.parse_args()

url = f"https://www.sports-reference.com/cfb/schools/oregon/2023-schedule.html"
r = requests.get(url)
print(r)
soup = bs(r.text, "html.parser")

table = soup.find("table", class_ ="sortable stats_table now_sortable")
print(table)
'''anchor1 = soup.find_all('span',{"class": "AnchorLink"})
anchor2 = soup.find_all('a',{"class":"AnchorLink"})'''