package org.backend.service;

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

import org.backend.model.Recipe;
import org.backend.repository.RecipeRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * A lightweight recipe recommendation service that replaces Spark-based implementation
 * with a pure Java solution using word embeddings and approximate nearest neighbor search.
 */
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
    public void setup(String dbUrl, String dbUser, String dbPassword) {
        try {
            LOG.info("JavalinRecipeRecommender setup started...");

            // Load recipe data
            loadRecipeData();

            // Build word vectors (a simplified version - in production you'd use a pre-trained model)
            buildWordVectors();

            // Generate recipe vectors from word vectors
            generateRecipeVectors();

            // Set initialization flag
            isInitialized.set(true);

            LOG.info("JavalinRecipeRecommender setup completed successfully with {} recipes", recipeDataMap.size());
        } catch (Exception e) {
            LOG.error("Error during JavalinRecipeRecommender setup: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to initialize JavalinRecipeRecommender", e);
        }
    }

    /**
     * Check if the recommender is initialized
     */
    public boolean isInitialized() {
        return isInitialized.get();
    }

    /**
     * Reinitialize the recommender
     */
    public boolean reinitializeRecommender() {
        try {
            setup(null, null, null); // DataSource is injected, so we don't need connection parameters
            return true;
        } catch (Exception e) {
            LOG.error("Failed to reinitialize recommender: {}", e.getMessage(), e);
            return false;
        }
    }

    /**
     * Load recipe data from database
     */
    private void loadRecipeData() throws SQLException {
        LOG.info("Loading recipe data from database...");

        String sql = "SELECT id, name, ingredients FROM recipes";

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
        LOG.info("Generating recipe vectors...");

        for (Map.Entry<Integer, RecipeData> entry : recipeDataMap.entrySet()) {
            int id = entry.getKey();
            RecipeData recipe = entry.getValue();

            // Combine name and ingredients
            String combinedText = (recipe.name + " " + recipe.ingredients).toLowerCase();
            combinedText = NON_ALPHA.matcher(combinedText).replaceAll(" ");

            // Split into words
            List<String> words = Arrays.asList(WORD_TOKENIZER.split(combinedText));
            words = words.stream()
                    .filter(word -> word.length() > 2)
                    .filter(word -> !isStopWord(word))
                    .collect(Collectors.toList());

            // Average word vectors
            float[] recipeVector = new float[VECTOR_SIZE];

            if (!words.isEmpty()) {
                for (String word : words) {
                    float[] wordVector = wordVectors.get(word);
                    if (wordVector != null) {
                        for (int i = 0; i < VECTOR_SIZE; i++) {
                            recipeVector[i] += wordVector[i];
                        }
                    }
                }

                // Normalize the resulting vector
                normalizeVector(recipeVector);
                recipeVectors.put(id, recipeVector);
            }
        }

        LOG.info("Generated {} recipe vectors", recipeVectors.size());
    }

    /**
     * Find k similar recipes to the given query
     * Returns List<Recipe> for direct integration with the service layer
     */
    public List<Recipe> findKSimilar(String queryName, String queryIngredients, int k) {
        LOG.info("Finding similar recipes for query: {}", queryName);

        // Preprocess query text
        String combinedText = (queryName + " " + queryIngredients).toLowerCase();
        combinedText = NON_ALPHA.matcher(combinedText).replaceAll(" ");

        // Split into words
        List<String> words = Arrays.asList(WORD_TOKENIZER.split(combinedText));
        words = words.stream()
                .filter(word -> word.length() > 2)
                .filter(word -> !isStopWord(word))
                .collect(Collectors.toList());

        // Calculate query vector
        float[] queryVector = new float[VECTOR_SIZE];

        if (words.isEmpty()) {
            LOG.warn("Query contains no valid words for vector generation");
            return Collections.emptyList();
        }

        for (String word : words) {
            float[] wordVector = wordVectors.get(word);
            if (wordVector != null) {
                for (int i = 0; i < VECTOR_SIZE; i++) {
                    queryVector[i] += wordVector[i];
                }
            }
        }

        // Normalize query vector
        normalizeVector(queryVector);

        // Find nearest neighbors
        List<RecipeSimilarity> similarities = new ArrayList<>();

        for (Map.Entry<Integer, float[]> entry : recipeVectors.entrySet()) {
            int id = entry.getKey();
            float[] vector = entry.getValue();

            // Skip if it's the same recipe name
            RecipeData recipe = recipeDataMap.get(id);
            if (recipe.name.equalsIgnoreCase(queryName)) {
                continue;
            }

            // Calculate cosine similarity
            double similarity = cosineSimilarity(queryVector, vector);

            // Store recipe ID and similarity score
            similarities.add(new RecipeSimilarity(id, recipe.name, similarity));
        }

        // Sort by similarity (descending - higher similarity means more similar)
        similarities.sort(Comparator.comparingDouble(RecipeSimilarity::getSimilarity).reversed());

        // Create Recipe objects from top k matches
        List<Recipe> results = new ArrayList<>();
        for (RecipeSimilarity similarity : similarities.stream().limit(k).toList()) {
            Recipe recipe = new Recipe();
            recipe.setId(similarity.getId());
            recipe.setName(similarity.getName());
            results.add(recipe);
        }

        return results;
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