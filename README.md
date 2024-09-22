Value: 
There are no APIs or websites sitting around with all the relevant information on Food War dishes, but there are those who want to recreate or simply just want to watch pretty food items. Reason for lack of API is since it data is almost entirely fan contributed based on watching the anime itself and there really isn't a lot to profit off or learn from.

To run:
Set up a spoonacular API Key and put it into a .env file with the name "spoonacular_API_KEY"
git clone https://github.com/wg2261/foodwars_food
cd foodwars_food
code .
python m -venv .venv
// On Windows:
.venv\Scripts\activate

// On macOS and Linux:
source .venv/bin/activate

pip install -r requirements.txt
python main.py

Data gathered:
From web: List of food items that appeared in Food Wars
  Data gathered: Name, link to dish wiki, where the dish appears in, other relevant dish information
  Purpose: For foodies who wants a list of pretty foods with visualization and source
From API (spoonacular): Nutrient guess from input
  Data gathered: Nutrient guess based on input words
  Purpose: to provide more information on the food item, but it is faulty since not intelligent enough and anime food names are faulty

