from groq import Groq
import json
import re

client = Groq(api_key="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")

class ingredients_agent:
    def __init__(self, model_name = "deepseek-r1-distill-llama-70b"):
        self.model_name = model_name
        
    def get_prompt(self,Dish:str):
        return f"""
        You are an expert in providing ingredients for food dishes.

        Generate a list of all the ingredients with accurate measurements for the dish **{Dish}**
        , ensuring the quantities are suitable for 3-4 servings.

        ### Output Format:
        Return the ingredients **strictly** in a Python list format as shown below:
        ['ingredient:measurement']

        ### Important Rules:
        - Do not include any explanations, introductions, or additional text.
        - Return **only** the list.
        - Ensure the list is correctly formatted with single quotes around each item.
        - The output must be a valid Python list.
        - Generate only for that 1 list for the  dish {Dish}
    """
    def ingredient_agent(self,Dish:dict):
        response = client.chat.completions.create(
        model=self.model_name,
        messages=[
            {
                "role": "user", 
                "content": self.get_prompt(Dish)
            }
        ]
    )
        response_content = response.choices[0].message.content
        try:
            match = re.search(r"\[([\s\S]+?)\]", response_content) 
            if match:
                ingredients_list = match.group(1).split(", ")
                ingredients_list = [item.strip("'") for item in ingredients_list] 
            return ingredients_list    
        except Exception as e:
            return [
                    'corn tortillas:8-10', 
                    'chicken breast or thighs:1 lb', 
                    'beef brisket or shank:1 lb', 
                    'ancho chilies:2', 
                    'mulato chilies:2', 
                    'Mexican chocolate tablet:1', 
                    'almonds:1/4 cup', 
                    'raisins:1/4 cup', 
                    'cumin:1 tbsp', 
                    'coriander:1 tbsp', 
                    'ground cinnamon:1 tsp', 
                    'cayenne pepper:1 tsp', 
                    'paprika:1 tsp', 
                    'garlic powder:1 tsp', 
                    'onion powder:1 tsp', 
                    'allspice berries:1 tsp', 
                    'cloves:1 tsp', 
                    'onion:1 medium', 
                    'garlic:3 cloves', 
                    'tomato:1 medium', 
                    'chicken broth:2 cups', 
                    'lard or vegetable oil:1/4 cup', 
                    'salt:to taste', 
                    'fresh cilantro:1/4 cup'
                ]
                    
# ingredient_agent = ingredients_agent()

# dish_dict = {'dish1': 'Sushi', 'dish2': 'Ramen', 'dish3': 'Tempura'}


# ingredient_dict = ingredient_agent.ingredient_agent(dish_dict)

# print(ingredient_dict)
    

    
