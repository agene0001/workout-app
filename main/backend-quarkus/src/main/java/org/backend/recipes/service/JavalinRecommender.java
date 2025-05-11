package org.backend.recipes.service;

import io.quarkus.runtime.Startup;
import jakarta.annotation.PostConstruct;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

import java.io.Serializable;
import java.sql.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import javax.sql.DataSource;

import org.backend.recipes.model.Recipe;
import org.backend.recipes.repository.RecipeRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * A lightweight recipe recommendation service that replaces Spark-based implementation
 * with a pure Java solution using word embeddings and approximate nearest neighbor search.
 */
@Startup
@ApplicationScoped
public class JavalinRecommender implements Serializable {
    private static final Logger LOG = LoggerFactory.getLogger(JavalinRecommender.class);

    // Word embeddings map
    private Map<String, float[]> wordVectors = new ConcurrentHashMap<>();

    // Recipe data - stored as ID -> RecipeData mapping
    private Map<Integer, RecipeData> recipeDataMap = new ConcurrentHashMap<>();

    // Recipe vectors - stored as ID -> Vector mapping
    private Map<Integer, float[]> recipeVectors = new ConcurrentHashMap<>();

    // Initialization flag
    private AtomicBoolean isInitialized = new AtomicBoolean(false);

    // Common constants
    private static final int VECTOR_SIZE = 100;
    private static final Pattern WORD_TOKENIZER = Pattern.compile("\\s+");
    private static final Pattern NON_ALPHA = Pattern.compile("[^a-z\\s]");

    @Inject
    private DataSource dataSource;

    @Inject
    private RecipeRepository recipeRepository;

    // Store recipe data for easy lookup
    static class RecipeData {
        int id;
        String name;
        String ingredients;

        RecipeData(int id, String name, String ingredients) {
            this.id = id;
            this.name = name;
            this.ingredients = ingredients;
        }

        public int getId() {
            return id;
        }

        public String getName() {
            return name;
        }

        public String getIngredients() {
            return ingredients;
        }
    }

    /**
     * Initialize the recommender by loading recipes and building word vectors
     */
    @PostConstruct
    void initialize() {
        // Check if already initialized (e.g., if reinitializeRecommender was called)
        // Although with @Startup, this PostConstruct should ideally run only once.
        if (isInitialized.get()) {
            LOG.info("JavalinRecommender already initialized.");
            return;
        }

        try {
            LOG.info("JavalinRecommender initialization started via @PostConstruct...");

            // Load recipe data using the injected DataSource
            loadRecipeData();

            // Build word vectors
            buildWordVectors();

            // Generate recipe vectors
            generateRecipeVectors();

            // Set initialization flag
            isInitialized.set(true);

            LOG.info("JavalinRecommender initialization completed successfully with {} recipes", recipeDataMap.size());
        } catch (Exception e) {
            LOG.error("Error during JavalinRecommender initialization: {}", e.getMessage(), e);
            // Decide how to handle fatal initialization errors.
            // Throwing a runtime exception might prevent the app from starting,
            // which might be desirable if the recommender is critical.
            throw new RuntimeException("Failed to initialize JavalinRecommender", e);
        }
    }

    /**
     * Check if the recommender is initialized
     */
    public boolean isInitialized() {
        return isInitialized.get();
    }

    /**
     * Reinitialize the recommender (if needed, e.g., trigger manually via an endpoint)
     */
    public boolean reinitializeRecommender() {
        if (!isInitialized.compareAndSet(true, false)) {
            // If it wasn't initialized, or another thread is already reinitializing, just return false or wait.
            // For simplicity, we'll just proceed if it was set to false.
            if(isInitialized.get()){
                LOG.warn("Recommender is already being reinitialized or wasn't initialized before.");
                //return false; // Or handle concurrency differently
            }
        }

        LOG.info("Attempting to reinitialize recommender...");
        // Reset state if necessary
        wordVectors.clear();
        recipeDataMap.clear();
        recipeVectors.clear();

        try {
            // Call the main initialization logic again
            initialize();
            return true;
        } catch (Exception e) {
            LOG.error("Failed to reinitialize recommender: {}", e.getMessage(), e);
            isInitialized.set(false); // Ensure it's marked as not initialized on failure
            return false;
        }
    }



