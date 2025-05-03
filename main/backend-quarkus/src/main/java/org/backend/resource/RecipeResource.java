package org.backend.resource;

import io.quarkus.logging.Log;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import org.backend.model.Recipe;
import org.backend.service.JavalinRecommender;
import org.backend.service.RecipeService;
import org.backend.utils.Term;
import io.javalin.Javalin;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Path("/api/v1/recipes")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@ApplicationScoped
public class RecipeResource {
    private static final int DEFAULT_PAGE_SIZE = 6; // Define a default page size

    private final RecipeService recipeService;

    @Inject
    public RecipeResource(RecipeService recipeService) {
        this.recipeService = recipeService;
    }

    @GET
    @Path("/{k}")
    @Produces(MediaType.APPLICATION_JSON)

    public List<Recipe> getSampleRecipes(@PathParam("k") int k) {
        try {
            long start = System.currentTimeMillis();
            List<Recipe> recipes = recipeService.getSample(k);
            long end = System.currentTimeMillis();
            System.out.println("Execution time for getSample(k): " + (end - start) + " ms");
            System.out.println("Retrieved " + recipes.size() + " recipes");
            System.out.println("Retrieved " + recipes + " recipes");
            return recipes;
        } catch (Exception e) {
            System.err.println("Error in getSampleRecipes: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
    }

    @GET
    @Path("/recipe/{term}")
    @Produces(MediaType.APPLICATION_JSON)

    public List<Recipe> getRecipe(@PathParam("term") String term) {
        System.out.println("getRecipe called with term: " + term);
        List<Recipe> recipes = recipeService.getRecipe(term);
        System.out.println("getRecipe result: " + recipes);
        return recipes;
    }

    @POST
    @Path("/{string}")
    @Produces(MediaType.APPLICATION_JSON)
    public Term[] autocompleteRecipe(@PathParam("string") String string) {
        if (string == null || string.isEmpty()) {
            return new Term[0];
        }
        return recipeService.autocompleteRecipe(string);
    }


    @GET
    @Path("/category/{category}")
    public List<Recipe> getRecipesByCategory(
            @PathParam("category") String category,
            @QueryParam("page") @DefaultValue("0") int page, // Add page parameter (0-indexed)
            @QueryParam("pageSize") @DefaultValue("6") int pageSize) { // Add pageSize parameter

        // Ensure pageSize isn't excessively large or negative, adjust if necessary
        if (pageSize <= 0) {
            pageSize = DEFAULT_PAGE_SIZE;
        }
        // You might want to add an upper limit to pageSize as well

        Log.infof("Fetching recipes for category: %s, page: %d, pageSize: %d", category, page, pageSize);

        // **IMPORTANT:** You need to update your RecipeService.getRecipesByCategoryName
        // method to accept and use these page and pageSize parameters to limit the results.
        // The example below assumes the service method is updated.
        return recipeService.getRecipesByCategoryName(category, page, pageSize);
    }


    @GET
    @Path("/recommendations")
    public List<List<Recipe>> getRecommendations(
            @QueryParam("query") String query,
            @QueryParam("ingredients") String ingredients,
            @QueryParam("k") @DefaultValue("10") int k) {
        try {
            // Call the updated service method that returns List<Recipe> directly
            List<Recipe> recommendations = recipeService.getRecommendations(query, ingredients, k);

            if (recommendations == null) {
                Log.error("Failed to get recommendations, service returned null");
                return new ArrayList<>();
            }

            // Convert each Recipe into a List<Recipe> to maintain the expected return type
            return recommendations.stream()
                    .map(row -> {
                        // Get the recipe by name from the database
                        List<Recipe> recipesWithDetails = recipeService.getRecipe(row.getName());

                        // If the recipe isn't found in the DB, use the recommendation as-is
                        if (recipesWithDetails == null || recipesWithDetails.isEmpty()) {
                            List<Recipe> singleRecipe = new ArrayList<>();
                            singleRecipe.add(row);
                            return singleRecipe;
                        }



                        return recipesWithDetails;
                    })
                    .collect(Collectors.toList());
        } catch (Exception e) {
            Log.error("Error in getRecommendations endpoint: ", e);
            return new ArrayList<>();
        }
    }

//    @GET
//    @Path("/build_recipes")
//    public List<Recipe> buildRecipes(@QueryParam("calories") int calories) {
//        return recipeService.buildRecipes(calories);
//    }
}