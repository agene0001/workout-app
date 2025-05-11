package org.backend.blog.model;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import jakarta.enterprise.context.ApplicationScoped; // For ObjectMapper injection
import jakarta.inject.Inject;

import java.io.IOException;
import java.util.Collections;
import java.util.Map;

@Converter
@ApplicationScoped // Make it a bean so ObjectMapper can be injected
public class JsonToMapConverter implements AttributeConverter<Map<String, Object>, String> {

    // Quarkus will inject the ObjectMapper configured for your application
    @Inject
    ObjectMapper objectMapper;

    @Override
    public String convertToDatabaseColumn(Map<String, Object> attribute) {
        if (attribute == null) {
            return null; // Or "{}", depending on whether you want null or empty JSON in DB
        }
        try {
            return objectMapper.writeValueAsString(attribute);
        } catch (JsonProcessingException e) {
            // Consider proper logging and exception handling
            throw new IllegalArgumentException("Error converting Map to JSON string", e);
        }
    }

    @Override
    public Map<String, Object> convertToEntityAttribute(String dbData) {
        if (dbData == null || dbData.isEmpty()) {
            return Collections.emptyMap(); // Or null, depending on preference
        }
        try {
            return objectMapper.readValue(dbData, new TypeReference<Map<String, Object>>() {});
        } catch (IOException e) {
            // Consider proper logging and exception handling
            throw new IllegalArgumentException("Error converting JSON string to Map", e);
        }
    }
}