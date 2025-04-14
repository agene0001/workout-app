package com.example.server1.recipe;

import org.apache.spark.ml.feature.*;
import org.apache.spark.ml.linalg.Vector;
import org.apache.spark.ml.linalg.Vectors; // Import for Vectors utility if needed later
import org.apache.spark.ml.Pipeline; // Optional: Could structure preprocessing as a Pipeline
import org.apache.spark.ml.PipelineModel; // Optional
import org.apache.spark.sql.*;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import static org.apache.spark.sql.functions.*;
import java.io.Serializable;
import java.util.*;

@Component
public class SparkRecommender implements Serializable {

    private final SparkSession sparkSession;
    // Make models transient if running in certain distributed environments
    // where the driver might serialize the component but workers don't need the full model object
    // However, for typical Spring Boot + local/cluster Spark, they might not need to be transient
    // if setup() is called appropriately after construction. Let's keep them non-transient for now.
    private Word2VecModel word2VecModel;
    private BucketedRandomProjectionLSHModel lshModel;
    private Dataset<Row> recipeDataWithFeatures; // Store data with features for LSH lookup

    // Define constants for column names
    private static final String INPUT_COL_TEXT = "text_to_process"; // Combined text
    private static final String WORDS_COL = "words";
    private static final String FILTERED_WORDS_COL = "filtered_words";
    private static final String RAW_FEATURES_COL = "rawFeatures"; // Word2Vec output
    private static final String NORMALIZED_FEATURES_COL = "normFeatures"; // LSH input
    private static final String LSH_HASHES_COL = "hashes"; // LSH output (internal)
    private static final String DISTANCE_COL = "distance"; // LSH approxNearestNeighbors output


    @Autowired
    public SparkRecommender(SparkSession sparkSession) {
        this.sparkSession = sparkSession;
    }

    // Preprocessing: normalize text and tokenize
    // Returns DataFrame with a "filtered_words" column
    private Dataset<Row> preprocessText(Dataset<Row> dataset) {
        // 1. Combine relevant text columns and clean
        Dataset<Row> combinedTextData = dataset.withColumn(INPUT_COL_TEXT,
                lower(regexp_replace(concat_ws(" ", col("name"), col("ingredients")), "[^a-z\\s]", " "))
        );

        // 2. Tokenize
        RegexTokenizer tokenizer = new RegexTokenizer()
                .setInputCol(INPUT_COL_TEXT)
                .setOutputCol(WORDS_COL)
                .setPattern("\\s+"); // Split on one or more whitespace characters
        Dataset<Row> tokenizedData = tokenizer.transform(combinedTextData);

        // 3. Remove stop words
        String[] defaultStopWords = StopWordsRemover.loadDefaultStopWords("english");
        String[] recipeStopWords = {"a", "an", "the", "cup", "cups", "oz", "ounce", "ounces", "lb", "lbs", "pound", "pounds", "tsp", "tbsp", "teaspoon", "teaspoons", "tablespoon", "tablespoons", "pinch", "dash", "to", "taste", "chopped", "sliced", "minced", "diced", "optional", "garnish", "for", "and", "or", "with", "into", "in", "on", "at", "as", "if", "of", "add", "mix", "stir", "combine", "bake", "cook", "fry", "saute", "heat", "preheat", "degrees", "fahrenheit", "celsius", "minute", "minutes", "hour", "hours", "about", "approximately", "well", "until", "large", "medium", "small", "finely", "roughly", "fresh", "dried", "ground", "can", "cans", "package", "packages", "room", "temperature", "over", "under", "make", "serve", "set", "aside", "cover", "reduce", "bring", "boil", "simmer", "drain", "rinse", "remove", "cut", "place", "beat", "whisk", "blend", "pour", "spread", "top", "layer", "prepare", "use", "needed", "according", "instructions", "water", "oil", "salt", "pepper"}; // Add many more!
        Set<String> stopWordsSet = new HashSet<>(Arrays.asList(defaultStopWords));
        stopWordsSet.addAll(Arrays.asList(recipeStopWords));

        StopWordsRemover remover = new StopWordsRemover()
                .setInputCol(WORDS_COL)
                .setOutputCol(FILTERED_WORDS_COL)
                .setStopWords(stopWordsSet.toArray(new String[0]));

        return remover.transform(tokenizedData);
    }

