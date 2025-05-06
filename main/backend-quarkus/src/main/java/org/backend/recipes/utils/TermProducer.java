package org.backend.recipes.utils;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;
import org.backend.recipes.model.Recipe;
import org.backend.recipes.repository.RecipeRepository;

import java.util.List;

@ApplicationScoped
public class TermProducer {

    private final RecipeRepository recipeRepository;

    public TermProducer(RecipeRepository recipeRepository) {
        this.recipeRepository = recipeRepository;
    }

    @Produces
    public List<Term> produceTerms() {
        List<Recipe> recipes = recipeRepository.findAll().list();
        return recipes.stream()
                .map(recipe -> new Term(recipe.getName(), recipe.getRating()))
                .toList();
    }
}
