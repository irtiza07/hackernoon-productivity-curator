import csv
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Article = namedtuple('Article', ['name', 'link'])

def get_article_from_anchor_tag(anchor_tag):
  return Article(
    name=anchor_tag.text, 
    link=f'https://hackernoon.com{anchor_tag.get("href")}'
  )

def get_articles_from_featured_section(html_body):
  articles = []
  featured_section = soup.find(class_='pages__Featured-u07uoo-0 fBpkwj')
  for article in featured_section.find_all('article'):
    article_anchor_tag = article.find('a')
    articles.append(
      get_article_from_anchor_tag(article_anchor_tag)
    )
  return articles

def get_popular_articles(html_body):
  articles = []
  article_sections = soup.find(class_='Container-sc-11afu3a-0 ivWxYQ').find_all('section')
  for section in article_sections:
    article_elements = section.find('div').find_all('article')
    for element in article_elements:
      article_anchor_tag = element.find('h2').find('a')
      articles.append(
        get_article_from_anchor_tag(article_anchor_tag)
      )
  return articles

def write_to_local_csv(articles_to_write):
  with open('articles_to_read.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Link"])
    for article in articles_to_write:
      writer.writerow([article.name, article.link])



all_articles = []
html_body = requests.get('https://hackernoon.com/', allow_redirects=True).text
soup = BeautifulSoup(html_body, 'html.parser')
  
all_articles.extend(get_articles_from_featured_section(soup))
all_articles.extend(get_popular_articles(soup))
write_to_local_csv(all_articles)

print(len(all_articles))