package com.example.server1.recipe;

import jakarta.persistence.*;

import static jakarta.persistence.GenerationType.SEQUENCE;

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
            strategy = SEQUENCE,
            generator = "recipe_sequence"
    )

    @Column(name = "id", updatable = false)
    private Long id;
    private String name;

    public Recipe() {

    }

    public Recipe(Long id, String name, String url) {
        this.id = id;
        this.name = name;
        this.url = url;
    }

    public Recipe(Long id, String name, double rating) {
        this.id = id;
        this.name = name;
        this.rating = rating;
    }

    private String url;

    public Recipe(Long id,
                  String name,
                  String url,
                  String ingredients,
                  String nutrition,
                  String level,
                  int numOfRatings,
                  String imgSrc,
                  String duration,
                  double rating,
                  Integer calories) {
        this.id = id;
        this.name = name;
        this.url = url;
        this.ingredients = ingredients;
        this.nutrition = nutrition;
        this.level = level;
        this.numOfRatings = numOfRatings;
        this.imgSrc = imgSrc;
        this.duration = duration;
        this.rating = rating;
        this.calories = calories;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
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

    public String getIngredients() {
        return ingredients;
    }

    public void setIngredients(String ingredients) {
        this.ingredients = ingredients;
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

    public double getRating() {
        return rating;
    }

    public void setRating(double rating) {
        this.rating = rating;
    }

    @Column(name = "ingredients", columnDefinition = "TEXT")
    private String ingredients;
    @Column(name = "nutrition", columnDefinition = "TEXT")
    private String nutrition;
    @Column(name = "level")
    private String level;
    @Column(name = "numOfRatings", columnDefinition = "INT")
    private int numOfRatings;

    public Integer getCalories() {
        return calories;
    }

    public void setCalories(Integer calories) {
        this.calories = calories;
    }

    @Column(name = "calories", columnDefinition = "INT", nullable = true)
    private Integer calories;
    @Column(name = "imgSrc", columnDefinition = "varchar(300)")
    private String imgSrc;
    @Column(name = "duration")
    private String duration;
    @Column(name = "rating", columnDefinition = "decimal(5,2)")
    private double rating;

    @Override
    public String toString() {
        return "Recipe{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", url='" + url + '\'' +
                ", ingredients='" + ingredients + '\'' +
                ", nutrition='" + nutrition + '\'' +
                ", level='" + level + '\'' +
                ", numOfRatings=" + numOfRatings +
                ", imgSrc='" + imgSrc + '\'' +
                ", duration='" + duration + '\'' +
                ", rating=" + rating +
                ", calories=" + calories +
                '}';
    }
}
