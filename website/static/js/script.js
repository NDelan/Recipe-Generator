document.addEventListener('DOMContentLoaded', function() {
    // Ingredient list
    const ingredientsList = [
        // Proteins
        "Chicken Breast", "Chicken Thigh", "Ground Beef", "Beef Steak", "Pork Chop", "Pork Shoulder",
        "Bacon", "Ham", "Turkey", "Ground Turkey", "Salmon", "Tuna", "Shrimp", "Cod", "Tilapia",
        "Tofu", "Tempeh", "Seitan", "Eggs", "Egg Whites",

        // Dairy & Alternatives
        "Milk", "Almond Milk", "Soy Milk", "Oat Milk", "Coconut Milk", "Heavy Cream", "Half and Half",
        "Butter", "Margarine", "Cheddar Cheese", "Mozzarella", "Parmesan", "Feta", "Goat Cheese",
        "Cream Cheese", "Cottage Cheese", "Ricotta", "Greek Yogurt", "Yogurt", "Sour Cream",

        // Vegetables
        "Onion", "Garlic", "Carrot", "Celery", "Bell Pepper", "Spinach", "Kale", "Lettuce", "Arugula",
        "Tomato", "Potato", "Sweet Potato", "Zucchini", "Eggplant", "Cucumber", "Broccoli", "Cauliflower",
        "Brussels Sprouts", "Cabbage", "Corn", "Green Beans", "Peas", "Asparagus", "Mushroom",
        "Radish", "Beetroot", "Turnip", "Artichoke", "Avocado",

        // Fruits
        "Apple", "Banana", "Orange", "Lemon", "Lime", "Grapefruit", "Strawberry", "Blueberry",
        "Raspberry", "Blackberry", "Grape", "Pineapple", "Mango", "Peach", "Pear", "Plum", "Cherry",
        "Watermelon", "Cantaloupe", "Honeydew", "Kiwi", "Fig", "Apricot", "Coconut", "Date",

        // Grains & Starches
        "Rice", "Brown Rice", "Jasmine Rice", "Basmati Rice", "Quinoa", "Barley", "Oats", "Pasta",
        "Spaghetti", "Penne", "Linguine", "Fettuccine", "Macaroni", "Couscous", "Bread", "Sandwich Bread",
        "Baguette", "Sourdough", "Pita", "Tortilla", "Naan", "Bagel", "Breadcrumbs", "Panko", "Flour",
        "All-Purpose Flour", "Whole Wheat Flour", "Cornmeal", "Cornstarch",

        // Legumes & Nuts
        "Black Beans", "Kidney Beans", "Chickpeas", "Lentils", "Pinto Beans", "Lima Beans", "Peanut",
        "Almond", "Walnut", "Pecan", "Cashew", "Pistachio", "Pine Nut", "Sunflower Seed", "Pumpkin Seed",
        "Chia Seed", "Flax Seed", "Hemp Seed", "Sesame Seed",

        // Herbs & Spices
        "Salt", "Black Pepper", "Oregano", "Basil", "Thyme", "Rosemary", "Sage", "Parsley", "Cilantro",
        "Dill", "Mint", "Chives", "Bay Leaf", "Cinnamon", "Nutmeg", "Clove", "Allspice", "Cardamom",
        "Cumin", "Coriander", "Paprika", "Smoked Paprika", "Chili Powder", "Curry Powder", "Garam Masala",
        "Turmeric", "Ginger", "Cayenne Pepper", "Red Pepper Flake", "Vanilla Extract", "Almond Extract",

        // Oils & Vinegars
        "Olive Oil", "Vegetable Oil", "Canola Oil", "Coconut Oil", "Sesame Oil", "Peanut Oil",
        "White Vinegar", "Red Wine Vinegar", "Balsamic Vinegar", "Apple Cider Vinegar", "Rice Vinegar",

        // Condiments & Sauces
        "Ketchup", "Mustard", "Dijon Mustard", "Mayonnaise", "Hot Sauce", "Soy Sauce", "Tamari",
        "Fish Sauce", "Worcestershire Sauce", "BBQ Sauce", "Teriyaki Sauce", "Hoisin Sauce",
        "Sriracha", "Salsa", "Pesto", "Hummus", "Tahini", "Honey", "Maple Syrup", "Molasses",
        "Sugar", "Brown Sugar", "Powdered Sugar", "Stevia",

        // Baking
        "Baking Powder", "Baking Soda", "Yeast", "Chocolate Chips", "Cocoa Powder", "Shredded Coconut",
        "Dried Fruit", "Raisins", "Cranberries", "Apricot",

        // Prepared & Other
        "Broth", "Chicken Broth", "Beef Broth", "Vegetable Broth", "Tomato Sauce", "Tomato Paste",
        "Diced Tomatoes", "Crushed Tomatoes", "Pickle", "Olives", "Capers", "Anchovy", "Sun-Dried Tomato",
        "Jam", "Jelly", "Peanut Butter", "Almond Butter"
    ];

    const selectedIngredients = new Set();
    const selectedIngredientsContainer = document.getElementById('selected-ingredients');
    const noIngredientsMsg = document.getElementById('no-ingredients-msg');
    const generateBtn = document.getElementById('generate-btn');
    const clearAllBtn = document.getElementById('clear-all-btn');

    //add ingredient function
    function addIngredient(ingredient) {
        if (selectedIngredients.has(ingredient)) return;

        selectedIngredients.add(ingredient);
        updateIngredientsList();
    }

    // Remove ingredient function
    function removeIngredient(ingredient) {
        selectedIngredients.delete(ingredient);
        updateIngredientsList();
    }

    // Update the ingredients list display
    function updateIngredientsList() {
        // Clear existing ingredients
        selectedIngredientsContainer.innerHTML = '';
        selectedIngredientsContainer.appendChild(noIngredientsMsg);

        if (selectedIngredients.size == 0) {
            noIngredientsMsg.classList.remove('d-none');
            generateBtn.disabled = true;
            clearAllBtn.classList.add('d-none');
        } else {
            noIngredientsMsg.classList.add('d-none');
            generateBtn.disabled = false;
            clearAllBtn.classList.remove('d-none');
        }

        // Add ingredient tags
        selectedIngredients.forEach(ingredient => {
            const tag = document.createElement('div');
            tag.className = 'ingredient-tag';
            tag.innerHTML = `
                ${ingredient}
                <span class="remove-btn" title="Remove ${ingredient}">
                    <i class="fas fa-times"></i>
                </span>
            `;

            tag.querySelector('.remove-btn').addEventListener('click', () => {
                removeIngredient(ingredient);
            });

            selectedIngredientsContainer.appendChild(tag)
        });
    }
})