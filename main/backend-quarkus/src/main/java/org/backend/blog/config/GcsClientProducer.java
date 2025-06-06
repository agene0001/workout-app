package org.backend.blog.config;

import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;
import org.eclipse.microprofile.config.inject.ConfigProperty;

@ApplicationScoped
public class GcsClientProducer {

    @ConfigProperty(name = "quarkus.google.cloud.project-id", defaultValue = "")
    String projectId;

    @Produces
    @ApplicationScoped
    public Storage storage() {
        StorageOptions.Builder optionsBuilder = StorageOptions.newBuilder();
        if (!projectId.isEmpty()) {
            optionsBuilder.setProjectId(projectId);
        }
        // Quarkus handles authentication for GCS usually via service account from env, etc.
        // If running locally, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
        return optionsBuilder.build().getService();
    }
}