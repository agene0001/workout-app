package com.example.server1.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**") // Adjust path pattern as needed
                .allowedOrigins("http://localhost:8080") // Allow requests from the frontend's origin
                .allowedMethods("GET", "POST", "PUT", "DELETE") // Allow specific HTTP methods
                .allowedHeaders("*"); // Allow all headers
    }
}