    /**
     * Load recipe data from database
     */
    private void loadRecipeData() throws SQLException {
        LOG.info("Loading recipe data from database...");

        String sql = "SELECT id, name, ingredients FROM ( SELECT id, name, ingredients, ROW_NUMBER() OVER(PARTITION BY name ORDER BY id ASC) as rn FROM recipes) AS ranked_recipes WHERE rn = 1";

        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            Set<String> uniqueNames = new HashSet<>();
            int total = 0;
            int unique = 0;

            while (rs.next()) {
                total++;
                int id = rs.getInt("id");
                String name = rs.getString("name");

                // Handle array type for ingredients
                String ingredients = "";
                Object ingredientsObj = rs.getObject("ingredients");
                if (ingredientsObj != null) {
                    if (ingredientsObj instanceof Array) {
                        String[] ingredientsArray = (String[]) ((Array) ingredientsObj).getArray();
                        ingredients = String.join(" ", ingredientsArray);
                    } else if (ingredientsObj instanceof String) {
                        ingredients = (String) ingredientsObj;
                    }
                }

                // Deduplicate by name
                if (!uniqueNames.contains(name)) {
                    uniqueNames.add(name);
                    recipeDataMap.put(id, new RecipeData(id, name, ingredients));
                    unique++;
                }
            }

            LOG.info("Loaded {} recipes, {} unique by name", total, unique);
        }
    }

    /**
     * Build word vectors - in a real system you'd load pre-trained embeddings
     * This is a simplified approach for demonstration
     */
    private void buildWordVectors() {
        LOG.info("Building word vectors...");

        // Collect all unique words from recipes
        Set<String> vocabulary = new HashSet<>();

        for (RecipeData recipe : recipeDataMap.values()) {
            String text = (recipe.name + " " + recipe.ingredients).toLowerCase();
            text = NON_ALPHA.matcher(text).replaceAll(" ");

            for (String word : WORD_TOKENIZER.split(text)) {
                // Filter out common stopwords and short words
                if (word.length() > 2 && !isStopWord(word)) {
                    vocabulary.add(word);
                }
            }
        }

        LOG.info("Vocabulary size: {}", vocabulary.size());

        // Create random vectors for each word
        // In production, you'd use pre-trained vectors from Word2Vec, GloVe, etc.
        Random random = new Random(42); // Fixed seed for reproducibility

        for (String word : vocabulary) {
            float[] vector = new float[VECTOR_SIZE];
            for (int i = 0; i < VECTOR_SIZE; i++) {
                vector[i] = (random.nextFloat() * 2) - 1; // Random values between -1 and 1
            }
            // Normalize the vector
            normalizeVector(vector);
            wordVectors.put(word, vector);
        }

        LOG.info("Built {} word vectors", wordVectors.size());
    }

    /**
     * Generate recipe vectors by averaging word vectors
     */
    private void generateRecipeVectors() {
        LOG.info("Starting recipe vector generation...");
        recipeDataMap.values().parallelStream().forEach(data -> {
            // Assuming data.getName() and data.getIngredients() provide the text for vectorization
            String textToVectorize = (data.getName() + " " + data.getIngredients()).toLowerCase();
            textToVectorize = NON_ALPHA.matcher(textToVectorize).replaceAll("").trim(); // Ensure NON_ALPHA and WORD_TOKENIZER are accessible
            String[] words = WORD_TOKENIZER.split(textToVectorize);

            List<float[]> termVectors = new ArrayList<>();
            for (String word : words) {
                if (word.isEmpty() || isStopWord(word)) { // Added check for empty word
                    continue;
                }
                float[] vec = wordVectors.get(word);
                if (vec != null) {
                    termVectors.add(vec);
                }
            }

            if (termVectors.isEmpty()) {
                // LOG.warn("No valid word vectors found for recipe ID: {}. Skipping vector generation for this recipe.", data.getId());
                // Optionally, store a zero vector or handle as appropriate
                // recipeVectors.put(data.getId(), new float[VECTOR_SIZE]);
                return;
            }

            float[] recipeVec = new float[VECTOR_SIZE];
            for (float[] termVector : termVectors) {
                for (int i = 0; i < VECTOR_SIZE; i++) {
                    recipeVec[i] += termVector[i];
                }
            }

            for (int i = 0; i < VECTOR_SIZE; i++) {
                recipeVec[i] /= termVectors.size();
            }

            normalizeVector(recipeVec); // Assuming normalizeVector is thread-safe or operates on local data
            recipeVectors.put(data.getId(), recipeVec); // recipeVectors is ConcurrentHashMap, so put is thread-safe
        });
        LOG.info("Finished recipe vector generation. Total vectors: {}", recipeVectors.size());
    }

    /**
     * Find k similar recipes to the given query
     * Returns List<Recipe> for direct integration with the service layer
     */
    /**
     * Creates and normalizes a vector from query name and ingredients.
     *
     * @param queryName        The name of the query recipe/food.
     * @param queryIngredients The ingredients of the query.
     * @return A normalized float vector for the query, or null if a vector cannot be generated.
     */
    private float[] createAndNormalizeQueryVector(String queryName, String queryIngredients) {
        String queryText = (queryName + " " + queryIngredients).toLowerCase();
        queryText = NON_ALPHA.matcher(queryText).replaceAll("").trim();
        String[] queryWords = WORD_TOKENIZER.split(queryText);

        List<float[]> queryWordVecs = new ArrayList<>();
        for (String word : queryWords) {
            if (word.isEmpty() || isStopWord(word)) {
                continue;
            }
            float[] vec = wordVectors.get(word);
            if (vec != null) {
                queryWordVecs.add(vec);
            }
        }

        if (queryWordVecs.isEmpty()) {
            LOG.warn("Could not generate a vector for the query (no valid words found): name='{}', ingredients='{}'", queryName, queryIngredients);
            return null;
        }

        float[] queryVector = new float[VECTOR_SIZE];
        for (float[] vec : queryWordVecs) {
            for (int i = 0; i < VECTOR_SIZE; i++) {
                queryVector[i] += vec[i];
            }
        }
        for (int i = 0; i < VECTOR_SIZE; i++) {
            queryVector[i] /= queryWordVecs.size();
        }
        normalizeVector(queryVector);
        return queryVector;
    }

    /**
     * Find k similar recipes to the given query.
     * This version uses parallel streams for calculating similarities.
     * Returns List<Recipe> for direct integration with the service layer.
     */
    public List<Recipe> findKSimilar(String queryName, String queryIngredients, int k) {
        if (!isInitialized.get()) {
            LOG.warn("Recommender not initialized. Returning empty list for query: name='{}', ingredients='{}'", queryName, queryIngredients);
            return Collections.emptyList();
        }

        float[] queryVector = createAndNormalizeQueryVector(queryName, queryIngredients);
        if (queryVector == null) {
            // createAndNormalizeQueryVector already logs the warning
            return Collections.emptyList();
        }

        if (recipeVectors.isEmpty()) {
            LOG.warn("No recipe vectors available to compare against. Returning empty list.");
            return Collections.emptyList();
        }

        List<RecipeSimilarity> similarities = recipeVectors.entrySet().parallelStream()
                .map(entry -> {
                    int recipeId = entry.getKey();
                    float[] vec = entry.getValue();
                    double similarity = cosineSimilarity(queryVector, vec); // Assuming cosineSimilarity is thread-safe

                    RecipeData data = recipeDataMap.get(recipeId); // recipeDataMap is ConcurrentHashMap
                    String recipeName = (data != null) ? data.getName() : "Unknown Recipe ID: " + recipeId;
                    return new RecipeSimilarity(recipeId, recipeName, similarity);
                })
                .sorted(Comparator.comparingDouble(RecipeSimilarity::getSimilarity).reversed())
                .limit(k)
                .toList();

        if (similarities.isEmpty()) {
            return Collections.emptyList();
        }

        // Convert RecipeSimilarity objects to Recipe objects, by fetching from RecipeRepository
        return similarities.stream()
                .map(rs -> {
                    Recipe recipe = recipeRepository.findById((long) rs.getId()); // Assuming this returns Recipe or null
                    if (recipe == null) {
                        LOG.warn("Recipe with ID {} (name: '{}') found in similarity search but not in repository. Skipping.", rs.getId(), rs.getName());
                        return null; // This will be filtered out by the subsequent filter
                    }
                    return recipe;
                })
                .filter(Objects::nonNull) // This will remove any null recipes that were not found
                .collect(Collectors.toList());
    }
  // Helper class to store similarity scores
    private static class RecipeSimilarity {
        private final int id;
        private final String name;
        private final double similarity;

        public RecipeSimilarity(int id, String name, double similarity) {
            this.id = id;
            this.name = name;
            this.similarity = similarity;
        }

        public int getId() {
            return id;
        }

        public String getName() {
            return name;
        }

        public double getSimilarity() {
            return similarity;
        }
    }

    /**
     * Calculate cosine similarity between two vectors
     */
    private double cosineSimilarity(float[] v1, float[] v2) {
        double dotProduct = 0.0;

        for (int i = 0; i < v1.length; i++) {
            dotProduct += v1[i] * v2[i];
        }

        // Since we normalize vectors, this is just the dot product
        return dotProduct;
    }

    /**
     * Normalize a vector in-place
     */
    private void normalizeVector(float[] vector) {
        float norm = 0.0f;

        for (float v : vector) {
            norm += v * v;
        }

        norm = (float) Math.sqrt(norm);

        if (norm > 0) {
            for (int i = 0; i < vector.length; i++) {
                vector[i] /= norm;
            }
        }
    }

    /**
     * Check if a word is a stop word
     */
    private boolean isStopWord(String word) {
        // Common English stop words plus recipe-specific words
        Set<String> stopWords = Set.of(
                "a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "by", "in",
                "of", "cup", "cups", "oz", "ounce", "ounces", "lb", "lbs", "pound", "pounds",
                "tsp", "tbsp", "teaspoon", "teaspoons", "tablespoon", "tablespoons", "pinch",
                "dash", "taste", "chopped", "sliced", "minced", "diced", "optional", "garnish",
                "with", "into", "as", "if", "add", "mix", "stir", "combine", "bake", "cook",
                "fry", "saute", "heat", "preheat", "degrees", "fahrenheit", "celsius", "minute",
                "minutes", "hour", "hours", "about", "approximately", "well", "until", "large",
                "medium", "small", "finely", "roughly", "fresh", "dried", "ground", "can", "cans",
                "package", "packages", "room", "temperature", "over", "under", "make", "serve",
                "set", "aside", "cover", "reduce", "bring", "boil", "simmer", "drain", "rinse",
                "remove", "cut", "place", "beat", "whisk", "blend", "pour", "spread", "top",
                "layer", "prepare", "use", "needed", "according", "instructions", "water", "oil",
                "salt", "pepper"
        );

        return stopWords.contains(word);
    }
}