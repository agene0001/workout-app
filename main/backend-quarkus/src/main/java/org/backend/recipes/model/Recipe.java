package org.backend.recipes.model;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "recipes")
public class Recipe {
    @Id
    @SequenceGenerator(
            name = "recipe_sequence",
            sequenceName = "recipe_sequence",
            allocationSize = 1
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "recipe_sequence"
    )
    @Column(name = "id", updatable = false)
    private int id;
    
    private String name;
    private String url;

    // Add JsonIgnoreProperties annotation to break the infinite recursion
    @ManyToMany(mappedBy = "recipes")
    @JsonIgnoreProperties("recipes")
    private Set<Category> categories = new HashSet<>();

    @Column(name = "instructions", columnDefinition = "TEXT[]")
    @JdbcTypeCode(SqlTypes.ARRAY)
    private String[] instructions;

    @Column(name = "servings", columnDefinition = "TEXT")
    private String servings;

    @Column(name = "nutrition", columnDefinition = "TEXT")
    private String nutrition;

    @Column(name = "level")
    private String level;

    @Column(name = "num_of_ratings", columnDefinition = "INT")
    private int numOfRatings;

    @Column(name = "ingredients", columnDefinition = "text[]")
    @JdbcTypeCode(SqlTypes.ARRAY)
    private String[] ingredients;

    @Column(name = "img_src", columnDefinition = "varchar(255)")
    private String imgSrc;

    @Column(name = "duration")
    private String duration;

    @Column(name = "rating", columnDefinition = "decimal(3,2)")
    private float rating;

    // Constructors
    public Recipe() {
    }

    public Recipe(int id, String name, String url) {
        this.id = id;
        this.name = name;
        this.url = url;
    }

    public Recipe(int id, String name, Float rating) {
        this.id = id;
        this.name = name;
        this.rating = rating;
    }

    public Recipe(int id,
                  String name,
                  String url,
                  String[] ingredients,
                  String[] instructions,
                  String nutrition,
                  String level,
                  int numOfRatings,
                  String imgSrc,
                  String duration,
                  float rating,
                  String servings
    ) {
        this.id = id;
        this.name = name;
        this.url = url;
        this.ingredients = ingredients;
        this.instructions = instructions;
        this.nutrition = nutrition;
        this.level = level;
        this.numOfRatings = numOfRatings;
        this.imgSrc = imgSrc;
        this.duration = duration;
        this.rating = rating;
        this.servings = servings;
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

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getNutrition() {
        return nutrition;
    }

    public void setNutrition(String nutrition) {
        this.nutrition = nutrition;
    }

    public String getLevel() {
        return level;
    }

    public void setLevel(String level) {
        this.level = level;
    }

    public int getNumOfRatings() {
        return numOfRatings;
    }

    public void setNumOfRatings(int numOfRatings) {
        this.numOfRatings = numOfRatings;
    }

    public String getImgSrc() {
        return imgSrc;
    }

    public void setImgSrc(String imgSrc) {
        this.imgSrc = imgSrc;
    }

    public String getDuration() {
        return duration;
    }

    public void setDuration(String duration) {
        this.duration = duration;
    }

    public float getRating() {
        return rating;
    }

    public void setRating(Float rating) {
        this.rating = rating;
    }

    public String[] getIngredients() {
        return ingredients;
    }

    public void setIngredients(String[] ingredients) {
        this.ingredients = ingredients;
    }

    public String[] getInstructions() {
        return instructions;
    }

    public void setInstructions(String[] instructions) {
        this.instructions = instructions;
    }

    public String getServings() {
        return servings;
    }

    public void setServings(String servings) {
        this.servings = servings;
    }

    public Set<Category> getCategories() {
        return categories;
    }

    public void setCategories(Set<Category> categories) {
        this.categories = categories;
    }

    @Override
    public String toString() {
        return "{" +
                "\"id\":" + id +
                ", \"name\":\"" + name + '\"' +
                ", \"url\":\"" + url + '\"' +
                ", \"ingredients\":\"" + Arrays.toString(ingredients) + '"' +
                ", \"instructions\":\"" + Arrays.toString(instructions) + '"' +
                ", \"nutrition\":\"" + nutrition + '"' +
                ", \"level\": \""+level +'"'+
                ", \"numOfRatings\":" + numOfRatings +
                ", \"imgSrc\":\"" + imgSrc + '"' +
                ", \"duration\":\"" + duration.replace(", ","") + '"' +
                ", \"rating\":" + rating +
                ", \"servings\":\"" + servings +'"' +
                '}';
    }
}