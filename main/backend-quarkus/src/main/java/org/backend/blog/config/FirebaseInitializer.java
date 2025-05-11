package org.backend.blog.config;


import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import java.io.InputStream;

@ApplicationScoped
public class FirebaseInitializer {

    void onStart(@Observes StartupEvent ev) {
        try {
            if (FirebaseApp.getApps().isEmpty()) { // Check if already initialized
                InputStream serviceAccount = FirebaseInitializer.class.getResourceAsStream("/service-account-key.json");
                if (serviceAccount == null) {
                    throw new RuntimeException("Firebase service account key not found in resources.");
                }

                FirebaseOptions options = FirebaseOptions.builder()
                        .setCredentials(GoogleCredentials.fromStream(serviceAccount))
                        // .setDatabaseUrl("https://<DATABASE_NAME>.firebaseio.com") // If using Realtime DB
                        .build();

                FirebaseApp.initializeApp(options);
                System.out.println("Firebase Admin SDK Initialized");
            }
        } catch (Exception e) {
            throw new RuntimeException("Error initializing Firebase Admin SDK", e);
        }
    }
}

