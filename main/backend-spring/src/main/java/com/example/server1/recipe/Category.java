package com.example.server1.recipe;

import jakarta.persistence.*;

@Entity
@Table(name="categories")
public class Category {
    @Id
    @JoinTable(name="recipe_categories",joinColumns = @JoinColumn(name="recipe_id"),inverseJoinColumns = @JoinColumn(name="category_id"))
    @GeneratedValue
    private Long category_id;
    private String category_name;
}
