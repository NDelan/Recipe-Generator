"""
This file contains fixtures and mocks for testing the Flask application.
It sets up the necessary test client and mock responses for the Recipe Generator API.
"""

import os
import json
import pytest
from website import create_app # pylint: disable=import-error

@pytest.fixture(scope='module')
def test_client():
    """Returns a test client for making requests to the Flask app."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.test_client() as test_client: # pylint: disable=redefined-outer-name
        yield test_client

def test_ingredient_suggestions():
    """Mock suggestions for ingredients API endpoint."""
    return [
        "Chicken Breast",
        "Chicken Thigh",
        "Chicken Stock",
        "Chicken Broth",
        "Roasted Chicken"
    ]

def test_recipe_response():
    """Mock recipe response for generate_recipe()."""
    return {
        "title": "Chicken and Rice Bowl",
        "description": "A simple and delicious chicken and rice bowl with vegetables.",
        "ingredients": [
            "2 boneless, skinless chicken breasts, cut into bite-sized pieces",
            "1 cup white or brown rice, cooked",
            "1 cup broccoli florets",
            "1 tablespoon olive oil",
            "2 cloves garlic, minced",
            "2 tablespoons soy sauce",
            "Salt and pepper to taste"
        ],
        "instructions": [
            "Cook rice according to package instructions and set aside.",
            "Heat olive oil in a large skillet over medium-high heat.",
            "Add chicken pieces and cook until no longer pink, about 5-6 minutes.",
            "Add minced garlic and cook for 30 seconds until fragrant.",
            "Add broccoli and cook for 3-4 minutes until tender-crisp.",
            "Stir in soy sauce and season with salt and pepper.",
            "Serve the chicken and broccoli mixture over cooked rice."
        ],
        "cook_time": "25 minutes",
        "servings": 2,
        "difficulty": "Easy"
    }

def test_similar_recipes_response():
    """Mock similar recipes response."""
    return {
        "recipes": [
            {
                "title": "Garlic Butter Chicken",
                "description": "Tender chicken breasts cooked in a rich garlic butter sauce.",
                "cook_time": "20 minutes",
                "difficulty": "Easy",
                "matching_ingredients": ["Chicken Breast", "Garlic", "Butter"]
            },
            {
                "title": "Chicken Stir Fry",
                "description": "A quick and healthy stir fry with chicken and colorful vegetables.",
                "cook_time": "15 minutes",
                "difficulty": "Medium",
                "matching_ingredients": ["Chicken Breast", "Broccoli", "Soy Sauce"]
            },
            {
                "title": "One-Pot Chicken and Rice",
                "description": "A comforting meal where chicken and rice cook together with herbs.",
                "cook_time": "30 minutes",
                "difficulty": "Easy",
                "matching_ingredients": ["Chicken Breast", "Rice"]
            }
        ]
    }

def test_empty_ingredients_response():
    """Mock response when no ingredients are provided."""
    return {"error": "No ingredients provided"}

def test_invalid_input_response():
    """Mock response for invalid API input."""
    return {"error": "Invalid input format"}

def test_api_error_response():
    """Mock response for API error."""
    return {"error": "Error generating recipe. Please try again."}

@pytest.fixture(scope='function')
def recipe_api_mock_client(mocker):
    """Fixture to mock the recipe API calls during tests."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app() # pylint: disable=unused-variable

    # Mock the actual implementation in views.py

    # Mock the get_ingredients method that's called in views.py
    def mock_ingredients_filter(query): # pylint: disable=unused-variable
        # This mocks the behavior inside your get_ingredients route in views.py
        if not query or len(query) < 2: # pylint: disable=unused-variable
            return []
        if query.lower() == "chicken":
            return test_ingredient_suggestions()
        if query.lower() == "invalidquery":
            return []
        return ["Ingredient 1", "Ingredient 2"]

    # Mock the open method to return test data instead of reading the actual file
    mock_open = mocker.patch('builtins.open', mocker.mock_open( # pylint: disable=unused-variable
        read_data=json.dumps(["Chicken Breast", "Chicken Thigh", "Chicken Broth",
                              "Beef Steak", "Bacon", "Ham", "Salmon",
                              "Tuna", "Tofu", "Tempeh"])
    ))

    # Create a mock for model.generate_content that returns different responses
    mock_model = mocker.patch('google.generativeai.GenerativeModel.generate_content')

    def mock_response_for_generate_recipe(prompt):
        if "InvalidIngredient" in prompt:
            mock_response = mocker.MagicMock()
            mock_response.text = "error data"
            return mock_response

        mock_response = mocker.MagicMock()
        mock_response.text = json.dumps(test_recipe_response())
        return mock_response

    def mock_response_for_similar_recipes(prompt): # pylint: disable=unused-variable
        if "InvalidIngredient" in prompt:
            mock_response = mocker.MagicMock()
            mock_response.text = "error data"
            return mock_response

        mock_response = mocker.MagicMock()
        mock_response.text = json.dumps(test_similar_recipes_response())
        return mock_response

    # Configure the mock to return different responses based on the prompt
    mock_model.side_effect = mock_response_for_generate_recipe

    with flask_app.test_client() as mock_recipe_api_client:
        yield mock_recipe_api_client
