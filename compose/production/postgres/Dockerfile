FROM docker.io/postgres:15

# Install system dependencies for GDAL and PostGIS
RUN apt-get update \
    && apt-get install -y \
    gdal-bin \
    postgis \
    postgresql-15-postgis-3 \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

# Enable PostGIS extension in the Postgres database
COPY ./compose/production/postgres/init_postgis.sh /docker-entrypoint-initdb.d/
# RUN chmod +x /docker-entrypoint-initdb.d/init-postgis.sh
# RUN /docker-entrypoint-initdb.d/init-postgis.sh
