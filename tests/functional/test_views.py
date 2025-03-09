"""
Functional tests for the Recipe Generator application views.
"""

import os
import json
import pytest

def test_home_route(test_client):
    """
    Test the home route returns the index.html template.
    This improves coverage for the home() function in views.py.
    """
    response = test_client.get('/')
    assert response.status_code == 200

def test_ingredient_suggestions_route(recipe_api_mock_client):
    """
    Test getting ingredient suggestions for a valid query.
    """
    response = recipe_api_mock_client.get('/api/ingredients?query=chicken')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_ingredient_suggestions_empty_query(recipe_api_mock_client):
    """
    Test getting ingredient suggestions with an empty query.
    """
    response = recipe_api_mock_client.get('/api/ingredients?query=')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0

def test_ingredient_suggestions_short_query(recipe_api_mock_client, mocker):
    """
    Test getting ingredient suggestions with a query that's too short.
    """
    # Override the ingredients list for this specific test
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps([])))

    response = recipe_api_mock_client.get('/api/ingredients?query=a')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0

def test_ingredient_suggestions_no_results(recipe_api_mock_client, mocker):
    """
    Test getting ingredient suggestions with a query that returns no results.
    """
    # Make sure no items match the query
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(["Beef", "Pork", "Fish"])))

    response = recipe_api_mock_client.get('/api/ingredients?query=invalidquery')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0

