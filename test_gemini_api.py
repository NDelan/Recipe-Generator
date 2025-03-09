# import os
# import json
# import google.generativeai as genai
# from dotenv import load_dotenv
# import sys

# # Load environment variables
# load_dotenv()
# api_key = os.environ.get('GEMINI_API_KEY')

# if not api_key:
#     print("Error: GEMINI_API_KEY not found in environment variables.")
#     print("Create a .env file with your API key: GEMINI_API_KEY=your_key_here")
#     sys.exit(1)

# # Initialize the Gemini API
# print("Configuring Gemini API...")
# genai.configure(api_key=api_key)

# # Define model
# model = genai.GenerativeModel('models/gemini-1.5-pro')

# def test_api_connection():
#     """Test basic API connectivity"""
#     try:
#         response = model.generate_content("Hello, are you working?")
#         print("\n✅ API Connection Test: Successful")
#         print(f"Response: {response.text[:100]}...")
#         return True
#     except Exception as error:
#         print(f"\n❌ API Connection Test: Failed")
#         print(f"Error: {str(error)}")
#         return False

# def test_recipe_generation():
#     """Test recipe generation with sample ingredients"""
#     ingredients = ["chicken", "rice", "broccoli", "soy sauce"]

#     print(f"\nTesting recipe generation with ingredients: {', '.join(ingredients)}")

#     prompt = f"""
#     Create a detailed recipe using some or all of these ingredients: {', '.join(ingredients)}.

#     You must return your response in valid JSON format with the following structure:
#     {{
#         "title": "Recipe Name",
#         "description": "Brief description of the dish",
#         "ingredients": [
#             "1 cup ingredient 1",
#             "2 tbsp ingredient 2",
#             ...
#         ],
#         "instructions": [
#             "Step 1: Do this",
#             "Step 2: Do that",
#             ...
#         ],
#         "cook_time": "30 minutes",
#         "servings": 4,
#         "difficulty": "Easy/Medium/Hard"
#     }}

#     Do not include any text before or after the JSON. Only return valid JSON.
#     """

#     try:
#         print("Sending request to Gemini API...")
#         response = model.generate_content(
#             prompt,
#             generation_config=genai.types.GenerationConfig(
#                 temperature=0.7,
#                 top_p=0.95,
#                 max_output_tokens=1000,
#             )
#         )

#         # Get the response text
#         response_text = response.text
#         print("\nRaw response received:")
#         print("-" * 40)
#         print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
#         print("-" * 40)

#         # Clean the response if it contains markdown
#         if response_text.startswith("```json"):
#             response_text = response_text.replace("```json", "").replace("```", "")
#         elif response_text.startswith("```"):
#             response_text = response_text.replace("```", "")

#         # Parse JSON
#         try:
#             recipe_json = json.loads(response_text.strip())
#             print("\n✅ JSON Parsing: Successful")

#             # Validate structure
#             required_fields = ["title", "description", "ingredients", "instructions",
#                                "cook_time", "servings", "difficulty"]
#             missing_fields = [field for field in required_fields if field not in recipe_json]

#             if missing_fields:
#                 print(f"⚠️ Warning: JSON is missing some fields: {', '.join(missing_fields)}")
#             else:
#                 print("✅ JSON Structure: All required fields present")

#             # Pretty print the JSON
#             print("\nFormatted Recipe JSON:")
#             print(json.dumps(recipe_json, indent=2))

#             return True
#         except json.JSONDecodeError as error:
#             print(f"\n❌ JSON Parsing: Failed")
#             print(f"Error: {str(error)}")
#             return False

#     except Exception as error:
#         print(f"\n❌ Recipe Generation: Failed")
#         print(f"Error: {str(error)}")
#         return False

# def test_similar_recipes():
#     """Test generating similar recipes"""
#     ingredients = ["pasta", "tomato", "basil", "garlic"]

#     print(f"\nTesting similar recipes generation with ingredients: {', '.join(ingredients)}")

#     prompt = f"""
#     Generate 3 different recipe ideas (just titles and brief descriptions)
#     using some or all of these ingredients: {', '.join(ingredients)}.

#     You must return your response in valid JSON format with the following structure:
#     {{
#         "recipes": [
#             {{
#                 "title": "Recipe 1 Name",
#                 "description": "Brief description",
#                 "cook_time": "20 minutes",
#                 "difficulty": "Easy/Medium/Hard",
#                 "matching_ingredients": ["ingredient1", "ingredient2"]
#             }},
#             ...
#         ]
#     }}

#     Do not include any text before or after the JSON. Only return valid JSON.
#     """

#     try:
#         print("Sending request to Gemini API...")
#         response = model.generate_content(
#             prompt,
#             generation_config=genai.types.GenerationConfig(
#                 temperature=0.8,
#                 top_p=0.95,
#                 max_output_tokens=800,
#             )
#         )

#         # Get the response text
#         response_text = response.text
#         print("\nRaw response received:")
#         print("-" * 40)
#         print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
#         print("-" * 40)

#         # Clean the response if it contains markdown
#         if response_text.startswith("```json"):
#             response_text = response_text.replace("```json", "").replace("```", "")
#         elif response_text.startswith("```"):
#             response_text = response_text.replace("```", "")

#         # Parse JSON
#         try:
#             recipes_json = json.loads(response_text.strip())
#             print("\n✅ JSON Parsing: Successful")

#             # Validate structure
#             if "recipes" not in recipes_json or not isinstance(recipes_json["recipes"], list):
#                 print("❌ JSON Structure: 'recipes' array is missing or not an array")
#                 return False

#             if len(recipes_json["recipes"]) == 0:
#                 print("⚠️ Warning: No recipes returned")
#             else:
#                 print(f"✅ JSON Structure: {len(recipes_json['recipes'])} recipes returned")

#             # Pretty print the JSON
#             print("\nFormatted Similar Recipes JSON:")
#             print(json.dumps(recipes_json, indent=2))

#             return True
#         except json.JSONDecodeError as error:
#             print(f"\n❌ JSON Parsing: Failed")
#             print(f"Error: {str(error)}")
#             return False

#     except Exception as error:
#         print(f"\n❌ Similar Recipes Generation: Failed")
#         print(f"Error: {str(error)}")
#         return False

# if __name__ == "__main__":
#     print("=" * 50)
#     print("GEMINI API TEST")
#     print("=" * 50)

#     # Test API connection
#     connection_success = test_api_connection()
#     if not connection_success:
#         print("\n❌ Aborting further tests due to connection failure")
#         sys.exit(1)

#     # Test recipe generation
#     recipe_success = test_recipe_generation()

#     # Test similar recipes
#     similar_success = test_similar_recipes()

#     # Print summary
#     print("\n" + "=" * 50)
#     print("TEST SUMMARY")
#     print("=" * 50)
#     print(f"API Connection: {'✅ Pass' if connection_success else '❌ Fail'}")
#     print(f"Recipe Generation: {'✅ Pass' if recipe_success else '❌ Fail'}")
#     print(f"Similar Recipes: {'✅ Pass' if similar_success else '❌ Fail'}")
#     print("=" * 50)

#     if connection_success and recipe_success and similar_success:
#         print("\n✅ All tests passed! Your Gemini API is working correctly.")
#         print("You can now integrate it into your Flask application.")
#     else:
#         print("\n⚠️ Some tests failed. Please review the errors above before proceeding.")
