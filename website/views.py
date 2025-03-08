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