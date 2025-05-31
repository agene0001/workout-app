package org.backend.blog.services;


import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.ForbiddenException;
import jakarta.ws.rs.NotFoundException;
import org.backend.blog.model.Comment;
import org.backend.blog.model.Post;
import org.backend.blog.repositories.CommentRepository;
import org.backend.blog.repositories.PostRepository;
import org.jboss.logging.Logger;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@ApplicationScoped
public class CommentService {
    private static final Logger LOG = Logger.getLogger(CommentService.class);



    @Inject
    CommentRepository commentRepository;

    @Inject
    PostRepository postRepository;

    public List<Comment> getCommentsForPost(UUID postId) {
        Optional<Post> postOpt = postRepository.findByIdOptional(postId);
        return postOpt.map(commentRepository::findByPost).orElse(List.of());
    }

    // In CommentService.java
    @Transactional
    public Comment addComment(UUID postId, String content, String authorId, UUID parentCommentId) { // Add parentCommentId
        Post post = postRepository.findById(postId);
        if (post == null) {
            throw new IllegalArgumentException("Post not found with ID: " + postId);
        }

        Comment comment = new Comment();
        comment.setPost(post);
        comment.setContent(content);
        comment.setAuthorId(authorId);
        comment.setCreatedAt(Instant.now());

        if (parentCommentId != null) {
            Comment parentComment = commentRepository.findById(parentCommentId);
            if (parentComment == null) {
                // Decide on behavior: throw error, or create as top-level, or log warning.
                // For now, let's throw an error if parent is specified but not found.
                throw new IllegalArgumentException("Parent comment not found with ID: " + parentCommentId);
            }
            // Ensure the parent comment belongs to the same post (optional, but good practice)
            if (!parentComment.getPost().getId().equals(postId)) {
                throw new IllegalArgumentException("Parent comment does not belong to the specified post.");
            }
            comment.setParent(parentComment);
        }

        commentRepository.persist(comment);
        return comment;
    }

    public Comment updateComment(UUID commentId, String newContent, String requestingUserId) {

        Comment comment = commentRepository.findById(commentId);
        // ... find comment by commentId from your data store (e.g., PanacheEntity.findById(commentId))
        if (comment == null) {
            throw new NotFoundException("Comment not found with ID: " + commentId);
        }

        // Authorization: Check if the requesting user is the author
        // Optionally, allow admins to edit any comment
        // boolean isAdmin = checkUserRole(requestingUserId, "admin"); // Implement this if needed
        if (!comment.getAuthorId().equals(requestingUserId) /* && !isAdmin */ ) {
            throw new ForbiddenException("User not authorized to edit this comment.");
        }

        comment.setContent(newContent);
//        comment.setUpdatedAt(Instant.now()); // Assuming you have an updatedAt field
        // ... persist the updated comment (e.g., comment.persist())
        return comment;
    }

    public boolean deleteComment(UUID commentId, String requestingUserId /*, boolean isAdmin */) {
        Comment comment = commentRepository.findById(commentId);
        if (comment == null) {
            throw new NotFoundException("Comment not found with ID: " + commentId);
        }

        // Authorization
        if (!comment.getAuthorId().equals(requestingUserId) /* && !isAdmin */) {
            throw new ForbiddenException("User not authorized to delete this comment.");
        }

        // Business logic: e.g., handle replies.
        // Option 1: Prevent deletion if replies exist (unless admin override)
        // if (comment.getReplies() != null && !comment.getReplies().isEmpty() /* && !isAdmin */) {
        //    throw new IllegalStateException("Cannot delete comment with replies.");
        // }
        // Option 2: Cascade delete replies (often handled by @OneToMany(cascade = CascadeType.REMOVE) in JPA)
        // If manual cascade:
        // for (Comment reply : new ArrayList<>(comment.getReplies())) { // Iterate over a copy if modifying
        //     deleteComment(reply.getId(), requestingUserId, isAdmin); // Recursive call, ensure admin can bypass some checks
        // }

        // ... delete the comment from your data store (e.g., comment.delete())
        // return true if deletion was successful, otherwise false (or let exceptions bubble up)
        try {
            // Example: ((PanacheEntityBase)comment).delete();
            // For this example, assume deletion is successful if no exception
            LOG.infof("Comment %s deleted by user %s", commentId, requestingUserId);
            return true;
        } catch (Exception e) {
            LOG.errorf(e, "Failed to delete comment %s in service", commentId);
            return false; // Or rethrow as a service-specific exception
        }
    }
}

