import streamlit as st
import requests
import time

# Backend API URL
BACKEND_URL = "https://personalchef-mnhcl8h7as6w764fr97hw4.streamlit.app/submit"

# Page Configuration
st.set_page_config(page_title="Personal COOKBOOK", page_icon="🍽️", layout="centered")

# Custom Styling
st.markdown(
    """
    <style>
    .stTitle {
        text-align: center;
        font-size: 36px !important;
        color: #FF5733;
        font-weight: bold;
    }
    .stRadio > label {
        font-size: 18px !important;
    }
    .stButton button {
        width: 100%;
        background-color: #FF5733 !important;
        color: white !important;
        font-size: 16px !important;
        border-radius: 10px !important;
    }
    .error-box {
        background-color: #ffcccc;
        color: #d8000c;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.markdown("<h1 class='stTitle'>🍽️ Personal COOKBOOK</h1>", unsafe_allow_html=True)
st.write("### Find the perfect recipe based on your preference!")

# Initialize session state
if "recipes_list" not in st.session_state:
    st.session_state.recipes_list = []
    st.session_state.ingredients_list = []
    st.session_state.show_results = False
    st.session_state.error_message = ""

# User Input Method Selection
st.write("---")
st.subheader("📌 How would you like to get a recipe?")
option = st.radio("📌 Select a method to get a recipe:", 
("Recommend Dishes", "Enter a Dish Name", "Dinner Tonight"))
# Function to send requests and handle errors
def fetch_recipes(payload):
    try:
        with st.spinner("🔄 Fetching recipes... Please wait."):
            response = requests.post(BACKEND_URL, json=payload)
            time.sleep(1)  # Simulate processing delay

        if response.status_code == 200:
            data = response.json()
            st.session_state.recipes_list = data.get("Recipes", [])
            st.session_state.ingredients_list = data.get("ingredient_list", [])
            st.session_state.show_results = True
            st.session_state.error_message = ""
        else:
            st.session_state.error_message = "❌ Failed to fetch data. Please try again!"
    except requests.exceptions.RequestException:
        st.session_state.error_message = "🚨 Network error! Please check your connection and try again."

# -----------------------------------------------
# OPTION 1: RECOMMEND DISHES
# -----------------------------------------------
if option == "Recommend Dishes":
    st.subheader("👨‍🍳 Get Recommended Dishes")
    cuisine = st.text_input("🌍 Enter Cuisine (e.g., Italian, Indian, Mexican):")
    num_dishes = st.slider("🔢 Select Number of Dishes:", 1, 10, 3)

    if st.button("🍽️ Get Recipes"):
        if cuisine:
            payload = {
                "key": 1,
                "cuisine": cuisine,
                "number_of_recipes": str(num_dishes),
                "dish": "none",
                "ingredients": [],
                "diet_pref": "none",
                "spice_level": 0,
                "cooking_time": "none"
            }
            fetch_recipes(payload)
        else:
            st.warning("⚠️ Please enter a cuisine.")

# -----------------------------------------------
# OPTION 2: ENTER A DISH NAME
# -----------------------------------------------
elif option == "Enter a Dish Name":
    st.subheader("🍲 Find Recipe for a Dish")
    dish = st.text_input("🔍 Enter the dish name:")

    if st.button("📜 Get Recipe"):
        if dish:
            payload = {
                "key": 2,
                "cuisine": "Default",
                "number_of_recipes": "1",
                "dish": dish,
                "ingredients": [],
                "diet_pref": "none",
                "spice_level": 0,
                "cooking_time": "none"
            }
            fetch_recipes(payload)
        else:
            st.warning("⚠️ Please enter a dish name.")

# -----------------------------------------------
# OPTION 3: DINNER TONIGHT (Guided Q&A)
# -----------------------------------------------
elif option == "Dinner Tonight":
    st.subheader("🌙 Dinner Tonight Recommendation")

    with st.expander("📌 Answer these questions to get the best dish!"):
        cuisine_pref = st.selectbox("🌍 Preferred Cuisine:", ["Indian", "Italian", "Chinese", "Mexican", "Surprise Me!"])
        diet_pref = st.radio("🍖 Diet Preference:", ["Vegetarian", "Non-Vegetarian"])
        spice_level = st.slider("🌶️ Spice Level (1-5):", 1, 5, 3)
        cooking_time = st.selectbox("⏳ Cooking Time:", ["< 20 mins", "20-40 mins", "40+ mins"])

    if st.button("🔎 Find My Dinner"):
        payload = {
            "key": 3,
            "cuisine": cuisine_pref,
            "number_of_recipes": "1",
            "dish": "none",
            "ingredients": [],
            "diet_pref": diet_pref,
            "spice_level": spice_level,
            "cooking_time": cooking_time
        }
        fetch_recipes(payload)

# -----------------------------------------------
# DISPLAY RESULTS OR ERRORS
# -----------------------------------------------
if st.session_state.error_message:
    st.markdown(f"<div class='error-box'>{st.session_state.error_message}</div>", unsafe_allow_html=True)
    if st.button("🔄 Try Again"):
        st.session_state.error_message = ""
        st.session_state.recipes_list = []
        st.session_state.ingredients_list = []
        st.session_state.show_results = False
        st.rerun()

elif st.session_state.show_results and st.session_state.recipes_list:
    st.subheader("🍴 Recommended Dishes:")

    for i, recipe_data in enumerate(st.session_state.recipes_list):
        dish_name = list(recipe_data.keys())[0]  
        steps = recipe_data.get(dish_name, [])  
        dish_ingredients = st.session_state.ingredients_list[i]  

        with st.expander(f"🥘 {dish_name} (Click to View)"):
            st.markdown("**🛒 Ingredients:**")
            formatted_ingredients = "\n".join(f"- {item}" for item in dish_ingredients)
            st.markdown(f"{formatted_ingredients}")

            st.markdown("**📜 Recipe Steps:**")
            formatted_steps = "\n\n".join(steps) if isinstance(steps, list) else steps.replace("\n", "\n\n")
            st.markdown(f"{formatted_steps}")

    if st.button("🔄 Try Again"):
        st.session_state.recipes_list = []
        st.session_state.ingredients_list = []
        st.session_state.show_results = False
        st.rerun()
