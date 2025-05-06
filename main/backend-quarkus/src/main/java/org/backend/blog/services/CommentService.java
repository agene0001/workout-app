package org.backend.blog.services;


import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import org.backend.blog.model.Comment;
import org.backend.blog.model.Post;
import org.backend.blog.repositories.CommentRepository;
import org.backend.blog.repositories.PostRepository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@ApplicationScoped
public class CommentService {

    @Inject
    CommentRepository commentRepository;

    @Inject
    PostRepository postRepository;

    public List<Comment> getCommentsForPost(UUID postId) {
        Optional<Post> postOpt = postRepository.findByIdOptional(postId);
        return postOpt.map(commentRepository::findByPost).orElse(List.of());
    }

    @Transactional
    public Comment addComment(UUID postId, String content, String authorId) {
        Post post = postRepository.findById(postId);
        if (post == null) {
            throw new IllegalArgumentException("Post not found");
        }

        Comment comment = new Comment();
        comment.setPost(post);
        comment.setContent(content);
        comment.setAuthorId(authorId);
        comment.setCreatedAt(Instant.now());

        commentRepository.persist(comment);
        return comment;
    }
}

