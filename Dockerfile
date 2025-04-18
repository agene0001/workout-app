# Stage 1: Build the Spring Boot application
FROM mysql:8.0 AS mysql-with-backup

COPY  ./backup.sql /docker-entrypoint-initdb.d/

# Expose the MySQL port
EXPOSE 3306

FROM --platform=linux/amd64 maven:3.8-openjdk-17 AS backend-builder

# Install Maven
WORKDIR /app/backend-spring

# Copy pom.xml and source code for Spring Boot

COPY main/backend-spring/libs /libs

# Copy pom.xml and source code for Spring Boot
COPY main/backend-spring ./

RUN mvn install:install-file \
  -Dfile=/libs/algs4.jar \
  -DgroupId=edu.princeton.cs \
  -DartifactId=algs4 \
  -Dversion=1.0 \
  -Dpackaging=jar

# Install dependencies and build the Spring Boot project
RUN mvn clean package -DskipTests


# Set environment variables for Spring Boot
#ENV SPRING_DATASOURCE_URL=jdbc:mysql://mysql-db:3306/automation
ENV SPRING_DATASOURCE_USERNAME=root
ENV SPRING_DATASOURCE_PASSWORD=LexLuthern246!!??
ENV SERVER_PORT=8081

# Start the Spring Boot application

# Stage 2: Use CMD for starting the Spring Boot application
# Stage 2: Use CMD for starting the Spring Boot application

# CMD with ALL required --add-opens arguments
CMD ["java", \
     "--add-opens=java.base/java.lang=ALL-UNNAMED", \
     "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED", \
     "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED", \
     "--add-opens=java.base/java.io=ALL-UNNAMED", \
     "--add-opens=java.base/java.net=ALL-UNNAMED", \
     "--add-opens=java.base/java.nio=ALL-UNNAMED", \
     "--add-opens=java.base/java.util=ALL-UNNAMED", \
     "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED", \
     # Exports might not strictly be needed but were in your POM, safer to include
     "--add-exports=java.base/java.util.concurrent.atomic=ALL-UNNAMED", \
     "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED", \
     "--add-exports=java.base/sun.nio.ch=ALL-UNNAMED", \
     "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED", \
     "--add-opens=java.base/sun.nio.cs=ALL-UNNAMED", \
     "--add-opens=java.base/sun.security.action=ALL-UNNAMED", \
     "--add-opens=java.base/sun.util.calendar=ALL-UNNAMED", \
     "-jar", \
     "target/backend-spring-0.0.1-SNAPSHOT.jar"]

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

#FROM --platform=linux/amd64 python:3.12 as api-builder
#
## Set working directory
#WORKDIR /app
#
## Copy requirements and install dependencies
#COPY main/python/requirements.txt .
#RUN pip install --upgrade pip && pip install -r requirements.txt
#RUN python -m spacy download en_core_web_sm
#
#
## Copy the entire python directory
#COPY main/python/ .
#
## Print directory structure for debugging
#RUN ls -la
#
## Environment variables
##ENV DOCKER=true
#ENV PORT=8082
#
#EXPOSE 8082
#
## Run the application (removed the WORKDIR app command)
#CMD ["python", "xtractServer.py"]

#WORKDIR app
# Stage 4: Final image for Spring Boot service


# Expose Spring Boot port


# Stage 5: Serving the React app using npm start
FROM --platform=linux/amd64 node:22 AS frontend-final
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
