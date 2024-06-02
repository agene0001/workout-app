package com.example.server1.recipe;

import com.example.server1.Term;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@CrossOrigin(origins="http://localhost:5173")
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
//    @GetMapping(path="{term}")
//    List<Recipe> getRecipes(@PathVariable String term) {
//        return recipeService
//    }
    @GetMapping(path="/build/{k}")
    List<Recipe> getRecipesBuild(@PathVariable int k) {
        return recipeService.buildRecipes(k);
    }
    @PostMapping(path="{string}")
    Term[] autocompleteRecipe(@PathVariable String string) {
//        System.out.println(string);
        if (string == null || string.isEmpty()) {
            return new Term[0];
        }
        return recipeService.autocompleteRecipe(string);
    }
}
