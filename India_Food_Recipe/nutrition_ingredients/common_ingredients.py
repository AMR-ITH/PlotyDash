import openpyxl
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from googletrans import Translator


translator = Translator()

dict = {}
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'ingredients'
sheet.append(['ingredients', 'ingredients_counts'])
now = datetime.now()
date_time = now.strftime("dat-%Y-%m-%dtime%H-%M-%S")


def url_recipe_list(html_soup_recipe_list, url_prefix):
    lst_url = set()
    for recipe in html_soup_recipe_list:
        lst_url.add(url_prefix + recipe.get('href'))
    return lst_url


def scraping_url(url_list):
    global source

    for url in url_list:
        print(url)
        try:
            source = requests.get(url)
            source.raise_for_status()
        except Exception as HTTPError:
            print(HTTPError)
            continue
        try:
            soup_text_scrape = BeautifulSoup(source.text, 'html.parser')
            texts = soup_text_scrape.find('ul', class_='list-unstyled').find_all('span')
            cuisine = soup_text_scrape.find('span', itemprop='recipeCuisine').a.text
            cuisine_lst = ['Continental', 'Middle Eastern', 'Italian Recipes', 'French', 'Caribbean ', 'Vietnamese',
                           'Mediterranean', 'Thai', 'Japanese', 'Mexican', 'European', 'Fusion', 'American', 'Greek',
                           'African', 'Indonesian', 'Malaysian', 'Jewish', 'Korean', 'Arab', 'British', 'Singapore',
                           'Swedish']
            if cuisine not in cuisine_lst:
                print(cuisine)
                for tet in texts:
                    out = translator.translate(tet.text, dest='en').text
                    dict[out] = dict.get(out, 0) + 1
        except Exception as NoneType:
            print(NoneType)
    return dict


if __name__ == "__main__":
    url_recipe = 'https://www.archanaskitchen.com/recipes'
    source_url = requests.get(url_recipe)
    soup_url = BeautifulSoup(source_url.text, 'html.parser')
    last_page_url = soup_url.find('a', title='End').get('href')
    last_page = int(last_page_url.split('/')[-1].split('?')[0].split('-')[-1])
    for page in range(1, last_page + 1):
        url = f"https://www.archanaskitchen.com/recipes/page-{page}"
        url_prefix = f"https://www.archanaskitchen.com"
        print(url)
        source = requests.get(url)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, 'html.parser')
        recipes = soup.find('div', id='ak_recipe_categoryblog').find_all('a', itemprop='url')
        url_list = url_recipe_list(recipes, url_prefix)
        print(url_list)
        scraping_text = scraping_url(url_list)

for key, value in dict.items():
    sheet.append((key, value))
excel.save(f"ingredients_list{date_time}.xlsx")