    public void setup(String dbUrl, String dbUser, String dbPassword) {
        try {
            System.out.println("SparkRecommender setup started...");
            Dataset<Row> recipesData = sparkSession.read()
                    .format("jdbc")
                    .option("url", dbUrl)
                    .option("dbtable", "recipes") // Ensure this table name is correct
                    .option("user", dbUser)
                    .option("password", dbPassword)
                    .option("driver", "com.mysql.cj.jdbc.Driver") // Ensure correct driver
                    .load();

            System.out.println("Loaded " + recipesData.count() + " recipes from database.");
            recipesData.printSchema();
            recipesData.show(5, false);

            // --- Preprocessing and Feature Engineering ---
            System.out.println("Preprocessing text...");
            Dataset<Row> processedData = preprocessText(recipesData);
            processedData.select(FILTERED_WORDS_COL).show(5, false);

            System.out.println("Training Word2Vec model...");
            Word2Vec word2Vec = new Word2Vec()
                    .setInputCol(FILTERED_WORDS_COL)
                    .setOutputCol(RAW_FEATURES_COL) // Output raw features first
                    .setVectorSize(100)
                    .setMinCount(2)
                    .setNumPartitions(8) // Adjust based on data/cluster size
                    .setWindowSize(5);   // Added window size hyperparameter

            this.word2VecModel = word2Vec.fit(processedData);
            Dataset<Row> featuredData = word2VecModel.transform(processedData);
            featuredData.select(RAW_FEATURES_COL).show(5, false);


            System.out.println("Normalizing feature vectors...");
            Normalizer normalizer = new Normalizer()
                    .setInputCol(RAW_FEATURES_COL)
                    .setOutputCol(NORMALIZED_FEATURES_COL)
                    .setP(2.0); // L2 normalization for cosine similarity

            Dataset<Row> normalizedData = normalizer.transform(featuredData);
            normalizedData.select(NORMALIZED_FEATURES_COL).show(5, false);


            // Keep only necessary columns for LSH fitting and final lookup
            this.recipeDataWithFeatures = normalizedData
                    .select("id", "name", "ingredients", NORMALIZED_FEATURES_COL) // Keep id if available and useful
                    .filter(col(NORMALIZED_FEATURES_COL).isNotNull()) // Ensure vectors exist
                    .cache(); // Cache for faster LSH fitting and querying

            System.out.println("Recipe data with features count: " + this.recipeDataWithFeatures.count());
            this.recipeDataWithFeatures.printSchema();

            // --- LSH Model Training ---
            System.out.println("Training LSH model...");
            BucketedRandomProjectionLSH brp = new BucketedRandomProjectionLSH()
                    .setInputCol(NORMALIZED_FEATURES_COL)
                    .setOutputCol(LSH_HASHES_COL) // Internal column for hash values
                    .setBucketLength(2.0) // Adjust this hyperparameter - controls bucket width
                    .setNumHashTables(3);  // Adjust this - more tables increase accuracy but cost more

            this.lshModel = brp.fit(this.recipeDataWithFeatures);

            // Optional: Transform data with LSH model if you want to see the hashes (not usually needed)
            // this.lshModel.transform(this.recipeDataWithFeatures).show(5, false);

            System.out.println("SparkRecommender setup finished successfully.");

        } catch (Exception e) {
            System.err.println("Error during SparkRecommender setup: " + e.getMessage());
            e.printStackTrace();
            // Consider re-throwing or handling more gracefully depending on application needs
            throw new RuntimeException("Failed to initialize SparkRecommender", e);
        }
    }

    // No longer needed Word2VecModel builder as it's done in setup()
    // private Word2VecModel buildWord2VecModel(Dataset<Row> dataset) { ... }

