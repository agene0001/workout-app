# Stage 1: Build the Spring Boot application
FROM postgres AS postgres-with-backup

COPY  ./backup.sql /docker-entrypoint-initdb.d/

# Expose the MySQL port
EXPOSE 5432

FROM gradle:8.7-jdk21 AS backend-builder

# Install Maven

# Use a non-root user provided by the Gradle image
USER gradle
WORKDIR /home/gradle/project

# Copy only Gradle wrapper and build scripts to cache dependencies
COPY --chown=gradle:gradle main/backend-quarkus/gradlew .
COPY --chown=gradle:gradle main/backend-quarkus/gradle/ gradle/
COPY --chown=gradle:gradle main/backend-quarkus/settings.gradle .
COPY --chown=gradle:gradle main/backend-quarkus/build.gradle .
COPY --chown=gradle:gradle main/backend-quarkus/gradle.properties .

# Pre-download dependencies
RUN ./gradlew --no-daemon dependencies

# Copy the rest of the source
COPY --chown=gradle:gradle main/backend-quarkus/src ./src
COPY --chown=gradle:gradle main/backend-quarkus/libs ./libs

# Build the Quarkus "legacy jar" layout (quarkus-app/)
RUN ./gradlew --no-daemon -i clean build -x test


# ----------------------------------
# Stage 2: Run on a minimal JVM image
# ----------------------------------
FROM registry.access.redhat.com/ubi8/openjdk-21-runtime:latest AS backend-quarkus

ENV JAVA_OPTIONS="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager"
# ENV JAVA_APP_JAR is not strictly needed when using fast-jar and the default runner script

WORKDIR /work/

# Copy the entire quarkus-app directory structure
COPY --from=backend-builder /home/gradle/project/build/quarkus-app ./quarkus-app

# Expose the port your Quarkus app uses (default is 8080, but you use 8081)
EXPOSE 8081

# Set the working directory to where quarkus-run.jar is located
WORKDIR /work/quarkus-app

# Run using the quarkus-run.jar which knows how to load the rest
CMD ["java", "-jar", "./quarkus-run.jar"]

#FROM node:16 AS frontend-builder
#WORKDIR /app/frontend
#
## Copy package files and install dependencies for React
#COPY main/Frontend/package*.json ./
#RUN npm install
#
## Copy the rest of the frontend files and build the frontend
#COPY main/Frontend/ ./
#RUN npm run build

FROM  python:3.12 as api-builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Set working directory
WORKDIR /app
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
# Copy requirements and install dependencies
#COPY main/python/requirements.txt .
#RUN pip install --upgrade pip && pip install -r requirements.txt

RUN uv venv

# Copy the entire python directory
COPY main/backend-flask/ .

# Print directory structure for debugging
RUN ls -la

# Environment variables
#ENV DOCKER=true
ENV PORT=8082

EXPOSE 8082

# Run the application (removed the WORKDIR app command)
CMD ["uv", "run", "gunicorn", "--workers", "4", "--bind", "0.0.0.0:8082", "xtractServer:app"]

#WORKDIR app
# Stage 4: Final image for Spring Boot service


# Expose Spring Boot port


# Stage 5: Serving the React app using npm start
FROM node:22 AS frontend-final
WORKDIR /app/frontend

# Copy the necessary files for frontend
COPY main/frontend-svelte/package*.json ./
COPY main/frontend-svelte/ ./

# Install dependencies for serving the frontend
RUN npm install
RUN npm run build

# Expose the port for the frontend
EXPOSE 8080

# Use npm start to serve the React app
CMD ["npm","run", "preview"]


# Stage 6: Final image for Python API service

# Copy the Python API files from the builder stage
#RUN --from=api-builder /app/python /app/python
#
## Expose the API port
#EXPOSE 8082
#
## Start the Python API
#CMD ["python3", "/app/python/recommenderRoute.py"]