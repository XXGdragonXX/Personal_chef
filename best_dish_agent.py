from groq import Groq
import json
import re
import ast

# Initialize the Groq client

client = Groq(api_key="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")

class best_Dish_recommender:
    def __init__(self,model_name = "deepseek-r1-distill-llama-70b" ):
        self.model_name = model_name
        
    def generate_prompt(self,cuisine,diet_pref,spice_level,cooking_time):
        return f"""
            Recommend the best dish based on the below given preference 
            "cuisine_pref": {cuisine},
            "diet_pref": {diet_pref},
            "spice_level": {spice_level},
            "cooking_time": {cooking_time}
            
            generate only 1 dish and return in dictionary format 
            {{
                "best_dish":"name of the dish"
            }}
            ### **Important Rules:**
            - **Do not** include any explanations, introductions, or additional text.
            - **Return only** the dictionary.
            - Ensure the dictionary **always** contains exactly 1 dish.
            - The output must be a **valid JSON-compatible dictionary**.

            
    """
    def agent_best_Dish_recommender(self,cuisine,diet_pref,spice_level,cooking_time):
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user", 
                    "content": self.generate_prompt(cuisine,diet_pref,spice_level,cooking_time)
                }
            ]
        )
        response_content = response.choices[0].message.content
        match = re.search(r"\{[\s\S]*\}", response_content)
        if match:
            json_string = match.group().strip()  
            extracted_dict = json.loads(json_string) 
        else:
            extracted_dict = {"best_dish":"Oaxacan mole"}
        return extracted_dict
    


# best_Dish_agent = best_Dish_recommender()

# recipes = best_Dish_agent.agent_best_Dish_recommender("Indian","Non-Vegetarian","Medium","30 minutes")
# print(recipes)