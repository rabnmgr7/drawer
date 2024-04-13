# Use the official MySQL image as base
FROM mysql:latest
RUN { \
        echo '[mysqld]'; \
        echo 'default_authentication_plugin=mysql_native_password'; \
    } > /etc/mysql/conf.d/docker.cnf
# Environment variables
ENV MYSQL_ROOT_PASSWORD=Rabin@123
ENV MYSQL_DATABASE=file_storage_db
ENV MYSQL_USER=rabin
ENV MYSQL_PASSWORD=Rabin@123

# Expose port
EXPOSE 3306

# Copy init script to initialize database
COPY init.sql /docker-entrypoint-initdb.d/