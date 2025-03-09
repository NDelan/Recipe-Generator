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
    const recipeLoading = document.getElementById('recipe-loading');
    const similarRecipes = document.getElementById('similar-recipes');
    const similarRecipesContainer = document.getElementById('similar-recipes-container');
    const similarRecipesLoading = document.getElementById('similar-recipes-loading');

    // State
    const selectedIngredients = new Set();

    // Event Listeners
    inputEl.addEventListener('input', handleInput);
    addManualBtn.addEventListener('click', handleAddManual);
    inputEl.addEventListener('keydown', handleEnterKey);
    clearAllBtn.addEventListener('click', clearAllIngredients);
    generateBtn.addEventListener('click', generateRecipe);

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

    function renderSuggestions(ingredients) {
        suggestionsContainer.innerHTML = '';

        ingredients.forEach(ingredient => {
            const div = document.createElement('div');
            div.className = 'suggestion-item';
            div.textContent = ingredient;
            div.addEventListener('click', () => {
                addIngredient(ingredient);
                inputEl.value = '';
                suggestionsContainer.classList.add('d-none');
            });
            suggestionsContainer.appendChild(div);
        });

        suggestionsContainer.classList.remove('d-none');
    }

    function handleAddManual() {
        const input = inputEl.value.trim();
        if (input) {
            addIngredient(input);
            inputEl.value = '';
            suggestionsContainer.classList.add('d-none');
        }
    }

    function handleEnterKey(e) {
        if (e.key === 'Enter') {
            const input = inputEl.value.trim();
            if (input) {
                addIngredient(input);
                inputEl.value = '';
                suggestionsContainer.classList.add('d-none');
            }
            e.preventDefault();
        }
    }

    function addIngredient(ingredient) {
        if (selectedIngredients.has(ingredient)) return;

        selectedIngredients.add(ingredient);
        updateIngredientsList();
    }

    function removeIngredient(ingredient) {
        selectedIngredients.delete(ingredient);
        updateIngredientsList();
    }

    function updateIngredientsList() {
        // Clear existing ingredients
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

    function clearAllIngredients() {
        selectedIngredients.clear();
        updateIngredientsList();
        recipeDisplay.classList.add('d-none');
        similarRecipes.classList.add('d-none');
    }

    async function generateRecipe() {
        if (selectedIngredients.size === 0) return;

        // Show loading states
        recipeDisplay.classList.remove('d-none');
        recipeContent.classList.add('d-none');
        recipeLoading.classList.remove('d-none');

        similarRecipes.classList.add('d-none');

        // Scroll to recipe display
        recipeDisplay.scrollIntoView({ behavior: 'smooth' });

        // Convert set to array
        const ingredientsArray = Array.from(selectedIngredients);

        try {
            // Generate main recipe
            const recipeResponse = await fetch('/api/generate-recipe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ingredients: ingredientsArray }),
            });
            const recipeData = await recipeResponse.json();
            // Display recipe
            renderRecipe(recipeData);

            // Generate similar recipes
            // generateSimilarRecipes(ingredientsArray);
            // showSampleRecipes();

        } catch (error) {
            console.error('Error generating recipe:', error);
            recipeContent.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Sorry, there was an error generating your recipe. Please try again.
                </div>
            `;
            recipeLoading.classList.add('d-none');
            recipeContent.classList.remove('d-none');
        }
    }

    function renderRecipe(recipe) {
        recipeContent.innerHTML = `
            <h2 class="recipe-title">${recipe.title}</h2>
            <p class="recipe-description">${recipe.description}</p>

            <div class="recipe-meta">
                <div class="recipe-meta-item">
                    <i class="fas fa-clock"></i>
                    <span>${recipe.cook_time}</span>
                </div>
                <div class="recipe-meta-item">
                    <i class="fas fa-utensils"></i>
                    <span>${recipe.servings} servings</span>
                </div>
                <div class="recipe-meta-item">
                    <i class="fas fa-chart-line"></i>
                    <span>Difficulty: ${recipe.difficulty}</span>
                </div>
            </div>

            <div class="recipe-section">
                <h3>Ingredients</h3>
                <ul class="recipe-ingredients">
                    ${recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
                </ul>
            </div>

            <div class="recipe-section">
                <h3>Instructions</h3>
                <ol class="recipe-instructions">
                    ${recipe.instructions.map(instruction => `<li>${instruction}</li>`).join('')}
                </ol>
            </div>

            <div class="text-center mt-4">
                <button class="btn btn-outline-primary" onclick="window.print()">
                    <i class="fas fa-print me-2"></i> Print Recipe
                </button>
            </div>
        `;

        // Hide loading and show content
        recipeLoading.classList.add('d-none');
        recipeContent.classList.remove('d-none');
    }
});
