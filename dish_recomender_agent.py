from groq import Groq
import json
import re
import ast

# Initialize the Groq client

client = Groq(api_key="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")

class Dish_recommender:
    def __init__(self,model_name = "deepseek-r1-distill-llama-70b" ):
        self.model_name = model_name
        
    def generate_prompt(self,cuisine,num):
        return f"""
            You are an expert in creating and recommending recipes.

            Recommend the top **{num}** dishes from the **{cuisine}** cuisine.

            ### Output Format:
            Return the response **strictly** as a Python dictionary in the following format:
            {{ "dish1": "name of the dish", "dish2": "name of the dish", ... }}
            ### **Important Rules:**
            - **Do not** include any explanations, introductions, or additional text.
            - **Return only** the dictionary.
            - Ensure the dictionary **always** contains exactly {num} dishes.
            - The output must be a **valid JSON-compatible dictionary**.

            ---

            ### **Why This Works**
            **Explicit Structure** → Clearly defines the expected output format.  
            **No Extra Text** → Reinforces that only the dictionary should be returned.  
            **Forces a Valid Dictionary** → Prevents responses with missing keys or incorrect formatting.  
            **Ensures `num` dishes are always included** → AI knows it must return that exact number.

    """
    def agent_Dish_recommender(self,cuisne,num):
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user", 
                    "content": self.generate_prompt(cuisne,num)
                }
            ]
        )
        response_content = response.choices[0].message.content
        match = re.search(r"\{[\s\S]*\}", response_content)
        print(match)
        if match:
            json_string = match.group().strip() 
            print("This is the JSON STringggggg", json_string) 
            extracted_dict = json.loads(json_string) 
        else:
            extracted_dict = {"dish1":"Oaxacan mole"}
        return extracted_dict
    


# Dish_agent = Dish_recommender()

# recipes = Dish_agent.agent_Dish_recommender("Indian",10)
# print(recipes)