    public Dataset<Row> findKSimilar(String queryName, String queryIngredients, int k) {
        if (sparkSession == null) {
            throw new IllegalStateException("SparkSession is not initialized.");
        }
        if (word2VecModel == null) {
            throw new IllegalStateException("Word2Vec model is null. Ensure setup() was called successfully.");
        }
        if (lshModel == null) {
            throw new IllegalStateException("LSH model is null. Ensure setup() was called successfully.");
        }
        if (recipeDataWithFeatures == null) {
            throw new IllegalStateException("Recipe feature data is null. Ensure setup() was called successfully.");
        }
        if (queryName == null || queryIngredients == null) {
            throw new IllegalArgumentException("Query name and ingredients cannot be null.");
        }

        System.out.println("Finding similar recipes for query: name='" + queryName + "', ingredients='...'");

        // 1. Create DataFrame for the query
        // Use same schema structure as initial loading for consistency in preprocessing
        List<Row> queryList = Arrays.asList(RowFactory.create(queryName, queryIngredients));
        StructType querySchema = new StructType()
                .add("name", DataTypes.StringType)
                .add("ingredients", DataTypes.StringType);
        Dataset<Row> queryDataset = sparkSession.createDataFrame(queryList, querySchema);


        // 2. Preprocess the query text (same steps as training data)
        System.out.println("Preprocessing query...");
        Dataset<Row> processedQuery = preprocessText(queryDataset);
        // processedQuery.show(false); // Debug

        // 3. Transform query with Word2Vec model
        System.out.println("Applying Word2Vec to query...");
        Dataset<Row> queryFeatured = word2VecModel.transform(processedQuery);
        // queryFeatured.show(false); // Debug

        // 4. Normalize the query feature vector
        System.out.println("Normalizing query vector...");
        Normalizer normalizer = new Normalizer()
                .setInputCol(RAW_FEATURES_COL)
                .setOutputCol(NORMALIZED_FEATURES_COL)
                .setP(2.0);
        Dataset<Row> queryNormalized = normalizer.transform(queryFeatured);
        // queryNormalized.show(false); // Debug

        // 5. Extract the query vector
        Vector queryVector =null;
        try {
            Row queryRow = queryNormalized.select(NORMALIZED_FEATURES_COL).first();
            if (queryRow != null && !queryRow.isNullAt(0)) {
                queryVector = queryRow.getAs(0);
                System.out.println("Query vector generated.");
                // System.out.println("Query Vector (first 10 dims): " + Arrays.toString(Arrays.copyOf(queryVector.toArray(), 10))); // Debug
            }
        } catch (Exception e) {
            System.err.println("Error extracting query vector: " + e.getMessage());
            // This can happen if the query contains only unknown words or stop words
        }

        if (queryVector == null) {
            System.err.println("Could not generate a feature vector for the query (perhaps only unknown/stop words?). Returning empty results.");
            StructType emptySchema = new StructType()
                    .add("name", DataTypes.StringType)
                    .add("ingredients", DataTypes.StringType)
                    .add(DISTANCE_COL, DataTypes.DoubleType); // Match LSH output schema

            // Create an empty list of Row objects
            List<Row> emptyData = Collections.emptyList(); // Or: new java.util.ArrayList<>();
            return sparkSession.createDataFrame(emptyData, emptySchema);

        }


        // 6. Use LSH model to find approximate nearest neighbors
        System.out.println("Performing approximate nearest neighbor search using LSH...");
        // The k+1 is often recommended as the query itself might be considered a neighbor if it exists
        // Or adjust k based on whether you expect the exact query to be in the dataset
        Dataset<Row> similarItems = (Dataset<Row>) lshModel.approxNearestNeighbors(
                this.recipeDataWithFeatures, // The dataset containing features of all recipes
                queryVector,                 // The query vector
                k + 1                       // Number of neighbors to find
        );

        System.out.println("LSH search complete. Found potential neighbors.");
        similarItems.printSchema();
        similarItems.show(k+1, false); // Debug: Show results before filtering/renaming

        // 7. Process results
        // The output DataFrame 'similarItems' contains columns from recipeDataWithFeatures
        // plus a 'distCol' column representing the approximate Euclidean distance.
        // We sort by distance ascending (smaller distance is more similar).
        // We might want to filter out the query itself if it was perfectly matched.
        // Let's assume the query is *not* an exact recipe name/ingredient list from the DB for now.

        // 7. Process results
        Dataset<Row> finalResults = similarItems
                // Use col() for all arguments to select
                .select(col("name"), col("ingredients"), col("distCol").alias(DISTANCE_COL))
                .orderBy(asc(DISTANCE_COL)) // Sort by ascending distance
                .limit(k);                  // Limit to top k results

        System.out.println("Final top " + k + " similar recipes:");
        finalResults.show(k, false);

        return finalResults;
    }

    // No longer needed
    // private String arrayToString(double[] array) { ... }
}