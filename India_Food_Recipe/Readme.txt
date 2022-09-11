-Web-scrapped food recipes using beatuifulsoup library from Archana’s Kitchen website(i.e scraping.py)file
which produces excel file named as recipe_list-(date-time) 
-nutrition_ingredient folder from Archana’s Kitchen website only ingredient used is stored in ingredients_listdat(date and time) excel file
with help of common_ingredients.py file and india's common ingredient list with nutritional value is web scraped from
this website "https://www.medindia.net/calories-in-indian-food/index.asp" ,scrapd data is saved in ingredients_nut_valuesdat(date and time)
then manually ingredients facts is been copied to ingredients_listdat(date and time) excel file
-EDA, cleaning of data is done in EDA_Cleaning.ipynb which generates the final recipe_final_list excel file Using this
file dashboard is craeted using plotly and dash which is the folder plotly_dash
-plotly_dash dashboard is uploaded into web with help of heroku 
(https://recipe-456.herokuapp.com/)