package org.backend.blog.resources;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.storage.*;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
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
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.jboss.logging.Logger;
import org.jboss.resteasy.reactive.RestForm;
import org.jboss.resteasy.reactive.multipart.FileUpload;


@Path(ApiPaths.BLOG)
@ApplicationScoped
public class BlogResource extends ApiResource {

    private static final Logger LOG = Logger.getLogger(BlogResource.class);
    // This prefix is no longer strictly used for file paths, but can still identify GCS URLs
    // private static final String MANAGED_IMAGE_PATH_PREFIX = ApiPaths.BLOG + "/uploaded/images/";
    // It's better to check against the GCS bucket URL directly as shown below

    @Inject
    PostService postService;

    @Inject // Inject Google Cloud Storage client
    Storage storage;

    @Inject // Inject ObjectMapper
    ObjectMapper objectMapper;

    @ConfigProperty(name = "app.gcs.bucket-name") // New config property for GCS bucket
    String gcsBucketName;

    @Inject
    CommentService commentService;

    @Context // Inject SecurityContext
    SecurityContext securityContext;

    // Helper method to extract filename from a GCS public URL
    // e.g., "https://storage.googleapis.com/your-bucket/some-uuid.png" -> "some-uuid.png"
    private String extractFilenameFromGCSUrl(String gcsUrl) {
        if (gcsUrl == null || gcsUrl.trim().isEmpty()) {
            return null;
        }
        String prefix = String.format("https://storage.googleapis.com/%s/", gcsBucketName);
        if (gcsUrl.startsWith(prefix)) {
            return gcsUrl.substring(prefix.length());
        }
        return null; // Not a GCS URL we manage
    }

    // Helper method to delete a single image file (adapted for GCS)
    private void deleteSingleImageFile(String filename) {
        if (filename == null || filename.trim().isEmpty() || filename.contains("..") || filename.contains("/")) {
            LOG.warnf("Attempt to delete invalid filename (internal GCS call): %s", filename);
            return;
        }
        try {
            BlobId blobId = BlobId.of(gcsBucketName, filename);
            boolean deleted = storage.delete(blobId);
            if (deleted) {
                LOG.infof("Successfully deleted image file from GCS (internal call): %s", filename);
            } else {
                LOG.warnf("Image file not found for deletion in GCS (internal call): %s", filename);
            }
        } catch (StorageException e) {
            LOG.errorf(e, "Failed to delete image file from GCS (internal call) %s", filename);
        }
    }

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
            String originalFileName = fileUpload.fileName();
            String extension = "";
            int i = originalFileName.lastIndexOf('.');
            if (i > 0) {
                extension = originalFileName.substring(i);
            }
            String newFileName = UUID.randomUUID().toString() + extension;
            String contentType = fileUpload.contentType();
            if (contentType == null || contentType.isEmpty()) {
                // Try to infer content type if not provided, or default to a common one
                contentType = Files.probeContentType(fileUpload.uploadedFile());
                if (contentType == null) {
                    contentType = "application/octet-stream"; // Default fallback
                }
            }

            // Create BlobInfo for the GCS object
            BlobId blobId = BlobId.of(gcsBucketName, newFileName);
            BlobInfo blobInfo = BlobInfo.newBuilder(blobId)
                    .setContentType(contentType)
                    .build();

