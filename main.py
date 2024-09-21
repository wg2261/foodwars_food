import requests
from bs4 import BeautifulSoup
import random

# Scrape main dishes web
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
            dish_info = get_individual_dish_info(link)
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


def main():
    url = "https://shokugekinosoma.fandom.com/wiki/Category:Dishes"
    dishes = scrape_foodwars_dishes(url)
    print(dishes)

    #Testing individual
    # dish = get_individual_dish_info("https://shokugekinosoma.fandom.com/wiki/90%25_Buckwheat_Soba_Garnished_with_Sakura_Shrimp_Kakiage#Reference")
    # print(dish)

if __name__ == "__main__":
    main()