package org.backend.service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.backend.model.Category;
import org.backend.model.Recipe;
import org.backend.repository.CategoryRepository;
import org.backend.repository.RecipeRepository;
import org.backend.utils.Autocomplete;
import org.backend.utils.Term;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import io.javalin.Javalin;

import java.util.ArrayList;
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

    @PostConstruct
    public void initializeSparkRecommender() {
        try {
            logger.info("Initializing SparkRecommender...");
            // Wrap the initialization in a separate thread with a timeout
            Thread initThread = new Thread(() -> {
                try {
                    // Log the Hadoop configuration for debugging
                    logger.info("Hadoop home: " + System.getProperty("hadoop.home.dir"));
                    logger.info("Group mapping: " + System.getProperty("hadoop.security.group.mapping", "<not set>"));
                    
                    // Set system properties for Windows
                    if (System.getProperty("os.name").toLowerCase().contains("win")) {
                        // Additional Windows-specific settings at runtime
                        System.setProperty("hadoop.security.group.mapping", 
                                          "org.apache.hadoop.security.ShellBasedUnixGroupsMapping");
                        System.setProperty("hadoop.security.authentication", "simple");
                    }
                    
                    this.recommender.setup(dbUrl, dbUser, dbPassword);
                    isInitialized.set(true);
                    logger.info("SparkRecommender initialization completed successfully");
                } catch (Exception e) {
                    logger.error("Exception in SparkRecommender initialization thread: {}", e.getMessage(), e);
                }
            });
            initThread.setDaemon(true); // Don't block application shutdown
            initThread.start();
            
            // Wait for initialization to complete or timeout
            initThread.join(120000); // 2 minute timeout
            
            if (initThread.isAlive()) {
                logger.warn("SparkRecommender initialization is taking too long and will continue in background");
            }
        } catch (Exception e) {
            logger.error("Failed to initialize SparkRecommender: {}", e.getMessage(), e);
            // Don't set isInitialized to true if initialization fails
        }
    }

    public boolean reinitializeRecommender() {
        try {
            logger.info("Attempting to reinitialize SparkRecommender...");
            this.recommender.setup(dbUrl, dbUser, dbPassword);
            isInitialized.set(true);
            logger.info("SparkRecommender reinitialization completed successfully");
            return true;
        } catch (Exception e) {
            logger.error("Failed to reinitialize SparkRecommender: ", e);
            return false;
        }
    }

    public List<Recipe> getSample(int k) {
        try {
            return recipeRepository.findAllSample(k);
        } catch (Exception e) {
            logger.error("Error getting sample recipes: ", e);
            return Collections.emptyList();
        }
    }

    public Term[] autocompleteRecipe(String query) {
        try {
            return recipeAutocomplete.allMatches(query.toLowerCase());
        } catch (Exception e) {
            logger.error("Error during autocomplete: ", e);
            return new Term[0];
        }
    }

    public List<Recipe> getRecommendations(String query, String ingredients, int topK) {
        try {
            if (!isInitialized.get()) {
                logger.warn("JavalinRecommender not initialized. Attempting reinitialization...");
                if (!reinitializeRecommender()) {
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
    public List<Recipe> getRecipesByCategoryName(String categoryName) {
        return recipeRepository.findRecipesByCategoryName(categoryName);
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