            // Upload the file to GCS
            try (InputStream is = Files.newInputStream(fileUpload.uploadedFile())) {
                Blob blob = storage.create(blobInfo, is);
                LOG.infof("Successfully uploaded image to GCS: gs://%s/%s", gcsBucketName, newFileName);

                // Construct the URL to return to the frontend.
                String imageUrl = String.format("https://storage.googleapis.com/%s/%s", gcsBucketName, newFileName);

                return Response.ok(
                        Map.of("url", imageUrl, "name", newFileName)
                ).build();
            }
        } catch (StorageException e) {
            LOG.errorf(e, "Failed to upload image to GCS: %s", e.getMessage());
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity("Failed to upload image to cloud storage.")
                    .build();
        } catch (IOException e) {
            LOG.error("Failed to read uploaded file or process image", e);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity("Failed to process image file.")
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
        LOG.info("Attempting to delete image from GCS: " + filename);
        Principal userPrincipal = securityContext.getUserPrincipal();
        if (userPrincipal == null || !securityContext.isUserInRole("admin")) {
            LOG.warnf(
                    "Unauthorized attempt to delete image %s by user %s",
                    filename,
                    (userPrincipal != null ? userPrincipal.getName() : "anonymous/unauthenticated")
            );
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity(Map.of("message", "User not authorized to delete images."))
                    .build();
        }

        if (filename == null || filename.trim().isEmpty() || filename.contains("..") || filename.contains("/")) {
            LOG.warnf("Attempt to delete invalid filename for GCS: %s", filename);
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Invalid filename provided."))
                    .build();
        }

        try {
            BlobId blobId = BlobId.of(gcsBucketName, filename);
            boolean deleted = storage.delete(blobId);

            if (deleted) {
                LOG.infof("Successfully deleted image from GCS: %s", filename);
                return Response.noContent().build(); // 204 No Content
            } else {
                LOG.warnf("Image not found in GCS, could not delete: %s", filename);
                return Response.status(Response.Status.NOT_FOUND)
                        .entity(Map.of("message", "Image not found in cloud storage."))
                        .build();
            }
        } catch (StorageException e) {
            LOG.errorf(e, "Failed to delete image %s from GCS", filename);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(Map.of("message", "Failed to delete image from cloud storage due to an error."))
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
        String authorName = "Default Author Name"; // Placeholder
        String authorTitle = "Default Author Title"; // Placeholder

        try {
            Post newPost = postService.createPost(
                    postRequest.getTitle(),
                    postRequest.getContent(),
                    postRequest.getExcerpt(),
                    postRequest.getCategory(),
                    authorId,
                    authorName,
                    authorTitle,
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
            String errorId = java.util.UUID.randomUUID().toString();
            LOG.error("Error ID: " + errorId, e);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity("Failed to create post. Error ID: " + errorId)
                    .build();
        }
    }

    @PUT
    @Path("/posts")
    public Response updatePost(
            @Context SecurityContext securityContext,
            Post postData
    ) {
        Principal userPrincipal = securityContext.getUserPrincipal();
        if (userPrincipal == null) {
            LOG.warn(
                    "User principal not found in security context for updatePost."
            );
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity("User principal not found.")
                    .build();
        }
        if (!securityContext.isUserInRole("admin")) {
            LOG.warnf(
                    "User %s does not have admin privileges for updatePost.",
                    userPrincipal.getName()
            );
            return Response.status(Response.Status.FORBIDDEN)
                    .entity(Map.of("message", "User does not have admin privileges."))
                    .build();
        }

        LOG.info("Attempting to update post: " + postData.getId());

        if (postData.getId() == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Post ID is required for update."))
                    .build();
        }

        try {
            // 1. Retrieve the OLD post state from the database
            Optional<Post> oldPostOptional = postService.getPostById(postData.getId());
            if (oldPostOptional.isEmpty()) {
                return Response.status(Response.Status.NOT_FOUND)
                        .entity(Map.of("message", "Post not found for update."))
                        .build();
            }
            Post oldPost = oldPostOptional.get();

            // 2. Perform the update in the database
            Post updatedPost = postService.updatePost(postData);

            if (updatedPost == null) {
                // This indicates a problem in the service layer (e.g., post not found by ID despite initial check)
                return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                        .entity(Map.of("message", "Post update failed in service layer."))
                        .build();
            }

            // 3. Compare old vs. new image URLs and delete orphaned images from GCS

            // --- Featured Image Cleanup ---
            String oldFeaturedImageUrl = oldPost.getImageUrl();
            String newFeaturedImageUrl = updatedPost.getImageUrl();

            // Check if old image was managed by us (GCS bucket)
            boolean oldFeaturedImageWasManaged = oldFeaturedImageUrl != null &&
                    oldFeaturedImageUrl.startsWith(String.format("https://storage.googleapis.com/%s/", gcsBucketName));

            // If the old image was managed AND it's either removed or changed to a different URL
            if (oldFeaturedImageWasManaged &&
                    (newFeaturedImageUrl == null || !newFeaturedImageUrl.equals(oldFeaturedImageUrl))) {
                LOG.infof("Featured image changed/removed for post %s. Deleting old image: %s", oldPost.getId(), oldFeaturedImageUrl);
                String filenameToDelete = extractFilenameFromGCSUrl(oldFeaturedImageUrl);
                if (filenameToDelete != null) {
                    deleteSingleImageFile(filenameToDelete);
                }
            }

            // --- Content Images Cleanup ---
            Set<String> oldContentImageUrls = extractGCSUrlsFromContent(oldPost.getContent());
            Set<String> newContentImageUrls = extractGCSUrlsFromContent(updatedPost.getContent());

            // Find images present in old content but NOT in new content
            Set<String> imagesToDeleteFromContent = new HashSet<>(oldContentImageUrls);
            imagesToDeleteFromContent.removeAll(newContentImageUrls);

            for (String imageUrlToDelete : imagesToDeleteFromContent) {
                LOG.infof("Content image removed from post %s. Deleting: %s", oldPost.getId(), imageUrlToDelete);
                String filenameToDelete = extractFilenameFromGCSUrl(imageUrlToDelete);
                if (filenameToDelete != null) {
                    deleteSingleImageFile(filenameToDelete);
                }
            }

            // Return the updated post
            return Response.ok(enrichPostForFrontend(updatedPost)).build();

        } catch (IllegalArgumentException e) {
            LOG.errorf(e, "Invalid arguments for updating post %s: %s", postData.getId(), e.getMessage());
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Invalid post data: " + e.getMessage()))
                    .build();
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

    // Helper method to extract all GCS image URLs from the editor's content JSON
    private Set<String> extractGCSUrlsFromContent(Map<String, Object> content) throws JsonProcessingException {
        Set<String> urls = new HashSet<>();
        if (content != null && content.containsKey("blocks") && content.get("blocks") instanceof List) {
            @SuppressWarnings("unchecked")
            List<Map<String, Object>> blocks = (List<Map<String, Object>>) content.get("blocks");
            for (Map<String, Object> block : blocks) {
                if ("image".equals(block.get("type"))) {
                    Map<String, Object> data = (Map<String, Object>) block.get("data");
                    if (data != null && data.get("file") instanceof Map) {
                        Map<String, Object> fileData = (Map<String, Object>) data.get("file");
                        if (fileData != null && fileData.get("url") instanceof String) {
                            String imageUrl = (String) fileData.get("url");
                            // Ensure it's a GCS URL from OUR bucket before adding to set
                            if (imageUrl.startsWith(String.format("https://storage.googleapis.com/%s/", gcsBucketName))) {
                                urls.add(imageUrl);
                            }
                        }
                    }
                }
            }
        }
        return urls;
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

        try {
            // 1. Fetch the post to get its imageUrl and content BEFORE deleting from DB
            Optional<Post> postOptional = postService.getPostById(id);
            if (postOptional.isEmpty()) {
                return Response.status(Response.Status.NOT_FOUND)
                        .entity(Map.of("message", "Post not found."))
                        .build();
            }
            Post postToDelete = postOptional.get();

            // 2. Attempt to delete the featured image if it's a managed one
            String featuredImageUrl = postToDelete.getImageUrl();
            if (featuredImageUrl != null && featuredImageUrl.startsWith(String.format("https://storage.googleapis.com/%s/", gcsBucketName))) {
                String featuredImageFilename = extractFilenameFromGCSUrl(featuredImageUrl);
                if (featuredImageFilename != null) {
                    LOG.infof("Attempting to delete featured image: %s for post %s", featuredImageFilename, id);
                    deleteSingleImageFile(featuredImageFilename);
                }
            }

            // 3. Attempt to delete images from the post's content
            if (postToDelete.getContent() != null) {
                try {
                    Set<String> contentImageUrls = extractGCSUrlsFromContent(postToDelete.getContent());
                    for (String contentImageUrl : contentImageUrls) {
                        String contentImageFilename = extractFilenameFromGCSUrl(contentImageUrl);
                        if (contentImageFilename != null) {
                            LOG.infof("Attempting to delete content image: %s for post %s", contentImageFilename, id);
                            deleteSingleImageFile(contentImageFilename);
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
            Comment updatedComment = commentService.updateComment(commentId, request.getContent(), requestingUserId);
            if (updatedComment == null) {
                return Response.status(Response.Status.NOT_FOUND)
                        .entity(Map.of("message", "Comment not found or user not authorized.")).build();
            }
            return Response.ok(enrichCommentForFrontend(updatedComment)).build();
        } catch (NotFoundException e) {
            LOG.warnf("UpdateComment: Comment not found %s. Error: %s", commentId, e.getMessage());
            return Response.status(Response.Status.NOT_FOUND).entity(Map.of("message", e.getMessage())).build();
        } catch (ForbiddenException e) {
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
            @PathParam("postId") UUID postId,
            @PathParam("commentId") UUID commentId) {

        if (securityContext == null || securityContext.getUserPrincipal() == null) {
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity(Map.of("message", "User not authenticated.")).build();
        }
        String requestingUserId = securityContext.getUserPrincipal().getName();

        try {
            boolean deleted = commentService.deleteComment(commentId, requestingUserId);
            if (deleted) {
                return Response.noContent().build();
            } else {
                return Response.status(Response.Status.NOT_FOUND)
                        .entity(Map.of("message", "Comment not found or user not authorized to delete.")).build();
            }
        } catch (NotFoundException e) {
            LOG.warnf("DeleteComment: Comment not found %s. Error: %s", commentId, e.getMessage());
            return Response.status(Response.Status.NOT_FOUND).entity(Map.of("message", e.getMessage())).build();
        } catch (ForbiddenException e) {
            LOG.warnf("DeleteComment: User %s forbidden to delete comment %s. Error: %s", requestingUserId, commentId, e.getMessage());
            return Response.status(Response.Status.FORBIDDEN).entity(Map.of("message", e.getMessage())).build();
        } catch (IllegalStateException e) {
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

    private Map<String, Object> enrichPostForFrontend(Post post) {
        Map<String, Object> enrichedPost = new HashMap<>();
        enrichedPost.put(
                "id",
                post.getId() != null ? post.getId().toString() : null
        );
        enrichedPost.put("title", post.getTitle());
        enrichedPost.put("content", post.getContent());
        enrichedPost.put("slug", post.getSlug());

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
        Map<String, Object> enrichedComment = new HashMap<>();
        enrichedComment.put("id", comment.getId());
        enrichedComment.put("content", comment.getContent());
        enrichedComment.put("createdAt", comment.getCreatedAt().toString());
        Map<String, String> author = new HashMap<>();
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