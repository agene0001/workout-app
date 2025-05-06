package org.backend.recipes.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "categories")
public class Category {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private String name;

    // Add JsonIgnoreProperties annotation to break the infinite recursion
    @ManyToMany
    @JoinTable(
            name = "recipes_categories",
            joinColumns = @JoinColumn(name = "catid"),
            inverseJoinColumns = @JoinColumn(name = "recipeid")
    )
    @JsonIgnoreProperties("categories")
    private Set<Recipe> recipes = new HashSet<>();

    // Constructors
    public Category() {}

    public Category(String name) {
        this.name = name;
    }

    // Getters and Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Set<Recipe> getRecipes() {
        return recipes;
    }

    public void setRecipes(Set<Recipe> recipes) {
        this.recipes = recipes;
    }

    // Helper methods
    public void addRecipe(Recipe recipe) {
        this.recipes.add(recipe);
        recipe.getCategories().add(this);
    }

    public void removeRecipe(Recipe recipe) {
        this.recipes.remove(recipe);
        recipe.getCategories().remove(this);
    }
}