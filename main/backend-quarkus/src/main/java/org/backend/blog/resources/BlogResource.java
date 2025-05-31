package org.backend.blog.resources;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.security.Principal;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import org.backend.blog.model.Comment;
import org.backend.blog.model.Post;
import org.backend.blog.services.CommentService;
import org.backend.blog.services.PostService;
import org.backend.common.ApiPaths;
import org.backend.common.ApiResource;
import org.eclipse.microprofile.config.inject.ConfigProperty; // Ensure this import is present
import org.jboss.logging.Logger;
import org.jboss.resteasy.reactive.RestForm;
import org.jboss.resteasy.reactive.multipart.FileUpload;

// Removed specific import for java.nio.file.Path to avoid conflict with jakarta.ws.rs.Path
// We will use fully qualified name for java.nio.file.Path variables.

@Path(ApiPaths.BLOG)
@ApplicationScoped
public class BlogResource extends ApiResource {

    private static final Logger LOG = Logger.getLogger(BlogResource.class);
    private static final String MANAGED_IMAGE_PATH_PREFIX = ApiPaths.BLOG + "/uploaded/images/";
    @Inject
    PostService postService;

    @ConfigProperty(name = "app.upload.dir") // Use @ConfigProperty
    String uploadDir;

    @Inject // Inject ObjectMapper
    ObjectMapper objectMapper;

    @Inject
    CommentService commentService;

    @Context // Inject SecurityContext
    SecurityContext securityContext;

    // New Endpoint for Image Uploads
    @POST
    @Path("/images/upload")
    @Consumes(MediaType.MULTIPART_FORM_DATA)
    public Response uploadImage(
        @Context SecurityContext securityContext,
        FileUploadInput input
    ) {
        Principal userPrincipal = securityContext.getUserPrincipal();
        if (userPrincipal == null || !securityContext.isUserInRole("admin")) {
            LOG.warn("Unauthorized attempt to upload image.");
            return Response.status(Response.Status.UNAUTHORIZED)
                .entity("User not authorized to upload images.")
                .build();
        }

        if (input == null || input.imageFile == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                .entity("No image file provided.")
                .build();
        }

        FileUpload fileUpload = input.imageFile;

        try {
            // Create the upload directory if it doesn't exist
            java.nio.file.Path uploadPath = Paths.get(uploadDir); // Use the configured uploadDir
            LOG.info(
                "Attempting to use upload directory (from config): " +
                uploadPath.toAbsolutePath().toString()
            );
            if (!Files.exists(uploadPath)) {
                LOG.info(
                    "Upload directory does not exist, attempting to create: " +
                    uploadPath.toAbsolutePath().toString()
                );
                Files.createDirectories(uploadPath);
            }

            // Generate a unique filename (e.g., UUID + original extension)
            String originalFileName = fileUpload.fileName();
            LOG.info("Original filename from FileUpload: " + originalFileName);
            LOG.info(
                "Temporary uploaded file path: " +
                fileUpload.uploadedFile().toString()
            );
            String extension = "";
            int i = originalFileName.lastIndexOf('.');
            if (i > 0) {
                extension = originalFileName.substring(i);
            }
            String newFileName = UUID.randomUUID().toString() + extension;
            java.nio.file.Path filePath = uploadPath.resolve(newFileName);

            // Save the file
            Files.copy(
                fileUpload.uploadedFile(),
                filePath,
                StandardCopyOption.REPLACE_EXISTING
            );
            LOG.info(
                "Successfully copied image to: " +
                filePath.toAbsolutePath().toString()
            );

            // Construct the URL to return to the frontend.
            String imageUrl = ApiPaths.BLOG + "/uploaded/images/" + newFileName;

            return Response.ok(
                Map.of("url", imageUrl, "name", newFileName)
            ).build();
        } catch (IOException e) {
            LOG.error("Failed to upload image", e);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                .entity("Failed to upload image.")
                .build();
        }
    }

