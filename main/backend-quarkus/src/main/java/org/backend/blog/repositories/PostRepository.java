package org.backend.blog.repositories;

import io.quarkus.hibernate.orm.panache.PanacheRepositoryBase;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;
import java.util.UUID;
import org.backend.blog.model.Comment;
import org.backend.blog.model.Post;

@ApplicationScoped
public class PostRepository implements PanacheRepositoryBase<Post, UUID> {

    public List<Post> findByAuthor(String authorId) {
        return list("authorId", authorId);
    }
    public List<Post> findBySlug(String slug) {
        return list("slug", slug);
    }

    public List<Post> searchByTitle(String keyword) {
        return list("lower(title) like ?1", "%" + keyword.toLowerCase() + "%");
    }

    public boolean deletePostById(UUID id) {
        // This method wraps the provided delete functionality for clarity.
        return deleteById(id);
    }
}
