import streamlit as st
import requests
import time
from api import recipe_recommender

# Page Configuration
st.set_page_config(
    page_title="Personal COOKBOOK", 
    page_icon="🍽️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    /* Main Container */
    .main {
        background-color: #f9f5f0;
        padding: 2rem;
        border-radius: 15px;
    }
    
    /* Titles */
    .title {
        color: #e67e22;
        text-align: center;
        font-weight: 800;
        margin-bottom: 1.5rem;
    }
    
    /* Cards */
    .recipe-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .recipe-card:hover {
        transform: translateY(-5px);
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #e67e22 !important;
        color: white !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #d35400 !important;
        transform: scale(1.02);
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e67e22;
        color: white;
    }
    
    /* Error Box */
    .error-box {
        background-color: #ffebee;
        color: #c62828;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #c62828;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "recipes_list" not in st.session_state:
    st.session_state.recipes_list = []
    st.session_state.ingredients_list = []
    st.session_state.show_results = False
    st.session_state.error_message = ""
    st.session_state.current_page = "home"

# Navigation
def navigate_to(page):
    st.session_state.current_page = page

# Home Page
def home_page():
    st.markdown("<h1 class='title'>🍽️ Personal COOKBOOK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px; color:#666;'>Discover your next favorite recipe with AI-powered recommendations</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # Option Selection
    st.subheader("✨ How would you like to find recipes?")
    option = st.radio(
        "Select an option:",
        ("Recommend Dishes", "Search by Dish Name", "Dinner Tonight"),
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Option 1: Recommend Dishes
    if option == "Recommend Dishes":
        with st.container():
            st.subheader("🌍 Cuisine Recommendation")
            col1, col2 = st.columns([3, 1])
            with col1:
                cuisine = st.text_input("Enter cuisine type:", placeholder="e.g., Italian, Indian, Mexican")
            with col2:
                num_dishes = st.selectbox("Number of dishes:", [1, 2, 3, 4, 5])
            
            if st.button("Get Recommendations", key="recommend_btn"):
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
                    navigate_to("results")
                else:
                    st.warning("Please enter a cuisine type")
    
    # Option 2: Search by Dish
    elif option == "Search by Dish Name":
        with st.container():
            st.subheader("🔍 Search Specific Dish")
            dish = st.text_input("Enter dish name:", placeholder="e.g., Chicken Tikka Masala")
            
            if st.button("Find Recipe", key="search_btn"):
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
                    navigate_to("results")
                else:
                    st.warning("Please enter a dish name")
    
    # Option 3: Dinner Tonight
    else:
        with st.container():
            st.subheader("🌙 Dinner Tonight")
            with st.expander("Tell us your preferences", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    cuisine_pref = st.selectbox("Preferred cuisine:", ["Indian", "Italian", "Chinese", "Mexican", "Surprise Me!"])
                    diet_pref = st.radio("Diet:", ["Vegetarian", "Non-Vegetarian"])
                with col2:
                    spice_level = st.select_slider("Spice level:", options=["😊 Mild", "🌶️ Medium", "🔥 Hot", "💀 Extreme"])
                    cooking_time = st.radio("Time available:", ["< 30 mins", "30-60 mins", "1+ hours"])
            
            if st.button("Plan My Dinner", key="dinner_btn"):
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
                navigate_to("results")

# Results Page
def results_page():
    st.markdown("<h1 class='title'>🍳 Your Recipe Recommendations</h1>", unsafe_allow_html=True)
    
    if st.button("← Back to Search", key="back_btn"):
        navigate_to("home")
    
    st.write("---")
    
    if st.session_state.error_message:
        st.markdown(f"<div class='error-box'>{st.session_state.error_message}</div>", unsafe_allow_html=True)
    elif st.session_state.recipes_list:
        tab1, tab2 = st.tabs(["Recipes", "Shopping List"])
        
        with tab1:
            for i, recipe_data in enumerate(st.session_state.recipes_list):
                dish_name = list(recipe_data.keys())[0]
                steps = recipe_data.get(dish_name, [])
                ingredients = st.session_state.ingredients_list[i]
                
                with st.container():
                    st.markdown(f"### 🍲 {dish_name}")
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image("https://source.unsplash.com/random/300x200/?food," + dish_name, 
                                caption=dish_name, use_column_width=True)
                    with col2:
                        with st.expander("📝 Ingredients", expanded=True):
                            st.markdown("\n".join(f"- {ing}" for ing in ingredients))
                        
                        with st.expander("👩‍🍳 Preparation Steps"):
                            if isinstance(steps, list):
                                for j, step in enumerate(steps, 1):
                                    st.markdown(f"{j}. {step}")
                            else:
                                st.markdown(steps.replace("\n", "\n\n"))
        
        with tab2:
            st.subheader("🛒 Complete Shopping List")
            all_ingredients = set()
            for ingredients in st.session_state.ingredients_list:
                all_ingredients.update(ingredients)
            
            st.markdown("\n".join(f"- {ing}" for ing in sorted(all_ingredients)))
            
            if st.download_button(
                "Download Shopping List",
                "\n".join(sorted(all_ingredients)),
                file_name="shopping_list.txt",
                mime="text/plain"
            ):
                st.success("List downloaded!")

# Request Handler
def fetch_recipes(payload):
    try:
        with st.spinner("🔍 Finding the perfect recipes..."):
            # Simulate API call
            gen_recipe = recipe_recommender()
            response = gen_recipe.generate_recipe(payload)
            time.sleep(1.5)  # Simulate processing delay

        if response:
            st.session_state.recipes_list = response.get("Recipes", [])
            st.session_state.ingredients_list = response.get("ingredient_list", [])
            st.session_state.show_results = True
            st.session_state.error_message = ""
        else:
            st.session_state.error_message = "Failed to fetch recipes. Please try again later."
    except Exception as e:
        st.session_state.error_message = f"An error occurred: {str(e)}"

# Page Router
if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "results":
    results_page()