    // New Endpoint for Image Deletion
    @DELETE
    @Path("/images/delete/{filename}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response deleteImage(
        @Context SecurityContext securityContext,
        @PathParam("filename") String filename
    ) {
        LOG.info("Attempting to delete image: " + filename);
        Principal userPrincipal = securityContext.getUserPrincipal();
        if (userPrincipal == null || !securityContext.isUserInRole("admin")) {
            LOG.warnf(
                "Unauthorized attempt to delete image %s by user %s",
                filename,
                (userPrincipal != null
                        ? userPrincipal.getName()
                        : "anonymous/unauthenticated")
            );
            return Response.status(Response.Status.UNAUTHORIZED)
                .entity(
                    Map.of("message", "User not authorized to delete images.")
                )
                .build();
        }

        if (
            filename == null ||
            filename.trim().isEmpty() ||
            filename.contains("..")
        ) {
            LOG.warnf(
                "Attempt to access invalid filename for deletion: %s",
                filename
            );
            return Response.status(Response.Status.BAD_REQUEST)
                .entity(Map.of("message", "Invalid filename provided."))
                .build();
        }

        try {
            java.nio.file.Path uploadPathDir = Paths.get(uploadDir);
            java.nio.file.Path filePath = uploadPathDir
                .resolve(filename)
                .normalize();

            // Security check: Ensure the resolved path is still within the intended upload directory
            if (
                !filePath
                    .toAbsolutePath()
                    .startsWith(uploadPathDir.toAbsolutePath())
            ) {
                LOG.warnf(
                    "Attempt to delete file outside of upload directory: %s (resolved to %s)",
                    filename,
                    filePath.toAbsolutePath().toString()
                );
                return Response.status(Response.Status.FORBIDDEN)
                    .entity(
                        Map.of(
                            "message",
                            "Access to the requested file path is forbidden for deletion."
                        )
                    )
                    .build();
            }

            boolean deleted = Files.deleteIfExists(filePath);
            if (deleted) {
                LOG.infof(
                    "Successfully deleted image: %s",
                    filePath.toAbsolutePath().toString()
                );
                return Response.noContent().build(); // 204 No Content
            } else {
                // File was not found by deleteIfExists
                LOG.warnf(
                    "Image not found, could not delete: %s",
                    filePath.toAbsolutePath().toString()
                );
                return Response.status(Response.Status.NOT_FOUND)
                    .entity(Map.of("message", "Image not found."))
                    .build();
            }
        } catch (IOException e) {
            LOG.errorf(e, "Failed to delete image %s", filename);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                .entity(
                    Map.of(
                        "message",
                        "Failed to delete image due to a server error."
                    )
                )
                .build();
        }
    }

    // Helper class for multipart form input
    public static class FileUploadInput {

        @RestForm("image") // Name of the form field in the multipart request
        public FileUpload imageFile;
    }

    // GET all posts - remains public (or add security if needed)
    @GET
    @Path("/posts")
    public Response getAllPosts() {
        List<Post> posts = postService.getAllPosts();
        List<Map<String, Object>> enrichedPosts = posts
            .stream()
            .map(this::enrichPostForFrontend)
            .collect(Collectors.toList());

        return Response.ok(enrichedPosts).build();
    }

    // GET single post by ID - remains public (or add security if needed)
    @GET
    @Path("/posts/id/{id}")
    public Response getPostById(@PathParam("id") UUID id) {
        return postService
            .getPostById(id)
            .map(post -> Response.ok(enrichPostForFrontend(post)).build())
            .orElse(Response.status(Response.Status.NOT_FOUND).build());
    }

    // GET single post by ID - remains public (or add security if needed)
    @GET
    @Path("/posts/slug/{slug}")
    public Response getPostBySlug(@PathParam("slug") String slug) {
        List<Post> posts = postService.getPostBySlug(slug);
        List<Map<String, Object>> enrichedPosts = posts
            .stream()
            .map(this::enrichPostForFrontend)
            .collect(Collectors.toList());

        return Response.ok(enrichedPosts).build();
    }

    // GET categories - remains public
    @GET
    @Path("/categories")
    public Response getCategories() {
        List<Map<String, String>> categories = new ArrayList<>();
        categories.add(Map.of("slug", "fitness", "name", "Fitness"));
        categories.add(Map.of("slug", "nutrition", "name", "Nutrition"));
        categories.add(Map.of("slug", "wellness", "name", "Wellness"));
        categories.add(Map.of("slug", "training", "name", "Training"));

        return Response.ok(categories).build();
    }

    // CREATE new post - SECURED

