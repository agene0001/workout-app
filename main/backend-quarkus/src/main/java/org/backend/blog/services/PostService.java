package org.backend.blog.services;


import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import org.backend.blog.model.Post;
import org.backend.blog.repositories.PostRepository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@ApplicationScoped
public class PostService {

    @Inject
    PostRepository postRepository;

    public List<Post> getAllPosts() {
        return postRepository.listAll();
    }

    public Optional<Post> getPostById(UUID id) {
        return postRepository.findByIdOptional(id);
    }

    @Transactional
    public Post createPost(String title, String content, String authorId) {
        Post post = new Post();
        post.setTitle(title);
        post.setContent(content);
        post.setAuthorId(authorId);
        post.setCreatedAt(Instant.now());
        post.setUpdatedAt(Instant.now());

        postRepository.persist(post);
        return post;
    }

    @Transactional
    public boolean updatePost(UUID id, String title, String content, String authorId) {
        Optional<Post> postOpt = postRepository.findByIdOptional(id);
        if (postOpt.isPresent() && postOpt.get().getAuthorId().equals(authorId)) {
            Post post = postOpt.get();
            post.setTitle(title);
            post.setContent(content);
            post.setUpdatedAt(Instant.now());
            return true;
        }
        return false;
    }

    @Transactional
    public boolean deletePost(UUID id, String authorId) {
        Optional<Post> postOpt = postRepository.findByIdOptional(id);
        if (postOpt.isPresent() && postOpt.get().getAuthorId().equals(authorId)) {
            postRepository.delete(postOpt.get());
            return true;
        }
        return false;
    }
}
