package org.backend.blog.security;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseToken;
import io.quarkus.runtime.configuration.ConfigUtils; // Correct import for ConfigUtils
import jakarta.annotation.Priority;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.Priorities;
import jakarta.ws.rs.container.ContainerRequestContext;
import jakarta.ws.rs.container.ContainerRequestFilter;
import jakarta.ws.rs.core.HttpHeaders;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.SecurityContext;
import jakarta.ws.rs.ext.Provider;
import org.backend.common.ApiPaths;
import org.jboss.logging.Logger;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.Principal;
import java.util.Base64;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Provider
@ApplicationScoped
@Priority(Priorities.AUTHENTICATION)
public class FirebaseAuthFilter implements ContainerRequestFilter {

    private static final Logger LOG = Logger.getLogger(FirebaseAuthFilter.class);
    private static final String BEARER_PREFIX = "Bearer ";
    private static final String PROTECTED_POSTS_PATH = ApiPaths.BLOG + "/posts";
    private static final String PROTECTED_IMGS_PATH = ApiPaths.BLOG + "/images";

    // No longer need to inject ProfileManager

    @Inject // Inject ObjectMapper for JSON parsing
    ObjectMapper objectMapper;


    @Override
    public void filter(ContainerRequestContext requestContext) throws IOException {
        List<String> activeProfiles = ConfigUtils.getProfiles(); // Get active profiles

        LOG.infov("FirebaseAuthFilter invoked for path: {0}, method: {1}. Active profiles: {2}",
                requestContext.getUriInfo().getPath(), requestContext.getMethod(), activeProfiles);

        String path = requestContext.getUriInfo().getPath();
        String method = requestContext.getMethod();

        if (isPathProtected(path, method)) {
            LOG.infov("Path {0} with method {1} is PROTECTED. Proceeding with authentication.", path, method);

            String authHeader = requestContext.getHeaderString(HttpHeaders.AUTHORIZATION);
            if (authHeader == null || !authHeader.startsWith(BEARER_PREFIX)) {
                LOG.warn("Authorization header missing or does not start with Bearer.");
                abortWithUnauthorized(requestContext, "Authorization header with Bearer token is required.");
                return;
            }

            String idTokenString = authHeader.substring(BEARER_PREFIX.length());

            try {
                String uid;
                boolean isAdmin;

                if (activeProfiles.contains("dev")) { // Check if "dev" is in the list of active profiles
                    LOG.info("DEV profile active: Attempting to parse token assuming emulator origin.");
                    // For dev profile (emulator), decode token without signature verification
                    Map<String, Object> claims = decodeEmulatorToken(idTokenString);
                    uid = (String) Optional.ofNullable(claims.get("user_id")).orElse(claims.get("sub"));
                    isAdmin = Boolean.TRUE.equals(claims.get("admin"));
                    if (uid == null) {
                        LOG.error("DEV profile: UID (user_id or sub) not found in token claims.");
                        abortWithUnauthorized(requestContext, "Invalid token: UID not found.");
                        return;
                    }
                    LOG.infov("DEV profile: Token parsed. UID: {0}, isAdmin: {1}", uid, isAdmin);
                } else {
                    LOG.info("Non-DEV profile(s) active: Verifying Firebase ID token using Admin SDK.");
                    FirebaseToken decodedToken = FirebaseAuth.getInstance().verifyIdToken(idTokenString);
                    uid = decodedToken.getUid();
                    Map<String, Object> claims = decodedToken.getClaims();
                    isAdmin = Boolean.TRUE.equals(claims.get("admin")); // Assuming 'admin' is a custom claim
                    LOG.infov("Prod profile(s): Token verified. UID: {0}, isAdmin: {1}", uid, isAdmin);
                }

                setSecurityContext(requestContext, uid, isAdmin);
                LOG.info("Custom SecurityContext set.");

            } catch (Exception e) {
                LOG.error("Token processing failed: " + e.getMessage(), e);
                abortWithUnauthorized(requestContext, "Invalid token: " + e.getMessage());
            }
        } else {
            LOG.infov("Path {0} with method {1} is PUBLIC or not matching filter criteria. Passing through.", path, method);
        }
    }

    private boolean isPathProtected(String path, String method) {
        // Example: Only protect /api/v1/blog/posts for POST, PUT, DELETE
        // and /api/v1/blog/posts/{postId}/comments for POST
        if (path.startsWith(PROTECTED_POSTS_PATH) && ("POST".equals(method) || "PUT".equals(method) || "DELETE".equals(method))) {
            return true;
        }
        if (path.startsWith(PROTECTED_IMGS_PATH) && ("POST".equals(method) || "PUT".equals(method) || "DELETE".equals(method))) {
            return true;
        }
        // Protect adding comments: POST /api/v1/blog/posts/{postId}/comments
        // Regex to match comment paths like /api/v1/blog/posts/some-uuid/comments
        if (path.matches(ApiPaths.BLOG + "/posts/[^/]+/comments") && "POST".equals(method)) {
            return true;
        }

        // Add other protected paths and methods here
        return false;
    }

    private Map<String, Object> decodeEmulatorToken(String token) throws IOException {
        String[] parts = token.split("\\.");
        if (parts.length < 2) { // Emulator tokens might not have a signature part, or it might be empty. We need at least header and payload.
            throw new IllegalArgumentException("Invalid JWT token format (emulator). Expected at least 2 parts.");
        }
        String payload = new String(Base64.getUrlDecoder().decode(parts[1]), StandardCharsets.UTF_8);
        return objectMapper.readValue(payload, new TypeReference<Map<String, Object>>() {});
    }

    private void setSecurityContext(ContainerRequestContext requestContext, String uid, boolean isAdmin) {
        final SecurityContext originalSecurityContext = requestContext.getSecurityContext();
        requestContext.setSecurityContext(new SecurityContext() {
            @Override
            public Principal getUserPrincipal() {
                return () -> uid;
            }

            @Override
            public boolean isUserInRole(String role) {
                if ("admin".equalsIgnoreCase(role)) {
                    return isAdmin;
                }
                return false;
            }

            @Override
            public boolean isSecure() {
                return originalSecurityContext.isSecure();
            }

            @Override
            public String getAuthenticationScheme() {
                return "FIREBASE_JWT";
            }
        });
    }

    private void abortWithUnauthorized(ContainerRequestContext requestContext, String message) {
        requestContext.abortWith(Response.status(Response.Status.UNAUTHORIZED)
                .entity(Map.of("message", message)).build());
    }
}