    @POST
    @Path("/posts")
    public Response createPost(
        @Context SecurityContext securityContext,
        Post postRequest
    ) {
        Principal userPrincipal = securityContext.getUserPrincipal();
        if (userPrincipal == null) {
            LOG.warn(
                "User principal not found in security context for createPost."
            );
            return Response.status(Response.Status.UNAUTHORIZED)
                .entity("User principal not found.")
                .build();
        }
        String authorId = userPrincipal.getName();
        LOG.infof("User Principal in createPost: %s", authorId);
        LOG.infof("Is user in admin role (SecurityContext): %s",
                Optional.of(securityContext.isUserInRole("admin"))
        );

        // Fetch author details from Firebase Auth or your user service
        // This is a placeholder, replace with actual logic
        String authorName = "Default Author Name"; // Fetch appropriately
        String authorTitle = "Default Author Title"; // Fetch appropriately
        // Example:
        // try {
        //     UserRecord userRecord = FirebaseAuth.getInstance().getUser(authorId);
        //     authorName = userRecord.getDisplayName() != null ? userRecord.getDisplayName() : authorName;
        //     // You might have custom claims for authorTitle
        // } catch (FirebaseAuthException e) {
        //     LOG.error("Error fetching user details for authorId: " + authorId, e);
        //     // Decide how to handle - proceed with defaults or return error
        // }

        try {
            // Pass the Map<String, Object> content directly from the DTO
            Post newPost = postService.createPost(
                postRequest.getTitle(),
                postRequest.getContent(), // This is already a Map<String, Object>
                postRequest.getExcerpt(),
                postRequest.getCategory(),
                authorId,
                authorName, // Pass fetched or default authorName
                authorTitle, // Pass fetched or default authorTitle
                postRequest.getImageUrl(),
                    postRequest.isFeatured(),
                postRequest.getReadTime()
            );
            return Response.status(Response.Status.CREATED)
                .entity(enrichPostForFrontend(newPost))
                .build();
        } catch (IllegalArgumentException e) {
            LOG.errorf(
                e,
                "Invalid arguments for creating post: %s",
                e.getMessage()
            );
            return Response.status(Response.Status.BAD_REQUEST)
                .entity("Invalid post data: " + e.getMessage())
                .build();
        } catch (Exception e) {
            LOG.errorf(e, "Error creating post: %s", e.getMessage());
            // It's good to provide an error ID for correlation in logs
            String errorId = java.util.UUID.randomUUID().toString();
            LOG.error("Error ID: " + errorId, e);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                .entity("Failed to create post. Error ID: " + errorId)
                .build();
        }
    }

    @PUT
    @Path("/posts")
    // @RolesAllowed("admin") // This would be for SmallRye JWT.
    public Response updatePost(
        @Context SecurityContext securityContext,
        Post postData
    ) {
        Principal userPrincipal = securityContext.getUserPrincipal();
        if (userPrincipal == null) {
            LOG.warn(
                "User principal not found in security context for createPost."
            );
            return Response.status(Response.Status.UNAUTHORIZED)
                .entity("User principal not found.")
                .build();
        }

        // Add other fields from postData as needed for update
        // String excerpt = (String) postData.get("excerpt");
        // String category = (String) postData.get("category");
        // etc.
        LOG.info(postData.toString());
        if (postData.getTitle() == null && postData.getContent() == null) { // Or whatever your minimum update requirement is
            return Response.status(Response.Status.BAD_REQUEST)
                .entity(
                    Map.of(
                        "message",
                        "At least title or content must be provided for update."
                    )
                )
                .build();
        }

        try {
            // Assuming postService.updatePost is adapted to take the fields and adminUid for audit/logic
            // You'll need to decide how PostService.updatePost handles partial updates
            // and uses the adminUid.
            // The signature of postService.updatePost might need to be:
            // boolean updatePost(UUID id, String title, String content, /* other fields, */ String updaterAdminUid);
            // For this example, I'll keep your existing call signature if it fits,
            // otherwise, you need to adjust postService.updatePost
            LOG.info("Updating post: " + postData);
            Post updatedPost = postService.updatePost(postData); // Pass adminUid if service needs it

            if (updatedPost != null) {
                // If updatePost returns the updated post, use it directly
                return Response.ok(enrichPostForFrontend(updatedPost)).build();
            } else {
                // If updatePost returns null, try to fetch the post to see if it actually exists
                Optional<Post> updatedPostOpt = postService.getPostById(postData.getId());
                return updatedPostOpt
                        .map(post ->
                                Response.ok(enrichPostForFrontend(post)).build()
                        )
                        .orElse(
                                Response.status(Response.Status.NOT_FOUND)
                                        .entity(
                                                Map.of(
                                                        "message",
                                                        "Post not found or update failed."
                                                )
                                        )
                                        .build()
                        );
            }
        } catch (Exception e) {
            LOG.errorv(
                e,
                "Error updating post {0} in resource: {1}",
                postData.getId(),
                e.getMessage()
            );
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                .entity(
                    Map.of(
                        "message",
                        "An internal error occurred: " + e.getMessage()
                    )
                )
                .build();
        }
    }


