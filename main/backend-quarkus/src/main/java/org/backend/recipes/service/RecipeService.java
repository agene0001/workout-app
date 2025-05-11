package org.backend.recipes.service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.backend.recipes.model.Category;
import org.backend.recipes.model.Recipe;
import org.backend.recipes.repository.CategoryRepository;
import org.backend.recipes.repository.RecipeRepository;
import org.backend.recipes.utils.Autocomplete;
import org.backend.recipes.utils.Term;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicBoolean;

@ApplicationScoped
public class RecipeService {
    private static final Logger logger = LoggerFactory.getLogger(RecipeService.class);
    private final RecipeRepository recipeRepository;
    private final CategoryRepository categoryRepository;
    private final JavalinRecommender recommender;
    private final Autocomplete recipeAutocomplete;
    private final AtomicBoolean isInitialized = new AtomicBoolean(false);

    @ConfigProperty(name = "quarkus.datasource.jdbc.url")
    String dbUrl;

    @ConfigProperty(name = "quarkus.datasource.username")
    String dbUser;

    @ConfigProperty(name = "quarkus.datasource.password")
    String dbPassword;

    @Inject
    public RecipeService(RecipeRepository recipeRepository, CategoryRepository categoryRepository, JavalinRecommender recommender) {
        this.recipeRepository = recipeRepository;
        this.categoryRepository = categoryRepository;
        this.recommender = recommender;
        List<Recipe> recipes = recipeRepository.findAll().list();
        List<Term> terms = recipes.stream()
                .map(recipe -> new Term(recipe.getName(), recipe.getRating()))
                .toList();
        this.recipeAutocomplete = new Autocomplete(terms);
    }


    public List<Recipe> getSample(int k) {
        try {
            return recipeRepository.findAllSample(k);
        } catch (Exception e) {
            logger.error("Error getting sample recipes: ", e);
            return Collections.emptyList();
        }
    }

    public Term[] autocompleteRecipe(String query,int size,int offset) {
        try {
            return recipeAutocomplete.allMatches(query.toLowerCase(),size,offset);
        } catch (Exception e) {
            logger.error("Error during autocomplete: ", e);
            return new Term[0];
        }
    }

    public List<Recipe> getRecommendations(String query, String ingredients, int topK) {
        try {
            if (!this.recommender.isInitialized()) {
                logger.warn("JavalinRecommender not initialized. Attempting reinitialization...");
                if (!this.recommender.reinitializeRecommender()) {
                    logger.error("Reinitialization failed. Cannot provide recommendations.");
                    return null;
                }
            }

            // Get recommendations from JavalinRecommender
            List<Recipe> similarRows = recommender.findKSimilar(query, ingredients, topK);

            // Convert Row objects to Recipe objects


            return similarRows.isEmpty() ? null : similarRows;
        } catch (IllegalStateException e) {
            logger.error("JavalinRecommender not properly initialized: ", e);
            return null;
        } catch (Exception e) {
            logger.error("Error getting recommendations: ", e);
            return null;
        }
    }

    public List<Recipe> getRecipe(String query) {
        try {
            return this.recipeRepository.getRecipe(query.toLowerCase());
        } catch (Exception e) {
            logger.error("Error retrieving recipe: ", e);
            return null;
        }
    }
    
    // Get recipes by category ID
    public List<Recipe> getRecipesByCategoryId(Integer categoryId) {
        return recipeRepository.findRecipesByCategoryId(categoryId);
    }

    // Get recipes by category name
    public List<Recipe> getRecipesByCategoryName(String categoryName, int page, int pageSize) {
        return recipeRepository.findRecipesByCategoryName(categoryName,page,pageSize);
    }

    // Alternative way to get recipes by category using the Category entity
    public List<Recipe> getRecipesByCategory(Long categoryId) {
        Optional<Category> category = categoryRepository.find("id", categoryId).firstResultOptional();
        return category.map(c -> List.copyOf(c.getRecipes())).orElse(Collections.emptyList());
    }

    public boolean isRecommenderInitialized() {
        return isInitialized.get();
    }
    
//    public List<RecipeData> buildRecipes(int calories) {
//        // Mock implementation of `build_recipes`
//        // Replace this logic with your actual constraints solver (e.g., OR-Tools)
//        return List.of(); // Placeholder
//    }
}