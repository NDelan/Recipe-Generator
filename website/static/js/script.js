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

    // Image mapping for recipe categories (used for placeholder images)
    const categoryImages = {
        'chicken': 'chicken-dish.jpg',
        'beef': 'beef-dish.jpg',
        'pork': 'pork-dish.jpg',
        'fish': 'fish-dish.jpg',
        'seafood': 'seafood-dish.jpg',
        'vegetarian': 'vegetarian-dish.jpg',
        'vegan': 'vegan-dish.jpg',
        'pasta': 'pasta-dish.jpg',
        'soup': 'soup-dish.jpg',
        'salad': 'salad-dish.jpg',
        'dessert': 'dessert.jpg',
        'breakfast': 'breakfast.jpg',
        'mexican': 'mexican-food.jpg',
        'italian': 'italian-food.jpg',
        'asian': 'asian-food.jpg',
        'default': 'default-dish.jpg'
    };

    // Event Listeners
    inputEl.addEventListener('input', handleInput);
    addManualBtn.addEventListener('click', handleAddManual);
    inputEl.addEventListener('keydown', handleEnterKey);
    clearAllBtn.addEventListener('click', clearAllIngredients);
    generateBtn.addEventListener('click', generateRecipe);

    // Add smooth scrolling for the "Get Started" button
    const getStartedBtn = document.querySelector('a[href="#ingredient-section"]');
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    }

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

        // Add animation effect to newly added ingredient
        setTimeout(() => {
            const newTag = selectedIngredientsContainer.lastChild;
            if (newTag && newTag.classList.contains('ingredient-tag')) {
                newTag.classList.add('highlight');
                setTimeout(() => newTag.classList.remove('highlight'), 500);
            }
        }, 10);
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

    // Determine the appropriate hero image based on recipe title and ingredients
    function getRecipeImage(recipe) {
        const title = recipe.title.toLowerCase();
        const ingredients = recipe.ingredients.join(' ').toLowerCase();

        // Check title and ingredients for keywords
        for (const [category, image] of Object.entries(categoryImages)) {
            if (title.includes(category) || ingredients.includes(category)) {
                return `url(${window.location.origin}/static/img/recipe.avif)`;
            }
        }

        // Default image if no category matches
        return `url(${window.location.origin}/static/img/recipe.avif)`;
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

            if (!recipeResponse.ok) {
                throw new Error(`API error: ${recipeResponse.status}`);
            }

            const recipeData = await recipeResponse.json();

            // Check if there's an error in the response
            if (recipeData.error) {
                throw new Error(recipeData.error);
            }

            // Display recipe
            renderRecipe(recipeData);

            // Generate similar recipes
            generateSimilarRecipes(ingredientsArray);

        } catch (error) {
            console.error('Error generating recipe:', error);
            recipeContent.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Sorry, there was an error generating your recipe: ${error.message || 'Please try again.'}
                </div>
            `;
            recipeLoading.classList.add('d-none');
            recipeContent.classList.remove('d-none');
        }
    }

    function renderRecipe(recipe) {
        // Set hero image based on recipe content
        const heroBackground = getRecipeImage(recipe);

        recipeContent.innerHTML = `
            <div class="recipe-hero" style="background-image: ${heroBackground}">
                <div class="recipe-hero-overlay">
                    <h2 class="recipe-title">${recipe.title}</h2>
                </div>
            </div>

            <div class="card-body">
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

                <div class="row">
                    <div class="col-md-5">
                        <div class="recipe-section">
                            <h3><i class="fas fa-carrot me-2"></i>Ingredients</h3>
                            <ul class="recipe-ingredients">
                                ${recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-7">
                        <div class="recipe-section">
                            <h3><i class="fas fa-list-ol me-2"></i>Instructions</h3>
                            <ol class="recipe-instructions">
                                ${recipe.instructions.map(instruction => `<li>${instruction}</li>`).join('')}
                            </ol>
                        </div>
                    </div>
                </div>

                <div class="text-center mt-4">
                    <button class="btn btn-outline-primary" onclick="window.print()">
                        <i class="fas fa-print me-2"></i> Print Recipe
                    </button>
                    <button class="btn btn-outline-success ms-2" onclick="navigator.share({title: '${recipe.title}', text: 'Check out this recipe I found!'})">
                        <i class="fas fa-share-alt me-2"></i> Share Recipe
                    </button>
                </div>
            </div>
        `;

        // Hide loading and show content
        recipeLoading.classList.add('d-none');
        recipeContent.classList.remove('d-none');

        // Add animation
        recipeContent.style.opacity = '0';
        setTimeout(() => {
            recipeContent.style.opacity = '1';
        }, 100);
    }

    async function generateSimilarRecipes(ingredients) {
        similarRecipes.classList.remove('d-none');
        similarRecipesContainer.innerHTML = '';
        similarRecipesLoading.classList.remove('d-none');

        try {
            const response = await fetch('/api/similar-recipes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ingredients: ingredients }),
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();

            // Check if there's an error or if recipes are missing
            if (data.error) {
                throw new Error(data.error);
            }

            if (!data.recipes || !Array.isArray(data.recipes)) {
                throw new Error("Invalid recipe format received");
            }

            // Render similar recipes
            renderSimilarRecipes(data.recipes);

        } catch (error) {
            console.error('Error generating similar recipes:', error);
            similarRecipesLoading.classList.add('d-none');
            similarRecipesContainer.innerHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Unable to load additional recipe suggestions: ${error.message || 'Please try again.'}
                </div>
            `;
        }
    }

    function renderSimilarRecipes(recipes) {
        similarRecipesLoading.classList.add('d-none');

        recipes.forEach((recipe, index) => {
            const matchingCount = recipe.matching_ingredients ? recipe.matching_ingredients.length : 0;
            const ingredientsArray = Array.from(selectedIngredients);

            // Determine image for this recipe
            let recipeImg = 'other-recipe.avif';
            for (const [category, image] of Object.entries(categoryImages)) {
                if (recipe.title.toLowerCase().includes(category)) {
                    recipeImg = image;
                    break;
                }
            }

            const card = document.createElement('div');
            card.className = 'col-md-4';
            card.innerHTML = `
                <div class="card recipe-card mb-3">
                    <img src="${window.location.origin}/static/img/other-recipe.avif" class="card-img-top" alt="${recipe.title}">
                    <div class="card-body">
                        <h5 class="card-title">${recipe.title}</h5>
                        <p class="card-text">${recipe.description}</p>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="badge bg-info">${recipe.cook_time}</span>
                            <span class="badge bg-secondary">${recipe.difficulty}</span>
                        </div>
                        ${recipe.matching_ingredients ? `
                            <p class="card-text text-muted small">
                                <strong>Using:</strong> ${recipe.matching_ingredients.join(', ')}
                            </p>
                        ` : ''}
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-sm btn-outline-primary w-100 generate-this-btn">Make This Recipe</button>
                    </div>
                </div>
            `;

            // Add event listener to the "Make This Recipe" button
            card.querySelector('.generate-this-btn').addEventListener('click', () => {
                // Clear ingredients and add only those from this recipe
                selectedIngredients.clear();
                if (recipe.matching_ingredients) {
                    recipe.matching_ingredients.forEach(ing => selectedIngredients.add(ing));
                }
                updateIngredientsList();

                // Generate the recipe
                generateRecipe();
            });

            // Add animation delay based on index
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';

            setTimeout(() => {
                card.style.transition = 'all 0.3s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 + (index * 100));

            similarRecipesContainer.appendChild(card);
        });
    }

    // Initialize tooltips if Bootstrap 5 is used
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});