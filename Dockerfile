# Stage 1: Build the Spring Boot application
FROM maven:3.8.6-openjdk-18 AS backend-builder
WORKDIR /app/backend-spring

# Copy pom.xml and source code for Spring Boot
COPY ./main/backend-spring ./
  # Adjust path based on actual structure

# Install dependencies and build the Spring Boot project
RUN mvn clean install -DskipTests


# Set environment variables for Spring Boot
ENV SPRING_DATASOURCE_URL=jdbc:mysql://mysql-db:3306/automation
ENV SPRING_DATASOURCE_USERNAME=root
ENV SPRING_DATASOURCE_PASSWORD=LexLuthern246!!??
ENV SERVER_PORT=8081

# Start the Spring Boot application
ENTRYPOINT ["java", "-jar", "/app/backend-spring/target/backend-spring-0.0.1-SNAPSHOT.jar"]
# Stage 2: Build the React frontend
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

FROM python:3.9 as api-builder

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY main/python/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader punkt_tab

# Copy the entire python directory
COPY main/python/ .

# Print directory structure for debugging
#RUN ls -la
#RUN ls -la data/

# Environment variables
ENV DOCKER=true
ENV PORT=8082
ENV PYTHONUNBUFFERED=1

EXPOSE 8082

# Run the application (removed the WORKDIR app command)
CMD ["python", "recommenderRoute.py"]

#WORKDIR app
# Stage 4: Final image for Spring Boot service

# Expose Spring Boot port


# Stage 5: Serving the React app using npm start
FROM node:16 AS frontend-final
WORKDIR /app/frontend

# Copy the necessary files for frontend
COPY main/Frontend/package*.json ./
COPY main/Frontend/ ./

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
