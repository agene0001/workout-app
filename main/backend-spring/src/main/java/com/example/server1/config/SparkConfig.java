package com.example.server1.config;

import jakarta.annotation.PreDestroy;
import org.apache.spark.SparkConf;
import org.apache.spark.sql.SparkSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SparkConfig {
    private static final Logger logger = LoggerFactory.getLogger(SparkConfig.class);

    @Value("${spark.app.name}")
    private String appName;

    @Value("${spark.master}")
    private String masterUri;

    @Value("${spark.default.parallelism:2}")
    private int defaultParallelism;

    private SparkSession sparkSession;

    @Bean
    public SparkConf sparkConf() {
        return new SparkConf()
                .setAppName(appName)
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

    private String buildJavaOptions() {
        return String.join(" ",
                // Existing permissions
                "--add-exports=java.base/sun.nio.ch=ALL-UNNAMED",
                "--add-exports=java.base/sun.security.action=ALL-UNNAMED",
                "--add-exports=java.base/sun.util.calendar=ALL-UNNAMED",
                "--add-exports=java.management/sun.management=ALL-UNNAMED",
                "--add-opens=java.base/java.nio=ALL-UNNAMED",
                "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED",
                "--add-opens=java.base/java.util=ALL-UNNAMED",
                "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED",
                "--add-exports java.base/sun.security.action=ALL-UNNAMED",
                "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED",
                "--add-opens=java.base/java.lang=ALL-UNNAMED",
                "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED",
                "--add-opens=java.base/java.io=ALL-UNNAMED",
                "--add-opens=java.base/java.security=ALL-UNNAMED",
                "--add-opens=java.base/java.lang.module=ALL-UNNAMED",
                "--add-opens=java.base/jdk.internal.loader=ALL-UNNAMED",
                "--add-opens=java.base/jdk.internal.ref=ALL-UNNAMED",
                "--add-opens=java.base/jdk.internal.reflect=ALL-UNNAMED",
                "--add-opens=java.base/jdk.internal.math=ALL-UNNAMED",
                "--add-opens=java.base/jdk.internal.module=ALL-UNNAMED",
                "--add-opens=java.base/jdk.internal.util.jar=ALL-UNNAMED",
                // Additional permissions for serialization
                "--add-opens=java.base/java.lang.constant=ALL-UNNAMED",
                "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED",
                "--add-opens=java.base/java.util.concurrent.locks=ALL-UNNAMED",
                "--add-exports=java.base/sun.reflect.generics.reflectiveObjects=ALL-UNNAMED",
                // New permissions for ByteBuffer serialization
                "--add-opens=java.base/java.nio=ALL-UNNAMED",
                "--add-opens=java.base/java.nio.charset=ALL-UNNAMED",
                "--add-opens=java.base/java.nio.channels=ALL-UNNAMED",
                "--add-opens=java.base/java.nio.file=ALL-UNNAMED",
                "-Dio.netty.tryReflectionSetAccessible=true",
                "-Dlog4j.logLevel=ERROR"
        );
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