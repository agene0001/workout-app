package org.backend.blog.config;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import java.io.InputStream;
import java.io.IOException; // Import IOException

@ApplicationScoped
public class FirebaseInitializer {

    void onStart(@Observes StartupEvent ev) {
        try {
            if (FirebaseApp.getApps().isEmpty()) { // Check if already initialized
                FirebaseOptions options;
                InputStream serviceAccountStream = FirebaseInitializer.class.getResourceAsStream("/service-account-key.json");

                if (serviceAccountStream != null) {
                    // Local development or environment where service-account-key.json is explicitly provided
                    System.out.println("Found service-account-key.json in resources. Initializing Firebase with explicit credentials.");
                    try {
                        options = FirebaseOptions.builder()
                                .setCredentials(GoogleCredentials.fromStream(serviceAccountStream))
                                // .setDatabaseUrl("https://<DATABASE_NAME>.firebaseio.com") // If using Realtime DB
                                .build();
                    } finally {
                        try {
                            serviceAccountStream.close(); // Always close the stream
                        } catch (IOException e) {
                            System.err.println("Error closing service account stream: " + e.getMessage());
                        }
                    }
                } else {
                    // GKE environment or any environment where service-account-key.json is NOT present
                    // Rely on Application Default Credentials (ADC)
                    // This typically means Workload Identity is configured in GKE.
                    System.out.println("service-account-key.json not found in resources. Attempting to initialize Firebase with Application Default Credentials.");
                    options = FirebaseOptions.builder()
                            .setCredentials(GoogleCredentials.getApplicationDefault())
                            // .setDatabaseUrl("https://<DATABASE_NAME>.firebaseio.com") // If using Realtime DB
                            // You might also need to set the projectId if ADC doesn't pick it up correctly
                            // .setProjectId("your-gcp-project-id") // Usually picked up by ADC
                            .build();
                }

                FirebaseApp.initializeApp(options);
                System.out.println("Firebase Admin SDK Initialized successfully.");
            } else {
                System.out.println("Firebase Admin SDK already initialized.");
            }
        } catch (Exception e) {
            // Log the detailed error
            System.err.println("Critical error initializing Firebase Admin SDK: " + e.getMessage());
            e.printStackTrace(); // Print stack trace for more details in logs
            // Decide if you want to re-throw or let the application continue (potentially in a degraded state)
            // For critical services like Firebase Admin, re-throwing is often appropriate.
            throw new RuntimeException("Fatal error initializing Firebase Admin SDK", e);
        }
    }
}