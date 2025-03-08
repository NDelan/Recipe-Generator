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
    # Load ingredients from JSON file
    with open('website/static/data/ingredients.json', 'r') as f:
        ingredients = json.load(f)

    query = request.args.get('query', '').lower()

    if query:
        # Filter ingredients that contain the query
        filtered_ingredients = [
            ingredient for ingredient in ingredients
            if query in ingredient.lower()
        ]
        print(filtered_ingredients[:10])
        return jsonify(filtered_ingredients[:10])  # Limit to 10 suggestions
    print('nothing')
    return jsonify([])

