package org.backend.blog.routes;

import io.quarkus.vertx.web.Route;
import io.quarkus.vertx.web.RoutingExchange; // Alternative for RoutingContext if preferred
import io.vertx.core.http.HttpMethod;
import io.vertx.ext.web.RoutingContext;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.jboss.logging.Logger;
import org.backend.common.ApiPaths; // Assuming ApiPaths.BLOG is /api/v1/blog

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static io.quarkus.vertx.web.Route.HttpMethod.GET;

@ApplicationScoped
public class StaticContentRoutes {

    private static final Logger LOG = Logger.getLogger(StaticContentRoutes.class);

    @Inject
    @ConfigProperty(name = "app.upload.dir")
    String uploadDir;

    // Route to serve uploaded files
    // It will match URLs like /api/v1/blog/files/some-image-name.jpg
    @Route(path = ApiPaths.BLOG + "/uploaded/images/:filename", methods = GET)
    void serveUploadedFile(RoutingContext rc) {
        String filename = rc.request().getParam("filename");

        if (filename == null || filename.trim().isEmpty() || filename.contains("..")) {
            LOG.warnf("Attempt to access invalid filename via reactive route: %s", filename);
            rc.response().setStatusCode(400).end("Invalid filename.");
            return;
        }

        Path targetDir = Paths.get(uploadDir);
        Path filePath = targetDir.resolve(filename).normalize(); // normalize() for path traversal protection

        LOG.info("Reactive route attempting to serve file: " + filePath.toAbsolutePath().toString());

        // Security check: Ensure the resolved path is still within the intended upload directory
        if (!filePath.toAbsolutePath().startsWith(targetDir.toAbsolutePath())) {
            LOG.warnf("Attempt to access file outside of upload directory via reactive route: %s (resolved to %s)", filename, filePath.toAbsolutePath().toString());
            rc.response().setStatusCode(403).end("Access to the requested file path is forbidden.");
            return;
        }

        if (!Files.exists(filePath) || !Files.isRegularFile(filePath)) {
            LOG.warn("File not found or is not a regular file via reactive route at: " + filePath.toAbsolutePath().toString());
            rc.response().setStatusCode(404).end("File not found.");
            return;
        }

        // Vert.x sendFile handles Content-Type detection and efficient streaming
        rc.response().sendFile(filePath.toAbsolutePath().toString(), sendFileResult -> {
            if (sendFileResult.succeeded()) {
                LOG.info("Successfully served file: " + filename);
            } else {
                LOG.error("Failed to send file: " + filename, sendFileResult.cause());
                if (!rc.response().ended()) {
                    rc.response().setStatusCode(500).end("Failed to serve file.");
                }
            }
        });
    }
}
