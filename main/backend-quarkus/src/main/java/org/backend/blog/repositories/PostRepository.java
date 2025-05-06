package org.backend.blog.repositories;

import io.quarkus.hibernate.orm.panache.PanacheRepositoryBase;
import jakarta.enterprise.context.ApplicationScoped;
import org.backend.blog.model.Comment;
import org.backend.blog.model.Post;

import java.util.List;
import java.util.UUID;

@ApplicationScoped
public class PostRepository implements PanacheRepositoryBase<Post,UUID> {

    public List<Post> findByAuthor(String authorId) {
        return list("authorId", authorId);
    }

    public List<Post> searchByTitle(String keyword) {
        return list("lower(title) like ?1", "%" + keyword.toLowerCase() + "%");
    }

}
