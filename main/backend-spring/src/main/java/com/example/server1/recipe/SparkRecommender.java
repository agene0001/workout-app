package com.example.server1.recipe;

import org.apache.spark.ml.feature.StopWordsRemover;
import org.apache.spark.ml.feature.Word2Vec;
import org.apache.spark.ml.feature.Word2VecModel;
import org.apache.spark.ml.linalg.Vector;
import org.apache.spark.ml.feature.Normalizer;
import org.apache.spark.sql.*;
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.api.java.UDF2;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import static org.apache.spark.sql.functions.*;
import java.io.Serializable;

@Component
public class SparkRecommender implements Serializable {

    private final SparkSession sparkSession;
    private transient Word2VecModel word2VecModel;
    private transient Dataset<Row> featuredData;

    @Autowired
    public SparkRecommender(SparkSession sparkSession) {
        this.sparkSession = sparkSession;
    }

    // Preprocessing: normalize text and tokenize
    public Dataset<Row> preprocess(Dataset<Row> dataset) {
        // 1. Clean text (consider removing numbers too with "[^a-z\\s]")
        Dataset<Row> cleanedData = dataset.withColumn("processed_text",
                lower(regexp_replace(concat_ws(" ", col("name"), col("ingredients")), "[^a-z\\s]", " ")) // Example: Removed numbers
        );

        // 2. Split into words (split on one or more whitespace characters)
        Dataset<Row> tokenizedData = cleanedData.withColumn("words", split(col("processed_text"), "\\s+"));

        // 3. Remove stop words
        StopWordsRemover remover = new StopWordsRemover()
                .setInputCol("words")         // Input is the 'words' column from step 2
                .setOutputCol("filtered_words"); // Output will be a new column

        // Apply the remover to the tokenized data
//        Dataset<Row> filteredData = remover.transform(tokenizedData);

        // You can customize the stop words (optional but recommended for recipes)
        String[] myStopWords = StopWordsRemover.loadDefaultStopWords("english"); // Start with default

        String[] recipeStopWords = {"a", "an", "the", "cup", "cups", "oz", "ounce", "ounces", "lb", "lbs", "pound", "pounds", "tsp", "tbsp", "teaspoon", "teaspoons", "tablespoon", "tablespoons", "pinch", "dash", "to", "taste", "chopped", "sliced", "minced", "diced", "optional", "garnish", "for", "and", "or", "with", "into", "in", "on", "at", "as", "if", "of", "add", "mix", "stir", "combine", "bake", "cook", "fry", "saute", "heat", "preheat", "degrees", "fahrenheit", "celsius", "minute", "minutes", "hour", "hours", "about", "approximately", "well", "until", "large", "medium", "small", "finely", "roughly", "fresh", "dried", "ground", "can", "cans", "package", "packages", "room", "temperature", "over", "under", "make", "serve", "set", "aside", "cover", "reduce", "bring", "boil", "simmer", "drain", "rinse", "remove", "cut", "place", "beat", "whisk", "blend", "pour", "spread", "top", "layer", "prepare", "use", "needed", "according", "instructions", "water", "oil", "salt", "pepper"}; // Add many more!
        java.util.Set<String> stopWordsSet = new java.util.HashSet<>(java.util.Arrays.asList(myStopWords));
        stopWordsSet.addAll(java.util.Arrays.asList(recipeStopWords));
        remover.setStopWords(stopWordsSet.toArray(new String[0]));
        // Re-apply if customizing

        return remover.transform(tokenizedData); // Return the dataset including the new 'filtered_words' column
    }

    public void setup(String dbUrl, String dbUser, String dbPassword) {
        try {
            Dataset<Row> recipesData = sparkSession.read()
                    .format("jdbc")
                    .option("url", dbUrl)
                    .option("dbtable", "recipes")
                    .option("user", dbUser)
                    .option("password", dbPassword)
                    .option("driver", "com.mysql.cj.jdbc.Driver")
                    .load();

            // Preprocess the data
            Dataset<Row> processedData = preprocess(recipesData);
            System.out.println("Processed Data Sample:");
            // Train Word2Vec model and transform data
            this.word2VecModel = buildWord2VecModel(processedData);
            Dataset<Row> transformedData = word2VecModel.transform(processedData);

            // Normalize the features vectors
            Normalizer normalizer = new Normalizer()
                    .setInputCol("features")
                    .setOutputCol("normFeatures") // Output to a new column
                    .setP(2.0);
            this.featuredData = normalizer.transform(transformedData)
                    .select("name", "ingredients", "normFeatures");

        } catch (Exception e) {
            System.err.println("Error connecting to the database: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private Word2VecModel buildWord2VecModel(Dataset<Row> dataset) {
        Word2Vec word2Vec = new Word2Vec()
                .setInputCol("filtered_words")
                .setOutputCol("features")
                .setVectorSize(100)  // Reduce dimensionality for efficiency
                .setMinCount(2)  // Ignore words with frequency < 2
                .setNumPartitions(16); // Example: Set based on your cluster cores
        return word2Vec.fit(dataset);
    }

    public Dataset<Row> findKSimilar(String query, int k) {
        if (sparkSession == null) {
            throw new IllegalStateException("SparkSession is not initialized");
        }

        if (word2VecModel == null) {
            throw new IllegalStateException("Word2Vec model is null. Ensure setup() was called successfully.");
        }

        if (featuredData == null) {
            throw new IllegalStateException("Featured data is null. Ensure setup() was called successfully.");
        }
        Dataset<Row> queryDataset = sparkSession.createDataFrame(
                java.util.Collections.singletonList(RowFactory.create(query, query)),
                new StructType()
                        .add("name", "string")
                        .add("ingredients", "string")
        );

        // Transform query with Word2Vec
        Dataset<Row> processedQuery = preprocess(queryDataset);
        Dataset<Row> queryFeaturesRaw = word2VecModel.transform(processedQuery);
        Normalizer queryNormalizer = new Normalizer()
                .setInputCol("features")
                .setOutputCol("normFeatures")
                .setP(2.0);

        Dataset<Row> queryFeatures = queryNormalizer.transform(queryFeaturesRaw);
        // Extract query vector
        Row featuresRow = queryFeatures.select("normFeatures").first();
        Vector queryVector = featuresRow.getAs(0);

        // Make the vector final to help indicate it's captured by the lambda
        final Vector capturedQueryVector = queryVector;

        // --- Define and Register the UDF (now UDF1) ---
        sparkSession.udf().register(
                "dot_product_udf", // Same UDF name is fine
                // UDF1 takes the Vector from the column (`colVector`)
                (UDF1<Vector, Double>) (colVector) -> colVector.dot(capturedQueryVector), // Use the captured vector here
                DataTypes.DoubleType // Specify the return type
        );
        // -------------------------------------------

        // --- Calculate similarity using the UDF ---
        Dataset<Row> results = featuredData.withColumn(
                        "similarity",
                        // Call the UDF with only the 'features' column
                        callUDF("dot_product_udf", col("normFeatures"))
                )
                .select("name", "ingredients", "similarity")
                .orderBy(col("similarity").desc())
                .limit(k);
        // ----------------------------------------

        return results;
    }


    // Helper function to convert vector to a Spark SQL-compatible array
    private String arrayToString(double[] array) {
        StringBuilder sb = new StringBuilder();
        for (double num : array) {
            sb.append(num).append(",");
        }
        return sb.substring(0, sb.length() - 1); // Remove last comma
    }
}
