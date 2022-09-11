import openpyxl
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from googletrans import Translator

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'recipe'
sheet.append(
    ['name of the dish', 'ingredients descrption', 'ingredients only', 'type of diet', 'cuisine', 'course of meal',
     'preparation time', 'cooking time', 'servings', 'equipments used', 'content view'])
now = datetime.now()
date_time = now.strftime("dat-%Y-%m-%dtime%H-%M-%S")
translator = Translator()



def url_recipe_list(html_soup_recipe_list, url_prefix):
    lst_url = set()
    for recipe in html_soup_recipe_list:
        lst_url.add(url_prefix + recipe.get('href'))
    return lst_url


def scraping_url(url_list):
    global source, dish_title, ingredients_descrip, ingredients_only, \
        diet, cuisine, course, prep_time, cook_time, servings, views, equipments
    for url in url_list:
        try:
            source = requests.get(url)
            source.raise_for_status()
        except Exception as HTTPError:
            print(HTTPError)
            continue
        try:
            soup_text_scrape = BeautifulSoup(source.text, 'html.parser')

            dish_title = soup_text_scrape.find('div', class_='row recipe-header').h1.text

            cuisine_course_lst = soup_text_scrape.find_all('span', itemprop='keywords')
            course, diet = cuisine_course_lst[0].text, cuisine_course_lst[1].text

            cuisine_course = soup_text_scrape.find('div', class_='col-12 products').find_all('a')
            cuisine = soup_text_scrape.find('span', itemprop='recipeCuisine').a.text
            equipments = ''.join([cuisine_course[j].text for j in range(0, len(cuisine_course))])

            html_page_recipe = soup_text_scrape.find('div', class_='row RecipeServesTime').find_all('p')
            prep_time, cook_time = html_page_recipe[0].text, html_page_recipe[1].text
            servings = int(html_page_recipe[3].text.split(' ')[0].split('-')[0])

            ingredients_descrip = (" ".join(soup_text_scrape.find('ul', class_='list-unstyled').text.split())).replace(
                ',', '\n')
            ingredients_texts = soup_text_scrape.find('ul', class_='list-unstyled').find_all('span')
            ingredients_only = ("\n".join([translator.translate(txt.text).text for txt in ingredients_texts])).strip()
            # print(ingredients_only)
            views = int(soup_text_scrape.find('span', id="recipenumvotes").text.split()[0])
        except Exception as NoneType:
            print(NoneType)
        finally:
            yield dish_title, ingredients_descrip, ingredients_only, diet, cuisine, course, prep_time, \
                  cook_time, servings, equipments, views


if __name__ == "__main__":
    url_recipe = 'https://www.archanaskitchen.com/recipes'
    source_url = requests.get(url_recipe)
    soup_url = BeautifulSoup(source_url.text, 'html.parser')
    last_page_url = soup_url.find('a', title='End').get('href')
    last_page = int(last_page_url.split('/')[-1].split('?')[0].split('-')[-1])

    for page in range(1, last_page+1):
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
        for text in scraping_text:
            sheet.append(text)

    excel.save(f"recipe_list{date_time}.xlsx")
