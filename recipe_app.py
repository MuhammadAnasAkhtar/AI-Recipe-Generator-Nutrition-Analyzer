# recipe_app.py
import streamlit as st
import pandas as pd
from recipe_backend import generate_recipe

# Page configuration
st.set_page_config(
    page_title="🍳 AI Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recipe-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #FF6B6B;
    }
    .nutrition-card {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
    }
    .shopping-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #FFA726;
    }
    .ingredient-tag {
        background-color: #FF6B6B;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🍳 AI Recipe Generator & Nutrition Analyzer</h1>', unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Recipe Preferences")
    
    # Available ingredients input
    st.subheader("🥕 Available Ingredients")
    ingredients_input = st.text_area(
        "Enter ingredients (comma-separated):",
        placeholder="e.g., chicken, rice, tomatoes, onions, garlic",
        help="List all ingredients you have available"
    )
    
    # Dietary preferences
    st.subheader("🏃‍♀️ Dietary Preferences")
    dietary_options = [
        "High-Protein", "Low-Carb", "Vegetarian", "Vegan", 
        "Gluten-Free", "Dairy-Free", "Balanced", "Keto"
    ]
    dietary_pref = st.selectbox("Select dietary preference:", dietary_options)
    
    # Cuisine type
    st.subheader("🌍 Cuisine Type")
    cuisine_options = ["Asian", "Italian", "Mexican", "Indian", "Mediterranean", "American", "Fusion"]
    cuisine_type = st.selectbox("Select cuisine type:", cuisine_options)
    
    # Generate button
    generate_btn = st.button("🚀 Generate Recipe", type="primary", use_container_width=True)

# Main content area
if generate_btn and ingredients_input:
    # Process ingredients
    ingredients = [ing.strip() for ing in ingredients_input.split(",") if ing.strip()]
    
    if len(ingredients) < 2:
        st.warning("⚠️ Please enter at least 2 ingredients for better recipe generation.")
    else:
        with st.spinner("🧠 Generating your personalized recipe..."):
            # Generate recipe
            result = generate_recipe(ingredients, dietary_pref, cuisine_type)
            
            # Display results
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Recipe Card
                recipe = result['generated_recipes'][0]
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.subheader("📖 Generated Recipe")
                st.markdown(f"**Recipe Name:** {recipe['name']}")
                st.markdown(f"**Cuisine:** {recipe['cuisine']}")
                st.markdown(f"**Dietary Type:** {recipe['dietary_type']}")
                st.markdown(f"**Cooking Time:** {recipe['cooking_time']}")
                st.markdown(f"**Difficulty:** {recipe['difficulty']}")
                
                st.markdown("**Ingredients:**")
                for ingredient in recipe['ingredients']:
                    st.markdown(f'<span class="ingredient-tag">{ingredient}</span>', unsafe_allow_html=True)
                
                st.markdown("**Cooking Steps:**")
                for i, step in enumerate(recipe['steps'], 1):
                    st.markdown(f"{i}. {step}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # Nutrition Analysis
                nutrition = result['nutritional_analysis']
                st.markdown('<div class="nutrition-card">', unsafe_allow_html=True)
                st.subheader("📊 Nutrition Analysis")
                st.metric("Calories", f"{nutrition['calories']} kcal")
                st.metric("Protein", nutrition['protein'])
                st.metric("Carbohydrates", nutrition['carbs'])
                st.metric("Fat", nutrition['fat'])
                st.metric("Fiber", nutrition['fiber'])
                st.metric("Health Score", f"{nutrition['health_score']}/10")
                st.metric("Dietary Compliance", nutrition['dietary_compliance'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Shopping List
                st.markdown('<div class="shopping-card">', unsafe_allow_html=True)
                st.subheader("🛒 Shopping List")
                st.markdown(f"**Budget Estimate:** ${result['budget_estimate']:.2f}")
                for item in result['shopping_list']:
                    st.markdown(f"✅ {item.title()}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Additional features
            st.markdown("---")
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("📈 Nutrition Chart")
                nutrition_data = {
                    'Nutrient': ['Protein', 'Carbs', 'Fat'],
                    'Amount (g)': [
                        float(nutrition['protein'].replace('g', '')),
                        float(nutrition['carbs'].replace('g', '')),
                        float(nutrition['fat'].replace('g', ''))
                    ]
                }
                chart_df = pd.DataFrame(nutrition_data)
                st.bar_chart(chart_df.set_index('Nutrient'))
            
            with col4:
                st.subheader("💡 Recipe Tips")
                tips = [
                    "Store fresh ingredients in airtight containers",
                    "Prep all ingredients before starting to cook",
                    "Taste and adjust seasoning as you cook",
                    "Let the dish rest for 5 minutes before serving",
                    "Double the recipe for meal prep"
                ]
                for tip in tips:
                    st.markdown(f"• {tip}")

elif generate_btn and not ingredients_input:
    st.error("❌ Please enter some ingredients to generate a recipe!")

else:
    # Welcome message and instructions
    st.markdown("""
    ## 🎯 Welcome to AI Recipe Generator!
    
    **How to use:**
    1. 🥕 **Enter your available ingredients** in the sidebar
    2. 🏃‍♀️ **Select your dietary preferences**
    3. 🌍 **Choose your preferred cuisine type**
    4. 🚀 **Click 'Generate Recipe'**
    
    ### ✨ Features:
    - 🍳 **AI-Powered Recipe Generation** - Get personalized recipes based on your ingredients
    - 📊 **Nutrition Analysis** - Detailed nutritional information and health score
    - 🛒 **Smart Shopping List** - Automatically generated with budget estimate
    - 🌍 **Multi-Cuisine Support** - Various cuisine types to choose from
    - 🏃‍♀️ **Dietary Compliance** - Recipes tailored to your dietary needs
    
    ### 🎯 Example Input:
    - **Ingredients:** chicken, rice, tomatoes, onions, garlic
    - **Dietary Preference:** High-Protein
    - **Cuisine Type:** Asian
    """)
    
    # Example output preview
    with st.expander("📋 See Example Output"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🍳 Example Recipe**")
            st.markdown("""
            **Asian High-Protein Recipe with Chicken, Rice, Tomatoes**
            - **Cuisine:** Asian
            - **Cooking Time:** 30 minutes
            - **Difficulty:** Easy
            """)
        
        with col2:
            st.markdown("**📊 Nutrition**")
            st.markdown("""
            - Calories: 750 kcal
            - Protein: 37.5g
            - Carbs: 100.0g
            - Health Score: 8.7/10
            """)
        
        with col3:
            st.markdown("**🛒 Shopping**")
            st.markdown("""
            - Budget: $17.50
            - Items: olive oil, salt, soy sauce, ginger, garlic...
            """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🍳 Built with LangGraph & Streamlit | AI Recipe Generator v1.0"
    "</div>",
    unsafe_allow_html=True
)