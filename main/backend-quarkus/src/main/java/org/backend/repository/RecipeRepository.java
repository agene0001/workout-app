package org.backend.repository;

import java.util.List;

import jakarta.enterprise.context.ApplicationScoped;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import org.backend.model.Recipe;

@ApplicationScoped
public class RecipeRepository implements PanacheRepository<Recipe> {
    
    // Get random sample of recipes
    public List<Recipe> findAllSample(int k) {
        return getEntityManager().createNativeQuery("SELECT * FROM recipes s ORDER BY RANDOM() LIMIT :limit", Recipe.class)
            .setParameter("limit", k)
            .getResultList();
    }
    
    // Get recipe by name
    public List<Recipe> getRecipe(String query) {
        return getEntityManager().createNativeQuery(
            "SELECT * FROM recipes s WHERE s.name=:query ORDER BY RANDOM()", Recipe.class)
            .setParameter("query", query)
            .getResultList();

    }
    
    // Find recipes by category ID
    public List<Recipe> findRecipesByCategoryId(Integer categoryId) {
        return getEntityManager().createNativeQuery(
            "SELECT r.* FROM recipes r JOIN recipes_categories rc ON r.id = rc.recipeid " +
            "WHERE rc.catid = :categoryId limit 10", Recipe.class)
            .setParameter("categoryId", categoryId)
            .getResultList();
    }
    
    // Find recipes by category name
    public List<Recipe> findRecipesByCategoryName(String categoryName) {
        return getEntityManager().createNativeQuery(
            "SELECT r.* FROM recipes r JOIN recipes_categories rc ON r.id = rc.recipeid " +
            "JOIN categories c ON rc.catid = c.id WHERE LOWER(c.name) = :categoryName limit 10", Recipe.class)
            .setParameter("categoryName", categoryName.toLowerCase())
            .getResultList();
    }
}