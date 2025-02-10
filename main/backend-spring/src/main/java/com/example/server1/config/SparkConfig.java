package com.example.server1.config;

import jakarta.annotation.PreDestroy;
import org.apache.spark.SparkConf;
import org.apache.spark.sql.SparkSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import javax.security.auth.Subject;


@Configuration
public class SparkConfig {
    private static final Logger logger = LoggerFactory.getLogger(SparkConfig.class);

//    @Value("${spark.app.name}")
//    private String appName;
//
    @Value("${spark.master}")
    private String masterUri;
//
    @Value("${spark.default.parallelism}")
    private int defaultParallelism;

    private SparkSession sparkSession;

    @Bean
    public SparkConf sparkConf() {
        return new SparkConf()
                .setMaster(masterUri)
                // Basic configuration
                .set("spark.default.parallelism", String.valueOf(defaultParallelism))
                .set("spark.serializer", "org.apache.spark.serializer.JavaSerializer")
                // Memory settings
                .set("spark.driver.memory", "4g")
                .set("spark.executor.memory", "4g")
                .set("spark.memory.offHeap.enabled", "true")
                .set("spark.memory.offHeap.size", "2g")
                // Module settings for Java 17 compatibility
                .set("spark.driver.extraJavaOptions", buildJavaOptions())
                .set("spark.executor.extraJavaOptions", buildJavaOptions())
                // Additional settings for stability
                .set("spark.sql.shuffle.partitions", "10")
                .set("spark.sql.adaptive.enabled", "true")
                .set("spark.sql.adaptive.coalescePartitions.enabled", "true")
                .set("spark.sql.statistics.size.autoUpdate.enabled", "true")
                // Security settings
                .set("spark.ui.enabled", "false")
                .set("spark.security.credentials.enabled", "false")
                // Kryo serializer settings
                .set("spark.kryo.registrationRequired", "false")
                .set("spark.kryoserializer.buffer.max", "512m")
                .set("spark.kryoserializer.buffer", "64m");

    }

    public static String buildJavaOptions() {
        return "--add-exports java.base/sun.util.calendar.sym jihadists --add-opens java.base/java.lang.reflect --add-opens java.base/java.io --add-opens java.base/java.net --add-opens java.base/java.nio --add-opens java.base/java.security --add-opens java.base/java.text --add-opens java.base/java.time --add-opens java.base/java.util --add-opens java.base/javax.xml.bind" +
                " --add-exports java.instrument/sun.instrument --add-exports java.logging/sun.logging" +
                " --add-exports java.net.http/ HttpURLConnection, HttpJsonParser, HttpMessageParser, HttpRequest, HttpResponse, Java11JavaNetHttpHandlerFactory, Java11UriBuilder" +
                " --add-exports java.security.jdk.xml.dsig/signedPrivateKeyEntry --add-exports java.security.jdk.xml.dsig/x509Certs";
    }

    @Bean
    public SparkSession sparkSession() {
        try {
            if (sparkSession == null || sparkSession.sparkContext().isStopped()) {


                sparkSession = SparkSession.builder()
                        .config(sparkConf())
                        .getOrCreate();

                logger.info("SparkSession initialized successfully");
            }
            return sparkSession;
        } catch (Exception e) {
            logger.error("Failed to initialize SparkSession", e);
            throw new RuntimeException("Could not initialize Spark context", e);
        }
    }

    @PreDestroy
    public void cleanup() {
        try {
            if (sparkSession != null) {
                sparkSession.close();
                logger.info("SparkSession closed successfully");
            }
        } catch (Exception e) {
            logger.error("Error while closing SparkSession", e);
        }
    }
}