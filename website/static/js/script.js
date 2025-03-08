document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const inputEl = document.getElementById('ingredient-input');
    const suggestionsContainer = document.getElementById('suggestions-container');
    const selectedIngredientsContainer = document.getElementById('selected-ingredients');
    const noIngredientsMsg = document.getElementById('no-ingredients-msg');
    const generateBtn = document.getElementById('generate-btn');
    const addManualBtn = document.getElementById('add-manual-btn');
    const clearAllBtn = document.getElementById('clear-all-btn');
    const recipeDisplay = document.getElementById('recipe-display');
    const recipeContent = document.getElementById('recipe-content');

    // State
    const selectedIngredients = new Set();

    // Event Listeners
    inputEl.addEventListener('input', handleInput);

    // Click outside to close suggestions
    document.addEventListener('click', function(e) {
        if (!inputEl.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.classList.add('d-none');
        }
    });

    // Functions
    async function handleInput() {
        const input = this.value.trim().toLowerCase();

        if (input.length < 2) {
            suggestionsContainer.classList.add('d-none');
            return;
        }

        try {
            const response = await fetch(`/api/ingredients?query=${encodeURIComponent(input)}`);
            const ingredients = await response.json();

            if (ingredients.length > 0) {
                renderSuggestions(ingredients);
            } else {
                suggestionsContainer.classList.add('d-none');
            }
        } catch (error) {
            console.error('Error fetching suggestions:', error);
            suggestionsContainer.classList.add('d-none');
        }
    }

    // Manual add button
    addManualBtn.addEventListener('click', function() {
        const input = inputEl.value.trim();
        if (input) {
            addIngredient(input);
            inputEl.value = '';
            suggestionsContainer.classList.add('d-none');
        }
    });

    // Handle enter key
    inputEl.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const input = this.value.trim();
            if (input) {
                addIngredient(input);
                this.value = '';
                suggestionsContainer.classList.add('d-none');
            }
            e.preventDefault();
        }
    });

    // Clear all ingredients
    clearAllBtn.addEventListener('click', function() {
        selectedIngredients.clear();
        updateIngredientsList();
        recipeDisplay.classList.add('d-none');
        document.getElementById('recipe-results').classList.add('d-none');
    });

    // Add ingredient function
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
        // Clear existing ingredients (proper way)
        selectedIngredientsContainer.innerHTML = '';
        selectedIngredientsContainer.appendChild(noIngredientsMsg);

        if (selectedIngredients.size === 0) {
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

            selectedIngredientsContainer.appendChild(tag);
        });
    }

    // Generate recipes button
    generateBtn.addEventListener('click', function() {
        // Show loading state
        this.disabled = true;
        this.innerHTML = '<span class="loading me-2"></span> Generating...';

        // Display recipe section
        setTimeout(() => {
            recipeDisplay.classList.remove('d-none');
            document.getElementById('recipe-results').classList.remove('d-none');

            // Scroll to recipe display
            recipeDisplay.scrollIntoView({ behavior: 'smooth' });

            // Reset button
            this.disabled = false;
            this.innerHTML = '<i class="fas fa-magic me-1"></i> Generate Recipes';

            // Display placeholder recipe
            recipeContent.innerHTML = getPlaceholderRecipe();

            // Show sample recipes
            showSampleRecipes();
        }, 1500);
    });

    // Get placeholder recipe content
    function getPlaceholderRecipe() {
        const ingredients = Array.from(selectedIngredients);
        const mainIngredients = ingredients.slice(0, Math.min(3, ingredients.length));

        return `
            <div class="mb-4">
                <h3>${mainIngredients.join(' & ')} ${mainIngredients.length < 3 ? 'Delight' : 'Special'}</h3>
                <p class="text-muted">A delicious recipe using your selected ingredients</p>
            </div>

            <div class="mb-4">
                <h4>Ingredients:</h4>
                <ul>
                    ${ingredients.map(ing => `<li>${ing}</li>`).join('')}
                    <li>Salt and pepper to taste</li>
                </ul>
            </div>

            <div class="mb-4">
                <h4>Instructions:</h4>
                <ol>
                    <li>Prepare all ingredients by washing and chopping as needed.</li>
                    <li>In a large pan, heat oil over medium heat.</li>
                    <li>Add your base ingredients and cook until softened.</li>
                    <li>Combine remaining ingredients and cook thoroughly.</li>
                    <li>Season with salt and pepper to taste.</li>
                    <li>Serve hot and enjoy your meal!</li>
                </ol>
            </div>
        `;
    }

    // Show sample recipes for demonstration
    function showSampleRecipes() {
        const recipesContainer = document.getElementById('recipes-container');
        recipesContainer.innerHTML = '';

        const sampleRecipes = [
            {
                title: "Quick Veggie Stir Fry",
                ingredients: ["Bell Pepper", "Broccoli", "Garlic", "Soy Sauce", "Rice"],
                time: "20 mins",
                difficulty: "Easy"
            },
            {
                title: "Simple Chicken Pasta",
                ingredients: ["Chicken Breast", "Pasta", "Tomato", "Basil", "Olive Oil", "Garlic"],
                time: "30 mins",
                difficulty: "Medium"
            },
            {
                title: "Hearty Bean Soup",
                ingredients: ["Black Beans", "Onion", "Garlic", "Cumin", "Cayenne Pepper"],
                time: "45 mins",
                difficulty: "Easy"
            }
        ];

        sampleRecipes.forEach(recipe => {
            const matching = recipe.ingredients.filter(ing =>
                selectedIngredients.has(ing)
            ).length;

            const matchPercentage = Math.round((matching / recipe.ingredients.length) * 100);

            const recipeCard = document.createElement('div');
            recipeCard.className = 'col-md-6 col-lg-4';
            recipeCard.innerHTML = `
                <div class="card recipe-card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${recipe.title}</h5>
                        <div class="mb-3">
                            <span class="badge bg-success">${recipe.time}</span>
                            <span class="badge bg-info">${recipe.difficulty}</span>
                        </div>
                        <div class="progress mb-3" title="${matchPercentage}% ingredients match">
                            <div class="progress-bar bg-success" style="width: ${matchPercentage}%">
                                ${matchPercentage}% match
                            </div>
                        </div>
                        <p><strong>You'll need:</strong></p>
                        <ul>
                            ${recipe.ingredients.map(ing => `
                                <li class="${selectedIngredients.has(ing) ? 'text-success' : 'text-muted'}">
                                    ${ing} ${selectedIngredients.has(ing) ? '✓' : ''}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-outline-primary w-100">View Recipe</button>
                    </div>
                </div>
            `;

            recipesContainer.appendChild(recipeCard);
        });
    }
});
