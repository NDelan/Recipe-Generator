"""
This module defines the views for the website, including API endpoints and home route.
"""

import os
import json
from flask import Blueprint, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a blueprint for the main routes
main_blueprint = Blueprint('main', __name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('models/gemini-1.5-pro')

# Home Route
@main_blueprint.route('/', methods=['GET'])
def home():
    """
    Render the home page.
    """
    return render_template("index.html")

# API endpoint for ingredient suggestions
@main_blueprint.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    """
    Get a list of ingredients based on a search query.
    """
    try:
        # Load ingredients from JSON file
        with open('website/static/data/ingredients.json', 'r', encoding='utf-8') as f:
            ingredients = json.load(f)

        query = request.args.get('query', '').lower()

        if query and len(query) >= 2:
            # Filter ingredients that contain the query
            filtered_ingredients = [
                ingredient for ingredient in ingredients
                if query in ingredient.lower()
            ]
            return jsonify(filtered_ingredients[:10])  # Limit to 10 suggestions
        return jsonify([])
    except FileNotFoundError:
        return jsonify({"error": "Ingredients file not found"}), 404
    except Exception as e: # pylint: disable=broad-except
        return jsonify({"error": str(e)}), 500  # Return 500 error for exceptions

# API endpoint for generating recipes
@main_blueprint.route('/api/generate-recipe', methods=['POST'])
def generate_recipe():
    """
    Generate a recipe using the provided ingredients.
    """
    data = request.get_json()
    ingredients = data.get('ingredients', [])

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    try:
        # Create a prompt for Gemini
        prompt = f"""
        Create a detailed recipe using some or all of these ingredients: {', '.join(ingredients)}.

        You must return your response in valid JSON format with the following structure:
        {{
            "title": "Recipe Name",
            "description": "Brief description of the dish",
            "ingredients": [
                "1 cup ingredient 1",
                "2 tbsp ingredient 2",
                ...
            ],
            "instructions": [
                "Step 1: Do this",
                "Step 2: Do that",
                ...
            ],
            "cook_time": "30 minutes",
            "servings": 4,
            "difficulty": "Easy/Medium/Hard"
        }}

        Do not include any text before or after the JSON. Only return valid JSON.
        """

        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=1000,
            )
        )

        # Clean response text if markdown formatting is present
        response_text = response.text
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "")
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "")

        recipe_json = json.loads(response_text.strip())
        return jsonify(recipe_json)

    except Exception as e: # pylint: disable=broad-except
        return jsonify({"error": str(e)}), 500

# API endpoint for generating similar recipes
@main_blueprint.route('/api/similar-recipes', methods=['POST'])
def similar_recipes():
    """
    Generate similar recipes based on provided ingredients.
    """
    data = request.get_json()
    ingredients = data.get('ingredients', [])

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    try:
        # Create a prompt for Gemini
        prompt = f"""
        Generate 3 different recipe ideas (just titles and brief descriptions)
        using some or all of these ingredients: {', '.join(ingredients)}.

        You must return your response in valid JSON format with the following structure:
        {{
            "recipes": [
                {{
                    "title": "Recipe 1 Name",
                    "description": "Brief description",
                    "cook_time": "20 minutes",
                    "difficulty": "Easy/Medium/Hard",
                    "matching_ingredients": ["ingredient1", "ingredient2"]
                }},
                ...
            ]
        }}

        Do not include any text before or after the JSON. Only return valid JSON.
        """

        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                top_p=0.95,
                max_output_tokens=800,
            )
        )

        # Clean response text if markdown formatting is present
        response_text = response.text
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "")
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "")

        recipes_json = json.loads(response_text.strip())
        return jsonify(recipes_json)

    except Exception as e: # pylint: disable=broad-except
        return jsonify({"error": str(e)}), 500
