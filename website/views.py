from flask import Blueprint, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load API key from .env

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('models/gemini-1.5-pro')

# Home Route
@main_blueprint.route('/', methods=['GET'])
def home():
    return render_template("index.html")

# API endpoint for ingredient suggestions
@main_blueprint.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    try:
        # Load ingredients from JSON file
        with open('website/static/data/ingredients.json', 'r') as f:
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return 500 error for exceptions

# API endpoint for generating recipes
@main_blueprint.route('/api/generate-recipe', methods=['POST'])
def generate_recipe():
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

        # Sometimes the model might return markdown-formatted JSON, so we need to clean it
        response_text = response.text
        # Remove markdown backticks if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "")
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "")

        recipe_json = json.loads(response_text.strip())
        return jsonify(recipe_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for generating similar recipes
@main_blueprint.route('/api/similar-recipes', methods=['POST'])
def similar_recipes():
    data = request.get_json()
    ingredients = data.get('ingredients', [])

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    try:
        # Create a prompt for Gemini
        prompt = f"""
        Generate 3 different recipe ideas (just titles and brief descriptions) using some or all of these ingredients: {', '.join(ingredients)}.

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

        # Parse the response
        response_text = response.text
        # Remove markdown backticks if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "")
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "")

        recipes_json = json.loads(response_text.strip())

        return jsonify(recipes_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500