package org.backend.blog.resources;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.backend.blog.model.Comment;
import org.backend.blog.model.Post;
import org.backend.blog.services.CommentService;
import org.backend.blog.services.PostService;
import org.backend.common.ApiPaths;
import org.backend.common.ApiResource;

import java.util.*;
import java.util.stream.Collectors;

@Path(ApiPaths.BLOG)
@ApplicationScoped
public class BlogResource extends ApiResource {

    @Inject
    PostService postService;

    @Inject
    CommentService commentService;

    // GET all posts with additional frontend-required fields
    @GET
    @Path("/posts")
    public Response getAllPosts() {
        List<Post> posts = postService.getAllPosts();
        List<Map<String, Object>> enrichedPosts = posts.stream()
            .map(this::enrichPostForFrontend)
            .collect(Collectors.toList());
        
        return Response.ok(enrichedPosts).build();
    }

    // GET single post by ID
    @GET
    @Path("/posts/{id}")
    public Response getPostById(@PathParam("id") UUID id) {
        return postService.getPostById(id)
            .map(post -> Response.ok(enrichPostForFrontend(post)).build())
            .orElse(Response.status(Response.Status.NOT_FOUND).build());
    }

    // GET categories
    @GET
    @Path("/categories")
    public Response getCategories() {
        // For now, return some sample categories matching what frontend expects
        List<Map<String, String>> categories = new ArrayList<>();
        categories.add(Map.of("slug", "fitness", "name", "Fitness"));
        categories.add(Map.of("slug", "nutrition", "name", "Nutrition"));
        categories.add(Map.of("slug", "wellness", "name", "Wellness"));
        categories.add(Map.of("slug", "training", "name", "Training"));
        
        return Response.ok(categories).build();
    }

    // CREATE new post
    @POST
    @Path("/posts")
    public Response createPost(Map<String, Object> postData) {
        String title = (String) postData.get("title");
        String content = (String) postData.get("content");
        String authorId = (String) postData.get("authorId");
        
        if (title == null || content == null || authorId == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                .entity("Title, content, and authorId are required").build();
        }
        
        Post newPost = postService.createPost(title, content, authorId);
        return Response.status(Response.Status.CREATED)
            .entity(enrichPostForFrontend(newPost)).build();
    }

    // UPDATE existing post
    @PUT
    @Path("/posts/{id}")
    public Response updatePost(@PathParam("id") UUID id, Map<String, Object> postData) {
        String title = (String) postData.get("title");
        String content = (String) postData.get("content");
        String authorId = (String) postData.get("authorId");
        
        if (title == null || content == null || authorId == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                .entity("Title, content, and authorId are required").build();
        }
        
        boolean updated = postService.updatePost(id, title, content, authorId);
        if (updated) {
            Optional<Post> updatedPost = postService.getPostById(id);
            return updatedPost
                .map(post -> Response.ok(enrichPostForFrontend(post)).build())
                .orElse(Response.status(Response.Status.NOT_FOUND).build());
        } else {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
    }

    // DELETE post
    @DELETE
    @Path("/posts/{id}")
    public Response deletePost(@PathParam("id") UUID id, @QueryParam("authorId") String authorId) {
        if (authorId == null || authorId.isEmpty()) {
            return Response.status(Response.Status.BAD_REQUEST)
                .entity("AuthorId is required").build();
        }
        
        boolean deleted = postService.deletePost(id, authorId);
        if (deleted) {
            return Response.noContent().build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
    }

    // GET comments for a post
    @GET
    @Path("/posts/{postId}/comments")
    public Response getCommentsForPost(@PathParam("postId") UUID postId) {
        List<Comment> comments = commentService.getCommentsForPost(postId);
        
        // Transform comments to include needed frontend data
        List<Map<String, Object>> enrichedComments = comments.stream()
            .map(this::enrichCommentForFrontend)
            .collect(Collectors.toList());
        
        return Response.ok(enrichedComments).build();
    }

    // ADD comment to a post
    @POST
    @Path("/posts/{postId}/comments")
    public Response addComment(@PathParam("postId") UUID postId, Map<String, String> commentData) {
        String content = commentData.get("content");
        String authorId = commentData.get("authorId");
        
        if (content == null || authorId == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                .entity("Content and authorId are required").build();
        }
        
        Comment newComment = commentService.addComment(postId, content, authorId);
        return Response.status(Response.Status.CREATED)
            .entity(enrichCommentForFrontend(newComment)).build();
    }

    // Helper method to enrich Post objects with frontend-required fields
    private Map<String, Object> enrichPostForFrontend(Post post) {
        Map<String, Object> enrichedPost = new HashMap<>();
        
        // Original post fields
        enrichedPost.put("id", post.getId());
        enrichedPost.put("title", post.getTitle());
        enrichedPost.put("content", post.getContent());
        
        // Generate slug from title
        String slug = post.getTitle().toLowerCase()
            .replaceAll("[^a-z0-9\\s]", "")
            .replaceAll("\\s+", "-");
        enrichedPost.put("slug", slug);
        
        // Extract excerpt from content (first 150 chars)
        String excerpt = post.getContent() != null 
            ? (post.getContent().length() > 150 
                ? post.getContent().substring(0, 150) + "..." 
                : post.getContent()) 
            : "";
        enrichedPost.put("excerpt", excerpt);
        
        // Default category until we implement categories properly
        enrichedPost.put("category", "fitness");
        
        // Calculate read time (rough estimate: 200 words per minute)
        int readTime = 1;
        if (post.getContent() != null) {
            int wordCount = post.getContent().split("\\s+").length;
            readTime = Math.max(1, wordCount / 200);
        }
        enrichedPost.put("readTime", readTime);
        
        // Timestamps
        enrichedPost.put("publishedAt", post.getCreatedAt().toString());
        enrichedPost.put("updatedAt", post.getUpdatedAt().toString());
        
        // Featured status (newest post is featured)
        enrichedPost.put("featured", false);
        
        // Placeholder for image
        enrichedPost.put("image", "https://placehold.co/600x400/gray/white?text=Fitness+Blog");
        
        // Mock author data (should be fetched from user service in real app)
        Map<String, String> author = new HashMap<>();
        author.put("name", "Fitness Expert");
        author.put("title", "Certified Trainer");
        enrichedPost.put("author", author);
        
        return enrichedPost;
    }

    // Helper method to enrich Comment objects with frontend-required fields
    private Map<String, Object> enrichCommentForFrontend(Comment comment) {
        Map<String, Object> enrichedComment = new HashMap<>();
        
        enrichedComment.put("id", comment.getId());
        enrichedComment.put("content", comment.getContent());
        enrichedComment.put("createdAt", comment.getCreatedAt().toString());
        
        // Mock author data (should be fetched from user service in real app)
        Map<String, String> author = new HashMap<>();
        author.put("name", "Fitness Enthusiast");
        author.put("avatar", "https://placehold.co/64x64/gray/white");
        enrichedComment.put("author", author);
        
        // Add empty replies array for root comments
        if (comment.getParent() == null) {
            List<Map<String, Object>> replies = comment.getReplies() != null 
                ? comment.getReplies().stream()
                    .map(this::enrichCommentForFrontend)
                    .collect(Collectors.toList())
                : new ArrayList<>();
            enrichedComment.put("replies", replies);
        }
        
        return enrichedComment;
    }
}