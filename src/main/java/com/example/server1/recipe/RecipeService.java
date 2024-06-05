package com.example.server1.recipe;

import com.example.server1.Autocomplete;
import com.example.server1.Term;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class RecipeService {
    private final RecipeRepository recipeRepository;
    private final Autocomplete recipeAutocomplete;

    @Autowired
    public RecipeService(RecipeRepository recipeRepository) {
        this.recipeRepository = recipeRepository;
        Term[] terms = Autocomplete.setup("static/automation_recipes.csv");
        this.recipeAutocomplete = new Autocomplete(terms);
    }

    public List<Recipe> getSample(int k) {
//        List<Recipe> lis =recipeRepository.findSample(10);
//        for(Recipe r:lis){
//            System.out.println(r);
//        }
        return recipeRepository.findAllSample(k);
    }

    public Term[] autocompleteRecipe(String query) {
        try {
            Term[] matches = recipeAutocomplete.allMatches(query.toLowerCase());
            return matches;
        } catch (Exception e) {
            return new Term[0];
        }

    }

//    public static Term[] recipesSetup(Recipe[] recipes, int k) {
//        Term[] terms = new Term[k];
//        int i = 0;
//        for (Recipe recipe : recipes) {
//            terms[i++] = new Term(recipe.getName().toLowerCase(), (long) recipe.getRating());
//        }
//        return terms;
//    }
}
