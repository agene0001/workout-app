package org.backend.blog.repositories;


import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import org.backend.blog.model.Comment;
import org.backend.blog.model.Post;

import java.util.List;

@ApplicationScoped
public class CommentRepository implements PanacheRepository<Comment> {

    public List<Comment> findByPost(Post post) {
        return list("post", post);
    }
}