def test_generate_recipe_route(recipe_api_mock_client, mocker):
    """
    Test generating a recipe with valid ingredients.
    """
    # Setup a good mock response
    mock_response = mocker.MagicMock()
    mock_response.text = json.dumps({
        "title": "Test Recipe",
        "description": "A test recipe",
        "ingredients": ["Ingredient 1", "Ingredient 2"],
        "instructions": ["Step 1", "Step 2"],
        "cook_time": "30 minutes",
        "servings": 2,
        "difficulty": "Easy"
    })
    mocker.patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response)

    ingredients = ["Chicken Breast", "Rice", "Broccoli"]
    response = recipe_api_mock_client.post('/api/generate-recipe',
                                         json={'ingredients': ingredients},
                                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "title" in data
    assert "ingredients" in data
    assert "instructions" in data
    assert isinstance(data["ingredients"], list)
    assert isinstance(data["instructions"], list)
    assert "cook_time" in data
    assert "difficulty" in data

def test_generate_recipe_empty_ingredients(recipe_api_mock_client):
    """
    Test generating a recipe with no ingredients.
    """
    response = recipe_api_mock_client.post('/api/generate-recipe',
                                         json={'ingredients': []},
                                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "No ingredients provided"

def test_generate_recipe_missing_ingredients_field(recipe_api_mock_client):
    """
    Test generating a recipe with missing ingredients field.
    """
    response = recipe_api_mock_client.post('/api/generate-recipe',
                                         json={},
                                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_generate_recipe_invalid_ingredients(recipe_api_mock_client, mocker):
    """
    Test generating a recipe with invalid ingredients.
    """
    # Setup an error response
    mock_exception = Exception("API Error")
    mocker.patch('google.generativeai.GenerativeModel.generate_content', side_effect=mock_exception)

    ingredients = ["InvalidIngredient"]
    response = recipe_api_mock_client.post('/api/generate-recipe',
                                         json={'ingredients': ingredients},
                                         content_type='application/json')
    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data

def test_generate_recipe_invalid_content_type(recipe_api_mock_client):
    """
    Test generating a recipe with invalid content type.
    """
    response = recipe_api_mock_client.post('/api/generate-recipe',
                                         data="This is not JSON",
                                         content_type='text/plain')
    assert response.status_code == 415

def test_generate_recipe_markdown_json(mocker, recipe_api_mock_client):
    """
    Test when the AI returns JSON wrapped in markdown format.
    This tests the specific branch where response starts with ```json
    """
    # Create a mock response with markdown-formatted JSON
    mock_response = mocker.MagicMock()
    mock_response.text = """```json
    {
        "title": "Test Recipe",
        "description": "A test recipe",
        "ingredients": ["Ingredient 1", "Ingredient 2"],
        "instructions": ["Step 1", "Step 2"],
        "cook_time": "30 minutes",
        "servings": 2,
        "difficulty": "Easy"
    }
    ```"""
    mocker.patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response)

    ingredients = ["Chicken Breast", "Rice"]
    response = recipe_api_mock_client.post('/api/generate-recipe',
                                          json={'ingredients': ingredients},
                                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "title" in data
    assert data["title"] == "Test Recipe"

def test_similar_recipes_route(recipe_api_mock_client, mocker):
    """
    Test generating similar recipes with valid ingredients.
    """
    # Setup a good mock response for similar recipes
    mock_response = mocker.MagicMock()
    mock_response.text = json.dumps({
        "recipes": [
            {
                "title": "Test Recipe 1",
                "description": "A test recipe",
                "cook_time": "20 minutes",
                "difficulty": "Easy",
                "matching_ingredients": ["Ingredient 1", "Ingredient 2"]
            }
        ]
    })
    mocker.patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response)

    ingredients = ["Chicken Breast", "Rice", "Broccoli"]
    response = recipe_api_mock_client.post('/api/similar-recipes',
                                         json={'ingredients': ingredients},
                                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "recipes" in data
    assert isinstance(data["recipes"], list)
    assert len(data["recipes"]) > 0
    assert "title" in data["recipes"][0]
    assert "description" in data["recipes"][0]
    assert "matching_ingredients" in data["recipes"][0]

def test_similar_recipes_empty_ingredients(recipe_api_mock_client):
    """
    Test generating similar recipes with no ingredients.
    """
    response = recipe_api_mock_client.post('/api/similar-recipes',
                                         json={'ingredients': []},
                                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "No ingredients provided"

def test_similar_recipes_missing_ingredients_field(recipe_api_mock_client):
    """
    Test generating similar recipes with missing ingredients field.
    """
    response = recipe_api_mock_client.post('/api/similar-recipes',
                                         json={},
                                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_similar_recipes_invalid_ingredients(recipe_api_mock_client, mocker):
    """
    Test generating similar recipes with invalid ingredients.
    """
    # Setup an error response
    mock_exception = Exception("API Error")
    mocker.patch('google.generativeai.GenerativeModel.generate_content', side_effect=mock_exception)

    ingredients = ["InvalidIngredient"]
    response = recipe_api_mock_client.post('/api/similar-recipes',
                                         json={'ingredients': ingredients},
                                         content_type='application/json')
    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data

def test_generate_recipe_api_failure(mocker, recipe_api_mock_client):
    """
    Test behavior when the generate recipe API fails.
    """
    # Mock the generate_content method to simulate an exception
    mocker.patch('google.generativeai.GenerativeModel.generate_content', side_effect=Exception("API Error"))

    ingredients = ["Chicken Breast", "Rice"]
    response = recipe_api_mock_client.post('/api/generate-recipe',
                                         json={'ingredients': ingredients},
                                         content_type='application/json')
    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data

def test_ingredient_suggestions_api_failure(mocker, recipe_api_mock_client):
    """
    Test behavior when the ingredient suggestions API fails.
    """
    # Mock the open function to raise an exception
    mocker.patch('builtins.open', side_effect=Exception("File not found"))

    response = recipe_api_mock_client.get('/api/ingredients?query=chicken')
    assert response.status_code == 500  # Your API should return 500 on error
    # We expect JSON with an error message
    data = json.loads(response.data)
    assert "error" in data

def test_ingredient_suggestions_special_characters(recipe_api_mock_client):
    """
    Test getting ingredient suggestions with special characters.
    """
    response = recipe_api_mock_client.get('/api/ingredients?query=@#$%^&*')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_ingredient_suggestions_numeric_query(recipe_api_mock_client):
    """
    Test getting ingredient suggestions with numbers.
    """
    response = recipe_api_mock_client.get('/api/ingredients?query=12345')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_generate_recipe_malformed_response(mocker, recipe_api_mock_client):
    """
    Test when the AI API returns a malformed response.
    """
    mock_response = mocker.MagicMock()
    mock_response.text = "Not a valid JSON response"
    mocker.patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response)

    response = recipe_api_mock_client.post('/api/generate-recipe',
                                           json={'ingredients': ["Chicken"]},
                                           content_type='application/json')
    assert response.status_code == 500


def test_generate_recipe_timeout(mocker, recipe_api_mock_client):
    """
    Test when the AI API call times out.
    """
    mocker.patch('google.generativeai.GenerativeModel.generate_content', side_effect=TimeoutError("Request timed out"))

    response = recipe_api_mock_client.post('/api/generate-recipe',
                                           json={'ingredients': ["Chicken"]},
                                           content_type='application/json')
    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Request timed out"

def test_generate_recipe_generic_markdown(mocker, recipe_api_mock_client):
    """
    Test when the AI returns JSON wrapped in generic markdown format.
    This tests the specific branch where response starts with ``` but not ```json
    """
    # Create a mock response with generic markdown format
    mock_response = mocker.MagicMock()
    mock_response.text = """```
    {
        "title": "Test Recipe",
        "description": "A test recipe",
        "ingredients": ["Ingredient 1", "Ingredient 2"],
        "instructions": ["Step 1", "Step 2"],
        "cook_time": "30 minutes",
        "servings": 2,
        "difficulty": "Easy"
    }
    ```"""
    mocker.patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response)

    ingredients = ["Chicken Breast", "Rice"]
    response = recipe_api_mock_client.post('/api/generate-recipe',
                                          json={'ingredients': ingredients},
                                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "title" in data
    assert data["title"] == "Test Recipe"

def test_similar_recipes_markdown_json(mocker, recipe_api_mock_client):
    """
    Test when the AI returns JSON wrapped in markdown format for similar recipes.
    This tests the specific branch where response starts with ```json in similar_recipes route
    """
    # Create a mock response with markdown-formatted JSON
    mock_response = mocker.MagicMock()
    mock_response.text = """```json
    {
        "recipes": [
            {
                "title": "Test Recipe 1",
                "description": "A test recipe",
                "cook_time": "20 minutes",
                "difficulty": "Easy",
                "matching_ingredients": ["Ingredient 1", "Ingredient 2"]
            }
        ]
    }
    ```"""
    mocker.patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response)

    ingredients = ["Chicken Breast", "Rice"]
    response = recipe_api_mock_client.post('/api/similar-recipes',
                                          json={'ingredients': ingredients},
                                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "recipes" in data
    assert isinstance(data["recipes"], list)
    assert len(data["recipes"]) > 0
    assert data["recipes"][0]["title"] == "Test Recipe 1"

def test_similar_recipes_generic_markdown(mocker, recipe_api_mock_client):
    """
    Test when the AI returns JSON wrapped in generic markdown format for similar recipes.
    This tests the specific branch where response starts with ``` but not ```json in similar_recipes route
    """
    # Create a mock response with generic markdown format
    mock_response = mocker.MagicMock()
    mock_response.text = """```
    {
        "recipes": [
            {
                "title": "Test Recipe 1",
                "description": "A test recipe",
                "cook_time": "20 minutes",
                "difficulty": "Easy",
                "matching_ingredients": ["Ingredient 1", "Ingredient 2"]
            }
        ]
    }
    ```"""
    mocker.patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response)

    ingredients = ["Chicken Breast", "Rice"]
    response = recipe_api_mock_client.post('/api/similar-recipes',
                                          json={'ingredients': ingredients},
                                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "recipes" in data
    assert isinstance(data["recipes"], list)
    assert len(data["recipes"]) > 0
    assert data["recipes"][0]["title"] == "Test Recipe 1"

# PYTHONPATH=$(pwd) pytest -v --cov=website tests/functional/test_views.py