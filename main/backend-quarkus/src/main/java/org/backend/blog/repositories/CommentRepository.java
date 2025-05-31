package org.backend.blog.repositories;


import io.quarkus.hibernate.orm.panache.PanacheRepositoryBase;
import jakarta.enterprise.context.ApplicationScoped;
import org.backend.blog.model.Comment;
import org.backend.blog.model.Post;

import java.util.List;
import java.util.UUID;

@ApplicationScoped
public class CommentRepository implements PanacheRepositoryBase<Comment, UUID> {

    public List<Comment> findByPost(Post post) {
        return list("post", post);
    }
}

