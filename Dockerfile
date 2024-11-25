# Stage 1: Build the Spring Boot application
FROM --platform=linux/arm64 maven:3.8-openjdk-17 AS backend-builder

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
CMD java \
    -Dio.netty.tryReflectionSetAccessible=true \
    -Dlog4j.logLevel=ERROR \
    -Djava.security.manager \
    -Djava.security.manager=allow \
    -Djava.util.logging.config.file=/app/backend-spring/logging.properties \
    --add-exports=java.base/sun.nio.ch=ALL-UNNAMED \
    --add-exports=java.base/sun.security.action=ALL-UNNAMED \
    --add-exports=java.base/sun.util.calendar=ALL-UNNAMED \
    --add-exports=java.management/sun.management=ALL-UNNAMED \
    --add-opens=java.base/java.nio=ALL-UNNAMED \
    --add-opens=java.base/sun.nio.ch=ALL-UNNAMED \
    --add-opens=java.base/java.util=ALL-UNNAMED \
    --add-opens=java.base/java.util.concurrent=ALL-UNNAMED \
    --add-opens=java.base/java.lang=ALL-UNNAMED \
    --add-opens=java.base/java.lang.invoke=ALL-UNNAMED \
    --add-opens=java.base/java.io=ALL-UNNAMED \
    --add-opens=java.base/java.security=ALL-UNNAMED \
    --add-opens=java.base/java.lang.module=ALL-UNNAMED \
    --add-opens=java.base/jdk.internal.loader=ALL-UNNAMED \
    --add-opens=java.base/jdk.internal.ref=ALL-UNNAMED \
    --add-opens=java.base/jdk.internal.reflect=ALL-UNNAMED \
    --add-opens=java.base/jdk.internal.math=ALL-UNNAMED \
    --add-opens=java.base/jdk.internal.module=ALL-UNNAMED \
    --add-opens=java.base/jdk.internal.util.jar=ALL-UNNAMED \
    --add-opens=java.base/java.lang.constant=ALL-UNNAMED \
    --add-opens=java.base/java.lang.invoke=ALL-UNNAMED \
    --add-opens=java.base/java.util.concurrent.locks=ALL-UNNAMED \
    --add-exports=java.base/sun.reflect.generics.reflectiveObjects=ALL-UNNAMED \
    --add-opens=java.base/java.nio=ALL-UNNAMED \
    --add-opens=java.base/java.nio.charset=ALL-UNNAMED \
    --add-opens=java.base/java.nio.channels=ALL-UNNAMED \
    --add-opens=java.base/java.nio.file=ALL-UNNAMED \
    -jar /app/backend-spring/target/workout-app-spring-0.0.1-SNAPSHOT.jar


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

#FROM python:3.9 as api-builder
#
## Set working directory
#WORKDIR /app
#
## Copy requirements and install dependencies
#COPY main/python/requirements.txt .
#RUN pip install --upgrade pip && pip install -r requirements.txt
#RUN python -m nltk.downloader punkt
#RUN python -m nltk.downloader punkt_tab
#
## Copy the entire python directory
#COPY main/python/ .
#
## Print directory structure for debugging
##RUN ls -la
##RUN ls -la data/
#
## Environment variables
##ENV DOCKER=true
#ENV PORT=8082
#ENV PYTHONUNBUFFERED=1
#
#EXPOSE 8082
#
## Run the application (removed the WORKDIR app command)
#CMD ["python", "recommenderRoute.py"]

#WORKDIR app
# Stage 4: Final image for Spring Boot service

# Expose Spring Boot port


# Stage 5: Serving the React app using npm start
FROM --platform=linux/arm64 node:16 AS frontend-final
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
