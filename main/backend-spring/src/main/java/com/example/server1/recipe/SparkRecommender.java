package com.example.server1.recipe;

import org.apache.spark.ml.feature.HashingTF;
import org.apache.spark.ml.feature.IDF;
import org.apache.spark.ml.Pipeline;
import org.apache.spark.ml.PipelineModel;
import org.apache.spark.ml.linalg.Vector;
import org.apache.spark.sql.*;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.apache.spark.sql.functions;
import static org.apache.spark.sql.functions.*;
import java.io.Serializable;

@Component
public class SparkRecommender implements Serializable {

    private final SparkSession sparkSession;
    private transient PipelineModel tfidfModel;
    private transient Dataset<Row> featuredData;

    @Autowired
    public SparkRecommender(SparkSession sparkSession) {
        this.sparkSession = sparkSession;
    }

    // Preprocessing: normalize text and tokenize
    public Dataset<Row> preprocess(Dataset<Row> dataset) {
        // First create processed text
        Dataset<Row> withProcessedText = dataset.withColumn("processed_text",
                functions.trim(
                        functions.regexp_replace(
                                functions.lower(functions.concat_ws(" ", functions.col("name"), functions.col("ingredients"))),
                                "[^a-z0-9\\s]", " ")));

        // Then tokenize into words column
        return withProcessedText.withColumn("words",
                functions.split(functions.col("processed_text"), " "));
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

            // Preprocess the data - now includes tokenization
            Dataset<Row> processedData = preprocess(recipesData);

            // Build and apply TF-IDF model
            this.tfidfModel = buildTFIDFModel(processedData);
            this.featuredData = tfidfModel.transform(processedData);

        } catch (Exception e) {
            System.err.println("Error connecting to the database: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private PipelineModel buildTFIDFModel(Dataset<Row> dataset) {
        // HashingTF configuration
        HashingTF hashingTF = new HashingTF()
                .setInputCol("words")  // Now using the words column created in preprocess
                .setOutputCol("raw_features")
                .setNumFeatures(1000);

        // IDF configuration
        IDF idf = new IDF()
                .setInputCol("raw_features")
                .setOutputCol("features")
                .setMinDocFreq(2);

        // Create and fit the pipeline
        Pipeline pipeline = new Pipeline()
                .setStages(new org.apache.spark.ml.PipelineStage[] { hashingTF, idf });

        return pipeline.fit(dataset);
    }

    public Dataset<Row> findKSimilar(String query, int k) {
        if (tfidfModel == null || featuredData == null) {
            throw new IllegalStateException("TF-IDF model not initialized. Call setup() first.");
        }

        // Create a single-row dataset for the query
        Dataset<Row> queryDataset = sparkSession.createDataFrame(
                java.util.Collections.singletonList(
                        RowFactory.create(query, query)
                ),
                new StructType()
                        .add("name", "string")
                        .add("ingredients", "string")
        );

        // Preprocess the query using the same pipeline
        Dataset<Row> processedQuery = preprocess(queryDataset);
        Dataset<Row> queryFeatures = tfidfModel.transform(processedQuery);

        // Register user-defined function for vector operations
        sparkSession.udf().register("enhanced_similarity", (Vector v1, Vector v2) -> {
            double cosineSim = computeCosineSimilarity(v1, v2);
            double jaccardSim = computeJaccardSimilarity(v1, v2);
            return 0.7 * cosineSim + 0.3 * jaccardSim;
        }, DataTypes.DoubleType);

        // Register the DataFrames as temp views
        featuredData.createOrReplaceTempView("recipes");
        queryFeatures.createOrReplaceTempView("query");

        // Use the registered UDF in the SQL query
        Dataset<Row> recipesDF = sparkSession.table("recipes");
        Dataset<Row> queryDF = sparkSession.table("query");



// Use DataFrame API instead of SQL
        return recipesDF
                .crossJoin(queryDF)
                .filter(functions.col("recipes.name").notEqual(functions.col("query.name")))
                .withColumn("similarity",
                        functions.callUDF("enhanced_similarity",
                                functions.col("recipes.features"),
                                functions.col("query.features")))
                .select("recipes.name", "recipes.ingredients", "similarity")
                .orderBy(functions.col("similarity").desc())
                .limit(k);

    }
    private double computeCosineSimilarity(org.apache.spark.ml.linalg.Vector v1,
                                           org.apache.spark.ml.linalg.Vector v2) {
        double dotProduct = org.apache.spark.ml.linalg.BLAS.dot(v1, v2);
        double norm1 = Math.sqrt(org.apache.spark.ml.linalg.BLAS.dot(v1, v1));
        double norm2 = Math.sqrt(org.apache.spark.ml.linalg.BLAS.dot(v2, v2));
        if (norm1 == 0 || norm2 == 0) return 0.0;
        return dotProduct / (norm1 * norm2);
    }

    private double computeJaccardSimilarity(org.apache.spark.ml.linalg.Vector v1,
                                            org.apache.spark.ml.linalg.Vector v2) {
        double intersection = 0.0;
        double union = 0.0;

        for (int i = 0; i < v1.size(); i++) {
            intersection += Math.min(v1.apply(i), v2.apply(i));
            union += Math.max(v1.apply(i), v2.apply(i));
        }

        return union == 0 ? 0.0 : intersection / union;
    }
}