package com.example.server1.recipe;

import com.example.server1.Term;
import org.apache.spark.sql.Row;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("api/v1/recipes")
public class RecipeController {
    private final RecipeService recipeService;

    @Autowired
    public RecipeController(RecipeService recipeService) {
        this.recipeService = recipeService;
    }

    @GetMapping(path = "{k}")
    public List<Recipe> getSampleRecipes(@PathVariable int k) {
        try {
            long start = System.currentTimeMillis();
            List<Recipe> recipes = recipeService.getSample(k);
            long end = System.currentTimeMillis();
            System.out.println("Execution time for getSample(k): " + (end - start) + " ms");
            System.out.println("Retrieved " + recipes.size() + " recipes");
            return recipes;
        } catch (Exception e) {
            System.err.println("Error in getSampleRecipes: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
    }

    @GetMapping(path = "/recipe/{term}")
    public Recipe getRecipe(@PathVariable String term) {
        return recipeService.getRecipe(term);
    }

    @PostMapping(path = "{string}")
    public Term[] autocompleteRecipe(@PathVariable String string) {
        if (string == null || string.isEmpty()) {
            return new Term[0];
        }
        return recipeService.autocompleteRecipe(string);
    }

    @GetMapping("/recommendations")
    public List<Recipe> getRecommendations(
            @RequestParam String query,
            @RequestParam String ingredients,
            @RequestParam(defaultValue = "10") int k) {
        List<Row> recommendations = recipeService.getRecommendations(query,ingredients, k);
        return recommendations.stream()
                .map(row -> recipeService.getRecipe(row.getAs("name").toString()))
                .collect(Collectors.toList());
    }

    @GetMapping("/build_recipes")
    public List<Row> buildRecipes(@RequestParam int calories) {
        return recipeService.buildRecipes(calories);
    }
}