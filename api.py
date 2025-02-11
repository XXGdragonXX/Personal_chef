from fastapi import FastAPI
from pydantic import BaseModel
from dish_recomender_agent import Dish_recommender
from ingredients_agent import ingredients_agent
from recipe import recipes
from best_dish_agent import best_Dish_recommender

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify Streamlit's domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class recipe_recommender(BaseModel):
    key : int
    cuisine : str
    number_of_recipes : str
    dish :str
    ingredients :list
    diet_pref : str
    spice_level: int
    cooking_time : str
    



def recommend_recipes_by_llm(data):
    cuisine_dict = data
    print(f"The cuisine selected by the user is {cuisine_dict['cuisine']}")
    dishes_recommender = Dish_recommender()
    ingredients = ingredients_agent()
    recipe = recipes()
    dishes = dishes_recommender.agent_Dish_recommender(cuisine_dict['cuisine'],cuisine_dict['number_of_recipes'])
    print(dishes)
    print(type(dishes))
    Recipes = []
    ingredients_list = []
    for key , value in dishes.items():
        print(value)
        dish_ingredients = ingredients.ingredient_agent(value)
        ingredients_list.append(dish_ingredients)
        print("------------------------------------------------------------")
        print(len(dish_ingredients))
        # dish_ingredients = dish_ingredients[value]
        recipe_dish = recipe.agent_recipe_recommender(value,dish_ingredients)
        Recipes.append(recipe_dish)
    return Recipes ,ingredients_list


def user_provided_dish(data):
    cuisine_dict = data
    ingredients_list = []
    Recipes = []
    ingredients = ingredients_agent()
    dish_ingredient = ingredients.ingredient_agent(cuisine_dict['dish']) 
    ingredients_list.append(dish_ingredient)
    recipe = recipes()
    recipe_dish = recipe.agent_recipe_recommender(cuisine_dict['dish'],ingredients_list)
    Recipes.append(recipe_dish)
    return Recipes , ingredients_list
    
    
def customize_dish_on_pref(data):
    cuisine_dict = data
    ingredients_list = []
    Recipes = []
    best_Dish = best_Dish_recommender()
    best_Dish_fin = best_Dish.agent_best_Dish_recommender(cuisine_dict['cuisine'],cuisine_dict['diet_pref'],str(cuisine_dict['spice_level']),cuisine_dict['cooking_time'])
    print(f"Best Dish Choosen for you is : {best_Dish_fin['best_dish']}")
    ingredients = ingredients_agent()
    dish_ingredient = ingredients.ingredient_agent(best_Dish_fin['best_dish']) 
    ingredients_list.append(dish_ingredient)
    recipe = recipes()
    recipe_dish = recipe.agent_recipe_recommender(best_Dish_fin['best_dish'],ingredients_list)
    Recipes.append(recipe_dish)
    return Recipes , ingredients_list
    
    
    
    
    
    
    
@app.post("/submit")
def main(data : recipe_recommender):
    data_dict = data.dict()
    if data_dict['key'] == 1:
        Recipes , ingredient_list = recommend_recipes_by_llm(data_dict)
    elif data_dict['key'] == 2:
        Recipes,ingredient_list = user_provided_dish(data_dict)
    elif data_dict['key'] == 3:
        Recipes,ingredient_list = customize_dish_on_pref(data_dict)
        
    return {
        "Recipes":Recipes,
        "ingredient_list":ingredient_list
    }
        
    
        
    