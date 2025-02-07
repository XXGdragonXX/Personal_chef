from groq import Groq
import json
import re
import ast

# Initialize the Groq client

client = Groq(api_key="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")

class recipes:
    def __init__(self,model_name = "deepseek-r1-distill-llama-70b" ):
        self.model_name = model_name
        
    def generate_prompt(self,dish,ingredients):
        return f"""
            You are an expert in creating recipes from ingredients.  

            Given:  
            - Dish Name: **{dish}**  
            - Ingredients: **{ingredients}**  

            ### **Task:**  
            Generate a recipe for **{dish}** using the provided ingredients.  

            ### **Output Format (Strictly JSON-Compatible Dictionary):**  
            {{ "{dish}": "recipe instructions" }}
            ### **Rules:**  
             **Return only** the dictionary, nothing else.  
             Ensure the recipe is **step-by-step** and logically structured.  
             **Do not** include explanations, introductions, or extra text.  
             The dictionary must contain exactly **one key-value pair**, where:  
            - The **key** is `{dish}`  
            - The **value** is the complete recipe.
    """
    def agent_recipe_recommender(self,dish,ingredients):
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user", 
                    "content": self.generate_prompt(dish,ingredients)
                }
            ]
        )
        response_content = response.choices[0].message.content
        match = re.search(r"\{[\s\S]*\}", response_content)

        if match:
            json_string = match.group().strip()  
            extracted_dict = json.loads(json_string) 
            
        else :
            extracted_dict = {}
        return extracted_dict
    


# Dish_agent = Dish_recommender()

# recipes = Dish_agent.agent_Dish_recommender("Japanese")
# print(recipes)