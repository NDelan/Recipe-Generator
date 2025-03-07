from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env

# Create a blueprint
main_blueprint = Blueprint('main', __name__)
OPENAI_KEY = os.environ.get('OPEN_AI_KEY')

# Home Route
@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")