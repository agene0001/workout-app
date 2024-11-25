package com.example.server1.recipe;

import com.example.server1.Autocomplete;
import com.example.server1.Term;
import jakarta.annotation.PostConstruct;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;

@Service
public class RecipeService {
    private static final Logger logger = LogManager.getLogger(RecipeService.class);
    private final RecipeRepository recipeRepository;
    private final SparkRecommender sparkRecommender;
    private final Autocomplete recipeAutocomplete;
    private final AtomicBoolean isInitialized = new AtomicBoolean(false);

    @Value("${spring.datasource.url}")
    private String dbUrl;

    @Value("${spring.datasource.username}")
    private String dbUser;

    @Value("${spring.datasource.password}")
    private String dbPassword;

    @Autowired
    public RecipeService(RecipeRepository recipeRepository, SparkRecommender sparkRecommender) {
        this.recipeRepository = recipeRepository;
        this.sparkRecommender = sparkRecommender;
        Term[] terms = Autocomplete.setup("static/automation_recipes.csv");
        this.recipeAutocomplete = new Autocomplete(terms);
    }

    @PostConstruct
    public void initializeSparkRecommender() {
        try {
            logger.info("Initializing SparkRecommender...");
            this.sparkRecommender.setup(dbUrl, dbUser, dbPassword);
            isInitialized.set(true);
            logger.info("SparkRecommender initialization completed successfully");
        } catch (Exception e) {
            logger.error("Failed to initialize SparkRecommender: ", e);
            // Don't set isInitialized to true if initialization fails
        }
    }

    public boolean reinitializeRecommender() {
        try {
            logger.info("Attempting to reinitialize SparkRecommender...");
            this.sparkRecommender.setup(dbUrl, dbUser, dbPassword);
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

    public List<Row> getRecommendations(String query, int topK) {
        try {
            if (!isInitialized.get()) {
                logger.warn("SparkRecommender not initialized. Attempting reinitialization...");
                if (!reinitializeRecommender()) {
                    logger.error("Reinitialization failed. Cannot provide recommendations.");
                    return Collections.emptyList();
                }
            }

            return sparkRecommender.findKSimilar(query, topK).collectAsList();
        } catch (IllegalStateException e) {
            logger.error("SparkRecommender not properly initialized: ", e);
            return Collections.emptyList();
        } catch (Exception e) {
            logger.error("Error getting recommendations: ", e);
            return Collections.emptyList();
        }
    }

    public Recipe getRecipe(String query) {
        try {
            return this.recipeRepository.getRecipe(query);
        } catch (Exception e) {
            logger.error("Error retrieving recipe: ", e);
            return null;
        }
    }

    public boolean isRecommenderInitialized() {
        return isInitialized.get();
    }
    public List<Row> buildRecipes(int calories) {
        // Mock implementation of `build_recipes`
        // Replace this logic with your actual constraints solver (e.g., OR-Tools)
        return List.of(); // Placeholder
    }
}