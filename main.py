# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from recipe_backend import generate_recipe
import json
import os

app = FastAPI(
    title="🍳 AI Recipe Generator API",
    description="Generate personalized recipes with nutrition analysis using AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class RecipeRequest(BaseModel):
    ingredients: List[str]
    dietary_preferences: str
    cuisine_type: str

class RecipeResponse(BaseModel):
    success: bool
    recipe: dict
    nutrition: dict
    shopping_list: List[str]
    budget_estimate: float
    message: str

# API Routes
@app.post("/generate-recipe", response_model=RecipeResponse)
async def generate_recipe_endpoint(request: RecipeRequest):
    try:
        if len(request.ingredients) < 2:
            raise HTTPException(status_code=400, detail="Please provide at least 2 ingredients")
        
        result = generate_recipe(
            request.ingredients,
            request.dietary_preferences,
            request.cuisine_type
        )
        
        return RecipeResponse(
            success=True,
            recipe=result["generated_recipes"][0],
            nutrition=result["nutritional_analysis"],
            shopping_list=result["shopping_list"],
            budget_estimate=result["budget_estimate"],
            message="Recipe generated successfully!"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Recipe Generator"}

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML Frontend
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🍳 AI Recipe Generator</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                min-height: 100vh;
                color: #333;
            }
            .header-bg {
                background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
            }
            .form-bg {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border: 2px solid #e9ecef;
            }
            .recipe-card {
                background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
                color: white;
                border: 2px solid #dc3545;
            }
            .nutrition-card {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                border: 2px solid #28a745;
            }
            .shopping-card {
                background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
                color: #212529;
                border: 2px solid #ffc107;
            }
            .chart-card {
                background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);
                color: white;
                border: 2px solid #6f42c1;
            }
            .ingredient-tag {
                background: rgba(255, 255, 255, 0.9);
                color: #dc3545;
                border: 1px solid #dc3545;
            }
            .welcome-card {
                background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
                color: white;
                border: 2px solid #17a2b8;
            }
            .feature-card {
                background: rgba(255, 255, 255, 0.95);
                color: #333;
                border: 1px solid #dee2e6;
            }
            .fade-in {
                animation: fadeIn 0.5s ease-in;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .pulse {
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            .text-high-contrast {
                color: #212529;
            }
            .bg-high-contrast {
                background-color: #ffffff;
            }
        </style>
    </head>
    <body class="min-h-screen py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <!-- Header -->
            <div class="header-bg rounded-2xl p-8 mb-8 shadow-2xl fade-in">
                <div class="text-center">
                    <h1 class="text-5xl font-bold text-white mb-4">
                        <i class="fas fa-utensils mr-4"></i>
                        AI Recipe Generator
                    </h1>
                    <p class="text-xl text-white max-w-2xl mx-auto font-semibold">
                        Create personalized recipes with AI-powered nutrition analysis and smart shopping lists
                    </p>
                </div>
            </div>

            <!-- Main Content -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Input Form -->
                <div class="lg:col-span-1">
                    <div class="form-bg rounded-2xl p-8 shadow-2xl">
                        <h2 class="text-2xl font-bold text-gray-800 mb-6">
                            <i class="fas fa-sliders-h mr-2 text-blue-600"></i>Recipe Preferences
                        </h2>
                        
                        <form id="recipeForm" class="space-y-6">
                            <!-- Ingredients -->
                            <div>
                                <label class="block text-gray-800 font-bold mb-2">
                                    <i class="fas fa-carrot mr-2 text-orange-500"></i>Available Ingredients
                                </label>
                                <textarea 
                                    id="ingredients" 
                                    placeholder="e.g., chicken, rice, tomatoes, onions, garlic"
                                    class="w-full px-4 py-3 rounded-xl bg-white border-2 border-gray-300 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium"
                                    rows="4"
                                ></textarea>
                                <p class="text-gray-600 text-sm mt-1 font-medium">Enter ingredients separated by commas</p>
                            </div>

                            <!-- Dietary Preferences -->
                            <div>
                                <label class="block text-gray-800 font-bold mb-2">
                                    <i class="fas fa-heart mr-2 text-red-500"></i>Dietary Preferences
                                </label>
                                <select id="dietaryPref" class="w-full px-4 py-3 rounded-xl bg-white border-2 border-gray-300 text-gray-800 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                    <option value="High-Protein">High-Protein</option>
                                    <option value="Low-Carb">Low-Carb</option>
                                    <option value="Vegetarian">Vegetarian</option>
                                    <option value="Vegan">Vegan</option>
                                    <option value="Gluten-Free">Gluten-Free</option>
                                    <option value="Dairy-Free">Dairy-Free</option>
                                    <option value="Balanced">Balanced</option>
                                    <option value="Keto">Keto</option>
                                </select>
                            </div>

                            <!-- Cuisine Type -->
                            <div>
                                <label class="block text-gray-800 font-bold mb-2">
                                    <i class="fas fa-globe mr-2 text-green-500"></i>Cuisine Type
                                </label>
                                <select id="cuisineType" class="w-full px-4 py-3 rounded-xl bg-white border-2 border-gray-300 text-gray-800 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                    <option value="Asian">Asian</option>
                                    <option value="Italian">Italian</option>
                                    <option value="Mexican">Mexican</option>
                                    <option value="Indian">Indian</option>
                                    <option value="Mediterranean">Mediterranean</option>
                                    <option value="American">American</option>
                                    <option value="Fusion">Fusion</option>
                                </select>
                            </div>

                            <!-- Generate Button -->
                            <button 
                                type="submit" 
                                id="generateBtn"
                                class="w-full bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-green-300 pulse text-lg"
                            >
                                <i class="fas fa-bolt mr-2"></i>
                                Generate Recipe
                            </button>
                        </form>

                        <!-- Loading Spinner -->
                        <div id="loading" class="hidden text-center mt-6">
                            <div class="inline-flex items-center px-6 py-3 rounded-xl bg-blue-600 text-white font-semibold">
                                <i class="fas fa-spinner fa-spin mr-3"></i>
                                <span>Generating your recipe...</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Results -->
                <div class="lg:col-span-2">
                    <div id="results" class="space-y-6 hidden">
                        <!-- Recipe Card -->
                        <div class="recipe-card rounded-2xl p-6 shadow-2xl fade-in">
                            <div class="flex items-center justify-between mb-4">
                                <h2 class="text-2xl font-bold">
                                    <i class="fas fa-book-open mr-2"></i>Generated Recipe
                                </h2>
                                <span id="recipeCuisine" class="bg-white text-red-600 px-3 py-1 rounded-full text-sm font-bold"></span>
                            </div>
                            <h3 id="recipeName" class="text-xl font-semibold mb-4"></h3>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <h4 class="font-bold mb-3 text-lg">
                                        <i class="fas fa-list mr-2"></i>Ingredients
                                    </h4>
                                    <div id="ingredientsList" class="space-y-2"></div>
                                </div>
                                <div>
                                    <h4 class="font-bold mb-3 text-lg">
                                        <i class="fas fa-mortar-pestle mr-2"></i>Cooking Steps
                                    </h4>
                                    <ol id="cookingSteps" class="list-decimal list-inside space-y-2 font-medium"></ol>
                                </div>
                            </div>

                            <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                                <div class="bg-white/20 p-3 rounded-lg">
                                    <div class="font-bold">Cuisine</div>
                                    <div id="recipeCuisineType" class="font-semibold"></div>
                                </div>
                                <div class="bg-white/20 p-3 rounded-lg">
                                    <div class="font-bold">Diet</div>
                                    <div id="recipeDietType" class="font-semibold"></div>
                                </div>
                                <div class="bg-white/20 p-3 rounded-lg">
                                    <div class="font-bold">Time</div>
                                    <div id="recipeTime" class="font-semibold"></div>
                                </div>
                                <div class="bg-white/20 p-3 rounded-lg">
                                    <div class="font-bold">Level</div>
                                    <div id="recipeDifficulty" class="font-semibold"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Nutrition & Shopping -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <!-- Nutrition Card -->
                            <div class="nutrition-card rounded-2xl p-6 shadow-2xl fade-in">
                                <h3 class="text-2xl font-bold mb-4">
                                    <i class="fas fa-chart-bar mr-2"></i>Nutrition Analysis
                                </h3>
                                <div id="nutritionInfo" class="space-y-3 text-lg"></div>
                            </div>

                            <!-- Shopping Card -->
                            <div class="shopping-card rounded-2xl p-6 shadow-2xl fade-in">
                                <h3 class="text-2xl font-bold mb-4">
                                    <i class="fas fa-shopping-cart mr-2"></i>Shopping List
                                </h3>
                                <div class="flex items-center justify-between mb-4 p-3 bg-white/20 rounded-lg">
                                    <span class="font-bold text-lg">Budget Estimate:</span>
                                    <span id="budgetEstimate" class="text-xl font-bold bg-yellow-500 text-white px-3 py-1 rounded-lg"></span>
                                </div>
                                <div id="shoppingItems" class="space-y-2"></div>
                            </div>
                        </div>

                        <!-- Nutrition Chart -->
                        <div class="chart-card rounded-2xl p-6 shadow-2xl fade-in">
                            <h3 class="text-2xl font-bold mb-4">
                                <i class="fas fa-chart-pie mr-2"></i>Nutrition Chart
                            </h3>
                            <div class="grid grid-cols-3 gap-4 text-center">
                                <div class="bg-white/20 p-4 rounded-lg">
                                    <div class="text-2xl font-bold" id="proteinValue">0g</div>
                                    <div class="font-semibold">Protein</div>
                                </div>
                                <div class="bg-white/20 p-4 rounded-lg">
                                    <div class="text-2xl font-bold" id="carbsValue">0g</div>
                                    <div class="font-semibold">Carbs</div>
                                </div>
                                <div class="bg-white/20 p-4 rounded-lg">
                                    <div class="text-2xl font-bold" id="fatValue">0g</div>
                                    <div class="font-semibold">Fat</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Welcome Message -->
                    <div id="welcomeMessage" class="welcome-card rounded-2xl p-8 text-center fade-in">
                        <i class="fas fa-utensils text-6xl mb-4 text-white"></i>
                        <h3 class="text-3xl font-bold mb-4 text-white">Welcome to AI Recipe Generator!</h3>
                        <p class="text-white text-lg mb-6 font-medium">
                            Enter your ingredients, select your preferences, and generate amazing recipes with AI!
                        </p>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                            <div class="feature-card p-4 rounded-xl shadow-lg">
                                <i class="fas fa-brain text-3xl mb-2 text-blue-600"></i>
                                <div class="font-bold text-gray-800">AI-Powered Recipes</div>
                                <p class="text-gray-600 text-xs mt-1">Smart recipe generation using AI</p>
                            </div>
                            <div class="feature-card p-4 rounded-xl shadow-lg">
                                <i class="fas fa-chart-line text-3xl mb-2 text-green-600"></i>
                                <div class="font-bold text-gray-800">Nutrition Analysis</div>
                                <p class="text-gray-600 text-xs mt-1">Detailed nutrition information</p>
                            </div>
                            <div class="feature-card p-4 rounded-xl shadow-lg">
                                <i class="fas fa-list-alt text-3xl mb-2 text-orange-600"></i>
                                <div class="font-bold text-gray-800">Smart Shopping Lists</div>
                                <p class="text-gray-600 text-xs mt-1">Automatic budget estimates</p>
                            </div>
                        </div>

                        <div class="mt-6 p-4 bg-white/20 rounded-lg">
                            <h4 class="font-bold text-white mb-2">🎯 Example Input:</h4>
                            <div class="text-white text-sm font-medium">
                                <p>• <strong>Ingredients:</strong> chicken, rice, tomatoes, onions, garlic</p>
                                <p>• <strong>Dietary Preference:</strong> High-Protein</p>
                                <p>• <strong>Cuisine Type:</strong> Asian</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div class="mt-8 text-center">
                <div class="bg-white rounded-lg p-4 shadow-lg">
                    <p class="text-gray-700 font-semibold">
                        🍳 Built with FastAPI & LangGraph | AI Recipe Generator v2.0
                    </p>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('recipeForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const ingredients = document.getElementById('ingredients').value
                    .split(',')
                    .map(ing => ing.trim())
                    .filter(ing => ing.length > 0);
                
                if (ingredients.length < 2) {
                    alert('Please enter at least 2 ingredients');
                    return;
                }

                const dietaryPref = document.getElementById('dietaryPref').value;
                const cuisineType = document.getElementById('cuisineType').value;

                // Show loading
                document.getElementById('loading').classList.remove('hidden');
                document.getElementById('welcomeMessage').classList.add('hidden');
                document.getElementById('results').classList.add('hidden');

                try {
                    const response = await fetch('/generate-recipe', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            ingredients: ingredients,
                            dietary_preferences: dietaryPref,
                            cuisine_type: cuisineType
                        })
                    });

                    const data = await response.json();

                    if (data.success) {
                        displayResults(data);
                    } else {
                        throw new Error(data.message || 'Failed to generate recipe');
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    document.getElementById('loading').classList.add('hidden');
                }
            });

            function displayResults(data) {
                // Recipe Info
                document.getElementById('recipeName').textContent = data.recipe.name;
                document.getElementById('recipeCuisine').textContent = data.recipe.cuisine;
                document.getElementById('recipeCuisineType').textContent = data.recipe.cuisine;
                document.getElementById('recipeDietType').textContent = data.recipe.dietary_type;
                document.getElementById('recipeTime').textContent = data.recipe.cooking_time;
                document.getElementById('recipeDifficulty').textContent = data.recipe.difficulty;

                // Ingredients
                const ingredientsList = document.getElementById('ingredientsList');
                ingredientsList.innerHTML = data.recipe.ingredients.map(ing => 
                    `<div class="ingredient-tag px-3 py-2 rounded-full font-semibold inline-block mr-2 mb-2">${ing}</div>`
                ).join('');

                // Cooking Steps
                const cookingSteps = document.getElementById('cookingSteps');
                cookingSteps.innerHTML = data.recipe.steps.map((step, index) => 
                    `<li class="mb-2 font-medium">${step}</li>`
                ).join('');

                // Nutrition Info
                const nutritionInfo = document.getElementById('nutritionInfo');
                nutritionInfo.innerHTML = `
                    <div class="flex justify-between items-center bg-white/20 p-3 rounded-lg">
                        <span class="font-semibold">Calories:</span>
                        <span class="font-bold text-xl">${data.nutrition.calories} kcal</span>
                    </div>
                    <div class="flex justify-between items-center bg-white/20 p-3 rounded-lg">
                        <span class="font-semibold">Protein:</span>
                        <span class="font-bold text-xl">${data.nutrition.protein}</span>
                    </div>
                    <div class="flex justify-between items-center bg-white/20 p-3 rounded-lg">
                        <span class="font-semibold">Carbohydrates:</span>
                        <span class="font-bold text-xl">${data.nutrition.carbs}</span>
                    </div>
                    <div class="flex justify-between items-center bg-white/20 p-3 rounded-lg">
                        <span class="font-semibold">Fat:</span>
                        <span class="font-bold text-xl">${data.nutrition.fat}</span>
                    </div>
                    <div class="flex justify-between items-center bg-white/20 p-3 rounded-lg">
                        <span class="font-semibold">Fiber:</span>
                        <span class="font-bold text-xl">${data.nutrition.fiber}</span>
                    </div>
                    <div class="flex justify-between items-center bg-white/20 p-3 rounded-lg">
                        <span class="font-semibold">Health Score:</span>
                        <span class="font-bold text-xl">${data.nutrition.health_score}/10</span>
                    </div>
                    <div class="flex justify-between items-center bg-white/20 p-3 rounded-lg">
                        <span class="font-semibold">Dietary Compliance:</span>
                        <span class="font-bold text-xl">${data.nutrition.dietary_compliance}</span>
                    </div>
                `;

                // Shopping List
                document.getElementById('budgetEstimate').textContent = `$${data.budget_estimate.toFixed(2)}`;
                const shoppingItems = document.getElementById('shoppingItems');
                shoppingItems.innerHTML = data.shopping_list.map(item => 
                    `<div class="flex items-center bg-white/30 p-3 rounded-lg">
                        <i class="fas fa-check-circle mr-3 text-green-600 text-lg"></i>
                        <span class="font-semibold text-gray-800">${item}</span>
                    </div>`
                ).join('');

                // Nutrition Chart Values
                document.getElementById('proteinValue').textContent = data.nutrition.protein;
                document.getElementById('carbsValue').textContent = data.nutrition.carbs;
                document.getElementById('fatValue').textContent = data.nutrition.fat;

                // Show results
                document.getElementById('results').classList.remove('hidden');
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)