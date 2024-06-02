package com.example.server1.recipe;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Optional;

public interface RecipeRepository extends JpaRepository<Recipe, Long> {
    @Query(value="SELECT * FROM Recipes s ORDER BY RAND() LIMIT ?1", nativeQuery = true)
    List<Recipe> findAllSample(int k);
    @Query(value="SELECT recipes.* FROM categories INNER JOIN recipe_categories ON categories.category_id=recipe_categories.category_id INNER JOIN recipes ON recipes.id=recipe_categories.recipe_id WHERE categories.category_name like ?1", nativeQuery = true)
    List<Recipe> findByCategory(String category);
}
