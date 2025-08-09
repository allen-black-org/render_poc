# Use a slim Python image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /usr/app

# Install dbt core and Snowflake adapter
RUN pip install --no-cache-dir dbt-core dbt-snowflake

# Copy your dbt project directory into the container
# Assumes your host has a top‑level `dbt/` folder
COPY dbt/ ./dbt/

# Switch to the dbt project directory
WORKDIR /usr/app/dbt

# Default entrypoint and command
ENTRYPOINT ["dbt"]
CMD ["--help"]