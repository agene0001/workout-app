package org.backend.blog.config; // Ensure this matches your actual package

import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import java.io.InputStream;
import java.io.IOException;
import org.eclipse.microprofile.config.inject.ConfigProperty; // Don't forget this import

@ApplicationScoped
public class FirebaseInitializer {

    // Inject the Firebase Project ID from application.properties or env var (FIREBASE_PROJECT_ID)
    @ConfigProperty(name = "firebase.project-id")
    String firebaseProjectId;

    void onStart(@Observes StartupEvent ev) {
        System.out.println("Initializing Firebase Admin SDK..."); // Using System.out for quick debugging in logs

        if (firebaseProjectId == null || firebaseProjectId.trim().isEmpty()) {
            System.err.println("Firebase project ID is not configured. Please set 'firebase.project-id' property or FIREBASE_PROJECT_ID environment variable.");
            // Throwing a runtime exception here will prevent the application from starting if misconfigured.
            throw new RuntimeException("Firebase project ID is missing for Firebase Admin SDK initialization.");
        }

        try {
            if (FirebaseApp.getApps().isEmpty()) {
                FirebaseOptions options;
                InputStream serviceAccountStream = FirebaseInitializer.class.getResourceAsStream("/service-account-key.json");

                if (serviceAccountStream != null) {
                    System.out.println("Found service-account-key.json in resources. Initializing Firebase with explicit credentials.");
                    try {
                        options = FirebaseOptions.builder()
                                .setCredentials(GoogleCredentials.fromStream(serviceAccountStream))
                                .setProjectId(firebaseProjectId) // <--- ADDED: Explicitly set Project ID
                                .build();
                    } finally {
                        try {
                            serviceAccountStream.close();
                        } catch (IOException e) {
                            System.err.println("Error closing service account stream: " + e.getMessage());
                        }
                    }
                } else {
                    System.out.println("service-account-key.json not found in resources. Attempting to initialize Firebase with Application Default Credentials.");
                    options = FirebaseOptions.builder()
                            .setCredentials(GoogleCredentials.getApplicationDefault())
                            .setProjectId(firebaseProjectId) // <--- ADDED: Explicitly set Project ID for ADC fallback
                            .build();
                }
                FirebaseApp.initializeApp(options);
                System.out.println("Firebase Admin SDK Initialized successfully for project: " + firebaseProjectId);
            } else {
                System.out.println("Firebase Admin SDK already initialized.");
            }
        } catch (Exception e) {
            System.err.println("Critical error initializing Firebase Admin SDK: " + e.getMessage());
            e.printStackTrace();
            throw new RuntimeException("Fatal error initializing Firebase Admin SDK", e);
        }
    }
}