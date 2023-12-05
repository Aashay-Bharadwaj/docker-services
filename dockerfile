# Use the official MySQL 5.7 image as the base image
FROM mysql:5.7

# Set environment variables for MySQL configuration
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=videos

# Create a directory for custom initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy the MySQL initialization scripts to the container
COPY ./mysql-init/ /docker-entrypoint-initdb.d/

# Expose the default MySQL port
EXPOSE 3306

# Define a volume for persistent MySQL data
VOLUME /var/lib/mysql
