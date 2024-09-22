import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv

# Scrape Food Wars dishes web and return a list of all dishes on the web
def scrape_foodwars_dishes(url = "https://shokugekinosoma.fandom.com/wiki/Category:Dishes"):
    # Scrape from the website
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get wanted info section
    item_chart = soup.find_all('li', {'class': 'category-page__member'})
    if not item_chart:
        print("No items found on the page")    
        return []
    
    # Get the dish items only
    dishes = []
    for item in item_chart:
        section = item.find('a')
        name = section.get('title').strip()

        if name[:8] != 'Category':
            link = 'https://shokugekinosoma.fandom.com' + section.get('href')
            dish_info = {}
            # Get more information on the dish
            # dish_info = get_individual_dish_info(link)
            dish_info['Dish name'] = name
            dish_info['Link'] = link
            dishes.append(dish_info)
    
    return dishes

# Scrap individual dish information
def get_individual_dish_info(url):
    # Scrape from the website
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get information on the dish
    info_section = soup.find_all('div', class_='pi-item pi-data pi-item-spacing pi-border-color')
    if not info_section:
        print("No related info found on the page")

    # Get desired values from that one box on the page
    dish_info = {
        'Chef': 'N/A',
        'Cuisine Type': 'N/A',
        'Dish Type': 'N/A',
        'Menu Category': 'N/A',
        'Manga Debut': 'N/A',
        'Anime Debut': 'N/A',
        'Description': 'N/A',
        'Recipe': 'Please check website, the format varies too much :('
    }

    # Extract info from that one box
    for section in info_section:
        info = section.find('h3')
        if info:
            category = info.text.strip()
            
            # Find the corresponding value using next_sibling
            value_div = section.find('div', class_='pi-data-value')
            value = value_div.text.strip() if value_div else 'N/A'

            if category == 'Chef':
                dish_info['Chef'] = value
            elif category == 'Cuisine Type':
                dish_info['Cuisine Type'] = value
            elif category == 'Dish Type':
                dish_info['Dish Type'] = value
            elif category == 'Menu Category':
                dish_info['Menu Category'] = value
            elif category == 'Manga Debut':
                dish_info['Manga Debut'] = value
            elif category == 'Anime Debut':
                dish_info['Anime Debut'] = value
    
    # Getting description from the page
    description_section = soup.find('span', id="Description")
    if description_section:
        description = description_section.find_parent('h2').find_next_sibling('p')
        if description:
            dish_info['Description'] = description.text.strip()
    
    return dish_info

# Retrieve API key
def get_API_KEY(key):
    load_dotenv()
    API_KEY = os.getenv(key)
    if API_KEY:
        print("API key retrieved successfully!")
        return API_KEY
    else:
        print("Failed to retrieve API key. Please check your setup.")
        return None

# Get a generated estimate of nutritional value
def get_nutritional_value(name):
    spoonacular_API_KEY = get_API_KEY('spoonacular_API_KEY')

    if spoonacular_API_KEY == None:
        print("No key")
        return

    url = f'https://api.spoonacular.com/recipes/guessNutrition?apiKey={spoonacular_API_KEY}&title={name}'
    response = requests.get(url)
    data = response.json()

    nutrition = {
        'Calories': 'N/A',
        'Carbs': 'N/A',
        'Fat': 'N/A',
        'Protein': 'N/A'}

    # If error is produced or nothing is returned
    if 'calories' not in data:
        print("Unable to get an estimated guess:(")
        return nutrition

    # Obtain wanted information
    nutrition = {
        'Calories': data['calories']['value'],
        'Carbs': data['carbs']['value'],
        'Fat': data['fat']['value'],
        'Protein': data['protein']['value']}
    return nutrition


def test():
    #Testing scraper
    url = "https://shokugekinosoma.fandom.com/wiki/Category:Dishes"
    dishes = scrape_foodwars_dishes(url)
    print(dishes)

    #Testing individual
    dish = get_individual_dish_info("https://shokugekinosoma.fandom.com/wiki/90%25_Buckwheat_Soba_Garnished_with_Sakura_Shrimp_Kakiage#Reference")
    print(dish)

    #Testing getting nutritional value from API
    nutrition = get_nutritional_value('beef stew')
    print(nutrition)

def main():
    # Load all the dishes
    url = "https://shokugekinosoma.fandom.com/wiki/Category:Dishes"
    dishes = scrape_foodwars_dishes(url)

    # Get API Key
    spoonacular_API_KEY = get_API_KEY('spoonacular_API_KEY')
    if spoonacular_API_KEY == None:
        print("Please set up and input an API Key from spoonacular into the .env file")
        return
    
    # Get only a single letter
    letter = ""
    while len(letter) != 1:
        letter = input("Enter a single letter that dishes start with: ").strip()
        if len(letter) != 1:
            print("Too long")
        elif len(letter) == 1 and not letter.isalpha():
            print("Not a single letter")
            letter = ""
    letter = letter.lower()
    
    dish_list = []
    for dish in dishes:
        if dish['Dish name'][0].lower() == letter:
            more_info = get_individual_dish_info(dish['Link'])
            dish.update(more_info)
            nutrition = get_nutritional_value(dish['Dish name'])
            dish.update(nutrition)
            dish_list.append(dish)
    
    # Put data into a df format and organizing it
    df = pd.DataFrame(dish_list)
    cols = ['Dish name'] + [col for col in df.columns if col != 'Dish name'] # Make dish name the first column in final CSV/df
    df = df[cols] # Reorder the columns

    # Clean CSV file
    df.columns = df.columns.str.lower().str.replace(' ', '_') # Make all columns lower space and replacing spaces with _
    df = df.apply(lambda col: col.fillna(0) if col.dtype in ['int64', 'float64'] else col.fillna('Unknown')) # unknown is filled if player does not have that statistic (for example, a batter definitely won't have a numberGamesPitched in stat!)

    df.to_csv(f'dishes_starting_with_letter_{letter}.csv', index=False)
    
if __name__ == "__main__":
    main()