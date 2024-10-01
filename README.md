# Food Wars wiki x Nutrients estimate
This scrapes the Food Wars wiki for dish names starting with a letter that user inputs and uses the spoonacular API to get an nutrition estimate.

## Value
There are no APIs or websites sitting around with all the relevant information on Food War dishes, but there are those who want to recreate or simply just want to watch pretty food items. Reason for lack of API is since it data is almost entirely fan contributed based on watching the anime itself and there really isn't a lot to profit off or learn from.

## Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

## Setup
1. Clone this repository or download the source code. `git clone https://github.com/wg2261/foodwars_food.git`
2. Navigate to the project directory:
   ```
   cd path/to/foodwars_food
   ```
3. Create a virtual environemnt if you'd like
    ```
    python -m venv .venv 

    # On Windows:
    .venv\Scripts\activate

    # On macOS and Linux:
    source .venv/bin/activate

    ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root directory with your spoonacular connection string:
   ```
   spoonacular_API_KEY=your_key_here
   ```
   Replace `your_key_here` with your spoonacular connection string

## Usage
To run the application:
```
python main.py
```

Follow the on-screen prompts to interact
Enter only a single letter

## Data gathered
- From web: List of food items that appeared in Food Wars
  - Data gathered: Name, link to dish wiki, where the dish appears in, other relevant dish information
  - Purpose: For foodies who wants a list of pretty foods with visualization and source
- From API (spoonacular): Nutrient guess from input
  - Data gathered: Nutrient guess based on input words
  - Purpose: to provide more information on the food item, but it is faulty since not intelligent enough and anime food names are faulty

