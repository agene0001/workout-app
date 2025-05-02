package org.backend.repository;

import java.util.Optional;

import jakarta.enterprise.context.ApplicationScoped;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import org.backend.model.Category;

@ApplicationScoped
public class CategoryRepository implements PanacheRepository<Category> {
    
    public Optional<Category> findByName(String name) {
        return find("name", name).firstResultOptional();
    }
}