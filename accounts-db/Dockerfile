FROM postgres:latest

ENV POSTGRES_USER=accountsadmin
ENV POSTGRES_PASSWORD=accountspwd
ENV POSTGRES_DB=accountsdb
ENV DATABASE_POOL_SIZE=10
ENV password_encryption=md5

RUN apt-get -y update \
    && apt-get install -y build-essential gettext libpq-dev\
    && apt-get install -y wkhtmltopdf\
    && apt-get install -y gdal-bin\
    && apt-get install -y libgdal-dev\
    && apt-get install -y --no-install-recommends software-properties-common\
    && apt-add-repository contrib\
    && apt-get update

# Files for initializing the database.
COPY initdb/0-accounts-schema.sql /docker-entrypoint-initdb.d/0-accounts-schema.sql
#COPY initdb/1-load-testdata.sh /docker-entrypoint-initdb.d/1-load-testdata.sh
#RUN chmod 755  /docker-entrypoint-initdb.d/1-load-testdata.sh
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 5432

CMD ["postgres"]