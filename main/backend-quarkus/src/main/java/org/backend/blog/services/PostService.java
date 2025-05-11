package org.backend.blog.services;

import com.google.cloud.firestore.FieldValue;
import com.google.cloud.firestore.Firestore;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseToken;
import com.google.firebase.auth.UserRecord;
import com.google.firebase.cloud.FirestoreClient;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject; // Assuming you might inject other Quarkus beans
import jakarta.transaction.Transactional;
import jakarta.ws.rs.ForbiddenException;
import jakarta.ws.rs.NotFoundException;
import java.text.Normalizer;
import java.time.Instant;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ExecutionException;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import org.backend.blog.model.Post; // Your existing Post model
import org.backend.blog.repositories.PostRepository;
import org.jboss.logging.Logger;

@ApplicationScoped
public class PostService {

    @Inject // Inject PostRepository
    PostRepository postRepository;

    private static final Logger LOG = Logger.getLogger(PostService.class);
    // Dummy in-memory store for demonstration - replace with Firestore logic
    private final Map<UUID, Post> posts = new HashMap<>();

    // Utility for slugify (basic example)
    private static final Pattern NONLATIN = Pattern.compile("[^\\w-]");
    private static final Pattern WHITESPACE = Pattern.compile("[\\s]");
    private static final Pattern EDGESDHASHES = Pattern.compile("(^-|-$)");

    public static String slugify(String input) {
        if (input == null) return "";
        String nowhitespace = WHITESPACE.matcher(input).replaceAll("-");
        String normalized = Normalizer.normalize(
            nowhitespace,
            Normalizer.Form.NFD
        );
        String slug = NONLATIN.matcher(normalized).replaceAll("");
        slug = EDGESDHASHES.matcher(slug).replaceAll("");
        return slug.toLowerCase();
    }

    // This method signature matches your BlogResource's expectation for creating a post.
    // It now takes more details to construct the Firestore document.

    @Transactional
    public Post createPost(
        String title,
        Map<String, Object> content,
        String excerpt,
        String category,
        String authorId,
        String authorName,
        String authorTitle, // Added missing parameters from your previous version
        String imageUrl,
        Boolean featured,
        Integer readTime
    ) { // Corrected to use imageUrl
        // This was how you fetched authorName and authorTitle in your previous code.
        // String actualAuthorName = authorName; // Or fetch from DB/Auth
        // String actualAuthorTitle = authorTitle; // Or fetch from DB/Auth
        // try {
        //     UserRecord userRecord = FirebaseAuth.getInstance().getUser(authorId); // adminUid was authorId
        //     if (userRecord.getDisplayName() != null && !userRecord.getDisplayName().isEmpty()) {
        //         actualAuthorName = userRecord.getDisplayName();
        //     }
        // } catch (Exception e) {
        //     System.err.println("Error fetching user details for author: " + e.getMessage());
        // }

        Post newPost = new Post();
        newPost.setTitle(title);

        // Set the content directly as a Map.
        // If 'content' is null and you want to default to excerpt, you'd need to structure excerpt as a Map.
        // For example: Map.of("type", "paragraph", "text", excerpt)
        // For now, we'll just pass the content map as is.
        newPost.setContent(content);

        newPost.setExcerpt(excerpt);
        newPost.setCategory(category);
        newPost.setSlug(slugify(title));
        newPost.setAuthorId(authorId);
        newPost.setAuthorName(authorName); // Use the passed or fetched authorName
        newPost.setAuthorTitle(authorTitle); // Use the passed or fetched authorTitle
        newPost.setImageUrl(imageUrl); // Changed from 'image' to 'imageUrl'
        newPost.setFeatured(featured != null ? featured : false);
        newPost.setReadTime(readTime != null ? readTime : 5);
        newPost.setCreatedAt(Instant.now());
        newPost.setUpdatedAt(Instant.now());

        postRepository.persist(newPost);

        System.out.println(
            "Successfully added blog post '" +
            title +
            "' by " +
            authorId +
            ". New post ID: " +
            newPost.getId()
        );
        return newPost;
    }

    public List<Post> getAllPosts() {
        return postRepository.listAll();
    }

    public Optional<Post> getPostById(UUID id) {
        return postRepository.findByIdOptional(id);
    }
    public List<Post> getPostBySlug(String slug) {
        return postRepository.findBySlug(slug);
    }

    @Transactional
    public Post updatePost(Post post) {
        Post existingPost = postRepository
            .findByIdOptional(post.getId())
            .orElseThrow(() ->
                new NotFoundException("Post with id " + post.getId() + " not found")
            );

        // Update fields only if they are present in the DTO
        if (post.getTitle() != null) {
            existingPost.setTitle(post.getTitle());
            // Update slug when title changes
            existingPost.setSlug(slugify(post.getTitle()));
        }

        if (post.getContent() != null) {
            existingPost.setContent(post.getContent());
        }

        if (post.getExcerpt() != null) {
            existingPost.setExcerpt(post.getExcerpt());
        }

        if (post.getCategory() != null) {
            existingPost.setCategory(post.getCategory());
        }

        if (post.getAuthorName() != null) {
            existingPost.setAuthorName(post.getAuthorName());
        }

        if (post.getAuthorTitle() != null) {
            existingPost.setAuthorTitle(post.getAuthorTitle());
        }

        if (post.getImageUrl() != null) {
            existingPost.setImageUrl(post.getImageUrl());
        }

        if (post.isFeatured()) {
            existingPost.setFeatured(post.isFeatured()||existingPost.isFeatured());
        }

        if (post.getReadTime() != null) {
            existingPost.setReadTime(post.getReadTime());
        } else if (existingPost.getReadTime() == null) {
            // Set default read time if not set previously
            existingPost.setReadTime(5);
        }

        // Always update the updatedAt timestamp
        existingPost.setUpdatedAt(Instant.now());


        postRepository.persist(existingPost);
        LOG.info("Post with id " + post.getId() + " updated by user " + post.getAuthorId());
        return existingPost;
    }

    @Transactional
    public boolean deletePost(UUID id) {
        return postRepository
            .deletePostById(id);


    }
}