    @DELETE
    @Path("/posts/{id}")
    public Response deletePost(
            @Context SecurityContext securityContext,
            @PathParam("id") UUID id
    ) {
        if (securityContext.getUserPrincipal() == null) {
            LOG.warn("User not authenticated for deletePost.");
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity(Map.of("message", "User not authenticated."))
                    .build();
        }
        if (!securityContext.isUserInRole("admin")) {
            LOG.warnf(
                    "User %s does not have admin privileges for deletePost.",
                    securityContext.getUserPrincipal().getName()
            );
            return Response.status(Response.Status.FORBIDDEN)
                    .entity(
                            Map.of("message", "User does not have admin privileges.")
                    )
                    .build();
        }
        // String adminUid = securityContext.getUserPrincipal().getName(); // Not used directly in this simplified version

        try {
            // 1. Fetch the post to get its imageUrl and content
            Optional<Post> postOptional = postService.getPostById(id);
            if (postOptional.isEmpty()) {
                return Response.status(Response.Status.NOT_FOUND)
                        .entity(Map.of("message", "Post not found."))
                        .build();
            }
            Post postToDelete = postOptional.get();

            // 2. Attempt to delete the featured image if it's a managed one
            if (postToDelete.getImageUrl() != null && postToDelete.getImageUrl().startsWith(MANAGED_IMAGE_PATH_PREFIX)) {
                String featuredImageFilename = extractFilenameFromUrl(postToDelete.getImageUrl());
                if (featuredImageFilename != null) {
                    LOG.infof("Attempting to delete featured image: %s for post %s", featuredImageFilename, id);
                    deleteSingleImageFile(featuredImageFilename); // Re-uses logic, ignoring response for this sub-task
                }
            }

            // 3. Attempt to delete images from the post's content
            if (postToDelete.getContent() != null) {
                try {
                    // The content is already Map<String, Object> in your Post model
                    Map<String, Object> contentMap = postToDelete.getContent();
                    if (contentMap.containsKey("blocks") && contentMap.get("blocks") instanceof List) {
                        @SuppressWarnings("unchecked") // Safe cast after instanceof check
                        List<Map<String, Object>> blocks = (List<Map<String, Object>>) contentMap.get("blocks");
                        for (Map<String, Object> block : blocks) {
                            if ("image".equals(block.get("type"))) {
                                Map<String, Object> data = (Map<String, Object>) block.get("data");
                                if (data != null && data.get("file") instanceof Map) {
                                    Map<String, Object> fileData = (Map<String, Object>) data.get("file");
                                    if (fileData != null && fileData.get("url") instanceof String) {
                                        String contentImageUrl = (String) fileData.get("url");
                                        if (contentImageUrl.startsWith(MANAGED_IMAGE_PATH_PREFIX)) {
                                            String contentImageFilename = extractFilenameFromUrl(contentImageUrl);
                                            if (contentImageFilename != null) {
                                                LOG.infof("Attempting to delete content image: %s for post %s", contentImageFilename, id);
                                                deleteSingleImageFile(contentImageFilename); // Re-uses logic
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } catch (Exception e) {
                    // Log this error but don't let it stop the post deletion itself
                    LOG.errorf(e, "Error processing content for image deletion for post %s. Post will still be deleted.", id);
                }
            }

            // 4. Delete the post from the database
            boolean deleted = postService.deletePost(id);
            if (deleted) {
                LOG.infof("Successfully deleted post %s from database.", id);
                return Response.noContent().build(); // 204 No Content is standard for successful DELETE
            } else {
                // This case should ideally not be reached if postOptional was present
                LOG.warnf("Post %s was found but database deletion reported failure.", id);
                return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                        .entity(
                                Map.of("message", "Post found but failed to delete from database.")
                        )
                        .build();
            }
        } catch (Exception e) {
            LOG.errorv(
                    e,
                    "General error deleting post {0} in resource: {1}",
                    id,
                    e.getMessage()
            );
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(
                            Map.of(
                                    "message",
                                    "An internal error occurred while deleting the post: " + e.getMessage()
                            )
                    )
                    .build();
        }
    }

    // Helper method to extract filename from a managed URL
    private String extractFilenameFromUrl(String imageUrl) {
        if (imageUrl != null && imageUrl.startsWith(MANAGED_IMAGE_PATH_PREFIX)) {
            return imageUrl.substring(MANAGED_IMAGE_PATH_PREFIX.length());
        }
        return null;
    }

    // Helper method to delete a single image file (simplified, adapt from your existing deleteImage)
    // This is a non-HTTP version, just for internal file system operations.
    private void deleteSingleImageFile(String filename) {
        if (filename == null || filename.trim().isEmpty() || filename.contains("..")) {
            LOG.warnf("Attempt to delete invalid filename (internal call): %s", filename);
            return;
        }
        try {
            java.nio.file.Path uploadPathDir = Paths.get(uploadDir);
            java.nio.file.Path filePath = uploadPathDir.resolve(filename).normalize();

            if (!filePath.toAbsolutePath().startsWith(uploadPathDir.toAbsolutePath())) {
                LOG.warnf("Attempt to delete file outside of upload directory (internal call): %s", filePath);
                return;
            }

            boolean deleted = Files.deleteIfExists(filePath);
            if (deleted) {
                LOG.infof("Successfully deleted image file (internal call): %s", filePath);
            } else {
                LOG.warnf("Image file not found for deletion (internal call): %s", filePath);
            }
        } catch (IOException e) {
            LOG.errorf(e, "Failed to delete image file (internal call) %s", filename);
        }
    }

    // GET comments for a post - public
    @GET
    @Path("/posts/{postId}/comments")
    public Response getCommentsForPost(@PathParam("postId") UUID postId) {
        List<Comment> comments = commentService.getCommentsForPost(postId);
        List<Map<String, Object>> enrichedComments = comments
            .stream()
            .map(this::enrichCommentForFrontend)
            .collect(Collectors.toList());
        return Response.ok(enrichedComments).build();
    }

    @POST
    @Path("/posts/{postId}/comments")
    public Response addComment(
            @PathParam("postId") UUID postId,
            Comment commentPayload // Use a DTO for clarity
    ) {
        if (securityContext == null || securityContext.getUserPrincipal() == null) {
            return Response.status(Response.Status.UNAUTHORIZED).entity(Map.of("message", "User not authenticated.")).build();
        }
        String authorId = securityContext.getUserPrincipal().getName();

        if (commentPayload.getContent() == null || commentPayload.getContent().trim().isEmpty()) {
            return Response.status(Response.Status.BAD_REQUEST).entity(Map.of("message", "Content is required.")).build();
        }

        // Attempt to parse parentCommentId if present
        UUID parentId = null;
        if (commentPayload.getParent() != null) {
            try {
                parentId = UUID.fromString(commentPayload.getParent().getId().toString());
            } catch (IllegalArgumentException e) {
                LOG.warnf("Invalid UUID format for parentCommentId: %s", commentPayload.getParent());
                return Response.status(Response.Status.BAD_REQUEST).entity(Map.of("message", "Invalid parentCommentId format.")).build();
            }
        }
        if(parentId != null) {
            LOG.info(parentId.toString());
        }
        LOG.info(commentPayload.toString());
        try {
            Comment newComment = commentService.addComment(
                    postId,
                    commentPayload.getContent(),
                    authorId,
                    parentId // Pass the parsed parentId (can be null)
            );
            return Response.status(Response.Status.CREATED)
                    .entity(enrichCommentForFrontend(newComment)) // enrichComment will now potentially have parent info
                    .build();
        } catch (IllegalArgumentException e) {
            LOG.warnf("Error adding comment: %s", e.getMessage());
            return Response.status(Response.Status.BAD_REQUEST).entity(Map.of("message", e.getMessage())).build();
        } catch (Exception e) {
            LOG.error("Unexpected error adding comment", e);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity(Map.of("message", "Could not add comment.")).build();
        }
    }
    @PUT
    @Path("/posts/{postId}/comments/{commentId}")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response updateComment(
            @Context SecurityContext securityContext,
            @PathParam("postId") UUID postId, // postId might be used for context or further validation if needed
            @PathParam("commentId") UUID commentId,
            Comment request) {

        if (securityContext == null || securityContext.getUserPrincipal() == null) {
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity(Map.of("message", "User not authenticated.")).build();
        }
        String requestingUserId = securityContext.getUserPrincipal().getName();

        if (request.getContent() == null || request.getContent().trim().isEmpty()) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Content cannot be empty.")).build();
        }

        try {
            // You'll need a method in CommentService like:
            // Comment updateComment(UUID commentId, String newContent, String authorId)
            // This service method should handle checking if the comment exists and if the authorId matches.
            Comment updatedComment = commentService.updateComment(commentId, request.getContent(), requestingUserId);
            if (updatedComment == null) { // Should be handled by exceptions in service preferably
                return Response.status(Response.Status.NOT_FOUND)
                        .entity(Map.of("message", "Comment not found or user not authorized.")).build();
            }
            return Response.ok(enrichCommentForFrontend(updatedComment)).build();
        } catch (NotFoundException e) { // Assuming your service throws this
            LOG.warnf("UpdateComment: Comment not found %s. Error: %s", commentId, e.getMessage());
            return Response.status(Response.Status.NOT_FOUND).entity(Map.of("message", e.getMessage())).build();
        } catch (ForbiddenException e) { // Assuming your service throws this for auth failure
            LOG.warnf("UpdateComment: User %s forbidden to update comment %s. Error: %s", requestingUserId, commentId, e.getMessage());
            return Response.status(Response.Status.FORBIDDEN).entity(Map.of("message", e.getMessage())).build();
        } catch (IllegalArgumentException e) {
            LOG.warnf("UpdateComment: Invalid argument for comment %s. Error: %s", commentId, e.getMessage());
            return Response.status(Response.Status.BAD_REQUEST).entity(Map.of("message", e.getMessage())).build();
        } catch (Exception e) {
            LOG.errorf(e, "Error updating comment %s", commentId);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(Map.of("message", "Could not update comment due to a server error.")).build();
        }
    }

    @DELETE
    @Path("/posts/{postId}/comments/{commentId}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response deleteComment(
            @Context SecurityContext securityContext,
            @PathParam("postId") UUID postId, // postId for context
            @PathParam("commentId") UUID commentId) {

        if (securityContext == null || securityContext.getUserPrincipal() == null) {
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity(Map.of("message", "User not authenticated.")).build();
        }
        String requestingUserId = securityContext.getUserPrincipal().getName();
        // You could also check for an "admin" role here if admins should be able to delete any comment.
        // boolean isAdmin = securityContext.isUserInRole("admin");

        try {
            // You'll need a method in CommentService like:
            // boolean deleteComment(UUID commentId, String authorId /*, boolean isAdmin */)
            // This service method should handle checking existence, ownership, and deleting.
            boolean deleted = commentService.deleteComment(commentId, requestingUserId /*, isAdmin */);
            if (deleted) {
                return Response.noContent().build(); // 204 No Content for successful deletion
            } else {
                // This path might be taken if service returns false instead of throwing NotFound/Forbidden
                return Response.status(Response.Status.NOT_FOUND)
                        .entity(Map.of("message", "Comment not found or user not authorized to delete.")).build();
            }
        } catch (NotFoundException e) {
            LOG.warnf("DeleteComment: Comment not found %s. Error: %s", commentId, e.getMessage());
            return Response.status(Response.Status.NOT_FOUND).entity(Map.of("message", e.getMessage())).build();
        } catch (ForbiddenException e) {
            LOG.warnf("DeleteComment: User %s forbidden to delete comment %s. Error: %s", requestingUserId, commentId, e.getMessage());
            return Response.status(Response.Status.FORBIDDEN).entity(Map.of("message", e.getMessage())).build();
        } catch (IllegalStateException e) { // e.g., if comment has replies and deletion is restricted
            LOG.warnf("DeleteComment: Cannot delete comment %s. Error: %s", commentId, e.getMessage());
            return Response.status(Response.Status.CONFLICT).entity(Map.of("message", e.getMessage())).build();
        }
        catch (Exception e) {
            LOG.errorf(e, "Error deleting comment %s", commentId);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(Map.of("message", "Could not delete comment due to a server error.")).build();
        }
    }
    // Helper method to enrich Post objects

    // Helper method to enrich Post objects
    private Map<String, Object> enrichPostForFrontend(Post post) {
        Map<String, Object> enrichedPost = new HashMap<>();
        enrichedPost.put(
            "id",
            post.getId() != null ? post.getId().toString() : null
        );
        enrichedPost.put("title", post.getTitle());
        enrichedPost.put("content", post.getContent()); // Content is Map<String, Object>
        enrichedPost.put("slug", post.getSlug()); // Use slug from Post entity directly

        enrichedPost.put("excerpt", post.getExcerpt());
        enrichedPost.put(
            "category",
            post.getCategory() != null ? post.getCategory() : "fitness"
        );

        int readTimeValue = 1; // Default read time
        if (post.getReadTime() != null && post.getReadTime() > 0) {
            readTimeValue = post.getReadTime();
        } else if (post.getContent() != null && !post.getContent().isEmpty()) {
            try {
                // Convert Map content to JSON String to estimate word count
                String contentAsString = objectMapper.writeValueAsString(
                    post.getContent()
                );
                // Basic word count (splits by whitespace). This is an approximation.
                int wordCount = contentAsString.split("\\s+").length;
                readTimeValue = Math.max(
                    1,
                    (int) Math.ceil((double) wordCount / 200)
                ); // Ensure it's at least 1
            } catch (JsonProcessingException e) {
                LOG.warnf(
                    e,
                    "Could not calculate word count from post content for post ID %s. Using default read time.",
                    post.getId()
                );
                // Keep default or set a predefined average if content processing fails
                readTimeValue = 5; // Fallback read time if word count fails
            }
        }
        enrichedPost.put("readTime", readTimeValue);

        enrichedPost.put(
            "publishedAt",
            post.getCreatedAt() != null
                ? post.getCreatedAt().toString()
                : Instant.now().toString()
        );
        enrichedPost.put(
            "updatedAt",
            post.getUpdatedAt() != null
                ? post.getUpdatedAt().toString()
                : Instant.now().toString()
        );
        enrichedPost.put("featured", post.isFeatured());
        String imageUrl = post.getImageUrl();
        String placeholderBase = "https://placehold.co/";

        if (imageUrl == null || imageUrl.trim().isEmpty()) {
            // --- Customizable Parameters ---
//            String dimensions = "600x400";       // Desired dimensions
            String color = "2D3748";            // A dark slate gray (hex without #)
            // Or a more vibrant color like "4A90E2" (a nice blue)
            // Or a subtle light gray like "F7FAFC"




            // RECOMMENDED placehold.co URL for a solid color:
            imageUrl = String.format("%s/%s", placeholderBase, color);

        }

        enrichedPost.put("image", imageUrl);

        Map<String, String> author = new HashMap<>();
        author.put(
            "name",
            post.getAuthorName() != null
                ? post.getAuthorName()
                : "Fitness Expert"
        );
        author.put(
            "title",
            post.getAuthorTitle() != null
                ? post.getAuthorTitle()
                : "Certified Trainer"
        );
        enrichedPost.put("author", author);
        return enrichedPost;
    }

    // Helper method to enrich Comment objects
    private Map<String, Object> enrichCommentForFrontend(Comment comment) {
        // ... (implementation as before)
        Map<String, Object> enrichedComment = new HashMap<>();
        enrichedComment.put("id", comment.getId());
        enrichedComment.put("content", comment.getContent());
        enrichedComment.put("createdAt", comment.getCreatedAt().toString());
        Map<String, String> author = new HashMap<>();
        // Fetch actual author details based on comment.getAuthorId()
        author.put("name", "Fitness Enthusiast"); // Placeholder
        author.put("avatar", "https://placehold.co/64x64/gray/white"); // Placeholder
        enrichedComment.put("author", author);
        if (comment.getParent() == null) {
            List<Map<String, Object>> replies = comment.getReplies() != null
                ? comment
                    .getReplies()
                    .stream()
                    .map(this::enrichCommentForFrontend)
                    .collect(Collectors.toList())
                : new ArrayList<>();
            enrichedComment.put("replies", replies);
        }
        return enrichedComment;
    }
}
