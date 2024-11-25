package com.example.server1.recipe;

import com.example.server1.Term;
import org.apache.spark.sql.Row;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
//
@RestController
@RequestMapping("api/v1/recipes")
public class RecipeController {
    private final RecipeService recipeService;
    @Autowired
    public RecipeController(RecipeService recipeService) {
        this.recipeService = recipeService;
    }
    @GetMapping(path="{k}")
    List<Recipe> getSampleRecipes(@PathVariable int k) {
        return recipeService.getSample(k);
    }
    @GetMapping(path="/recipe/{term}")
    Recipe getRecipes(@PathVariable String term) {
        return recipeService.getRecipe(term);
    }

    @PostMapping(path="{string}")
    Term[] autocompleteRecipe(@PathVariable String string) {
//        System.out.println(string);
        if (string == null || string.isEmpty()) {
            return new Term[0];
        }
        return recipeService.autocompleteRecipe(string);
    }
    @GetMapping("/recommendations")
    public List<String> getRecommendations(
            @RequestParam String query,
            @RequestParam(defaultValue = "10") int k) {

        List<Row> recommendations = recipeService.getRecommendations(query, k);
        return recommendations.stream()
                .map(row -> row.getAs("name").toString())
                .collect(Collectors.toList()); // Use Collectors.toList() instead
    }

    @GetMapping("/build_recipes")
    public List<Row> buildRecipes(@RequestParam int calories) {
        return recipeService.buildRecipes(calories);
    }
}
