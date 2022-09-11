import openpyxl
import requests
from bs4 import BeautifulSoup
from datetime import datetime

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'ingredients'
sheet.append(['ingredients', 'protein', 'carbs', 'fat', 'fibre', 'calcium', 'iron', 'energy'])
now = datetime.now()
date_time = now.strftime("dat-%Y-%m-%dtime%H-%M-%S")

food_url = []
url = "https://www.medindia.net/calories-in-indian-food/index.asp"
source = requests.get(url)
source.raise_for_status()
soup_html_text = BeautifulSoup(source.text, 'html.parser')
url_html = soup_html_text.find_all('div', class_='card card-block')
lst = []
for url_ex in url_html:
    lst.append(url_ex.a.get('href'))

for url in lst:
    source_url = requests.get(url)
    soup_url = BeautifulSoup(source_url.text, 'html.parser')
    lst_food_html = soup_url.find('ul', class_='mi-list-group xs-block-grid-1 sm-block-grid-2').find_all('li')
    for food in lst_food_html:
        food_url.append(food.a.get('href'))

for each_food in food_url:
    print(each_food)
    sources_url = requests.get(each_food)
    soups_url = BeautifulSoup(sources_url.text, 'html.parser')
    title = each_food.split('/')[-1].split('.')[0]
    print(title)
    try:
        each_elem = soups_url.find('table', class_='table-bordered table table-responsive').find_all('td')
        energy = each_elem[2].text
        protein = each_elem[6].text
        fat = each_elem[8].text
        fibre = each_elem[12].text
        carb = each_elem[14].text
        cal = each_elem[16].text
        iron = each_elem[-1].text
        sheet.append((title, protein, carb, fat, fibre, cal, iron, energy))
    except Exception as NoneType:
        print(Exception)


excel.save(f"ingredients_nut_values{date_time}.xlsx")
