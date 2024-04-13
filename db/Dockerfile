# Use the official MySQL image as base
FROM mysql:latest

# Environment variables
ENV MYSQL_ROOT_PASSWORD=Rabin@123
ENV MYSQL_DATABASE=file_storage_db
ENV MYSQL_USER=rabin
ENV MYSQL_PASSWORD=Rabin@123

# Copy init script to initialize database
COPY init.sql /docker-entrypoint-initdb.d/

# Expose port
EXPOSE 3306